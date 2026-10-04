<?php
/** Plugin Name: Shustrik temporary Pinterest callback attribution */
if(!defined('ABSPATH') || PHP_SAPI==='cli' || time()>=1791115200) return; // 2026-10-04 12:00 UTC / 15:00 Moscow
$shu_capi_path=parse_url($_SERVER['REQUEST_URI']??'/',PHP_URL_PATH);
$shu_capi_route=$shu_capi_path==='/'?'home':null;
foreach(['product','product-category','cart','checkout'] as $prefix) if(preg_match('#^/'.$prefix.'(?:/|$)#',$shu_capi_path)) $shu_capi_route=$prefix;
if(!$shu_capi_route) return;
(static function($route) {
    $start=microtime(true);$pending=[];$calls=[];
    add_filter('pre_http_request',static function($pre,$args,$url) use(&$pending) {
        if($pre!==false) return $pre;
        $host=strtolower((string)parse_url($url,PHP_URL_HOST));
        if($host!=='pinterest.com' && substr($host,-14)!=='.pinterest.com') return $pre;
        $callback='other';
        $allowed=['handle_add_to_cart'=>'AddToCart','handle_checkout'=>'Checkout','handle_search'=>'Search','handle_page_visit'=>'PageVisit','handle_view_category'=>'ViewCategory'];
        foreach(debug_backtrace(DEBUG_BACKTRACE_IGNORE_ARGS,40) as $frame) {
            if(($frame['class']??'')==='Automattic\\WooCommerce\\Pinterest\\Tracking' && isset($allowed[$frame['function']??''])) {
                $callback=$allowed[$frame['function']];break;
            }
        }
        // URL is transiently hashed only to pair WP HTTP callbacks. Never stored.
        $pending[hash('sha256',$url)][]=[microtime(true),$callback,!empty($args['blocking'])];
        return $pre; // Never short-circuit, retry, change payload, or claim success.
    },PHP_INT_MAX,3);
    add_action('http_api_debug',static function($response,$context,$class,$args,$url) use(&$pending,&$calls) {
        if($context!=='response') return;
        $key=hash('sha256',$url);if(empty($pending[$key])) return;
        [$t,$callback,$blocking]=array_pop($pending[$key]);
        $calls[]=['callback'=>$callback,'blocking'=>$blocking,'ms'=>round((microtime(true)-$t)*1000,2),
            'error'=>is_wp_error($response)||wp_remote_retrieve_response_code($response)>=400];
        if(count($calls)>20) $calls=array_slice($calls,-20);
    },PHP_INT_MAX,5);
    add_action('shutdown',static function() use($route,$start,&$calls,&$pending) {
        if(!$calls) return;
        $dir='/tmp/shustrik-capi-attribution';
        if(!is_dir($dir) && !@mkdir($dir,0700)) return;
        $file=$dir.'/callbacks-2026-10-04.jsonl';clearstatcache(true,$file);
        if(is_file($file)&&filesize($file)>262144) return;
        $row=['utc'=>gmdate('c'),'route'=>$route,'total_ms'=>round((microtime(true)-$start)*1000,2),'calls'=>$calls,'incomplete_calls'=>array_sum(array_map('count',$pending))];
        $fp=@fopen($file,'ab');if(!$fp)return;@chmod($file,0600);
        if(flock($fp,LOCK_EX)){fwrite($fp,json_encode($row,JSON_UNESCAPED_SLASHES)."\n");flock($fp,LOCK_UN);}fclose($fp);
    },PHP_INT_MAX);
})($shu_capi_route);
unset($shu_capi_path,$shu_capi_route);
