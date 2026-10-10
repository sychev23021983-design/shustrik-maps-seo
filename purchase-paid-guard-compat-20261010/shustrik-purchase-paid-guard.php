<?php
/**
 * Plugin Name: Shustrik Site Kit paid purchase guard
 * Description: Disabled-by-default preview; gates the existing Site Kit purchase callback.
 * Version: 0.1.1
 */
namespace Shustrik\PurchasePaidGuard;
if (!defined('ABSPATH')) { exit; }
const PROVIDER_SHA256 = '82da28caecda75acca747963336c170ddf6399999a91f7ecb7588db0b6182c85';
const PROVIDER_CLASS = 'Google\\Site_Kit\\Core\\Conversion_Tracking\\Conversion_Event_Providers\\WooCommerce';
const OPTION = 'shustrik_purchase_paid_guard_enabled';

function confirmed_paid($order) {
    // is_paid alone is status based; require WooCommerce's recorded payment date too.
    return $order && $order->is_paid() && $order->get_date_paid() !== null;
}

/** Replace only the verified provider closure, preserving its hook slot/order/arity. */
function wrap_hook($hook) {
    if (!$hook instanceof \WP_Hook) { return 'missing-hook'; }
    $matches = [];
    foreach ($hook->callbacks as $priority => $callbacks) {
        foreach ($callbacks as $id => $entry) {
            $callback = $entry['function'];
            if (!$callback instanceof \Closure) { continue; }
            $reflection = new \ReflectionFunction($callback);
            $bound = $reflection->getClosureThis();
            if (!$bound || !is_a($bound, PROVIDER_CLASS)) { continue; }
            $file = $reflection->getFileName();
            if ($priority !== 10 || $entry['accepted_args'] !== 1 || !$file
                || !is_file($file) || hash_file('sha256', $file) !== PROVIDER_SHA256) {
                return 'provider-drift';
            }
            $matches[] = [$priority, $id, $callback];
        }
    }
    if (count($matches) !== 1) { return 'ambiguous-or-missing-provider'; }
    [$priority, $id, $original] = $matches[0];
    $hook->callbacks[$priority][$id]['function'] = static function ($order_id) use ($original) {
        $order = wc_get_order($order_id);
        if (!confirmed_paid($order)) { return; }
        // Original checks order key, marker and WGAI ownership and writes its own payload.
        $original($order_id);
    };
    return 'wrapped';
}

function environment_ready() {
    return in_array(get_option(OPTION, false), [true, '1'], true)
        && rtrim(home_url(), '/') === 'https://shustrik-maps.com'
        && defined('GOOGLESITEKIT_VERSION') && GOOGLESITEKIT_VERSION === '1.184.0'
        && defined('WC_VERSION') && WC_VERSION === '11.2.1'
        && !wp_is_block_theme() && !is_admin() && !wp_doing_ajax() && !wp_doing_cron()
        && !(defined('REST_REQUEST') && REST_REQUEST)
        && !is_user_logged_in() && is_order_received_page();
}

function install() {
    static $installed = false;
    if ($installed || !environment_ready()) { return; }
    global $wp_filter;
    $result = wrap_hook($wp_filter['woocommerce_thankyou'] ?? null);
    $GLOBALS['shustrik_purchase_paid_guard_state'] = $result;
    $installed = $result === 'wrapped';
}
// Site Kit registers provider hooks before wp. Change only this request's thankyou slot.
add_action('wp', __NAMESPACE__ . '\\install', PHP_INT_MAX);
