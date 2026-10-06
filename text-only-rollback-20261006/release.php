<?php
ini_set('display_errors','0');define('WP_USE_THEMES',false);ob_start();require '/var/www/html/wp-load.php';ob_end_clean();
function fail_text($s){throw new RuntimeException($s);}
function state_text($id){$p=get_post($id);$h=[];foreach(['_price','_regular_price','_sale_price','_sku','_stock','_stock_status','_downloadable','_virtual','_downloadable_files','_thumbnail_id','_product_image_gallery','_yoast_wpseo_canonical','_yoast_wpseo_meta-robots-noindex','_yoast_wpseo_meta-robots-nofollow'] as $k)$h[$k]=hash('sha256',serialize(get_post_meta($id,$k,true)));$media=[];foreach(explode(',',get_post_meta($id,'_product_image_gallery',true)) as $aid){if(!$aid)continue;$a=get_post($aid);$media[$aid]=hash('sha256',serialize([$a->post_title,$a->post_content,$a->post_excerpt,get_post_meta($aid,'_wp_attachment_image_alt',true),wp_get_attachment_url($aid)]));}return ['id'=>$id,'title'=>$p->post_title,'excerpt'=>$p->post_excerpt,'url'=>get_permalink($id),'protected'=>$h,'media'=>$media,'gallery'=>get_post_meta($id,'_product_image_gallery',true),'content'=>$p->post_content,'seo_title'=>get_post_meta($id,'_yoast_wpseo_title',true),'meta_description'=>get_post_meta($id,'_yoast_wpseo_metadesc',true)];}
function stable_text($a,$b){foreach(['title','excerpt','url','protected','media','gallery'] as $k)if($a[$k]!==$b[$k])fail_text('Protected drift '.$a['id'].' '.$k);}
function refresh_text($id){clean_post_cache($id);wp_cache_delete($id,'post_meta');if(function_exists('YoastSEO')&&class_exists('Yoast\\WP\\SEO\\Builders\\Indexable_Builder'))YoastSEO()->classes->get('Yoast\\WP\\SEO\\Builders\\Indexable_Builder')->build_for_id_and_type($id,'post');}
try{
 if(PHP_SAPI!=='cli'||rtrim(home_url(),'/')!=='https://shustrik-maps.com')fail_text('Site');
 $mode=$argv[1]??'--preview';if(!in_array($mode,['--preview','--apply','--verify']))fail_text('Mode');
 $targets=json_decode(file_get_contents(__DIR__.'/targets.json'),true,512,JSON_THROW_ON_ERROR)['rows'];if(array_column($targets,'id')!==[9520,9522,9446,10668])fail_text('Scope');
 $key='_shustrik_text_only_rollback_20261006';$saved=get_option($key,null);$out=[];$prepared=[];
 $az=get_option('_shustrik_arizona_visual_backup_20261005');$three=get_option('_shustrik_visual_three_backup_20261005');if(!$az||!$three)fail_text('Original backups missing');
 foreach($targets as $t){$id=$t['id'];$now=state_text($id);
  if($mode==='--verify'){$row=null;foreach($saved['rows']??[] as $r)if($r['before']['id']===$id)$row=$r;if(!$row)fail_text('Rollback backup missing');stable_text($row['before'],$now);if($now['content']!==$row['after_content']||$now['seo_title']!==$t['seo_title']||$now['meta_description']!==$t['meta_description'])fail_text('Restored text drift '.$id);}
  else{if($saved!==null)fail_text('Already applied; verify instead');$expected=$id===9520?['content_after'=>$az['content_after'],'gallery_after'=>$az['gallery_after']]:null;if(!$expected)foreach($three['rows'] as $r)if($r['product_id']===$id)$expected=$r;if(!$expected||$now['content']!==$expected['content_after']||$now['gallery']!==$expected['gallery_after'])fail_text('Published drift '.$id);
   $start=strpos($now['content'],'<section id="'.$t['slug'].'-ai-application-concepts">');if($start===false)fail_text('AI section missing');$end=strpos($now['content'],'</section>',$start);if($end===false)fail_text('AI section end');$section=substr($now['content'],$start,$end+10-$start);if(substr_count($section,'<figure')!==3)fail_text('Three AI figures required');
   $after=$t['content'].'[vc_row][vc_column][vc_column_text]'.$section.'[/vc_column_text][/vc_column][/vc_row]';$prepared[]=['before'=>$now,'after_content'=>$after];
  }
  $out[]=['id'=>$id,'url'=>$now['url'],'h1'=>$now['title'],'seo_title'=>$t['seo_title'],'meta_description'=>$t['meta_description'],'gallery'=>$now['gallery'],'media_preserved'=>true,'original_description_sha256'=>hash('sha256',$t['content'])];
 }
 if($mode==='--apply'){
  if(!add_option($key,['utc'=>gmdate('c'),'rows'=>$prepared],'',false))fail_text('Backup exists');global $wpdb;$wpdb->query('START TRANSACTION');try{
   foreach($prepared as $i=>$r){$id=$r['before']['id'];$t=$targets[$i];$wpdb->get_var($wpdb->prepare("SELECT ID FROM {$wpdb->posts} WHERE ID=%d FOR UPDATE",$id));clean_post_cache($id);$now=state_text($id);if($now!==$r['before'])fail_text('Concurrent edit '.$id);$n=$wpdb->query($wpdb->prepare("UPDATE {$wpdb->posts} SET post_content=%s,post_modified=%s,post_modified_gmt=%s WHERE ID=%d AND post_content=%s",$r['after_content'],current_time('mysql'),current_time('mysql',true),$id,$r['before']['content']));if($n!==1)fail_text('Write '.$id);update_post_meta($id,'_yoast_wpseo_title',wp_slash($t['seo_title']));update_post_meta($id,'_yoast_wpseo_metadesc',wp_slash($t['meta_description']));refresh_text($id);$now=state_text($id);stable_text($r['before'],$now);if($now['content']!==$r['after_content']||$now['seo_title']!==$t['seo_title']||$now['meta_description']!==$t['meta_description'])fail_text('Write verification '.$id);
   }$wpdb->query('COMMIT');
  }catch(Throwable $e){$wpdb->query('ROLLBACK');foreach($prepared as $r)clean_post_cache($r['before']['id']);throw $e;}
  foreach($out as $r){if(function_exists('rocket_clean_files'))rocket_clean_files([$r['url']]);do_action('litespeed_purge_url',$r['url']);}
 }
 echo json_encode(['ok'=>true,'mode'=>$mode,'utc'=>gmdate('c'),'rows'=>$out,'backup_option'=>$key],JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";
}catch(Throwable $e){echo json_encode(['ok'=>false,'reason'=>$e instanceof RuntimeException?$e->getMessage():'Internal error'])."\n";exit(1);}
