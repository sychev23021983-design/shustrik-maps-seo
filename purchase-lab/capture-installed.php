<?php
// CLI only. Fake order lookup and persistence; capture installed PHP/JS behavior.
namespace Google\Site_Kit\Core\Conversion_Tracking\Conversion_Event_Providers {
    function wc_get_order($id) { return $GLOBALS['shustrik_lab_order'] ?? false; }
    function wp_add_inline_script($handle, $code, $position='after') {
        $GLOBALS['shustrik_lab_inline'][]=$code; return true;
    }
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
            public $status,$marker,$save_calls=0,$valid,$item;
            public function __construct($status,$item,$valid,$marker){$this->status=$status;$this->item=$item;$this->valid=$valid;$this->marker=$marker;}
            public function get_id(){return 9000000001;} // Synthetic, lookup always overridden.
            public function get_currency(){return 'USD';}
            public function get_total_tax(){return '0';}
            public function get_total_shipping(){return '0';}
            public function get_total(){return '15';}
            public function get_items(){return [$this->item];}
            public function get_meta($key){return $this->marker;}
            public function key_is_valid($key){return $this->valid;}
            public function is_paid(){return in_array($this->status,['completed','processing'],true);}
            public function update_meta_data($key,$value){$this->marker=(string)$value;}
            public function save(){ $this->save_calls++; return 0; } // No DB persistence.
        };
    }
    $cases=[];
    foreach(['pending','failed','cancelled','on-hold','completed','processing','invalid-key','already-marked','wgai-owned','block-two-hooks','late-payment'] as $name) {
        $status=in_array($name,['pending','failed','cancelled','on-hold'],true)?$name:'completed';
        if($name==='late-payment') $status='pending';
        $fake=fake_order($status,$item,$name!=='invalid-key',$name==='already-marked'?'1':'');
        $GLOBALS['shustrik_lab_order']=$fake; $GLOBALS['shustrik_lab_inline']=[];
        $provider->wgai=$name==='wgai-owned'?['purchase']:[];
        $provider->render($name==='block-two-hooks');
        $first=$GLOBALS['shustrik_lab_inline']; $first_marker=$fake->marker;
        $GLOBALS['shustrik_lab_inline']=[];
        if($name==='late-payment') $fake->status='completed';
        $provider->render(); $second=$GLOBALS['shustrik_lab_inline'];
        $cases[]=['name'=>$name,'initial_status'=>$status,'final_status'=>$fake->status,
            'first_inline'=>$first,'second_inline'=>$second,'first_marker'=>$first_marker,'final_marker'=>$fake->marker,
            'memory_save_calls'=>$fake->save_calls,'actual_order_saved'=>false];
    }
    unset($GLOBALS['shustrik_lab_order'],$GLOBALS['shustrik_lab_inline']);
    $base=WP_PLUGIN_DIR.'/google-site-kit/';
    $js=glob($base.'dist/assets/js/googlesitekit-events-provider-woocommerce-*.js');
    if(count($js)!==1) exit(2);
    $tracking=file_get_contents($base.'includes/Core/Conversion_Tracking/Conversion_Tracking.php');
    if(!preg_match('/\$gtag_event = \'(.*?)\';/s',$tracking,$matches)) exit(3);
    $provider_php=file_get_contents($base.'includes/Core/Conversion_Tracking/Conversion_Event_Providers/WooCommerce.php');
    $template=wc_locate_template('checkout/thankyou.php');
    $template_source=file_get_contents($template);
    $out=['utc'=>gmdate('c'),'scope'=>'installed methods with synthetic objects, local JS collector only',
        'configuration_changed'=>false,'actual_orders_saved'=>0,'real_ga4_requests'=>0,
        'provider_js'=>file_get_contents($js[0]),'gtag_wrapper_js'=>$matches[1],
        'source_sha256'=>['provider_js'=>hash_file('sha256',$js[0]),'provider_php'=>hash('sha256',$provider_php),'tracking_php'=>hash('sha256',$tracking)],
        'template_evidence'=>['relative_path'=>str_replace(ABSPATH,'',$template),'sha256'=>hash('sha256',$template_source),
            'block_theme'=>wp_is_block_theme(),'woodmart_default_thankyou_content_enabled'=>function_exists('woodmart_get_opt')?(bool)woodmart_get_opt('thank_you_page_default_content'):null,
            'thankyou_hook_count'=>substr_count($template_source,"do_action( 'woocommerce_thankyou',")],
        'cases'=>$cases];
    echo json_encode($out,JSON_PRETTY_PRINT|JSON_UNESCAPED_SLASHES)."\n";
}
