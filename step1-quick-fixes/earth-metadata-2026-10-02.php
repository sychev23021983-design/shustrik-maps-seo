<?php
// Narrow, guarded metadata release. Default is read-only; no credentials are logged.
require '/var/www/html/wp-load.php';
$id = 11517;
$url = 'https://shustrik-maps.com/product/earth-3d-model-terrain-without-water/';
$backup = '_shustrik_earth_metadata_backup_20261002';
$before = [
    '_yoast_wpseo_title' => 'Earth Terrain Without Water – 3D Model for Printing & CNC',
    '_yoast_wpseo_metadesc' => '3D terrain model of Earth with ocean surface removed, showing landmass elevation only. Ready for 3D printing and CNC.',
];
$after = [
    '_yoast_wpseo_title' => 'Earth Without Water 3D Model — C4D & OBJ Terrain',
    '_yoast_wpseo_metadesc' => "Explore Earth's terrain beneath the oceans with a 3D model in C4D and OBJ formats. View the file specifications, previews and texture details.",
];
function values($id, $keys) {
    $result = [];
    foreach ($keys as $key) $result[$key] = get_post_meta($id, $key, true);
    return $result;
}
function invariant($id) {
    $post = get_post($id);
    return [
        'url' => get_permalink($id), 'post_type' => $post->post_type,
        'status' => $post->post_status, 'post_title' => $post->post_title,
        'content_sha256' => hash('sha256', $post->post_content),
        'price' => get_post_meta($id, '_price', true),
        'robots_noindex' => get_post_meta($id, '_yoast_wpseo_meta-robots-noindex', true),
        'canonical_override' => get_post_meta($id, '_yoast_wpseo_canonical', true),
    ];
}
function abort_release($message) { fwrite(STDERR, $message . "\n"); exit(1); }
$state = invariant($id);
if ($state !== [
    'url' => $url, 'post_type' => 'product', 'status' => 'publish',
    'post_title' => 'Earth 3D model Terrain Without Water',
    'content_sha256' => '0762c44814ac11eea5781ce4fdfd1c9a44e94e3ea702c9504e71148107360528',
    'price' => '32', 'robots_noindex' => '', 'canonical_override' => '',
]) abort_release('Product invariants differ; no changes applied.');
$current = values($id, array_keys($before));
$mode = $argv[1] ?? '--preview';
if ($mode === '--preview') {
    echo json_encode(['mode' => 'preview', 'invariants' => $state, 'current' => $current,
        'proposed' => $after, 'expected_before_matches' => $current === $before], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE) . "\n";
    exit($current === $before ? 0 : 1);
}
if ($mode === '--apply') {
    if ($current !== $before) abort_release('Expected metadata differ; no changes applied.');
    if (metadata_exists('post', $id, $backup)) abort_release('Release backup already exists; no changes applied.');
    if (!add_post_meta($id, $backup, ['utc' => gmdate('c'), 'fields' => $before, 'invariants' => $state], true))
        abort_release('Backup failed; no changes applied.');
    $target = $after;
} elseif ($mode === '--rollback') {
    $saved = get_post_meta($id, $backup, true);
    if ($current !== $after || !is_array($saved) || ($saved['fields'] ?? null) !== $before || ($saved['invariants'] ?? null) !== $state)
        abort_release('Rollback guard failed; no changes applied.');
    $target = $before;
} else abort_release('Use --preview, --apply or --rollback.');
foreach ($target as $key => $value) update_post_meta($id, $key, $value);
if (values($id, array_keys($before)) !== $target || invariant($id) !== $state) {
    foreach ($current as $key => $value) update_post_meta($id, $key, $value);
    abort_release('Verification failed; previous metadata restored.');
}
if (function_exists('rocket_clean_files')) rocket_clean_files([$url]);
do_action('litespeed_purge_url', $url);
echo json_encode(['mode' => $mode, 'utc' => gmdate('c'), 'url' => $url,
    'post_id' => $id, 'fields' => values($id, array_keys($before)),
    'invariants_unchanged' => invariant($id) === $state, 'backup_key' => $backup],
    JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE) . "\n";
