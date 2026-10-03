<?php
// Own-option-only deployment helper. No auth, customer or order data.
ini_set('display_errors', '0');
define('WP_USE_THEMES', false);
ob_start(); require '/var/www/html/wp-load.php'; ob_end_clean();
if (PHP_SAPI !== 'cli' || rtrim(home_url(), '/') !== 'https://shustrik-maps.com') { exit(1); }
$key = 'shustrik_ecommerce_funnel_enabled';
$backup = '/tmp/shustrik-ecommerce-option-backup-20261003.json';
$option = get_option($key, '__absent__');
$context = new \Google\Site_Kit\Context(WP_PLUGIN_DIR . '/google-site-kit/google-site-kit.php');
$provider = new \Google\Site_Kit\Core\Conversion_Tracking\Conversion_Event_Providers\WooCommerce($context);
$tracking = get_option('googlesitekit_conversion_tracking', []);
$mode = $argv[1] ?? '--inspect';
if ($mode === '--apply') {
    if (GOOGLESITEKIT_VERSION !== '1.184.0' || WC_VERSION !== '11.1.2' || empty($tracking['enabled'])
        || array_intersect(['view_item', 'begin_checkout'], $provider->get_event_names())
        || !in_array($option, ['__absent__', false, ''], true) || file_exists($backup)) { exit(2); }
    foreach (['php' => 'd5192098c17102d6d99c8b217b5231b90ff959930ace2c59cdb3914194fae4e6', 'js' => '5aee12fd60f52329f1f55122196ed8fb202db4f19d6d008857ee1cab809c4804'] as $extension => $hash) {
        if (hash_file('sha256', WPMU_PLUGIN_DIR . '/shustrik-ecommerce-funnel.' . $extension) !== $hash) { exit(3); }
    }
    file_put_contents($backup, json_encode(['existed' => $option !== '__absent__', 'value' => $option === '__absent__' ? null : $option]), LOCK_EX);
    chmod($backup, 0600);
    update_option($key, true, false);
} elseif ($mode === '--rollback') {
    $saved = json_decode(file_get_contents($backup), true);
    if (!is_array($saved) || !isset($saved['existed'])) { exit(4); }
    if ($saved['existed']) { update_option($key, $saved['value'], false); }
    else { delete_option($key); }
} elseif ($mode !== '--inspect') { exit(5); }
echo json_encode(['utc' => gmdate('c'), 'mode' => $mode, 'enabled' => in_array(get_option($key, false), [true, '1'], true),
    'own_option_existed_before' => $option !== '__absent__', 'wc_version' => WC_VERSION,
    'sitekit_version' => GOOGLESITEKIT_VERSION, 'conversion_tracking_enabled' => !empty($tracking['enabled']),
    'provider_events' => $provider->get_event_names()]) . "\n";
