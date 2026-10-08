<?php
ini_set('display_errors','0');define('WP_USE_THEMES',false);ob_start();require '/var/www/html/wp-load.php';ob_end_clean();
function kh_fail($s){throw new RuntimeException($s);}
function kh_meta_hash($id){$m=get_post_meta($id);ksort($m);return hash('sha256',serialize($m));}
function kh_state(){
 $id=21381;$p=get_post($id);if(!$p||$p->post_type!=='product'||$p->post_name!=='new-zealand-medallion-kiwi-stl')kh_fail('Product identity');
 $other=[];foreach([10140,10324,16379,18721] as $oid){$q=get_post($oid);$other[$oid]=hash('sha256',serialize([$q->post_content,$q->post_title,$q->post_excerpt,$q->post_name,$q->post_status,kh_meta_hash($oid)]));}
 return ['id'=>$id,'content'=>$p->post_content,'h1'=>$p->post_title,'excerpt'=>$p->post_excerpt,'slug'=>$p->post_name,'status'=>$p->post_status,'url'=>get_permalink($id),'gallery'=>get_post_meta($id,'_product_image_gallery',true),'seo_title'=>get_post_meta($id,'_yoast_wpseo_title',true),'meta_description'=>get_post_meta($id,'_yoast_wpseo_metadesc',true),'all_product_meta_hash'=>kh_meta_hash($id),'other_four_hashes'=>$other,'shared_block_hash'=>hash('sha256',get_post(9586)->post_content)];
}
function kh_media($aid){
 $p=get_post($aid);$file=get_attached_file($aid);if(!$p||!is_file($file))kh_fail('Missing old media');
 $d=wp_get_attachment_metadata($aid);
 return ['id'=>(int)$aid,'url'=>wp_get_attachment_url($aid),'title'=>$p->post_title,'alt'=>get_post_meta($aid,'_wp_attachment_image_alt',true),'caption'=>$p->post_excerpt,'content'=>$p->post_content,'mime'=>get_post_mime_type($aid),'width'=>$d['width'],'height'=>$d['height'],'sha256'=>hash_file('sha256',$file),'metadata_hash'=>kh_meta_hash($aid)];
}
function kh_gallery($content){preg_match_all('/\[woodmart_gallery\b[^\]]*\]/',$content,$g);if(count($g[0])!==1)kh_fail('Gallery count');preg_match('/images="([^"]+)"/',$g[0][0],$m);if(!$m)kh_fail('Gallery image IDs');return array_map('intval',explode(',',$m[1]));}
function kh_stable($before,$after){unset($before['content'],$after['content']);if($before!==$after)kh_fail('Protected product or other card drift');}
function kh_refresh(){clean_post_cache(21381);wp_cache_delete(21381,'post_meta');$u=get_permalink(21381);if(function_exists('rocket_clean_files'))rocket_clean_files([$u]);do_action('litespeed_purge_url',$u);}
function kh_write($now,$content){
 global $wpdb;$wpdb->query('START TRANSACTION');
 try{$wpdb->get_var("SELECT ID FROM {$wpdb->posts} WHERE ID=21381 FOR UPDATE");clean_post_cache(21381);if(kh_state()!==$now)kh_fail('Concurrent edit');
 $n=$wpdb->query($wpdb->prepare("UPDATE {$wpdb->posts} SET post_content=%s,post_modified=%s,post_modified_gmt=%s WHERE ID=21381 AND post_content=%s",$content,current_time('mysql'),current_time('mysql',true),$now['content']));if($n!==1)kh_fail('Content write');
 clean_post_cache(21381);$s=kh_state();kh_stable($now,$s);if($s['content']!==$content)kh_fail('Content mismatch');$wpdb->query('COMMIT');
 }catch(Throwable $e){$wpdb->query('ROLLBACK');clean_post_cache(21381);throw $e;}kh_refresh();
}
try{
 if(PHP_SAPI!=='cli'||rtrim(home_url(),'/')!=='https://shustrik-maps.com')kh_fail('Site');
 $mode=$argv[1]??'--preview';$key='_shustrik_kiwi_hand_fix_backup_20261008_21381';$journal='_shustrik_kiwi_hand_fix_media_20261008_21381';$now=kh_state();
 if($mode==='--snapshot'){$ids=kh_gallery($now['content']);echo json_encode(['ok'=>true,'utc'=>gmdate('c'),'state'=>$now,'gallery_ids'=>$ids,'old_media'=>array_map('kh_media',$ids)],JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE)."\n";exit;}
 if(!in_array($mode,['--preview','--apply','--verify','--rollback-preview','--rollback','--backup-export']))kh_fail('Mode');
 if($mode==='--backup-export'){echo json_encode(['ok'=>true,'backup'=>get_option($key),'journal'=>get_option($journal)],JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE)."\n";exit;}
 $m=json_decode(file_get_contents(__DIR__.'/manifest.json'),true,512,JSON_THROW_ON_ERROR);$a=$m['asset'];$b=$m['baseline'];
 if($m['product_id']!==21381||$m['replace_media_id']!==22766||$b['gallery_ids']!==[22766,22767,22768,22769])kh_fail('Scope');
 if(hash_file('sha256',__DIR__.'/'.$a['file'])!==$a['sha256'])kh_fail('Asset SHA');$size=getimagesize(__DIR__.'/'.$a['file']);if($size[0]!==1500||$size[1]!==1000||$size['mime']!=='image/jpeg')kh_fail('JPEG validation');
 foreach($b['old_media'] as $old)if(kh_media($old['id'])!==$old)kh_fail('Old media drift');
 $backup=get_option($key,null);
 if(in_array($mode,['--verify','--rollback-preview','--rollback'])){
  if(!$backup||get_option($journal)['status']!=='published')kh_fail('Missing published backup');kh_stable($backup['before'],$now);if($now['content']!==$backup['after'])kh_fail('Published content drift');
 }else{if($backup!==null||get_option($journal,null)!==null)kh_fail('Already applied or journal present');if($now!==$b['state'])kh_fail('Baseline drift');}
 if($mode==='--apply'){
  if(!add_option($journal,['status'=>'importing','ids'=>[]],'',false))kh_fail('Journal exists');
  require_once ABSPATH.'wp-admin/includes/file.php';require_once ABSPATH.'wp-admin/includes/media.php';require_once ABSPATH.'wp-admin/includes/image.php';
  $tmp=wp_tempnam($a['file']);if(!copy(__DIR__.'/'.$a['file'],$tmp))kh_fail('Copy');
  $aid=media_handle_sideload(['name'=>$a['file'],'tmp_name'=>$tmp],21381,$a['caption']);if(is_wp_error($aid))kh_fail('Import');update_option($journal,['status'=>'importing','ids'=>[$aid]],false);
  $r=wp_update_post(wp_slash(['ID'=>$aid,'post_title'=>$a['title'],'post_excerpt'=>$a['caption'],'post_content'=>$a['caption']]),true);if(is_wp_error($r))kh_fail('Media metadata');
  update_post_meta($aid,'_wp_attachment_image_alt',wp_slash($a['alt']));$am=kh_media($aid);if($am['sha256']!==$a['sha256']||$am['width']!==1500||$am['height']!==1000||$am['mime']!=='image/jpeg')kh_fail('Uploaded asset');
  $needle='images="22766,22767,22768,22769"';if(substr_count($now['content'],$needle)!==1)kh_fail('Replacement occurrence');
  $after=str_replace($needle,'images="'.$aid.',22767,22768,22769"',$now['content']);
  $backup=['utc'=>gmdate('c'),'before'=>$now,'after'=>$after,'media_id'=>$aid,'old_media'=>$b['old_media']];
  if(!add_option($key,$backup,'',false))kh_fail('Backup exists');kh_write($now,$after);update_option($journal,['status'=>'published','ids'=>[$aid]],false);$now=kh_state();
 }
 if($mode==='--rollback'){$before=$backup['before'];kh_write($now,$before['content']);$now=kh_state();if($now!==$before)kh_fail('Rollback mismatch');}
 $media=[];if($mode==='--verify'){
  foreach(kh_gallery($now['content']) as $aid){$am=kh_media($aid);if($am['mime']!=='image/jpeg'||$am['width']!==1500||$am['height']!==1000)kh_fail('Gallery media');$media[]=$am;}
  $am=$media[0];if($am['id']!==$backup['media_id']||$am['title']!==$a['title']||$am['alt']!==$a['alt']||$am['caption']!==$a['caption']||$am['sha256']!==$a['sha256'])kh_fail('New media metadata');
 }
 echo json_encode(['ok'=>true,'mode'=>$mode,'utc'=>gmdate('c'),'rows'=>[['id'=>21381,'url'=>$now['url'],'h1'=>$now['h1'],'seo_title'=>$now['seo_title'],'meta_description'=>$now['meta_description'],'media'=>$media,'protected_preserved'=>true]]],JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE)."\n";
}catch(Throwable $e){echo json_encode(['ok'=>false,'reason'=>$e instanceof RuntimeException?$e->getMessage():'Internal error'])."\n";exit(1);}
