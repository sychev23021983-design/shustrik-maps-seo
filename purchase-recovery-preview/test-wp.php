<?php
// Run only from CLI with WordPress loaded and wp-adapter.php loaded; synthetic orders.
namespace {
if (PHP_SAPI!=='cli') exit(1);
$checks=0;
function check($name,$ok) { global $checks; if (!$ok) throw new \RuntimeException($name); $checks++; }
$table='shustrik_recovery_lab_'.bin2hex(random_bytes(6));
global $wpdb;
$wpdb->query("CREATE TEMPORARY TABLE `$table` (id VARBINARY(96) PRIMARY KEY,state VARCHAR(32) NOT NULL,generation INT NOT NULL,expiry BIGINT NOT NULL,lease_until BIGINT NOT NULL) ENGINE=InnoDB");
check('temporary SQL table created',$wpdb->last_error==='');
$store=new \Shustrik\RecoveryPreview\Store($wpdb,$table);
$context=new \Google\Site_Kit\Context(WP_PLUGIN_DIR.'/google-site-kit/google-site-kit.php');
$provider=new class($context) extends \Google\Site_Kit\Core\Conversion_Tracking\Conversion_Event_Providers\WooCommerce {
    public $wgai=[];
    protected function get_wgai_event_names(){return $this->wgai;}
    public function format($order) {return $this->get_formatted_order($order);}
};
$product=new \WC_Product_Simple();$product->set_name('Synthetic adapter item');$product->set_price('15');
$item=new class($product) extends \WC_Order_Item_Product {
    private $p;
    public function __construct($p){parent::__construct();$this->p=$p;$this->set_quantity(1);$this->set_total('15');}
    public function get_product(){return $this->p;}
};
$now=2000000000;$release=$now-100;
$order=new class($item,$now) {
    public $paid=true,$valid=true,$customer=0,$created,$paidAt,$marker='',$item,$total='15',$tax='0',$shipping='0';
    public function __construct($item,$now){$this->item=$item;$this->created=$now-50;$this->paidAt=$now-10;}
    public function get_id(){return 9000000002;}
    public function get_customer_id(){return $this->customer;}
    public function key_is_valid($key){return $this->valid && $key==='synthetic-private-key';}
    public function get_date_created(){return $this->created===null?null:new \WC_DateTime('@'.$this->created);}
    public function get_date_paid(){return $this->paidAt===null?null:new \WC_DateTime('@'.$this->paidAt);}
    public function is_paid(){return $this->paid;}
    public function get_meta($key){return $this->marker;}
    public function get_currency(){return 'USD';}
    public function get_total_tax(){return $this->tax;}
    public function get_total_shipping(){return $this->shipping;}
    public function get_total(){return $this->total;}
    public function get_items(){return [$this->item];}
    public function save(){throw new \RuntimeException('real order persistence forbidden');}
};
$format=fn($o)=>$provider->format($o);
$off=new \Shustrik\RecoveryPreview\Adapter($store,$release,$format);
check('disabled default',$off->prepare($order,'synthetic-private-key',false,$now)===false);
check('disabled wrote no row',$store->row('9000000002')===null);
$adapter=new \Shustrik\RecoveryPreview\Adapter($store,$release,$format,true);
foreach ([['paid',false],['valid',false],['customer',1],['created',$release-1],['paidAt',null],['marker','1']] as [$field,$value]) {
    $copy=clone $order;$copy->$field=$value;
    check('rejected '.$field,!$adapter->prepare($copy,'synthetic-private-key',false,$now));
}
check('logged in rejected',!$adapter->prepare($order,'synthetic-private-key',true,$now));
check('bad key rejected',!$adapter->prepare($order,'bad',false,$now));
check('valid prepare',$adapter->prepare($order,'synthetic-private-key',false,$now));
check('repeat prepare idempotent',$adapter->prepare($order,'synthetic-private-key',false,$now));
check('ready row',$store->row('9000000002')['state']==='ready');
check('unknown consent no claim',$adapter->claim($order,'synthetic-private-key',false,'unknown',true,true,$now)===null);
check('offline no claim',$adapter->claim($order,'synthetic-private-key',false,'granted',false,true,$now)===null);
$order->tax='1';$order->shipping='2';$order->total='18';
$ticket=$adapter->claim($order,'synthetic-private-key',false,'granted',true,true,$now);
check('claim obtained',is_array($ticket));
check('installed formatter value',$ticket['payload']['value']===18);
check('installed formatter tax',$ticket['payload']['tax']===1);
check('installed formatter shipping',$ticket['payload']['shipping']===2);
check('installed formatter item price',$ticket['payload']['items'][0]['price']===15);
check('PII omitted',!isset($ticket['payload']['user_data']));
check('another service cannot claim',$store->claim('9000000002',$now)===null);
$order->total='20'; // fresh authoritative payload wins over stale browser ticket
$payload=$adapter->authorize($ticket,$order,'synthetic-private-key',false,'granted',$now+1);
check('updated total regenerated',$payload['value']===20);
check('authorization transitions before send',$store->row('9000000002')['state']==='await_reconciliation');
check('same authorization blocked',$adapter->authorize($ticket,$order,'synthetic-private-key',false,'granted',$now+1)===null);
check('repeat render cannot reset attempt',$adapter->prepare($order,'synthetic-private-key',false,$now+2));
check('no resend',$adapter->claim($order,'synthetic-private-key',false,'granted',true,true,$now+2)===null);
$store->insert('lease-test',$now+1000);$lease=$store->claim('lease-test',$now);
check('SQL lease expiry ambiguous',$store->claim('lease-test',$now+31)===null);
check('lease state reconciles',$store->row('lease-test')['state']==='await_reconciliation');
check('stale generation blocked',!$store->transition('lease-test',$lease['generation'],'inflight','ready'));
$store->insert('deny-test',$now+1000);$store->suppress('deny-test');
check('deny terminal',$store->claim('deny-test',$now)===null);
$store->insert('expiry-test',$now);check('cleanup expires states',$store->expire($now+2000000)>=1);
check('cleanup covers ambiguous rows',$store->row('9000000002')['state']==='expired');
check('terminal cannot reopen',$store->claim('9000000002',$now+2000001)===null);
$wpdb->query("DROP TEMPORARY TABLE `$table`");
// Actual WP_Hook and installed provider registration; request-local only.
$GLOBALS['wp_filter']['woocommerce_thankyou']=new \WP_Hook();$provider->register_hooks();
$hook=$GLOBALS['wp_filter']['woocommerce_thankyou'];$before=$hook->callbacks;$calls=0;
$receipt=function($id)use(&$calls){if($id===9000000002)$calls++;};
$context=['target'=>'https://shustrik-maps.com','sitekit'=>GOOGLESITEKIT_VERSION,'woo'=>WC_VERSION,
    'guest_receipt'=>true,'classic_frontend'=>true,'consent_bridge_verified'=>true];
check('hook disabled by default',\Shustrik\RecoveryPreview\Hook::wrap($hook,$receipt)==='disabled');
check('disabled hook untouched',$hook->callbacks===$before);
$bad=$context;$bad['consent_bridge_verified']=false;
check('unwired consent refuses install',\Shustrik\RecoveryPreview\Hook::wrap($hook,$receipt,true,$bad)==='environment-not-ready');
check('unready hook untouched',$hook->callbacks===$before);
$provider->wgai=['purchase'];
check('external purchase owner refused',\Shustrik\RecoveryPreview\Hook::wrap($hook,$receipt,true,$context)==='external-purchase-owner');
check('external owner hook unchanged',$hook->callbacks===$before);$provider->wgai=[];
check('single sender replaced',\Shustrik\RecoveryPreview\Hook::wrap($hook,$receipt,true,$context)==='replaced');
check('same slots preserved',array_keys($hook->callbacks[10])===array_keys($before[10]));
$hook->do_action([9000000002]);check('only replacement called',$calls===1);
$GLOBALS['wp_filter']['woocommerce_thankyou']=new \WP_Hook();$provider->register_hooks();$provider->register_hooks();
$multiple=$GLOBALS['wp_filter']['woocommerce_thankyou'];$snapshot=$multiple->callbacks;
check('ambiguous owner refuses',\Shustrik\RecoveryPreview\Hook::wrap($multiple,$receipt,true,$context)==='ambiguous-or-missing-provider');
check('ambiguous owners unchanged',$multiple->callbacks===$snapshot);
echo json_encode(['checks'=>$checks,'passed'=>true,'sitekit'=>GOOGLESITEKIT_VERSION,'woo'=>WC_VERSION,
  'storage'=>'connection-scoped temporary InnoDB table','actual_order_writes'=>0,'google_requests'=>0,
  'production_hooks_changed'=>0,'request_local_test_hooks'=>true,'production_installed'=>false],JSON_PRETTY_PRINT),"\n";
}
