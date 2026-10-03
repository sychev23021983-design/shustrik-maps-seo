<?php
// CLI only. Fake order lookup and persistence; capture installed PHP/JS behavior.
namespace Google\Site_Kit\Core\Conversion_Tracking\Conversion_Event_Providers {
    function wc_get_order($id) { return $GLOBALS['shustrik_lab_order'] ?? false; }
    function wp_add_inline_script($handle, $code, $position='after') {
        $GLOBALS['shustrik_lab_inline'][]=$code; return true;
    }
}
namespace Shustrik\PurchasePaidGuard {
    function wc_get_order($id){return $GLOBALS['shustrik_lab_order']??false;}
    function get_option($key,$default=false){return $key===OPTION?($GLOBALS['lab_enabled']??false):\get_option($key,$default);}
    function is_order_received_page(){return $GLOBALS['lab_receipt']??false;}
}
namespace {
    ini_set('display_errors','0'); define('WP_USE_THEMES',false);
    ob_start(); require '/var/www/html/wp-load.php'; ob_end_clean();
    if(PHP_SAPI!=='cli' || rtrim(home_url(),'/')!=='https://shustrik-maps.com') exit(1);
    $context=new \Google\Site_Kit\Context(WP_PLUGIN_DIR.'/google-site-kit/google-site-kit.php');
    $provider=new class($context) extends \Google\Site_Kit\Core\Conversion_Tracking\Conversion_Event_Providers\WooCommerce {
        public $wgai=[];
        protected function get_wgai_event_names(){ return $this->wgai; }
        public function render($skip=false){ $this->maybe_add_purchase_inline_script(9000000001,$skip); }
    };
    $product=new \WC_Product_Simple(); $product->set_name('Synthetic lab item'); $product->set_price('15');
    $item=new class($product) extends \WC_Order_Item_Product {
        private $lab_product;
        public function __construct($product){ parent::__construct(); $this->lab_product=$product; $this->set_quantity(1); $this->set_total('15'); }
        public function get_product(){ return $this->lab_product; }
    };
    function fake_order($status,$item,$valid=true,$marker='') {
        return new class($status,$item,$valid,$marker) {
            public $status,$marker,$save_calls=0,$valid,$item,$paid_date=true,$total="15";
            public function __construct($status,$item,$valid,$marker){$this->status=$status;$this->item=$item;$this->valid=$valid;$this->marker=$marker;}
            public function get_id(){return 9000000001;} // Synthetic, lookup always overridden.
            public function get_date_paid(){return $this->paid_date && $this->is_paid()?new \WC_DateTime('2026-10-03T00:00:00Z'):null;}
            public function get_currency(){return 'USD';}
            public function get_total_tax(){return '0';}
            public function get_total_shipping(){return '0';}
            public function get_total(){return $this->total;}
            public function get_items(){return [$this->item];}
            public function get_meta($key){return $this->marker;}
            public function key_is_valid($key){return $this->valid;}
            public function is_paid(){return in_array($this->status,['completed','processing'],true);}
            public function update_meta_data($key,$value){$this->marker=(string)$value;}
            public function save(){ $this->save_calls++; return 0; } // No DB persistence.
        };
    }
    require __DIR__.'/shustrik-purchase-paid-guard.php';
    $checks=[];
    function verify($name,$value){global $checks;if(!$value){fwrite(STDERR,"FAIL: $name\n");exit(2);}$checks[]=$name;}
    verify('disabled by default', !\Shustrik\PurchasePaidGuard\environment_ready());
    $GLOBALS['lab_enabled']=true; $GLOBALS['lab_receipt']=true;
    verify('enabled guest classic supported receipt',\Shustrik\PurchasePaidGuard\environment_ready());
    $GLOBALS['lab_receipt']=false;
    verify('does not apply away from receipt',!\Shustrik\PurchasePaidGuard\environment_ready());
    $GLOBALS['lab_receipt']=true;
    $wp_filter['woocommerce_thankyou']=new \WP_Hook();
    $provider->register_hooks();
    add_action('woocommerce_thankyou',function($id){$GLOBALS['lab_other_calls']++;},10,1);
    $base=clone $wp_filter['woocommerce_thankyou'];
    $rows=[];
    foreach(['pending','failed','cancelled','on-hold','refunded','completed-no-date','processing-no-date','completed','processing','free-paid','invalid-key','already-marked','wgai-owned','late-payment'] as $name){
        $status=in_array($name,['pending','failed','cancelled','on-hold','refunded'],true)?$name:'completed';
        if(str_starts_with($name,'processing'))$status='processing';
        if($name==='late-payment')$status='pending';
        $fake=fake_order($status,$item,$name!=='invalid-key',$name==='already-marked'?'1':'');
        if(str_ends_with($name,'no-date'))$fake->paid_date=false;
        if($name==='free-paid')$fake->total='0';
        $GLOBALS['shustrik_lab_order']=$fake;$GLOBALS['shustrik_lab_inline']=[];$GLOBALS['lab_other_calls']=0;
        $provider->wgai=$name==='wgai-owned'?['purchase']:[];
        $hook=clone $base;
        $keys_before=array_keys($hook->callbacks[10]);
        verify($name.': verified single callback wrapped',\Shustrik\PurchasePaidGuard\wrap_hook($hook)==='wrapped');
        verify($name.': hook slot/order retained',$keys_before===array_keys($hook->callbacks[10]));
        $hook->do_action([9000000001]);$first=$GLOBALS['shustrik_lab_inline'];$marker=$fake->marker;
        $GLOBALS['shustrik_lab_inline']=[];
        if($name==='late-payment')$fake->status='completed';
        $hook->do_action([9000000001]);$second=$GLOBALS['shustrik_lab_inline'];
        $paid=in_array($name,['completed','processing','free-paid'],true);
        verify($name.': first inline count',count($first)===($paid?1:0));
        verify($name.': later inline count',count($second)===($name==='late-payment'?1:0));
        verify($name.': unpaid does not acquire marker', $paid||$name==='already-marked'||$name==='late-payment'||$marker==='');
        verify($name.': other callback still runs',$GLOBALS['lab_other_calls']===2);
        $rows[]=['name'=>$name,'first_inline'=>$first,'second_inline'=>$second,'marker_after_first'=>$marker,'memory_save_calls'=>$fake->save_calls];
    }
    $missing=new \WP_Hook();verify('missing provider unchanged',\Shustrik\PurchasePaidGuard\wrap_hook($missing)==='ambiguous-or-missing-provider');
    $ambiguous=clone $base;
    // Original register_hooks creates a second distinct provider closure.
    $wp_filter['woocommerce_thankyou']=$ambiguous;$provider->register_hooks();
    $snapshot=$ambiguous->callbacks;
    verify('ambiguous provider refused',\Shustrik\PurchasePaidGuard\wrap_hook($ambiguous)==='ambiguous-or-missing-provider');
    verify('ambiguity causes no partial mutation',$snapshot===$ambiguous->callbacks);
    $drift=clone $base;$drift->callbacks[11]=$drift->callbacks[10];unset($drift->callbacks[10]);$snapshot=$drift->callbacks;
    verify('priority drift refused',\Shustrik\PurchasePaidGuard\wrap_hook($drift)==='provider-drift');
    verify('drift causes no partial mutation',$snapshot===$drift->callbacks);
    $fixture_path=is_file(__DIR__.'/installed-fixture-2026-10-03.json')?__DIR__.'/installed-fixture-2026-10-03.json':__DIR__.'/../purchase-lab/installed-fixture-2026-10-03.json';
    $fixture=json_decode(file_get_contents($fixture_path),true);
    $out=['utc'=>gmdate('c'),'checks_passed'=>count($checks),'assertion_failures'=>0,'actual_orders_saved'=>0,'real_ga4_requests'=>0,
        'cases'=>$rows,'provider_js'=>$fixture['provider_js'],'gtag_wrapper_js'=>$fixture['gtag_wrapper_js'],
        'guard_sha256'=>hash_file('sha256',__DIR__.'/shustrik-purchase-paid-guard.php'),'source_sha256'=>$fixture['source_sha256'],'checks'=>$checks];
    echo json_encode($out,JSON_PRETTY_PRINT|JSON_UNESCAPED_SLASHES)."\n";
}
