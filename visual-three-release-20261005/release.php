<?php
ini_set('display_errors','0');define('WP_USE_THEMES',false);ob_start();require '/var/www/html/wp-load.php';ob_end_clean();
function stop_visual_three($s){throw new RuntimeException($s);}
function protect_visual_three($b){
 $id=$b['id'];foreach($b['protected'] as $k=>$h){if($k==='_product_image_gallery')continue;if(hash('sha256',serialize(get_post_meta($id,$k,true)))!==$h)stop_visual_three('Protected field drift '.$id.' '.$k);}
 $p=get_post($id);if(!$p||$p->post_title!==$b['title']||$p->post_excerpt!==$b['excerpt']||get_permalink($id)!==$b['url'])stop_visual_three('Identity/excerpt drift '.$id);
}
function refresh_visual_three($id){clean_post_cache($id);wp_cache_delete($id,'post_meta');if(function_exists('YoastSEO')&&class_exists('Yoast\\WP\\SEO\\Builders\\Indexable_Builder'))YoastSEO()->classes->get('Yoast\\WP\\SEO\\Builders\\Indexable_Builder')->build_for_id_and_type($id,'post');}
try{
 if(PHP_SAPI!=='cli'||rtrim(home_url(),'/')!=='https://shustrik-maps.com')stop_visual_three('Wrong site');
 $mode=$argv[1]??'--preview';if(!in_array($mode,['--preview','--apply','--verify','--rollback-preview','--rollback']))stop_visual_three('Invalid mode');
 $base=json_decode(file_get_contents(__DIR__.'/baseline.json'),true,512,JSON_THROW_ON_ERROR)['rows'];$manifest=json_decode(file_get_contents(__DIR__.'/manifest.json'),true,512,JSON_THROW_ON_ERROR)['products'];
 $ids=array_column($base,'id');if($ids!==[9522,9446,10668]||array_column($manifest,'product_id')!==$ids)stop_visual_three('Scope drift');
 $key='_shustrik_visual_three_backup_20261005';$journal='_shustrik_visual_three_media_20261005';$backup=get_option($key,null);$after=in_array($mode,['--verify','--rollback-preview','--rollback']);
 foreach($base as $i=>$b){$m=$manifest[$i];protect_visual_three($b);if(count($m['media'])!==3)stop_visual_three('Media count');foreach($m['media'] as $a)if(hash_file('sha256',__DIR__.'/'.$a['file'])!==$a['sha256'])stop_visual_three('Asset hash');
  if($after){if(!$backup||count($backup['rows'])!==3)stop_visual_three('Missing backup');$expected=$backup['rows'][$i];if(get_post($b['id'])->post_content!==$expected['content_after']||get_post_meta($b['id'],'_product_image_gallery',true)!==$expected['gallery_after']||get_post_meta($b['id'],'_yoast_wpseo_title',true)!==$m['seo_title']||get_post_meta($b['id'],'_yoast_wpseo_metadesc',true)!==$m['meta_description'])stop_visual_three('Published state drift '.$b['id']);}
  else{if($backup!==null||get_option($journal,null)!==null||get_post($b['id'])->post_content!==$b['content']||hash('sha256',$b['content'])!==$m['before_content_sha256']||get_post_meta($b['id'],'_product_image_gallery',true)!==$b['gallery']||get_post_meta($b['id'],'_yoast_wpseo_title',true)!==$b['seo_title']||get_post_meta($b['id'],'_yoast_wpseo_metadesc',true)!==$b['meta_description'])stop_visual_three('Baseline drift '.$b['id']);}
 }
 if(in_array($mode,['--preview','--rollback-preview'])){echo json_encode(['ok'=>true,'mode'=>$mode,'products'=>$ids,'media'=>9,'protected_preserved'=>true])."\n";exit;}
 if($mode==='--verify'){
  $out=[];foreach($base as $i=>$b){$media=[];foreach($backup['rows'][$i]['media_ids'] as $j=>$aid){$a=$manifest[$i]['media'][$j];$p=get_post($aid);if(!$p||$p->post_parent!==$b['id']||$p->post_title!==$a['title']||$p->post_excerpt!==$a['caption']||get_post_meta($aid,'_wp_attachment_image_alt',true)!==$a['alt'])stop_visual_three('Media metadata drift');$media[]=['id'=>$aid,'url'=>wp_get_attachment_url($aid),'title'=>$a['title'],'alt'=>$a['alt']];}$out[]=['product_id'=>$b['id'],'url'=>$b['url'],'media'=>$media];}
  echo json_encode(['ok'=>true,'mode'=>$mode,'utc'=>gmdate('c'),'rows'=>$out,'protected_preserved'=>true,'backup_option'=>$key],JSON_UNESCAPED_SLASHES)."\n";exit;
 }
 if($mode==='--rollback'){
  foreach($base as $b){$id=$b['id'];$res=wp_update_post(wp_slash(['ID'=>$id,'post_content'=>$b['content']]),true);if(is_wp_error($res))stop_visual_three('Rollback write');update_post_meta($id,'_product_image_gallery',$b['gallery']);update_post_meta($id,'_yoast_wpseo_title',wp_slash($b['seo_title']));update_post_meta($id,'_yoast_wpseo_metadesc',wp_slash($b['meta_description']));refresh_visual_three($id);if(function_exists('rocket_clean_files'))rocket_clean_files([$b['url']]);do_action('litespeed_purge_url',$b['url']);}
  echo json_encode(['ok'=>true,'mode'=>$mode,'media_retained'=>true])."\n";exit;
 }
 require_once ABSPATH.'wp-admin/includes/file.php';require_once ABSPATH.'wp-admin/includes/media.php';require_once ABSPATH.'wp-admin/includes/image.php';
 if(!add_option($journal,['utc'=>gmdate('c'),'status'=>'importing','media_ids'=>[]],'',false))stop_visual_three('Import journal exists');
 $journal_data=get_option($journal);$prepared=[];
 foreach($base as $i=>$b){$m=$manifest[$i];$newids=[];$figures='';foreach($m['media'] as $a){
  $tmp=wp_tempnam($a['file']);if(!copy(__DIR__.'/'.$a['file'],$tmp))stop_visual_three('Asset copy');$aid=media_handle_sideload(['name'=>$a['file'],'tmp_name'=>$tmp],$b['id'],$a['caption']);if(is_wp_error($aid))stop_visual_three('Media import');
  $newids[]=$aid;$journal_data['media_ids'][]=$aid;update_option($journal,$journal_data,false);
  $res=wp_update_post(wp_slash(['ID'=>$aid,'post_title'=>$a['title'],'post_excerpt'=>$a['caption'],'post_content'=>$a['caption']]),true);if(is_wp_error($res))stop_visual_three('Media metadata');update_post_meta($aid,'_wp_attachment_image_alt',wp_slash($a['alt']));
  $figures.='<figure style="margin:24px 0"><h3>'.esc_html($a['heading']).'</h3>'.wp_get_attachment_image($aid,'large',false,['alt'=>$a['alt'],'title'=>$a['title'],'loading'=>'lazy','style'=>'display:block;width:100%;height:auto;border-radius:4px']).'<figcaption style="font-size:14px;line-height:1.5;margin-top:8px">'.esc_html($a['caption']).'</figcaption></figure>';
 }
 $content=str_replace('{{AI_FIGURES}}',$figures,$m['content_template']);if(strpos($content,'{{AI_FIGURES}}')!==false)stop_visual_three('Figure substitution');$gallery=trim($b['gallery'].','.implode(',',$newids),',');$prepared[]=['product_id'=>$b['id'],'content_after'=>$content,'gallery_after'=>$gallery,'media_ids'=>$newids];
 }
 if(!add_option($key,['utc'=>gmdate('c'),'baseline'=>$base,'rows'=>$prepared],'',false))stop_visual_three('Backup option');
 global $wpdb;$wpdb->query('START TRANSACTION');try{
  foreach($base as $i=>$b){$id=$b['id'];$m=$manifest[$i];$new=$prepared[$i];$wpdb->get_var($wpdb->prepare("SELECT ID FROM {$wpdb->posts} WHERE ID=%d FOR UPDATE",$id));clean_post_cache($id);protect_visual_three($b);
   if(get_post($id)->post_content!==$b['content']||get_post_meta($id,'_product_image_gallery',true)!==$b['gallery']||get_post_meta($id,'_yoast_wpseo_title',true)!==$b['seo_title']||get_post_meta($id,'_yoast_wpseo_metadesc',true)!==$b['meta_description'])stop_visual_three('Concurrent drift '.$id);
   $ok=$wpdb->query($wpdb->prepare("UPDATE {$wpdb->posts} SET post_content=%s,post_modified=%s,post_modified_gmt=%s WHERE ID=%d AND post_content=%s",$new['content_after'],current_time('mysql'),current_time('mysql',true),$id,$b['content']));if($ok!==1)stop_visual_three('Guarded write '.$id);
   update_post_meta($id,'_product_image_gallery',$new['gallery_after']);update_post_meta($id,'_yoast_wpseo_title',wp_slash($m['seo_title']));update_post_meta($id,'_yoast_wpseo_metadesc',wp_slash($m['meta_description']));refresh_visual_three($id);protect_visual_three($b);
   if(get_post($id)->post_content!==$new['content_after'])stop_visual_three('Written content verification');
  }$wpdb->query('COMMIT');
 }catch(Throwable $e){$wpdb->query('ROLLBACK');foreach($base as $b)clean_post_cache($b['id']);throw $e;}
 $journal_data['status']='published';update_option($journal,$journal_data,false);foreach($base as $b){if(function_exists('rocket_clean_files'))rocket_clean_files([$b['url']]);do_action('litespeed_purge_url',$b['url']);}
 echo json_encode(['ok'=>true,'mode'=>$mode,'utc'=>gmdate('c'),'rows'=>$prepared,'backup_option'=>$key],JSON_UNESCAPED_SLASHES)."\n";
}catch(Throwable $e){echo json_encode(['ok'=>false,'reason'=>$e instanceof RuntimeException?$e->getMessage():'Internal error'])."\n";exit(1);}
