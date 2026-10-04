<?php
if(PHP_SAPI!=='cli')exit(1);
ob_start();require '/var/www/html/wp-load.php';ob_end_clean();
if(in_array('--cart-enable',$argv,true)){update_option('_shu_pin_add_to_cart_async_enabled',true,false);echo 'cart-enabled';exit;}
if(in_array('--cart-disable',$argv,true)){update_option('_shu_pin_add_to_cart_async_enabled',false,false);echo 'cart-disabled';exit;}
if(in_array('--cart-restore-absent',$argv,true)){delete_option('_shu_pin_add_to_cart_async_enabled');echo 'cart-flag-absent';exit;}
if(in_array('--disable',$argv,true)){update_option('_shu_pin_enqueue_disabled',true,false);echo 'enqueue-disabled';exit;}
if(in_array('--enable',$argv,true)){delete_option('_shu_pin_enqueue_disabled');echo 'enqueue-enabled';exit;}
global $wpdb;
$prefix=defined('SHU_PIN_PREFIX')?SHU_PIN_PREFIX:'_shu_pin_event_';
$out=['enqueue_disabled'=>(bool)get_option('_shu_pin_enqueue_disabled',false),
 'payloads'=>(int)$wpdb->get_var($wpdb->prepare("SELECT COUNT(*) FROM {$wpdb->options} WHERE option_name LIKE %s",$wpdb->esc_like($prefix).'%')),
 'cart_enabled'=>(bool)get_option('_shu_pin_add_to_cart_async_enabled',false),'cart_flag_exists'=>get_option('_shu_pin_add_to_cart_async_enabled','__absent__')!=='__absent__','metrics'=>[],'trackers'=>[]];
$out['oldest_payload_age_seconds']=0;
$keys=$wpdb->get_col($wpdb->prepare("SELECT option_name FROM {$wpdb->options} WHERE option_name LIKE %s",$wpdb->esc_like($prefix).'%'));
foreach($keys as $key){$record=get_option($key,false);if(is_array($record))$out['oldest_payload_age_seconds']=max($out['oldest_payload_age_seconds'],time()-($record['expires']-21600));}
foreach(['queued','delivered','retry','expired','terminal','fallback','bot_skipped','queued_add_to_cart','delivered_add_to_cart'] as $name)$out['metrics'][$name]=(int)get_option('_shu_pin_count_'.$name,0);
global $wp_filter;
if(!empty($wp_filter['wp_footer']))foreach($wp_filter['wp_footer']->callbacks as $callbacks)foreach($callbacks as $cb){$f=$cb['function'];if(is_array($f)&&is_object($f[0])&&$f[0] instanceof \Automattic\WooCommerce\Pinterest\Tracking)foreach($f[0]->get_trackers() as $t)$out['trackers'][get_class($t)]=true;}
$out['trackers']=array_keys($out['trackers']);
$out['queue_status']=$wpdb->get_results($wpdb->prepare("SELECT a.status,COUNT(*) AS count FROM {$wpdb->prefix}actionscheduler_actions a JOIN {$wpdb->prefix}actionscheduler_groups g ON g.group_id=a.group_id WHERE g.slug=%s GROUP BY a.status",'shustrik-pinterest-views'),ARRAY_A);
echo json_encode($out);
