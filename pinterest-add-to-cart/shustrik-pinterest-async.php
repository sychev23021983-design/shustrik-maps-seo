<?php
/** Plugin Name: Shustrik Pinterest view-event queue */
if (!defined('ABSPATH')) { exit; }

const SHU_PIN_HOOK = 'shustrik_pinterest_view_delivery';
const SHU_PIN_GROUP = 'shustrik-pinterest-views';
const SHU_PIN_PREFIX = '_shu_pin_event_';
const SHU_PIN_TTL = 21600;

function shu_pin_metric($name) {
    global $wpdb;
    $allowed=['queued','delivered','retry','expired','terminal','fallback','bot_skipped','queued_add_to_cart','delivered_add_to_cart'];
    if (!in_array($name,$allowed,true)) { return; }
    $key='_shu_pin_count_'.$name;
    add_option($key,0,'',false);
    $wpdb->query($wpdb->prepare("UPDATE {$wpdb->options} SET option_value=CAST(option_value AS UNSIGNED)+1 WHERE option_name=%s",$key));
    wp_cache_delete($key,'options');
}

function shu_pin_key() { return hash('sha256',wp_salt('auth').'|shustrik-pinterest-view-v1',true); }
function shu_pin_account_hash($id) { return hash_hmac('sha256',(string)$id,shu_pin_key()); }
function shu_pin_encrypt(array $payload) {
    $nonce=random_bytes(SODIUM_CRYPTO_SECRETBOX_NONCEBYTES);
    return base64_encode($nonce.sodium_crypto_secretbox(wp_json_encode($payload),$nonce,shu_pin_key()));
}
function shu_pin_decrypt($value) {
    $bytes=base64_decode($value,true);
    if ($bytes===false || strlen($bytes)<=SODIUM_CRYPTO_SECRETBOX_NONCEBYTES) { return false; }
    $plain=sodium_crypto_secretbox_open(substr($bytes,SODIUM_CRYPTO_SECRETBOX_NONCEBYTES),substr($bytes,0,SODIUM_CRYPTO_SECRETBOX_NONCEBYTES),shu_pin_key());
    return $plain===false ? false : json_decode($plain,true);
}

function shu_pin_enqueue(array $payload,$account) {
    global $wpdb;
    if (!function_exists('as_schedule_single_action') || !function_exists('sodium_crypto_secretbox') || empty($payload['event_id']) || empty($payload['event_time'])) { return false; }
    $id=hash('sha256',$payload['event_name'].'|'.$payload['event_id'].'|'.$payload['event_time']);
    $key=SHU_PIN_PREFIX.$id;
    if (get_option($key,false)!==false) { return true; }
    $count=(int)$wpdb->get_var($wpdb->prepare("SELECT COUNT(*) FROM {$wpdb->options} WHERE option_name LIKE %s",$wpdb->esc_like(SHU_PIN_PREFIX).'%'));
    if ($count>=2000) { return false; } // On overload retain original synchronous delivery.
    $record=['expires'=>time()+SHU_PIN_TTL,'attempt'=>0,'account'=>shu_pin_account_hash($account),'sealed'=>shu_pin_encrypt($payload)];
    if (!add_option($key,$record,'',false)) { return get_option($key,false)!==false; }
    try { $action=as_schedule_single_action(time()+10,SHU_PIN_HOOK,[$id],SHU_PIN_GROUP,false); }
    catch (Throwable $e) { $action=0; }
    if (!$action) { delete_option($key); return false; }
    shu_pin_metric('queued');
    if (($payload['event_name']??'')==='add_to_cart') shu_pin_metric('queued_add_to_cart');
    return true;
}

function shu_pin_delivery($id) {
    if (!is_string($id) || !preg_match('/^[a-f0-9]{64}$/D',$id)) { return; }
    $key=SHU_PIN_PREFIX.$id; $lock='_shu_pin_lock_'.$id;
    $record=get_option($key,false);
    if (!is_array($record)) { return; }
    // Action Scheduler claims serialize each action; this lease also guards duplicate actions.
    if (!add_option($lock,time(),'',false)) {
        $lease=(int)get_option($lock,0);
        if ($lease && $lease<time()-120) { delete_option($lock); }
        if (!add_option($lock,time(),'',false)) {
            as_schedule_single_action(time()+150,SHU_PIN_HOOK,[$id],SHU_PIN_GROUP,false);
            return;
        }
    }
    try {
        $record=get_option($key,false);
        if (!is_array($record)) { return; }
        if ($record['expires']<=time()) { delete_option($key); shu_pin_metric('expired'); return; }
        $record['attempt']++; update_option($key,$record,false);
        if (!class_exists('Automattic\\WooCommerce\\Pinterest\\API\\APIV5') || !function_exists('Pinterest_For_WooCommerce')) { throw new RuntimeException('Unavailable',503); }
        $account= Pinterest_For_WooCommerce()::get_setting('tracking_advertiser');
        if (!$account || !hash_equals($record['account'],shu_pin_account_hash($account))) { delete_option($key); shu_pin_metric('terminal'); return; }
        $payload=shu_pin_decrypt($record['sealed']);
        if (!is_array($payload) || !in_array($payload['event_name']??'', ['page_visit','view_category','add_to_cart'],true)) { delete_option($key); shu_pin_metric('terminal'); return; }
        $response=\Automattic\WooCommerce\Pinterest\API\APIV5::send_conversions_api_event((string)$account,$payload);
        if (isset($response['code'])) { throw new RuntimeException('API status',(int)$response['code']); }
        $status=$response['events'][0]['status']??'failed';
        if ($status==='failed') { throw new RuntimeException('Event rejected',400); }
        delete_option($key); shu_pin_metric('delivered');
        if ($payload['event_name']==='add_to_cart') shu_pin_metric('delivered_add_to_cart');
    } catch (Throwable $e) {
        $record=get_option($key,false);
        if (!is_array($record)) { return; }
        $code=(int)$e->getCode();
        $transient=in_array($code,[0,1,408,429,503],true) || $code>=500;
        $attempt=max(1,(int)$record['attempt']);
        if ($transient && $attempt<5 && $record['expires']>time()+60) {
            // No payload, exception message, endpoint or authentication enters AS logs/args.
            $delay=[60,300,900,1800][$attempt-1];
            if (as_schedule_single_action(time()+$delay,SHU_PIN_HOOK,[$id],SHU_PIN_GROUP,false)) { shu_pin_metric('retry'); return; }
        }
        delete_option($key); shu_pin_metric('terminal');
    } finally { delete_option($lock); }
}
add_action(SHU_PIN_HOOK,'shu_pin_delivery',10,1);

