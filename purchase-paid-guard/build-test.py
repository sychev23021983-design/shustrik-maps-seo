from pathlib import Path
p=Path(__file__).parent
source=(p.parent/'purchase-lab/capture-installed.php').read_text(encoding='utf-8-sig')
head=source.split('    $cases=[];')[0]
head=head.replace('namespace {', '''namespace Shustrik\\PurchasePaidGuard {
    function wc_get_order($id){return $GLOBALS['shustrik_lab_order']??false;}
    function get_option($key,$default=false){return $key===OPTION?($GLOBALS['lab_enabled']??false):\\get_option($key,$default);}
    function is_order_received_page(){return $GLOBALS['lab_receipt']??false;}
}
namespace {''',1)
head=head.replace('public $status,$marker,$save_calls=0,$valid,$item;', 'public $status,$marker,$save_calls=0,$valid,$item,$paid_date=true,$total="15";')
head=head.replace("public function get_total(){return '15';}", 'public function get_total(){return $this->total;}')
head=head.replace('public function get_currency()', "public function get_date_paid(){return $this->paid_date && $this->is_paid()?new \\WC_DateTime('2026-10-03T00:00:00Z'):null;}\n            public function get_currency()")
tail=(p/'test-body.txt').read_text(encoding='utf-8-sig')
(p/'test-installed.php').write_text(head+tail,encoding='utf-8')
