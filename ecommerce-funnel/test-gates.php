<?php
namespace Google\Site_Kit { class Context { function __construct($path) {} } }
namespace Google\Site_Kit\Core\Conversion_Tracking\Conversion_Event_Providers {
    class WooCommerce { function __construct($context) {} function get_event_names() { return $GLOBALS['state']['provider']; } }
}
namespace {
define('ABSPATH', '/test/'); define('WP_PLUGIN_DIR', '/test/plugins');
define('WC_VERSION', '11.1.2'); define('GOOGLESITEKIT_VERSION', '1.184.0');
function add_action(...$args) {}
function get_option($key, $fallback = false) { return $GLOBALS['state'][$key] ?? $fallback; }
function home_url() { return $GLOBALS['state']['home']; }
function is_admin() { return $GLOBALS['state']['admin']; }
function wp_doing_ajax() { return $GLOBALS['state']['ajax']; }
function wp_doing_cron() { return $GLOBALS['state']['cron']; }
function is_feed() { return $GLOBALS['state']['feed']; }
function is_user_logged_in() { return $GLOBALS['state']['loggedin']; }
function did_action($name) { return $GLOBALS['state']['analytics']; }
function wp_script_is($handle, $status) { return $GLOBALS['state']['tag']; }
function is_product() { return $GLOBALS['state']['product']; }
function is_checkout() { return $GLOBALS['state']['checkout']; }
function is_wc_endpoint_url() { return $GLOBALS['state']['endpoint']; }
function is_order_received_page() { return $GLOBALS['state']['received']; }
function WC() { return (object) ['cart' => new class { function is_empty() { return true; } }]; }
function get_queried_object_id() { return 11517; }
function wc_get_product($id) { return new class {
    function get_status() { return 'publish'; } function get_id() { return 11517; }
    function get_title() { return 'Public test product'; } function is_type($type) { return false; }
    function get_price() { return '32'; }
}; }
function wp_strip_all_tags($name) { return strip_tags($name); }
function wc_get_price_decimals() { return 2; }
function get_woocommerce_currency() { return 'USD'; }
function plugins_url($file, $base) { return '/test/' . $file; }
function wp_enqueue_script(...$args) { $GLOBALS['emitted']++; }
function wp_add_inline_script(...$args) {}
function wp_json_encode($data, $flags) { return json_encode($data, $flags); }
require __DIR__ . '/shustrik-ecommerce-funnel.php';
$base = ['shustrik_ecommerce_funnel_enabled' => true, 'googlesitekit_conversion_tracking' => ['enabled' => true],
    'home' => 'https://shustrik-maps.com', 'admin' => false, 'ajax' => false, 'cron' => false, 'feed' => false,
    'loggedin' => false, 'analytics' => 1, 'tag' => true, 'product' => true, 'checkout' => false,
    'endpoint' => false, 'received' => false, 'provider' => ['add_to_cart', 'purchase']];
$cases = [
    ['public product', [], 1], ['disabled default', ['shustrik_ecommerce_funnel_enabled' => false], 0],
    ['wrong site', ['home' => 'https://example.com'], 0], ['admin', ['admin' => true], 0],
    ['ajax', ['ajax' => true], 0], ['cron', ['cron' => true], 0], ['feed', ['feed' => true], 0],
    ['logged in excluded', ['loggedin' => true], 0], ['no analytics tag', ['analytics' => 0], 0],
    ['no enqueued loader', ['tag' => false], 0], ['conversion tracking off', ['googlesitekit_conversion_tracking' => ['enabled' => false]], 0],
    ['provider owns view_item', ['provider' => ['add_to_cart', 'purchase', 'view_item']], 0],
    ['provider owns begin_checkout', ['provider' => ['add_to_cart', 'purchase', 'begin_checkout']], 0],
    ['category/cart', ['product' => false], 0], ['order pay endpoint', ['product' => false, 'checkout' => true, 'endpoint' => true], 0],
    ['order received', ['product' => false, 'checkout' => true, 'received' => true], 0],
    ['empty checkout', ['product' => false, 'checkout' => true], 0],
];
foreach ($cases as [$name, $overrides, $expected]) {
    $GLOBALS['state'] = array_replace($base, $overrides); $GLOBALS['emitted'] = 0;
    \Shustrik\EcommerceFunnel\enqueue();
    if ($GLOBALS['emitted'] !== $expected) { throw new \RuntimeException($name); }
    echo 'PASS ' . $name . "\n";
}
echo count($cases) . " gate checks passed\n";
}
