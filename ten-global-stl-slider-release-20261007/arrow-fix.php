<?php
ini_set('display_errors','0');define('WP_USE_THEMES',false);ob_start();require '/var/www/html/wp-load.php';ob_end_clean();
function ng_fail($s){throw new RuntimeException($s);}
function ng_state($id){$p=get_post($id);if(!$p||$p->post_type!=='product')ng_fail('Product');$meta=get_post_meta($id);unset($meta['_yoast_wpseo_title'],$meta['_yoast_wpseo_metadesc']);return ['id'=>$id,'content'=>$p->post_content,'h1'=>$p->post_title,'excerpt'=>$p->post_excerpt,'url'=>get_permalink($id),'gallery'=>get_post_meta($id,'_product_image_gallery',true),'seo_title'=>get_post_meta($id,'_yoast_wpseo_title',true),'meta_description'=>get_post_meta($id,'_yoast_wpseo_metadesc',true),'protected_meta_hash'=>hash('sha256',serialize($meta)),'shared_block_hash'=>hash('sha256',get_post(9586)->post_content)];}
function ng_stable($a,$b){foreach(['h1','excerpt','url','gallery','protected_meta_hash','shared_block_hash'] as $k)if($a[$k]!==$b[$k])ng_fail('Protected drift '.$a['id'].' '.$k);}
function ng_refresh($id){clean_post_cache($id);wp_cache_delete($id,'post_meta');if(function_exists('YoastSEO')&&class_exists('Yoast\\WP\\SEO\\Builders\\Indexable_Builder'))YoastSEO()->classes->get('Yoast\\WP\\SEO\\Builders\\Indexable_Builder')->build_for_id_and_type($id,'post');$url=get_permalink($id);if(function_exists('rocket_clean_files'))rocket_clean_files([$url]);do_action('litespeed_purge_url',$url);}
try {
 $mode=$argv[1]??'--arrow-preview';if(!in_array($mode,['--arrow-preview','--arrow-apply','--arrow-verify']))ng_fail('Mode');
 if(PHP_SAPI!=='cli'||rtrim(home_url(),'/')!=='https://shustrik-maps.com')ng_fail('Site');
 $id=9507;$key='_shustrik_ten_global_stl_slider_backup_20261007_9507';$fixkey='_shustrik_ten_global_slider_arrow_fix_backup_20261007_9507';
 $manifest=json_decode(file_get_contents(__DIR__.'/manifest.json'),true,512,JSON_THROW_ON_ERROR);$t=null;foreach($manifest['rows'] as $row)if($row['id']===$id)$t=$row;if(!$t)ng_fail('Scope');
 $backup=get_option($key,null);if(!$backup||count($backup['media_ids'])!==4)ng_fail('Backup');$now=ng_state($id);ng_stable($backup['before'],$now);
 $after=str_replace('{{IMAGE_IDS}}',implode(',',$backup['media_ids']),$t['description']);$before=str_replace('carousel_arrows_position="together" ','',$after);$fix=get_option($fixkey,null);
 if($now['seo_title']!==$t['seo_title']||$now['meta_description']!==$t['meta_description'])ng_fail('SEO drift');
 if($mode==='--arrow-verify'){if(!$fix||$now['content']!==$after||$backup['after']!==$after)ng_fail('Fix missing/drift');}
 else {
  if($fix!==null||$now['content']!==$before||$backup['after']!==$before)ng_fail('Existing fix or content drift');
  if($mode==='--arrow-apply') {
   global $wpdb;$wpdb->query('START TRANSACTION');try{
    $wpdb->get_var($wpdb->prepare("SELECT ID FROM {$wpdb->posts} WHERE ID=%d FOR UPDATE",$id));clean_post_cache($id);if(ng_state($id)!==$now)ng_fail('Concurrent edit');
    if(!add_option($fixkey,['utc'=>gmdate('c'),'before'=>$before,'after'=>$after,'original_batch_backup'=>$backup],'',false))ng_fail('Fix backup');
    $n=$wpdb->query($wpdb->prepare("UPDATE {$wpdb->posts} SET post_content=%s,post_modified=%s,post_modified_gmt=%s WHERE ID=%d AND post_content=%s",$after,current_time('mysql'),current_time('mysql',true),$id,$before));if($n!==1)ng_fail('Write');
    $backup['after']=$after;$backup['arrow_fix']='native carousel_arrows_position=together for El Salvador only';update_option($key,$backup,false);clean_post_cache($id);$written=ng_state($id);ng_stable($now,$written);if($written['content']!==$after)ng_fail('Written drift');$wpdb->query('COMMIT');
   }catch(Throwable $e){$wpdb->query('ROLLBACK');clean_post_cache($id);throw $e;}ng_refresh($id);
  }
 }
 echo json_encode(['ok'=>true,'mode'=>$mode,'id'=>$id,'native_arrow_position'=>'together','other_products_unchanged'=>true,'original_before_backup_preserved'=>true,'media_reimported'=>false])."\n";
}catch(Throwable $e){echo json_encode(['ok'=>false,'reason'=>$e instanceof RuntimeException?$e->getMessage():'Internal error'])."\n";exit(1);}
