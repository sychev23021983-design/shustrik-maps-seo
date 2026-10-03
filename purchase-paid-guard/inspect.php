<?php
ini_set('display_errors','0');define('WP_USE_THEMES',false);
ob_start();require '/var/www/html/wp-load.php';ob_end_clean();
if(PHP_SAPI!=='cli'||rtrim(home_url(),'/')!=='https://shustrik-maps.com')exit(1);
$found=[];
foreach(($GLOBALS['wp_filter']['woocommerce_thankyou']->callbacks??[])as $priority=>$callbacks){
    foreach($callbacks as $entry){
        if(!$entry['function'] instanceof Closure)continue;
        $r=new ReflectionFunction($entry['function']);$bound=$r->getClosureThis();
        if($bound&&is_a($bound,'Google\\Site_Kit\\Core\\Conversion_Tracking\\Conversion_Event_Providers\\WooCommerce')){
            $found[]=['priority'=>$priority,'accepted_args'=>$entry['accepted_args'],'source_sha256'=>hash_file('sha256',$r->getFileName())];
        }
    }
}
$option=get_option('shustrik_purchase_paid_guard_enabled',null);
echo json_encode(['utc'=>gmdate('c'),'sitekit_version'=>defined('GOOGLESITEKIT_VERSION')?GOOGLESITEKIT_VERSION:null,
    'woocommerce_version'=>defined('WC_VERSION')?WC_VERSION:null,'block_theme'=>wp_is_block_theme(),
    'guard_option_present'=>$option!==null,'guard_enabled'=>in_array($option,[true,'1'],true),
    'guard_mu_file_exists'=>is_file(WPMU_PLUGIN_DIR.'/shustrik-purchase-paid-guard.php'),
    'installed_purchase_callbacks'=>$found,'configuration_changed'=>false],JSON_PRETTY_PRINT|JSON_UNESCAPED_SLASHES)."\n";
