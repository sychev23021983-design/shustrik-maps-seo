<?php
if(PHP_SAPI!=='cli')exit(1);
ob_start();require '/var/www/html/wp-load.php';ob_end_clean();
$file=WPMU_PLUGIN_DIR.'/shustrik-purchase-paid-guard.php';
$provider=new ReflectionClass('Google\\Site_Kit\\Core\\Conversion_Tracking\\Conversion_Event_Providers\\WooCommerce');
echo json_encode(['utc'=>gmdate('c'),'home'=>rtrim(home_url(),'/'),'sitekit'=>GOOGLESITEKIT_VERSION,'woo'=>WC_VERSION,
 'block_theme'=>wp_is_block_theme(),'option'=>get_option('shustrik_purchase_paid_guard_enabled',null),
 'guard_hash'=>is_file($file)?hash_file('sha256',$file):null,
 'provider_hash'=>hash_file('sha256',$provider->getFileName()),
 'guard_version_gate_satisfied'=>WC_VERSION==='11.2.1'],JSON_PRETTY_PRINT);
