<?php
/** Plugin Name: Shustrik temporary aggregate PHP timing */
// No SQL, paths, request values, headers, bodies or credentials are recorded.
if (!defined('ABSPATH') || PHP_SAPI === 'cli' || time() >= 1791072000) return; // 2026-10-04 00:00 UTC
$shustrik_path = parse_url($_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH);
$shustrik_route = null;
foreach (['product','product-category','cart','checkout'] as $prefix) {
    if (preg_match('#^/' . $prefix . '(?:/|$)#', $shustrik_path)) $shustrik_route = $prefix;
}
if ($shustrik_path === '/') $shustrik_route = 'home';
if (!$shustrik_route) return;
(function($route) {
    $start = microtime(true);
    $forced = ($_SERVER['HTTP_X_SHUSTRIK_PROFILE'] ?? '') === '1';
    $sample = mt_rand(1,10) === 1;
    $phases = []; $pending = []; $http = [];
    $mark = function($name) use (&$phases,$start) {
        if (isset($phases[$name])) return;
        global $wpdb;
        $phases[$name] = ['ms'=>round((microtime(true)-$start)*1000,2),'queries'=>(int)($wpdb->num_queries ?? 0)];
    };
    $mark('mu_loaded');
    foreach (['plugins_loaded','init','wp_loaded','template_redirect','wp_head','wp_footer'] as $hook) {
        add_action($hook, function() use ($mark,$hook) {$mark($hook);}, PHP_INT_MAX);
    }
    add_filter('pre_http_request',function($pre,$args,$url) use (&$pending) {
        if ($pre !== false) return $pre;
        $host = strtolower((string)parse_url($url,PHP_URL_HOST));
        $bucket = 'other';
        foreach (['stripe.com'=>'stripe','paypal.com'=>'paypal','googleapis.com'=>'google','google.com'=>'google','wordpress.org'=>'wordpress','woocommerce.com'=>'woocommerce'] as $domain=>$name) {
            if ($host===$domain || substr($host,-strlen('.'.$domain))==='.'. $domain) {$bucket=$name;break;}
        }
        $pending[hash('sha256',$url)][] = [microtime(true),$bucket];
        return $pre;
    },PHP_INT_MAX,3);
    add_action('http_api_debug',function($response,$context,$class,$args,$url) use (&$pending,&$http) {
        if ($context !== 'response') return;
        $key=hash('sha256',$url);
        if (empty($pending[$key])) return;
        [$t,$bucket]=array_pop($pending[$key]);
        $ms=round((microtime(true)-$t)*1000,2);
        if (!isset($http[$bucket])) $http[$bucket]=['count'=>0,'ms'=>0,'max_ms'=>0,'errors'=>0];
        $http[$bucket]['count']++;$http[$bucket]['ms']+= $ms;$http[$bucket]['max_ms']=max($http[$bucket]['max_ms'],$ms);
        if (is_wp_error($response) || wp_remote_retrieve_response_code($response)>=400) $http[$bucket]['errors']++;
    },PHP_INT_MAX,5);
    add_action('shutdown',function() use ($mark,$start,$route,$forced,$sample,&$phases,&$http) {
        $mark('shutdown');$total=round((microtime(true)-$start)*1000,2);
        if (!$forced && !$sample && $total < 2000) return;
        $dir='/tmp/shustrik-php-profile';
        if (!is_dir($dir) && !@mkdir($dir,0700)) return;
        $file=$dir.'/php-2026-10-03.jsonl';
        clearstatcache(true,$file);if (is_file($file) && filesize($file)>2097152) return;
        $row=['utc'=>gmdate('c'),'route'=>$route,'qa'=>$forced,'total_ms'=>$total,'request_age_ms'=>round((microtime(true)-(float)($_SERVER['REQUEST_TIME_FLOAT'] ?? $start))*1000,2),'peak_mib'=>round(memory_get_peak_usage(true)/1048576,2),'phases'=>$phases,'external_http'=>$http];
        $fp=@fopen($file,'ab');if (!$fp) return;@chmod($file,0600);
        if (flock($fp,LOCK_EX)) {fwrite($fp,json_encode($row,JSON_UNESCAPED_SLASHES)."\n");flock($fp,LOCK_UN);}fclose($fp);
    },PHP_INT_MAX);
})($shustrik_route);
unset($shustrik_path,$shustrik_route);
