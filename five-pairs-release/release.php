<?php
// Owner-approved title/meta/H1 release, CLI only. No credentials or file URLs are emitted.
ini_set('display_errors', '0');
define('WP_USE_THEMES', false);
ob_start(); require '/var/www/html/wp-load.php'; ob_end_clean();
function fail_release($message) { throw new RuntimeException($message); }
function invariant($id) {
    $p = get_post($id);
    if (!$p) fail_release('Missing product');
    $commerce = [];
    foreach (['_price','_regular_price','_sale_price','_sku','_stock','_stock_status','_manage_stock','_downloadable','_virtual','_downloadable_files','_download_limit','_download_expiry','_thumbnail_id','_product_image_gallery','_tax_status','_tax_class'] as $key) {
        $commerce[$key] = hash('sha256', serialize(get_post_meta($id, $key, true)));
    }
    $categories = wp_get_post_terms($id, 'product_cat', ['fields'=>'ids']);
    if (is_wp_error($categories)) fail_release('Category read failed');
    sort($categories);
    return ['url'=>get_permalink($id),'type'=>$p->post_type,'status'=>$p->post_status,'slug'=>$p->post_name,
        'content_sha256'=>hash('sha256',$p->post_content),'excerpt_sha256'=>hash('sha256',$p->post_excerpt),
        'commerce_hashes'=>$commerce,'categories'=>$categories,'currency'=>get_woocommerce_currency(),
        'robots'=>get_post_meta($id,'_yoast_wpseo_meta-robots-noindex',true),
        'robots_follow'=>get_post_meta($id,'_yoast_wpseo_meta-robots-nofollow',true),
        'canonical'=>get_post_meta($id,'_yoast_wpseo_canonical',true)];
}
function fields($id) {
    return ['h1'=>get_post($id)->post_title,
        'title'=>get_post_meta($id,'_yoast_wpseo_title',true),
        'description'=>get_post_meta($id,'_yoast_wpseo_metadesc',true),
        'title_exists'=>metadata_exists('post',$id,'_yoast_wpseo_title'),
        'description_exists'=>metadata_exists('post',$id,'_yoast_wpseo_metadesc')];
}
function after_fields($r) { return ['h1'=>$r['h1'],'title'=>$r['title'],'description'=>$r['description'],'title_exists'=>true,'description_exists'=>true]; }
function write_fields($id,$target,$slug) {
    foreach (['title'=>'_yoast_wpseo_title','description'=>'_yoast_wpseo_metadesc'] as $field=>$key) {
        if ($target[$field.'_exists']) update_post_meta($id,$key,wp_slash($target[$field]));
        else delete_post_meta($id,$key);
    }
    $result=wp_update_post(wp_slash(['ID'=>$id,'post_title'=>$target['h1'],'post_name'=>$slug]),true);
    if (is_wp_error($result)) fail_release('Product title write failed');
    clean_post_cache($id);
    if (fields($id)!==$target) fail_release('Exact field verification failed');
}
try {
    if (PHP_SAPI!=='cli' || rtrim(home_url(),'/')!=='https://shustrik-maps.com') fail_release('CLI/site guard failed');
    $mode=$argv[1] ?? '--preview';
    if (!in_array($mode,['--snapshot','--preview','--apply','--verify','--rollback'],true)) fail_release('Unsupported mode');
    $rows=json_decode(file_get_contents(__DIR__.'/proposals.json'),true,512,JSON_THROW_ON_ERROR);
    if(count($rows)!==10 || count(array_unique(array_column($rows,'url')))!==10) fail_release('Scope guard failed');
    $key='_shustrik_five_pairs_backup_20261003';
    $snapshot=[];
    foreach($rows as $r) {
        $id=url_to_postid($r['url']); $state=invariant($id);
        if($state['url']!==$r['url'] || $state['type']!=='product' || $state['status']!=='publish') fail_release('Product identity guard failed');
        $snapshot[]=['id'=>$id,'url'=>$r['url'],'fields'=>fields($id),'invariants'=>$state];
    }
    if($mode==='--snapshot') {
        echo json_encode(['mode'=>'snapshot','utc'=>gmdate('c'),'rows'=>$snapshot],JSON_PRETTY_PRINT|JSON_UNESCAPED_SLASHES)."\n"; exit;
    }
    $baseline=json_decode(file_get_contents(__DIR__.'/baseline.json'),true,512,JSON_THROW_ON_ERROR)['rows'];
    if(count($baseline)!==10) fail_release('Baseline count guard failed');
    $backup=get_option($key,null);
    foreach($snapshot as $i=>$s) {
        if($s['id']!==$baseline[$i]['id'] || $s['url']!==$baseline[$i]['url'] || $s['invariants']!==$baseline[$i]['invariants']) fail_release('Invariant drift; no writes');
        if($mode==='--rollback') {
            if(!is_array($backup) || ($backup['rows'] ?? null)!==$baseline || ($backup['proposals'] ?? null)!==$rows) fail_release('Backup guard failed');
            if($s['fields']!==after_fields($rows[$i]) && $s['fields']!==$baseline[$i]['fields']) fail_release('Rollback field drift; no writes');
        } elseif($mode==='--verify') {
            if($s['fields']!==after_fields($rows[$i])) fail_release('Published field mismatch');
        } elseif($s['fields']!==$baseline[$i]['fields']) fail_release('Field drift; no writes');
    }
    if($mode==='--verify') {
        echo json_encode(['mode'=>'verify','ok'=>true,'utc'=>gmdate('c'),'count'=>10,'fields_match'=>true,'invariants_preserved'=>true,'backup_present'=>is_array($backup)])."\n"; exit;
    }
    if($mode==='--preview') {
        echo json_encode(['mode'=>'preview','count'=>10,'all_guards_pass'=>true,'backup_exists'=>$backup!==null])."\n"; exit($backup===null ? 0 : 1);
    }
    if($mode==='--apply') {
        if($backup!==null) fail_release('Backup exists; repeat apply refused');
        if(!add_option($key,['utc'=>gmdate('c'),'rows'=>$baseline,'proposals'=>$rows],'',false)) fail_release('Backup write failed');
    }
    $attempted=[];
    try {
        foreach($baseline as $i=>$old) {
            // Recheck each product immediately before mutation, preserving concurrent owner edits.
            if(invariant($old['id'])!==$old['invariants'] || fields($old['id'])!==$snapshot[$i]['fields']) fail_release('Concurrent drift');
            $attempted[]=$i;
            $target=$mode==='--apply' ? after_fields($rows[$i]) : $old['fields'];
            write_fields($old['id'],$target,$old['invariants']['slug']);
            if(invariant($old['id'])!==$old['invariants']) fail_release('Untouched invariant changed');
        }
    } catch(Throwable $e) {
        // Restore only fields still equal to this release's before/after values.
        $restored=0;
        foreach(array_reverse($attempted) as $i) {
            $id=$baseline[$i]['id']; $current=fields($id);
            $safe=$current['h1']===$baseline[$i]['fields']['h1'] || $current['h1']===$rows[$i]['h1'];
            foreach(['title','description'] as $f) $safe=$safe && in_array($current[$f],[$baseline[$i]['fields'][$f],$rows[$i][$f]],true);
            if(!$safe) continue;
            write_fields($id,$snapshot[$i]['fields'],$baseline[$i]['invariants']['slug']); $restored++;
        }
        echo json_encode(['mode'=>$mode,'ok'=>false,'attempted'=>count($attempted),'restored'=> $restored,'manual_check_required'=>$restored!==count($attempted)])."\n"; exit(2);
    }
    foreach($baseline as $old) {
        if(function_exists('rocket_clean_files')) rocket_clean_files([$old['url']]);
        do_action('litespeed_purge_url',$old['url']);
    }
    echo json_encode(['mode'=>$mode,'ok'=>true,'utc'=>gmdate('c'),'count'=>10,'invariants_preserved'=>true,'backup_option'=>$key])."\n";
} catch(Throwable $e) {
    echo json_encode(['ok'=>false,'classification'=>'release_guard_or_execution_error','reason'=>$e instanceof RuntimeException ? $e->getMessage() : 'internal_error'])."\n"; exit(1);
}
