<?php
namespace Automattic\WooCommerce\Pinterest\Tracking {
    class Data { public $id='test-id'; }
    abstract class Tracker { public function init_hooks() {} public function disable_hooks() {} abstract public function track_event(string $name,Data $data); }
    class Conversions extends Tracker {
        public $sync=[];
        public function track_event(string $name,Data $data) { $this->sync[]=$name; }
        public function prepare_request_data(string $name,Data $data) { return ['event_id'=>$data->id,'event_time'=>123456,'event_name'=>match($name){'PageVisit'=>'page_visit','ViewCategory'=>'view_category','AddToCart'=>'add_to_cart',default=>'checkout'},'user_data'=>['synthetic'=>'unit-test-only']]; }
    }
}
namespace Automattic\WooCommerce\Pinterest\Utilities {
    class CrawlerDetector { public static $bot=false; public static function is_crawler_request() { return self::$bot; } }
}
namespace Automattic\WooCommerce\Pinterest\API {
    class APIV5 { public static $failure=0; public static $last; public static function send_conversions_api_event($account,$data) { self::$last=$data; if(self::$failure)throw new \RuntimeException('synthetic',self::$failure);return ['events'=>[['status'=>'processed']]]; } }
}
namespace {
    define('ABSPATH','unit-test'); $options=[]; $actions=[]; $hooks=[]; $schedule_ok=true;
    function add_action($name,$fn,$priority=10,$args=1) { global $hooks; $hooks[$name][]=$fn; }
    function add_option($k,$v,$unused='',$autoload=false) { global $options;if(array_key_exists($k,$options))return false;$options[$k]=$v;return true; }
    function get_option($k,$default=false) { global $options;return $options[$k]??$default; }
    function update_option($k,$v,$autoload=false) {global $options;$options[$k]=$v;return true;}
    function delete_option($k) {global $options;unset($options[$k]);return true;}
    function wp_cache_delete($k,$group) {}
    function wp_salt($scheme) {return 'synthetic-unit-test-key-only';}
    function wp_json_encode($v) {return json_encode($v);}
    function as_schedule_single_action($time,$hook,$args,$group,$unique) {global $actions,$schedule_ok;if(!$schedule_ok)return 0;$actions[]=[$time,$hook,$args,$group];return count($actions);}
    function as_has_scheduled_action($hook,$args,$group) { return false; }
    class FakeDB {public $options='fake_options';function prepare($sql,...$args){return $sql;}function esc_like($s){return $s;}function get_var($sql){return 0;}function query($sql){return 1;}function get_col($sql){global $options;return array_values(array_filter(array_keys($options),fn($k)=>str_starts_with($k,SHU_PIN_PREFIX)));}}
    $wpdb=new FakeDB();
    class Settings {static function get_setting($name){return 'synthetic-account';}}
    function Pinterest_For_WooCommerce(){return new Settings();}
    require __DIR__.'/shustrik-pinterest-async.php';
    foreach($hooks['plugins_loaded'] as $fn)$fn();
    function must($ok,$name){if(!$ok)throw new \RuntimeException($name);echo "PASS $name\n";}
    $original=new \Automattic\WooCommerce\Pinterest\Tracking\Conversions();
    $wrapper=new ShustrikPinterestAsyncTracker($original);$data=new \Automattic\WooCommerce\Pinterest\Tracking\Data();
    $wrapper->track_event('PageVisit',$data);
    must(count($actions)===1 && !$original->sync,'page visit queued without sync');
    $id=$actions[0][2][0];$r=get_option(SHU_PIN_PREFIX.$id);
    must(!str_contains(json_encode($r),'synthetic-unit-test-only') && shu_pin_decrypt($r['sealed'])['event_time']===123456,'encrypted payload retains timestamp');
    $wrapper->track_event('PageVisit',$data);must(count($actions)===1,'duplicate event not rescheduled');
    $wrapper->track_event('AddToCart',$data);$wrapper->track_event('Checkout',$data);must($original->sync===['AddToCart','Checkout'],'commerce events remain synchronous');
    \Automattic\WooCommerce\Pinterest\Utilities\CrawlerDetector::$bot=true;$data->id='bot-event';$wrapper->track_event('PageVisit',$data);must(count($actions)===1,'crawler exclusion preserved');\Automattic\WooCommerce\Pinterest\Utilities\CrawlerDetector::$bot=false;
    \Automattic\WooCommerce\Pinterest\API\APIV5::$failure=503;shu_pin_delivery($id);must(get_option(SHU_PIN_PREFIX.$id)['attempt']===1 && count($actions)===2,'transient retry preserves payload');
    \Automattic\WooCommerce\Pinterest\API\APIV5::$failure=0;shu_pin_delivery($id);must(get_option(SHU_PIN_PREFIX.$id)===false && \Automattic\WooCommerce\Pinterest\API\APIV5::$last['event_id']==='test-id','successful delivery deletes payload and retains event ID');
    $schedule_ok=false;$data->id='fallback-event';$wrapper->track_event('ViewCategory',$data);must(end($original->sync)==='ViewCategory','schedule failure falls back to original');$schedule_ok=true;
    $data->id='expired-event';$wrapper->track_event('ViewCategory',$data);$id=end($actions)[2][0];$r=get_option(SHU_PIN_PREFIX.$id);$r['expires']=time()-1;update_option(SHU_PIN_PREFIX.$id,$r);shu_pin_cleanup();must(get_option(SHU_PIN_PREFIX.$id)===false,'expiry cleanup removes encrypted payload');
    $data->id='orphan-event';$wrapper->track_event('PageVisit',$data);$n=count($actions);shu_pin_cleanup();must(count($actions)===$n+1,'orphan payload recovers a scheduled consumer');$id=end($actions)[2][0];delete_option(SHU_PIN_PREFIX.$id);
    $data->id='permanent-event';$wrapper->track_event('PageVisit',$data);$id=end($actions)[2][0];\Automattic\WooCommerce\Pinterest\API\APIV5::$failure=400;shu_pin_delivery($id);must(get_option(SHU_PIN_PREFIX.$id)===false,'permanent failure terminates');
    $data->id='retry-limit';$wrapper->track_event('PageVisit',$data);$id=end($actions)[2][0];\Automattic\WooCommerce\Pinterest\API\APIV5::$failure=503;for($i=0;$i<5;$i++)shu_pin_delivery($id);must(get_option(SHU_PIN_PREFIX.$id)===false,'five attempt limit enforced');
    must(array_reduce($actions,fn($ok,$a)=>$ok && count($a[2])===1 && preg_match('/^[a-f0-9]{64}$/D',$a[2][0]),true),'action args contain opaque ID only');
    $data->id='cart-disabled';$before=count($actions);$wrapper->track_event('AddToCart',$data);must(count($actions)===$before && end($original->sync)==='AddToCart','new cart admission defaults off');
    update_option('_shu_pin_add_to_cart_async_enabled',true,false);
    $data->id='synthetic-cart-enabled';$before=count($actions);$syncBefore=count($original->sync);$wrapper->track_event('AddToCart',$data);
    must(count($actions)===$before+1 && count($original->sync)===$syncBefore,'enabled AddToCart queued without synchronous CAPI');
    $cartId=end($actions)[2][0];$sealed=get_option(SHU_PIN_PREFIX.$cartId);$cart=shu_pin_decrypt($sealed['sealed']);
    must($cart['event_name']==='add_to_cart' && $cart['event_id']===$data->id && $cart['event_time']===123456,'prepared cart identity and timestamp preserved');
    $wrapper->track_event('AddToCart',$data);must(count($actions)===$before+1,'same cart event deduplicated');
    update_option('_shu_pin_add_to_cart_async_enabled',false,false);\Automattic\WooCommerce\Pinterest\API\APIV5::$failure=0;shu_pin_delivery($cartId);
    must(get_option(SHU_PIN_PREFIX.$cartId)===false && \Automattic\WooCommerce\Pinterest\API\APIV5::$last['event_name']==='add_to_cart','disabled admission still drains queued cart events');
    update_option('_shu_pin_add_to_cart_async_enabled',true,false);$schedule_ok=false;$data->id='cart-scheduler-failure';$wrapper->track_event('AddToCart',$data);
    must(end($original->sync)==='AddToCart','cart scheduling failure preserves original fallback');$schedule_ok=true;
    $before=count($actions);$wrapper->track_event('Checkout',$data);$wrapper->track_event('Search',$data);
    must(count($actions)===$before && array_slice($original->sync,-2)===['Checkout','Search'],'Checkout and Search remain original');

}
