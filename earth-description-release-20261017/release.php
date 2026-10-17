<?php
ini_set('display_errors', '0');
define('WP_USE_THEMES', false);
ob_start(); require '/var/www/html/wp-load.php'; ob_end_clean();

function stop_release($message) { throw new RuntimeException($message); }
function protected_hash($id) {
    $post = (array) get_post($id);
    unset($post['post_content'], $post['post_modified'], $post['post_modified_gmt']);
    $meta = get_post_meta($id); unset($meta['wd_page_css_files']);
    $terms = wp_get_object_terms($id, get_object_taxonomies(get_post($id)->post_type), ['fields' => 'all']);
    return hash('sha256', serialize([$post, $meta, $terms]));
}
function assert_previous_release($baseline) {
    foreach ($baseline['previous_release'] as $id => $expected) {
        clean_post_cache((int)$id); $meta = get_post_meta((int)$id); unset($meta['wd_page_css_files']);
        $actual = hash('sha256', serialize([get_post((int)$id), $meta, wp_get_object_terms((int)$id, get_object_taxonomies(get_post((int)$id)->post_type), ['fields'=>'all'])]));
        if ($actual !== $expected) stop_release('Prior article release drift');
    }
}
function assert_scope($manifest, $baseline) {
    assert_previous_release($baseline);
    if (array_column($manifest['posts'], 'id') !== [11517]) stop_release('Wrong post scope');
    if (array_column($baseline['posts'], 'id') !== [11517]) stop_release('Wrong baseline scope');
    foreach ($manifest['posts'] as $index => $item) {
        $before = $baseline['posts'][$index]['content'];
        if (hash('sha256', $before) !== $item['before_sha256']) stop_release('Baseline hash mismatch');
        $edits = $item['edits']; usort($edits, function($a, $b) { return $b['at'] <=> $a['at']; });
        $computed = $before;
        foreach ($edits as $edit) {
            $offset = $edit['at_bytes'];
            $prefix = substr($computed, 0, $offset);
            $old = $edit['old'] ?? '';
            if (substr($computed, $offset, strlen($old)) !== $old) stop_release('Edit guard mismatch');
            $computed = $prefix . $edit['text'] . substr($computed, $offset + strlen($old));
        }
        $after = file_get_contents(__DIR__ . '/' . $item['file']);
        if ($computed !== $after || hash('sha256', $after) !== $item['after_sha256']) stop_release('Candidate mismatch');
        $normalized = $after;
        preg_match_all('/\[[^\]]+\]/', $before, $left); preg_match_all('/\[[^\]]+\]/', $normalized, $right);
        if ($left[0] !== $right[0]) stop_release('Shortcode drift');
        if (substr_count($after, '<a ') - substr_count($before, '<a ') !== $item['links_added']) stop_release('Link count mismatch');
        $post = get_post($item['id']);
        if (!$post || $post->post_type !== $item['post_type'] || $post->post_status !== 'publish' || $post->post_name !== $item['slug'] || get_permalink($item['id']) !== $item['url']) stop_release('Identity drift');
        if (protected_hash($item['id']) !== $item['protected_hash']) stop_release('Protected metadata or taxonomy drift');
    }
}
function assert_content($manifest, $baseline, $after) {
    foreach ($manifest['posts'] as $index => $item) {
        $expected = $after ? file_get_contents(__DIR__ . '/' . $item['file']) : $baseline['posts'][$index]['content'];
        if (get_post($item['id'])->post_content !== $expected) stop_release('Current content drift: ' . $item['id']);
    }
}
function write_all($manifest, $baseline, $rollback) {
    global $wpdb;
    $wpdb->query('START TRANSACTION');
    try {
        $wpdb->get_results("SELECT ID FROM {$wpdb->posts} WHERE ID IN (11517) ORDER BY ID FOR UPDATE");
        foreach ($manifest['posts'] as $item) clean_post_cache($item['id']);
        assert_scope($manifest, $baseline); assert_content($manifest, $baseline, $rollback);
        foreach ($manifest['posts'] as $index => $item) {
            $before = $baseline['posts'][$index]['content']; $after = file_get_contents(__DIR__ . '/' . $item['file']);
            $expected = $rollback ? $after : $before; $replacement = $rollback ? $before : $after;
            $changed = $wpdb->query($wpdb->prepare("UPDATE {$wpdb->posts} SET post_content=%s,post_modified=%s,post_modified_gmt=%s WHERE ID=%d AND BINARY post_content=BINARY %s", $replacement, current_time('mysql'), current_time('mysql', true), $item['id'], $expected));
            if ($changed !== 1) stop_release('Conditional write failed');
            clean_post_cache($item['id']);
        }
        assert_scope($manifest, $baseline); assert_content($manifest, $baseline, !$rollback);
        $wpdb->query('COMMIT');
    } catch (Throwable $error) {
        $wpdb->query('ROLLBACK'); foreach ($manifest['posts'] as $item) clean_post_cache($item['id']); throw $error;
    }
}
try {
    if (PHP_SAPI !== 'cli' || rtrim(home_url(), '/') !== 'https://shustrik-maps.com') stop_release('Wrong runtime');
    $mode = $argv[1] ?? '--preview';
    if (!in_array($mode, ['--preview','--apply','--verify','--rollback-preview','--rollback'], true)) stop_release('Wrong mode');
    $manifest = json_decode(file_get_contents(__DIR__ . '/manifest.json'), true, 512, JSON_THROW_ON_ERROR);
    $baseline = json_decode(file_get_contents(__DIR__ . '/baseline.json'), true, 512, JSON_THROW_ON_ERROR);
    foreach ($baseline['tables'] as $engine) if ($engine !== 'InnoDB') stop_release('Non-transactional baseline table');
    assert_scope($manifest, $baseline);
    $key = '_shustrik_earth_description_backup_20261017';
    if ($manifest['backup_key'] !== $key) stop_release('Wrong backup key');
    $backup = get_option($key, null);
    if (in_array($mode, ['--preview','--apply'], true)) {
        if ($backup !== null) stop_release('Existing release; inspect before retry');
        assert_content($manifest, $baseline, false);
    } else {
        if (!$backup || $backup['status'] !== 'published' || $backup['manifest_sha256'] !== hash_file('sha256', __DIR__ . '/manifest.json')) stop_release('Published backup missing or mismatched');
        assert_content($manifest, $baseline, true);
    }
    if ($mode === '--apply') {
        $backup = ['status'=>'prepared','prepared_at'=>gmdate('c'),'manifest_sha256'=>hash_file('sha256', __DIR__ . '/manifest.json'),'posts'=>$baseline['posts']];
        if (!add_option($key, $backup, '', false)) stop_release('Backup collision');
        write_all($manifest, $baseline, false);
        $backup['status'] = 'published'; $backup['published_at'] = gmdate('c'); update_option($key, $backup, false);
    }
    if ($mode === '--rollback') {
        write_all($manifest, $baseline, true);
        $backup['status'] = 'rolled-back'; $backup['rolled_back_at'] = gmdate('c'); update_option($key, $backup, false);
    }
    if (in_array($mode, ['--apply','--rollback'], true)) {
        foreach ($manifest['posts'] as $item) {
            clean_post_cache($item['id']);
            if (function_exists('rocket_clean_files')) rocket_clean_files([$item['url']]);
            do_action('litespeed_purge_url', $item['url']);
        }
    }
    $result = [];
    foreach ($manifest['posts'] as $item) $result[] = ['id'=>$item['id'],'url'=>$item['url'],'content_sha256'=>hash('sha256', get_post($item['id'])->post_content),'protected_preserved'=>protected_hash($item['id']) === $item['protected_hash'],'links_added'=>$item['links_added']];
    echo json_encode(['ok'=>true,'mode'=>$mode,'utc'=>gmdate('c'),'posts'=>$result,'backup_key'=>$key,'backup_status'=>$backup['status']??null], JSON_UNESCAPED_SLASHES) . "\n";
} catch (Throwable $error) {
    echo json_encode(['ok'=>false,'reason'=>$error instanceof RuntimeException?$error->getMessage():'Internal failure']) . "\n"; exit(1);
}
