<?php
// Read-only CLI preview. No cart sessions, option updates, orders or outbound GA calls.
ini_set('display_errors', '0');
define('WP_USE_THEMES', false);
ob_start(); require '/var/www/html/wp-load.php'; ob_end_clean();
if (PHP_SAPI !== 'cli' || rtrim(home_url(), '/') !== 'https://shustrik-maps.com') { exit(1); }
require __DIR__ . '/shustrik-ecommerce-funnel.php';
$product = wc_get_product(11517);
if (!$product) { exit(1); }
$tests = [];
$check = function ($name, $condition) use (&$tests) {
    $tests[$name] = (bool) $condition;
    if (!$condition) { throw new RuntimeException($name); }
};
$view = \Shustrik\EcommerceFunnel\product_payload($product);
$check('public_product', $view['items'][0]['item_id'] === '11517' && $view['currency'] === 'USD' && $view['value'] === 32.0);
$check('zero_quantity_rejected', \Shustrik\EcommerceFunnel\item($product, 0, 32) === null);
$check('negative_quantity_rejected', \Shustrik\EcommerceFunnel\item($product, -1, 32) === null);
$check('non_finite_quantity_rejected', \Shustrik\EcommerceFunnel\item($product, INF, 32) === null);
$check('empty_items_rejected', \Shustrik\EcommerceFunnel\payload([], 'USD') === null);
$check('invalid_currency_rejected', \Shustrik\EcommerceFunnel\payload($view['items'], 'bad') === null);
$check('oversized_cart_rejected', \Shustrik\EcommerceFunnel\payload(array_fill(0, 101, $view['items'][0]), 'USD') === null);
$line = ['data' => $product, 'quantity' => 2, 'line_total' => 60, 'customer_email' => 'SYNTHETIC-DO-NOT-EXPORT', 'custom_item_data' => 'SYNTHETIC-DO-NOT-EXPORT'];
$cart = new class($line) {
    private $line;
    function __construct($line) { $this->line = $line; }
    function is_empty() { return false; }
    function get_cart() { return [$this->line]; }
};
$checkout = \Shustrik\EcommerceFunnel\checkout_payload($cart);
$check('discounted_cart_value', $checkout['value'] === 60.0 && $checkout['items'][0]['price'] === 30.0 && $checkout['items'][0]['quantity'] === 2.0);
$check('no_custom_or_customer_fields', strpos(json_encode($checkout), 'SYNTHETIC') === false && array_keys($checkout['items'][0]) === ['item_id', 'item_name', 'quantity', 'price']);
$empty = new class { function is_empty() { return true; } };
$check('empty_cart_rejected', \Shustrik\EcommerceFunnel\checkout_payload($empty) === null);
$variable = new class {
    function get_status() { return 'publish'; } function get_id() { return 101; }
    function get_title() { return 'Synthetic variable'; } function is_type($type) { return $type === 'variable'; }
};
$variable_data = \Shustrik\EcommerceFunnel\product_payload($variable);
$check('variable_parent_no_invented_price', !isset($variable_data['value']) && !isset($variable_data['items'][0]['price']));
$variation = new class {
    function get_status() { return 'publish'; } function get_id() { return 102; } function get_parent_id() { return 101; }
    function get_title() { return 'Synthetic variable'; } function is_type($type) { return $type === 'variation'; }
    function get_attributes() { return ['pa_format' => 'stl']; }
};
$variant_item = \Shustrik\EcommerceFunnel\item($variation, 1, 12);
$check('variation_matches_sitekit_parent_id', $variant_item['item_id'] === '101' && $variant_item['item_variant'] === 'pa_format: stl');
$context = new \Google\Site_Kit\Context(WP_PLUGIN_DIR . '/google-site-kit/google-site-kit.php');
$provider = new \Google\Site_Kit\Core\Conversion_Tracking\Conversion_Event_Providers\WooCommerce($context);
echo json_encode([
    'utc' => gmdate('c'), 'mode' => 'read-only-cli-preview',
    'wc_version' => WC_VERSION, 'sitekit_version' => GOOGLESITEKIT_VERSION,
    'existing_provider_events' => $provider->get_event_names(),
    'enabled_option' => get_option('shustrik_ecommerce_funnel_enabled', false),
    'view_item_preview' => $view, 'synthetic_discounted_checkout_preview' => $checkout,
    'checks' => $tests, 'production_modified' => false, 'ga4_delivery_verified' => false,
], JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES) . "\n";
