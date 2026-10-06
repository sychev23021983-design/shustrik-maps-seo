<?php
ini_set('display_errors','0');define('WP_USE_THEMES',false);ob_start();require '/var/www/html/wp-load.php';ob_end_clean();
try{
 if(PHP_SAPI!=='cli'||rtrim(home_url(),'/')!=='https://shustrik-maps.com')throw new RuntimeException('Wrong site');
 $m=json_decode(file_get_contents(__DIR__.'/manifest.json'),true,512,JSON_THROW_ON_ERROR);$file=__DIR__.'/'.$m['file'];if(hash_file('sha256',$file)!==$m['sha256'])throw new RuntimeException('File hash');
 $mode=$argv[1]??'--preview';if(!in_array($mode,['--preview','--apply','--verify']))throw new RuntimeException('Mode');
 $key='_shustrik_california_wall_media_20261006';$state=get_option($key,null);$products=[];foreach([9520,9522,9446,10668] as $id)$products[$id]=hash('sha256',serialize([get_post($id),get_post_meta($id)]));
 if($mode==='--preview'){echo json_encode(['ok'=>true,'file'=>$m['file'],'already_imported'=>$state!==null])."\n";exit;}
 if($mode==='--apply'&&$state===null){
  if(!add_option($key,['status'=>'importing'],'',false))throw new RuntimeException('Journal exists');
  require_once ABSPATH.'wp-admin/includes/file.php';require_once ABSPATH.'wp-admin/includes/media.php';require_once ABSPATH.'wp-admin/includes/image.php';
  $tmp=wp_tempnam($m['file']);if(!copy($file,$tmp))throw new RuntimeException('Copy');$aid=media_handle_sideload(['name'=>$m['file'],'tmp_name'=>$tmp],0,$m['caption']);if(is_wp_error($aid))throw new RuntimeException('Media import');update_option($key,['status'=>'metadata','id'=>$aid],false);
  $r=wp_update_post(wp_slash(['ID'=>$aid,'post_title'=>$m['title'],'post_excerpt'=>$m['caption'],'post_content'=>$m['caption']]),true);if(is_wp_error($r))throw new RuntimeException('Metadata write');update_post_meta($aid,'_wp_attachment_image_alt',wp_slash($m['alt']));update_option($key,['status'=>'complete','id'=>$aid,'utc'=>gmdate('c')],false);$state=get_option($key);
 }
 if(!$state||($state['status']??'')!=='complete')throw new RuntimeException('Incomplete import; inspect journal');$aid=$state['id'];$p=get_post($aid);$meta=wp_get_attachment_metadata($aid);if(!$p||$p->post_parent!==0||$p->post_title!==$m['title']||get_post_meta($aid,'_wp_attachment_image_alt',true)!==$m['alt']||$p->post_excerpt!==$m['caption']||$meta['width']!==1500||$meta['height']!==1000||get_post_mime_type($aid)!=='image/jpeg'||hash_file('sha256',get_attached_file($aid))!==$m['sha256'])throw new RuntimeException('Media verification');
 foreach($products as $id=>$h){clean_post_cache($id);if(hash('sha256',serialize([get_post($id),get_post_meta($id)]))!==$h)throw new RuntimeException('Unexpected product change');}
 echo json_encode(['ok'=>true,'id'=>$aid,'url'=>wp_get_attachment_url($aid),'edit_url'=>admin_url('post.php?post='.$aid.'&action=edit'),'title'=>$p->post_title,'alt'=>get_post_meta($aid,'_wp_attachment_image_alt',true),'width'=>$meta['width'],'height'=>$meta['height'],'mime'=>'image/jpeg','product_cards_unchanged'=>true,'utc'=>gmdate('c')],JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";
}catch(Throwable $e){echo json_encode(['ok'=>false,'reason'=>$e instanceof RuntimeException?$e->getMessage():'Internal error'])."\n";exit(1);}
