<?php
ini_set('display_errors','0');define('WP_USE_THEMES',false);ob_start();require '/var/www/html/wp-load.php';ob_end_clean();
function sc_state($id){$p=get_post($id);return ['id'=>$id,'content'=>$p->post_content,'h1'=>$p->post_title,'excerpt'=>$p->post_excerpt,'meta_hash'=>hash('sha256',serialize(get_post_meta($id))),'url'=>get_permalink($id)];}
function sc_assert($a,$b){foreach(['h1','excerpt','meta_hash','url'] as $k)if($a[$k]!==$b[$k])throw new RuntimeException('Protected drift '.$k);}
try{
 if(PHP_SAPI!=='cli'||rtrim(home_url(),'/')!=='https://shustrik-maps.com')throw new RuntimeException('Site');
 $mode=$argv[1]??'--preview';if(!in_array($mode,['--preview','--apply','--verify']))throw new RuntimeException('Mode');
 $key='_shustrik_stl_center_caption_20261006';$saved=get_option($key,null);$rows=[];
 foreach([9522,9520] as $id){$now=sc_state($id);
  if($mode==='--verify'){if(!$saved)throw new RuntimeException('Backup missing');$r=$saved[$id];sc_assert($r['before'],$now);if($now['content']!==$r['after'])throw new RuntimeException('Body drift');$rows[$id]=$r;continue;}
  if($saved!==null)throw new RuntimeException('Already applied');
  $count=0;$after=preg_replace_callback('/(\[vc_column_text[^\]]*\])(.*?)(\[\/vc_column_text\])/s',function($m)use(&$count){if($m[2]!=='<p><strong>AI-generated application concepts.</strong></p>')return $m[0];$count++;return $m[1].'<p style="text-align: center;"><strong>AI-generated application concepts.</strong></p>'.$m[3];},$now['content']);
  if($count!==1||$after===$now['content'])throw new RuntimeException('Unexpected notice');
  $rows[$id]=['before'=>$now,'after'=>$after];
 }
 if($mode==='--apply'){
  if(!add_option($key,$rows,'',false))throw new RuntimeException('Backup exists');global $wpdb;$wpdb->query('START TRANSACTION');
  try{foreach($rows as $id=>$r){$wpdb->get_var($wpdb->prepare("SELECT ID FROM {$wpdb->posts} WHERE ID=%d FOR UPDATE",$id));clean_post_cache($id);if(sc_state($id)!==$r['before'])throw new RuntimeException('Concurrent edit');$n=$wpdb->query($wpdb->prepare("UPDATE {$wpdb->posts} SET post_content=%s,post_modified=%s,post_modified_gmt=%s WHERE ID=%d AND post_content=%s",$r['after'],current_time('mysql'),current_time('mysql',true),$id,$r['before']['content']));if($n!==1)throw new RuntimeException('Write');clean_post_cache($id);$now=sc_state($id);sc_assert($r['before'],$now);if($now['content']!==$r['after'])throw new RuntimeException('Body');}$wpdb->query('COMMIT');}catch(Throwable $e){$wpdb->query('ROLLBACK');throw $e;}
  foreach($rows as $r){if(function_exists('rocket_clean_files'))rocket_clean_files([$r['before']['url']]);do_action('litespeed_purge_url',$r['before']['url']);}
 }
 echo json_encode(['ok'=>true,'mode'=>$mode,'ids'=>array_keys($rows),'backup'=>$key,'protected_fields_preserved'=>true])."\n";
}catch(Throwable $e){echo json_encode(['ok'=>false,'reason'=>$e->getMessage()])."\n";exit(1);}