function shu_pin_cleanup() {
    global $wpdb;
    $keys=$wpdb->get_col($wpdb->prepare("SELECT option_name FROM {$wpdb->options} WHERE option_name LIKE %s ORDER BY option_id ASC",$wpdb->esc_like(SHU_PIN_PREFIX).'%'));
    foreach ($keys as $key) {
        $r=get_option($key,false);
        if (!is_array($r)) { continue; }
        if ($r['expires']<=time()) { delete_option($key); shu_pin_metric('expired'); continue; }
        if ($r['attempt']>=5) { delete_option($key); shu_pin_metric('terminal'); continue; }
        $id=substr($key,strlen(SHU_PIN_PREFIX));
        // Recover an orphan if a process died between durable payload write and action scheduling.
        if (function_exists('as_has_scheduled_action') && !as_has_scheduled_action(SHU_PIN_HOOK,[$id],SHU_PIN_GROUP)) {
            as_schedule_single_action(time()+10,SHU_PIN_HOOK,[$id],SHU_PIN_GROUP,true);
        }
    }
}

add_action('plugins_loaded',function() {
    if (!class_exists('Automattic\\WooCommerce\\Pinterest\\Tracking\\Tracker') || !class_exists('Automattic\\WooCommerce\\Pinterest\\Tracking\\Conversions')) { return; }
    class ShustrikPinterestAsyncTracker extends \Automattic\WooCommerce\Pinterest\Tracking\Tracker {
        private $original;
        public function __construct($original) { $this->original=$original; }
        public function track_event(string $event_name, \Automattic\WooCommerce\Pinterest\Tracking\Data $data) {
            // Wrapper is not instanceof Conversions: explicitly preserve installed crawler guard.
            if (\Automattic\WooCommerce\Pinterest\Utilities\CrawlerDetector::is_crawler_request()) { shu_pin_metric('bot_skipped'); return; }
            if (!in_array($event_name,['PageVisit','ViewCategory'],true) && !($event_name==='AddToCart' && get_option('_shu_pin_add_to_cart_async_enabled',false))) { return $this->original->track_event($event_name,$data); }
            $account= Pinterest_For_WooCommerce()::get_setting('tracking_advertiser');
            if (!$account) { return $this->original->track_event($event_name,$data); }
            try { $queued=shu_pin_enqueue($this->original->prepare_request_data($event_name,$data),$account); }
            catch (Throwable $e) { $queued=false; }
            if ($queued) { return; }
            shu_pin_metric('fallback');
            return $this->original->track_event($event_name,$data);
        }
    }
    $install=function() {
        global $wp_filter;
        if (get_option('_shu_pin_enqueue_disabled',false)) { return; }
        if (!defined('PINTEREST_FOR_WOOCOMMERCE_VERSION') || PINTEREST_FOR_WOOCOMMERCE_VERSION!=='1.4.27' || !function_exists('as_schedule_single_action') || !function_exists('sodium_crypto_secretbox')) { return; }
        if (empty($wp_filter['wp_footer'])) { return; }
        foreach ($wp_filter['wp_footer']->callbacks as $callbacks) {
            foreach ($callbacks as $callback) {
                $f=$callback['function'];
                if (!is_array($f) || !is_object($f[0]) || !($f[0] instanceof \Automattic\WooCommerce\Pinterest\Tracking)) { continue; }
                foreach ($f[0]->get_trackers() as $tracker) {
                    if (get_class($tracker)==='Automattic\\WooCommerce\\Pinterest\\Tracking\\Conversions') {
                        $f[0]->remove_tracker(get_class($tracker));
                        $f[0]->add_tracker(new ShustrikPinterestAsyncTracker($tracker));
                    }
                }
            }
        }
    };
    add_action('init',$install,999); add_action('wp_loaded',$install,1);
},100);
