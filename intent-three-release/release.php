<?php
// Exact owner-approved title/meta/intro release; no save filters or download URLs emitted.
ini_set('display_errors','0');
define('WP_USE_THEMES',false);
ob_start();require '/var/www/html/wp-load.php';ob_end_clean();
function stop_release($message){throw new RuntimeException($message);}
function invariant_three($id){
    $p=get_post($id);$hashes=[];
    foreach(['_price','_regular_price','_sale_price','_sku','_stock','_stock_status','_manage_stock','_downloadable','_virtual','_downloadable_files','_download_limit','_download_expiry','_thumbnail_id','_product_image_gallery','_tax_status','_tax_class'] as $k)$hashes[$k]=hash('sha256',serialize(get_post_meta($id,$k,true)));
    $cats=wp_get_post_terms($id,'product_cat',['fields'=>'ids']);if(is_wp_error($cats))stop_release('Category read failed');sort($cats);
    return ['url'=>get_permalink($id),'type'=>$p->post_type,'status'=>$p->post_status,'slug'=>$p->post_name,'h1'=>$p->post_title,'excerpt_sha256'=>hash('sha256',$p->post_excerpt),'commerce_hashes'=>$hashes,'categories'=>$cats,'currency'=>get_woocommerce_currency(),'robots'=>get_post_meta($id,'_yoast_wpseo_meta-robots-noindex',true),'follow'=>get_post_meta($id,'_yoast_wpseo_meta-robots-nofollow',true),'canonical'=>get_post_meta($id,'_yoast_wpseo_canonical',true)];
}
function current_three($id){$p=get_post($id);return ['seo_title'=>get_post_meta($id,'_yoast_wpseo_title',true),'meta_description'=>get_post_meta($id,'_yoast_wpseo_metadesc',true),'content_sha256'=>hash('sha256',$p->post_content)];}
function target_three($r,$body){
    if(substr_count($body,$r['before']['first_paragraph_source'])!==1)stop_release('Intro source not unique');
    return str_replace($r['before']['first_paragraph_source'],$r['after']['first_paragraph_text'],$body);
}
function invalidate_three($id){clean_post_cache($id);wp_cache_delete($id,'post_meta');}
function rebuild_three($id){
    invalidate_three($id);
    if(function_exists('YoastSEO')&&class_exists('Yoast\\WP\\SEO\\Builders\\Indexable_Builder'))YoastSEO()->classes->get('Yoast\\WP\\SEO\\Builders\\Indexable_Builder')->build_for_id_and_type($id,'post');
}
try{
    if(PHP_SAPI!=='cli'||rtrim(home_url(),'/')!=='https://shustrik-maps.com')stop_release('CLI/site mismatch');
    $mode=$argv[1]??'--preview';if(!in_array($mode,['--snapshot','--preview','--apply','--verify','--rollback','--rollback-preview'],true))stop_release('Unknown mode');
    $m=json_decode(file_get_contents(__DIR__.'/proposals.json'),true,512,JSON_THROW_ON_ERROR);
    $rows=$m['products'];$ids=array_column($rows,'id');
    if($m['status']!=='approved'||$m['mutation_allowed']!==true||$m['change_count']!==9||$ids!==[17483,16047,15996])stop_release('Approval/scope mismatch');
    $key='_shustrik_intent_three_backup_20261004';$snapshot=[];
    foreach($rows as $r){$id=$r['id'];invalidate_three($id);$s=invariant_three($id);$f=current_three($id);
        if($s['url']!==$r['url']||$s['slug']!==$r['slug']||$s['type']!=='product'||$s['status']!=='publish'||$s['h1']!==$r['unchanged_h1'])stop_release('Product identity drift');
        $snapshot[]=['id'=>$id,'invariants'=>$s,'fields'=>$f];
    }
    if($mode==='--snapshot'){echo json_encode(['utc'=>gmdate('c'),'rows'=>$snapshot],JSON_PRETTY_PRINT|JSON_UNESCAPED_SLASHES)."\n";exit;}
    $baseline=json_decode(file_get_contents(__DIR__.'/baseline.json'),true,512,JSON_THROW_ON_ERROR)['rows'];if(count($baseline)!==3)stop_release('Baseline scope');
    $backup=get_option($key,null);$rollback=in_array($mode,['--rollback','--rollback-preview'],true);$bodies=[];$targets=[];
    foreach($rows as $i=>$r){$id=$r['id'];$s=$snapshot[$i];$base=$baseline[$i];$g=$r['guards'];
        if($s['id']!==$base['id']||$s['invariants']!==$base['invariants'])stop_release('Protected drift');
        $inv=$s['invariants'];
        if($inv['excerpt_sha256']!==$g['excerpt_sha256']||$inv['commerce_hashes']['_downloadable_files']!==$g['download_config_sha256']||$inv['robots']!==$g['noindex_override']||$inv['canonical']!==$g['canonical_override'])stop_release('Approval baseline drift');
        if($base['fields']!==['seo_title'=>$r['before']['seo_title'],'meta_description'=>$r['before']['meta_description'],'content_sha256'=>$g['content_sha256']])stop_release('Baseline differs from approved before');
        if($rollback||$mode==='--verify'){
            if(!is_array($backup)||$backup['baseline']!==$baseline||$backup['proposals']!==$m)stop_release('Backup mismatch');
            $old=$backup['content'][$id];if(hash('sha256',$old)!==$g['content_sha256'])stop_release('Backup body mismatch');
        }else{$old=get_post($id)->post_content;}
        $new=target_three($r,$old);$bodies[$id]=$old;$targets[$id]=$new;
        $expected=$mode==='--verify'||$rollback?['seo_title'=>$r['after']['seo_title'],'meta_description'=>$r['after']['meta_description'],'content_sha256'=>hash('sha256',$new)]:$base['fields'];
        if($s['fields']!==$expected)stop_release('Exact field/content drift');
    }
    if($mode==='--verify'||$mode==='--rollback-preview'){
        echo json_encode(['mode'=>$mode,'ok'=>true,'utc'=>gmdate('c'),'products'=>3,'fields'=>9,'protected_preserved'=>true,'backup_present'=>true])."\n";exit;
    }
    if($mode==='--preview'){if($backup!==null)stop_release('Backup already exists');echo json_encode(['mode'=>$mode,'ok'=>true,'products'=>3,'fields'=>9,'unique_sources'=>true,'protected_preserved'=>true])."\n";exit;}
    if($mode==='--apply'&&!add_option($key,['utc'=>gmdate('c'),'baseline'=>$baseline,'proposals'=>$m,'content'=>$bodies],'',false))stop_release('Backup creation failed');
    global $wpdb;$wpdb->query('START TRANSACTION');
    try{
        foreach($rows as $i=>$r){$id=$r['id'];$wpdb->get_var($wpdb->prepare("SELECT ID FROM {$wpdb->posts} WHERE ID=%d FOR UPDATE",$id));invalidate_three($id);
            if(current_three($id)!==$snapshot[$i]['fields']||invariant_three($id)!==$baseline[$i]['invariants'])stop_release('Concurrent drift');
            $body=$mode==='--apply'?$targets[$id]:$bodies[$id];$expectedBody=$mode==='--apply'?$bodies[$id]:$targets[$id];$values=$mode==='--apply'?$r['after']:$r['before'];
            $ok=$wpdb->query($wpdb->prepare("UPDATE {$wpdb->posts} SET post_content=%s,post_modified=%s,post_modified_gmt=%s WHERE ID=%d AND post_content=%s",$body,current_time('mysql'),current_time('mysql',true),$id,$expectedBody));
            if($ok!==1)stop_release('Guarded body update failed');
            update_post_meta($id,'_yoast_wpseo_title',wp_slash($values['seo_title']));update_post_meta($id,'_yoast_wpseo_metadesc',wp_slash($values['meta_description']));
            rebuild_three($id);
            if(current_three($id)!==['seo_title'=>$values['seo_title'],'meta_description'=>$values['meta_description'],'content_sha256'=>hash('sha256',$body)]||invariant_three($id)!==$baseline[$i]['invariants'])stop_release('Exact/protected verification failed');
        }
        $wpdb->query('COMMIT');
    }catch(Throwable $e){$wpdb->query('ROLLBACK');foreach($rows as $r)invalidate_three($r['id']);throw $e;}
    foreach($rows as $r){invalidate_three($r['id']);if(function_exists('rocket_clean_files'))rocket_clean_files([$r['url']]);do_action('litespeed_purge_url',$r['url']);}
    echo json_encode(['mode'=>$mode,'ok'=>true,'utc'=>gmdate('c'),'products'=>3,'fields'=>9,'protected_preserved'=>true,'backup_option'=>$key,'transaction'=>'committed'])."\n";
}catch(Throwable $e){echo json_encode(['ok'=>false,'reason'=>$e instanceof RuntimeException?$e->getMessage():'Internal execution error'])."\n";exit(1);}
