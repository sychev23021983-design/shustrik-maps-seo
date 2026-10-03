<?php
ini_set('display_errors','0');define('WP_USE_THEMES',false);
ob_start();require '/var/www/html/wp-load.php';ob_end_clean();
if(PHP_SAPI!=='cli'||rtrim(home_url(),'/')!=='https://shustrik-maps.com')exit(1);
$key='shustrik_purchase_paid_guard_enabled';
$hash='666940e505df36627c2c556f680f0a0e3e71a7515c68e994b3f8c6a460b2fbe6';
$file=WPMU_PLUGIN_DIR.'/shustrik-purchase-paid-guard.php';$mode=$argv[1]??'--inspect';
$before=get_option($key,null);
if($mode==='--activate'){
    if($before!==null||!is_file($file)||hash_file('sha256',$file)!==$hash
        ||GOOGLESITEKIT_VERSION!=='1.184.0'||WC_VERSION!=='11.1.2'||wp_is_block_theme())exit(2);
    if(!add_option($key,true,'',false))exit(3);
}elseif($mode==='--rollback'){
    // This release only accepts an absent original file/option; restore that exact state.
    if(!in_array($before,[true,'1'],true)||!is_file($file)||hash_file('sha256',$file)!==$hash)exit(4);
    if(!delete_option($key))exit(5);
}elseif($mode!=='--inspect')exit(6);
echo json_encode(['utc'=>gmdate('c'),'option_present'=>get_option($key,null)!==null,
    'enabled'=>in_array(get_option($key,false),[true,'1'],true),'file_exists'=>is_file($file),
    'file_sha256'=>is_file($file)?hash_file('sha256',$file):null,
    'sitekit_version'=>GOOGLESITEKIT_VERSION,'woocommerce_version'=>WC_VERSION,
    'block_theme'=>wp_is_block_theme()],JSON_PRETTY_PRINT)."\n";
