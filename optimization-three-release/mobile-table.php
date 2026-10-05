<?php
ini_set('display_errors','0');define('WP_USE_THEMES',false);
ob_start();require '/var/www/html/wp-load.php';ob_end_clean();
try {
 if(PHP_SAPI!=='cli'||rtrim(home_url(),'/')!=='https://shustrik-maps.com')throw new RuntimeException('Site');
 $mode=$argv[1]??'--preview';if(!in_array($mode,['--preview','--apply','--verify','--rollback-preview','--rollback'],true))throw new RuntimeException('Mode');
 $m=json_decode(file_get_contents(__DIR__.'/proposals.json'),true,512,JSON_THROW_ON_ERROR);$r=$m['products'][2];$id=10102;
 if($r['id']!==$id||$m['status']!=='approved')throw new RuntimeException('Scope');
 $old=$r['content_after'];if(substr_count($old,'<table>')!==1)throw new RuntimeException('Table count');
 $new=str_replace(['<table>','</table>'],['<div role="region" aria-label="Included C4D and OBJ files" tabindex="0" style="overflow-x:auto;max-width:100%;"><table>','</table></div>'],$old);
 $key='_shustrik_optimization_table_backup_20261005';$after=in_array($mode,['--verify','--rollback-preview','--rollback'],true);$backup=get_option($key,null);
 global $wpdb;$wpdb->query('START TRANSACTION');
 try {
  $p=$wpdb->get_row($wpdb->prepare("SELECT * FROM {$wpdb->posts} WHERE ID=%d FOR UPDATE",$id));
  if($p->post_content!==($after?$new:$old)||$p->post_title!==$r['invariants']['h1']||$p->post_status!=='publish'||get_post_meta($id,'_yoast_wpseo_title',true)!==$r['after']['seo_title']||get_post_meta($id,'_yoast_wpseo_metadesc',true)!==$r['after']['meta_description'])throw new RuntimeException('Current state drift');
  if($after&&$backup!==$old)throw new RuntimeException('Backup mismatch');if(!$after&&$backup!==null)throw new RuntimeException('Backup exists');
  if($mode==='--apply'){if(!add_option($key,$old,'',false))throw new RuntimeException('Backup');}
  if(in_array($mode,['--apply','--rollback'],true)){
   $content=$mode==='--apply'?$new:$old;
   if($wpdb->update($wpdb->posts,['post_content'=>$content,'post_modified'=>current_time('mysql'),'post_modified_gmt'=>current_time('mysql',true)],['ID'=>$id])!==1)throw new RuntimeException('Update');
  }
  $wpdb->query('COMMIT');
 }catch(Throwable $e){$wpdb->query('ROLLBACK');throw $e;}
 if(in_array($mode,['--apply','--rollback'],true)){clean_post_cache($id);if(function_exists('rocket_clean_files'))rocket_clean_files([$r['url']]);do_action('litespeed_purge_url',$r['url']);}
 echo json_encode(['mode'=>$mode,'ok'=>true,'utc'=>gmdate('c'),'id'=>$id,'text_unchanged'=>true,'backup_option'=>$key])."\n";
}catch(Throwable $e){echo json_encode(['ok'=>false,'reason'=>$e instanceof RuntimeException?$e->getMessage():'Internal error'])."\n";exit(1);}
