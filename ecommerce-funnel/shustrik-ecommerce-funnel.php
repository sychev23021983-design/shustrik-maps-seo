<?php
/**
 * Plugin Name: Shustrik missing ecommerce events
 * Description: Disabled-by-default Site Kit view_item / begin_checkout extension.
 * Version: 0.1.0
 */
namespace Shustrik\EcommerceFunnel;
if (!defined('ABSPATH')) { exit; }

/** Only public catalogue fields enter the browser payload. */
function item($product, $quantity = 1, $unit_price = null) {
    if (!$product || $product->get_status() !== 'publish') { return null; }
    $quantity = (float) $quantity;
    if (!is_finite($quantity) || $quantity <= 0) { return null; }
    $result = [
        // Match Site Kit's parent-ID convention across all four funnel events.
        'item_id' => (string) ($product->is_type('variation') ? $product->get_parent_id() : $product->get_id()),
        'item_name' => wp_strip_all_tags($product->get_title()),
        'quantity' => $quantity,
    ];
    if ($product->is_type('variation')) {
        $attributes = $product->get_attributes();
        $parts = [];
        foreach ($attributes as $key => $value) {
            $parts[] = str_replace('attribute_', '', $key) . ': ' . $value;
        }
        if ($parts) { $result['item_variant'] = wp_strip_all_tags(implode(', ', $parts)); }
    }
    if ($unit_price !== null && is_numeric($unit_price) && is_finite((float) $unit_price) && (float) $unit_price >= 0) {
        $result['price'] = (float) $unit_price;
    }
    return $result;
}

function payload($items, $currency) {
    if (!$items || count($items) > 100 || !preg_match('/^[A-Z]{3}$/D', $currency)) { return null; }
    $data = ['currency' => $currency, 'items' => array_values($items), 'googlesitekit_event_provider' => 'woocommerce'];
    $value = 0;
    foreach ($items as $item) {
        if (!isset($item['price'])) { return $data; }
        $value += $item['price'] * $item['quantity'];
    }
    if (!is_finite($value)) { return null; }
    $data['value'] = round($value, wc_get_price_decimals());
    return $data;
}

function product_payload($product) {
    if (!$product) { return null; }
    // Variable parents have a price range: do not invent a selected variant or price.
    $price = $product->is_type('variable') ? null : $product->get_price();
    $item = item($product, 1, $price);
    return $item ? payload([$item], get_woocommerce_currency()) : null;
}

function checkout_payload($cart) {
    if (!$cart || $cart->is_empty()) { return null; }
    $items = [];
    foreach ($cart->get_cart() as $line) {
        $quantity = (float) ($line['quantity'] ?? 0);
        // Woo line_total is after discounts and excludes tax/shipping.
        $total = $line['line_total'] ?? null;
        if ($quantity <= 0 || !is_numeric($total) || !is_finite((float) $total) || (float) $total < 0) { return null; }
        // Re-read catalogue data instead of exporting customised cart item names/meta.
        $cart_product = $line['data'] ?? null;
        $catalogue_product = $cart_product ? wc_get_product($cart_product->get_id()) : null;
        $public_item = item($catalogue_product, $quantity, (float) $total / $quantity);
        if (!$public_item) { return null; }
        $items[] = $public_item;
    }
    return payload($items, get_woocommerce_currency());
}

function enqueue() {
    // WordPress persists a boolean true scalar as the string '1' on a fresh request.
    if (!in_array(get_option('shustrik_ecommerce_funnel_enabled', false), [true, '1'], true)
        || rtrim(home_url(), '/') !== 'https://shustrik-maps.com'
        || is_admin() || wp_doing_ajax() || wp_doing_cron() || is_feed()
        || (defined('REST_REQUEST') && REST_REQUEST)
        || is_user_logged_in()
        || !defined('GOOGLESITEKIT_VERSION') || GOOGLESITEKIT_VERSION !== '1.184.0'
        || !defined('WC_VERSION') || WC_VERSION !== '11.1.2'
        || !did_action('googlesitekit_analytics-4_init_tag')
        || !wp_script_is('google_gtagjs', 'enqueued')
        || !function_exists('WC') || !function_exists('is_product')) { return; }

    $tracking = get_option('googlesitekit_conversion_tracking', []);
    if (empty($tracking['enabled'])) { return; }
    // An upgrade that supplies either event must disable this extension entirely.
    $context = new \Google\Site_Kit\Context(WP_PLUGIN_DIR . '/google-site-kit/google-site-kit.php');
    $provider = new \Google\Site_Kit\Core\Conversion_Tracking\Conversion_Event_Providers\WooCommerce($context);
    if (array_intersect(['view_item', 'begin_checkout'], $provider->get_event_names())) { return; }

    $event = null;
    $data = null;
    if (is_product()) {
        $event = 'view_item';
        $data = product_payload(wc_get_product(get_queried_object_id()));
    } elseif (is_checkout() && !is_wc_endpoint_url() && !is_order_received_page()) {
        $event = 'begin_checkout';
        $data = checkout_payload(WC()->cart);
    }
    if (!$event || !$data) { return; }
    $handle = 'shustrik-ecommerce-funnel';
    wp_enqueue_script($handle, plugins_url('shustrik-ecommerce-funnel.js', __FILE__), ['google_gtagjs'], '0.1.0', true);
    wp_add_inline_script($handle, 'window.shustrikEcommerceFunnel = ' . wp_json_encode(['event' => $event, 'data' => $data], JSON_HEX_TAG | JSON_HEX_AMP | JSON_HEX_APOS | JSON_HEX_QUOT) . ';', 'before');
}
add_action('wp_enqueue_scripts', __NAMESPACE__ . '\\enqueue', 99);
