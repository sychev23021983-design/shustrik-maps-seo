<?php
ob_start();require '/var/www/html/wp-load.php';ob_end_clean();
$expected=[
 'src/Tracking.php'=>'956fca8df0f43b1636c15baa68aaa93efcbab3818a4e09077a8966452534009f',
 'src/Tracking/Conversions.php'=>'1712a9579b88b5cd349a9c7b4ec88567b5b53b5029e49a2e03cbd816224ef9a5',
 'src/Tracking/Tracker.php'=>'42cf6c207a66ad3ac0a548288539ec6e9c61748f67dfa6abcdf7ede3d9480c83'
];
$ok=true;foreach($expected as $path=>$sha){$ok=$ok && hash_file('sha256',WP_PLUGIN_DIR.'/pinterest-for-woocommerce/'.$path)===$sha;}
$checks=['plugin_version'=>defined('PINTEREST_FOR_WOOCOMMERCE_VERSION')?PINTEREST_FOR_WOOCOMMERCE_VERSION:null,'source_guards'=>$ok,'scheduler'=>function_exists('as_schedule_single_action'),'sodium'=>function_exists('sodium_crypto_secretbox')];
global $wpdb;
$checks['scheduler_counts']=$wpdb->get_results("SELECT status,COUNT(*) AS count FROM {$wpdb->prefix}actionscheduler_actions GROUP BY status",ARRAY_A);
$checks['latest_completed_utc']=$wpdb->get_var("SELECT MAX(last_attempt_gmt) FROM {$wpdb->prefix}actionscheduler_actions WHERE status='complete'");
echo json_encode($checks);
if(!$ok || $checks['plugin_version']!=='1.4.27' || !$checks['scheduler'] || !$checks['sodium'])exit(1);
