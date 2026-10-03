<?php
if (PHP_SAPI!=='cli') { exit(1); }
ob_start(); require '/var/www/html/wp-load.php'; ob_end_clean();
if (!function_exists('shu_pin_cleanup') || !class_exists('ActionScheduler')) { exit(1); }
shu_pin_cleanup();
global $wpdb;
$group_exists=$wpdb->get_var($wpdb->prepare("SELECT group_id FROM {$wpdb->prefix}actionscheduler_groups WHERE slug=%s",SHU_PIN_GROUP));
if (!$group_exists) { echo json_encode(['processed'=>0]); exit; }
$store=ActionScheduler::store();
$claim=$store->stake_claim(2,as_get_datetime_object(),[SHU_PIN_HOOK],SHU_PIN_GROUP);
try {
    foreach ($claim->get_actions() as $id) {
        if ($store->get_claim_id($id)!==$claim->get_id()) { continue; }
        ActionScheduler_QueueRunner::instance()->process_action($id,'Shustrik isolated CLI');
    }
} finally { $store->release_claim($claim); }
echo json_encode(['processed'=>count($claim->get_actions())]);
