<?php
require __DIR__.'/common.php';
function guard($condition,$message){if(!$condition)throw new RuntimeException($message);}
function check_all($manifest,$after){
 foreach($manifest['posts'] as $item){$id=$item['id'];clean_post_cache($id);$p=get_post($id);
  guard($p&&$p->post_name===$item['slug']&&$p->post_type==='product'&&$p->post_status==='publish'&&get_permalink($id)===$item['url'],'Identity mismatch');
  guard(invariant($id)===$item['invariant'],'Protected content/metadata/taxonomy drift');
  guard(meta_values($id)===($after?$item['after']:$item['before']),'SEO metadata drift');
  foreach(array_keys($item['before']) as $key)guard(count(get_post_meta($id,$key,false))===1,'Duplicate/missing SEO metadata');
 }
 foreach($manifest['prior'] as $id=>$hash){clean_post_cache((int)$id);guard(invariant((int)$id,false)===$hash,'Previous release drift');}
}
function indexables_match($manifest,$after){
 global $wpdb;$table=$wpdb->prefix.'yoast_indexable';
 foreach($manifest['posts'] as $item){$fields=$after?$item['after']:$item['before'];$row=$wpdb->get_row($wpdb->prepare("SELECT title,description FROM $table WHERE object_type='post' AND object_id=%d",$item['id']),ARRAY_A);
  guard($row&&$row['title']===$fields['_yoast_wpseo_title']&&$row['description']===$fields['_yoast_wpseo_metadesc'],'Yoast indexable mismatch');}
}
try{
 $mode=$argv[1]??'--preview';guard(in_array($mode,['--preview','--apply','--verify','--rollback-preview','--rollback'],true),'Wrong mode');
 $manifest=json_decode(file_get_contents(__DIR__.'/manifest.json'),true,512,JSON_THROW_ON_ERROR);guard(array_column($manifest['posts'],'id')===[16110,18062],'Wrong scope');
 $key='_shustrik_moon_sydney_metadata_backup_20261017';guard($manifest['backup_key']===$key,'Wrong backup key');$backup=get_option($key,null);
 global $wpdb;$table=$wpdb->prefix.'yoast_indexable';$engines=$wpdb->get_results("SHOW TABLE STATUS WHERE Name IN ('{$wpdb->postmeta}','{$wpdb->options}','$table')",ARRAY_A);guard(count($engines)===3,'Missing transactional tables');foreach($engines as $e)guard($e['Engine']==='InnoDB','Non-transactional table');
 $is_before=in_array($mode,['--preview','--apply'],true);check_all($manifest,!$is_before);indexables_match($manifest,!$is_before);
 if($is_before)guard($backup===null,'Existing release; inspect first');
 else guard($backup&&$backup['status']==='published'&&$backup['manifest_sha256']===hash_file('sha256',__DIR__.'/manifest.json'),'Backup mismatch');
 if(in_array($mode,['--apply','--rollback'],true)){
  $rollback=$mode==='--rollback';
  if(!$rollback){$backup=['status'=>'prepared','utc'=>gmdate('c'),'manifest_sha256'=>hash_file('sha256',__DIR__.'/manifest.json'),'posts'=>$manifest['posts']];guard(add_option($key,$backup,'',false),'Backup collision');}
  $wpdb->query('START TRANSACTION');
  try{
   $wpdb->get_results("SELECT meta_id FROM {$wpdb->postmeta} WHERE post_id IN (16110,18062) ORDER BY meta_id FOR UPDATE");
   check_all($manifest,$rollback);
   foreach($manifest['posts'] as $item){$fields=$rollback?$item['before']:$item['after'];foreach($fields as $field=>$value)guard(update_post_meta($item['id'],$field,$value)!==false,'Metadata update failed');
    clean_post_cache($item['id']);YoastSEO()->classes->get('Yoast\\WP\\SEO\\Builders\\Indexable_Builder')->build_for_id($item['id'],'post');
   }
   check_all($manifest,!$rollback);indexables_match($manifest,!$rollback);$wpdb->query('COMMIT');
  }catch(Throwable $e){$wpdb->query('ROLLBACK');foreach($manifest['posts'] as $item)clean_post_cache($item['id']);throw $e;}
  $backup['status']=$rollback?'rolled-back':'published';$backup['updated_at']=gmdate('c');update_option($key,$backup,false);
  foreach($manifest['posts'] as $item){clean_post_cache($item['id']);if(function_exists('rocket_clean_files'))rocket_clean_files([$item['url']]);do_action('litespeed_purge_url',$item['url']);}
 }
 $rows=[];foreach($manifest['posts'] as $item)$rows[]=['id'=>$item['id'],'url'=>$item['url'],'fields'=>meta_values($item['id']),'protected_preserved'=>invariant($item['id'])===$item['invariant']];
 echo json_encode(['ok'=>true,'mode'=>$mode,'utc'=>gmdate('c'),'posts'=>$rows,'prior_preserved'=>true,'yoast_indexables_match'=>true,'backup_key'=>$key,'backup_status'=>$backup['status']??null],JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";
}catch(Throwable $e){echo json_encode(['ok'=>false,'reason'=>$e instanceof RuntimeException?$e->getMessage():'Internal failure'])."\n";exit(1);}
