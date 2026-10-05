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

try {
 if(PHP_SAPI!=='cli'||rtrim(home_url(),'/')!=='https://shustrik-maps.com')stop_release('CLI/site mismatch');
 $mode=$argv[1]??'--preview';if(!in_array($mode,['--preview','--apply','--verify','--rollback-preview','--rollback'],true))stop_release('Mode');
 $m=json_decode(file_get_contents(__DIR__.'/proposals.json'),true,512,JSON_THROW_ON_ERROR);
 $baseline=json_decode(file_get_contents(__DIR__.'/baseline.json'),true,512,JSON_THROW_ON_ERROR)['rows'];
 if($m['status']!=='approved'||$m['mutation_allowed']!==true||array_column($m['products'],'id')!==[9522,9446,10102])stop_release('Scope');
 $key='_shustrik_optimization_three_backup_20261005';$backup=get_option($key,null);$rollback=in_array($mode,['--rollback','--rollback-preview'],true);$after=$rollback||$mode==='--verify';$snap=[];
 foreach($m['products'] as $i=>$r){$id=$r['id'];invalidate_three($id);$b=$baseline[$i];
  if($b['id']!==$id||$b['invariants']!==$r['invariants']||invariant_three($id)!==$r['invariants'])stop_release('Protected data drift');
  if($r['invariants']['url']!==$r['url']||$r['invariants']['type']!=='product'||$r['invariants']['status']!=='publish')stop_release('Identity');
  if($b['fields']!==$r['before']||hash('sha256',$b['post_content'])!==$r['before']['content_sha256']||hash('sha256',$r['content_after'])!==$r['after']['content_sha256'])stop_release('Manifest hashes');
  if($id===10102&&($r['before']['seo_title']!==$r['after']['seo_title']||$r['before']['meta_description']!==$r['after']['meta_description']))stop_release('USA metadata scope');
  $fields=current_three($id);if($fields!==($after?$r['after']:$r['before']))stop_release('Exact fields drift');$snap[$id]=$fields;
 }
 if($after&&(!is_array($backup)||$backup['baseline']!==$baseline||$backup['proposals']!==$m))stop_release('Backup mismatch');
 if(!$after&&$backup!==null)stop_release('Backup already exists');
 if(in_array($mode,['--preview','--verify','--rollback-preview'],true)){echo json_encode(['mode'=>$mode,'ok'=>true,'utc'=>gmdate('c'),'products'=>3,'changed_fields'=>7,'protected_preserved'=>true,'backup_present'=>is_array($backup)])."\n";exit;}
 if($mode==='--apply'&&!add_option($key,['utc'=>gmdate('c'),'baseline'=>$baseline,'proposals'=>$m],'',false))stop_release('Backup creation');
 global $wpdb;$wpdb->query('START TRANSACTION');
 try{
  foreach($m['products'] as $i=>$r){$id=$r['id'];$b=$baseline[$i];$wpdb->get_var($wpdb->prepare("SELECT ID FROM {$wpdb->posts} WHERE ID=%d FOR UPDATE",$id));invalidate_three($id);
   if(current_three($id)!==$snap[$id]||invariant_three($id)!==$r['invariants'])stop_release('Concurrent drift');
   $content=$rollback?$b['post_content']:$r['content_after'];$expected=$rollback?$r['content_after']:$b['post_content'];$values=$rollback?$r['before']:$r['after'];
   $ok=$wpdb->query($wpdb->prepare("UPDATE {$wpdb->posts} SET post_content=%s,post_modified=%s,post_modified_gmt=%s WHERE ID=%d AND post_content=%s",$content,current_time('mysql'),current_time('mysql',true),$id,$expected));if($ok!==1)stop_release('Guarded content update');
   if($id!==10102){update_post_meta($id,'_yoast_wpseo_title',wp_slash($values['seo_title']));update_post_meta($id,'_yoast_wpseo_metadesc',wp_slash($values['meta_description']));}
   rebuild_three($id);if(current_three($id)!==$values||invariant_three($id)!==$r['invariants'])stop_release('Post update verification');
  }
  $wpdb->query('COMMIT');
 }catch(Throwable $e){$wpdb->query('ROLLBACK');foreach($m['products'] as $r)invalidate_three($r['id']);throw $e;}
 foreach($m['products'] as $r){invalidate_three($r['id']);if(function_exists('rocket_clean_files'))rocket_clean_files([$r['url']]);do_action('litespeed_purge_url',$r['url']);}
 echo json_encode(['mode'=>$mode,'ok'=>true,'utc'=>gmdate('c'),'products'=>3,'changed_fields'=>7,'protected_preserved'=>true,'backup_option'=>$key,'transaction'=>'committed'])."\n";
}catch(Throwable $e){echo json_encode(['ok'=>false,'reason'=>$e instanceof RuntimeException?$e->getMessage():'Internal error'])."\n";exit(1);}
