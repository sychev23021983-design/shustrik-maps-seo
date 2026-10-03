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
if (in_array($mode, ['--apply', '--reactivate'], true)) {
    if (GOOGLESITEKIT_VERSION !== '1.184.0' || WC_VERSION !== '11.1.2' || empty($tracking['enabled'])
        || array_intersect(['view_item', 'begin_checkout'], $provider->get_event_names())
        || !in_array($option, ['__absent__', false, ''], true)
        || ($mode === '--apply' && file_exists($backup))
        || ($mode === '--reactivate' && !file_exists($backup))) { exit(2); }
    // Hash the release archive bytes, including its configured export line endings.
    foreach (['php' => '8045005bf5e530ef441f41112311203383521a8cd0d456bfd4a5d8cc87460492', 'js' => '16c5b77b86afc1256715f66f206c89cea7c3baf490fd0379ee649e393fe523dc'] as $extension => $hash) {
        if (hash_file('sha256', WPMU_PLUGIN_DIR . '/shustrik-ecommerce-funnel.' . $extension) !== $hash) { exit(3); }
    }
    if ($mode === '--apply') {
        file_put_contents($backup, json_encode(['existed' => $option !== '__absent__', 'value' => $option === '__absent__' ? null : $option]), LOCK_EX);
        chmod($backup, 0600);
    } else {
        $saved = json_decode(file_get_contents($backup), true);
        if (!is_array($saved) || !isset($saved['existed'])
            || ($saved['existed'] ? $option !== $saved['value'] : $option !== '__absent__')) { exit(6); }
    }
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
