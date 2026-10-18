<?php
require __DIR__.'/common.php';
function guard($condition,$message){if(!$condition)throw new RuntimeException($message);}
function expected_rows($p,$after){$rows=$p['indexables_before'];if($after)foreach($rows as &$r){$r['title']=$p['after']['_yoast_wpseo_title'];$r['description']=$p['after']['_yoast_wpseo_metadesc'];}return $rows;}
function check_state($m,$after){
 foreach($m['products'] as $p){$id=$p['id'];clean_post_cache($id);$post=get_post($id);
  guard($post&&$post->post_type==='product'&&$post->post_status==='publish'&&$post->post_name===$p['slug']&&get_permalink($id)===$p['url']&&has_term(204,'product_cat',$id),'Identity drift '.$id);
  guard(invariant($id)===$p['invariant'],'Protected fields drift '.$id);
  guard(hash('sha256',$post->post_content)===$p[$after?'after_sha256':'before_sha256'],'Content drift '.$id);
  guard(hash('sha256',$post->post_excerpt)===$p[$after?'excerpt_after_sha256':'excerpt_before_sha256'],'Excerpt drift '.$id);
  guard(values($id)===$p[$after?'after':'before'],'Metadata drift '.$id);
  $expected_counts=$p['counts'];if($after)foreach($p['after'] as $key=>$value)if($value!==$p['before'][$key])$expected_counts[$key]=1;
  guard(counts($id)===$expected_counts,'Metadata count drift '.$id);
  guard(indexable($id)===expected_rows($p,$after),'Indexable drift '.$id);
 }
 foreach($m['prior'] as $id=>$hash){clean_post_cache((int)$id);guard(invariant((int)$id,false)===$hash,'Protected prior drift '.$id);}
}
try{
 $mode=$argv[1]??'--preview';guard(in_array($mode,['--preview','--apply','--verify','--rollback-preview','--rollback'],true),'Wrong mode');
 $m=json_decode(file_get_contents(__DIR__.'/manifest.json'),true,512,JSON_THROW_ON_ERROR);$b=json_decode(file_get_contents(__DIR__.'/baseline.json'),true,512,JSON_THROW_ON_ERROR);$scope=json_decode(file_get_contents(__DIR__.'/scope.json'),true,512,JSON_THROW_ON_ERROR);
 guard($m['site_profile']==='shustrik-maps'&&$m['backup_key']==='_shustrik_satellite_descriptions_backup_20261018'&&count($m['products'])===87,'Wrong release');
 guard(array_column($m['products'],'id')===$scope['target_ids']&&array_column($b['products'],'id')===$scope['target_ids'],'Allowlist mismatch');
 $candidates=[];
 foreach($m['products'] as $i=>$p){$id=$p['id'];$old=$b['products'][$i]['content'];$oldex=$b['products'][$i]['excerpt'];$new=file_get_contents(__DIR__.'/'.$id.'-after.txt');$newex=file_get_contents(__DIR__.'/'.$id.'-excerpt-after.txt');$candidate=$old;$edits=$p['edits'];usort($edits,fn($a,$b)=>$b['at_bytes']<=>$a['at_bytes']);
  foreach($edits as $e){guard(substr($candidate,$e['at_bytes'],strlen($e['old']))===$e['old'],'Content edit mismatch '.$id);$candidate=substr_replace($candidate,$e['text'],$e['at_bytes'],strlen($e['old']));}
  guard($candidate===$new,'Content candidate mismatch '.$id);$ee=$p['excerpt_edit'];guard($p['before']===$p['after'],'Metadata mutation forbidden '.$id);guard($oldex===$newex&&$ee['old']===''&&$ee['text']==='','Excerpt mutation forbidden '.$id);guard(substr($oldex,$ee['at_bytes'],strlen($ee['old']))===$ee['old'],'Excerpt prefix mismatch '.$id);guard(substr_replace($oldex,$ee['text'],$ee['at_bytes'],strlen($ee['old']))===$newex,'Excerpt candidate mismatch '.$id);
  guard(hash('sha256',$old)===$p['before_sha256']&&hash('sha256',$new)===$p['after_sha256']&&hash('sha256',$oldex)===$p['excerpt_before_sha256']&&hash('sha256',$newex)===$p['excerpt_after_sha256'],'Candidate hash mismatch '.$id);
  foreach([[$old,$new],[$oldex,$newex]] as [$left,$right]){preg_match_all('/\[[^\]]+\]/',$left,$l);preg_match_all('/\[[^\]]+\]/',$right,$r);guard($l[0]===$r[0],'Shortcode drift '.$id);preg_match_all('/<a\b[^>]*>.*?<\/a>/s',$left,$l);preg_match_all('/<a\b[^>]*>.*?<\/a>/s',$right,$r);guard($l[0]===$r[0],'Link markup drift '.$id);}
  $candidates[$id]=[$old,$new,$oldex,$newex];
 }
 global $wpdb;$table=$wpdb->prefix.'yoast_indexable';$eng=$wpdb->get_results("SHOW TABLE STATUS WHERE Name IN ('{$wpdb->posts}','{$wpdb->postmeta}','{$wpdb->options}','$table')",ARRAY_A);guard(count($eng)===4,'Missing tables');foreach($eng as $x)guard($x['Engine']==='InnoDB','Nontransactional table');
 $initial=in_array($mode,['--preview','--apply'],true);check_state($m,!$initial);$key=$m['backup_key'];$saved=get_option($key,null);if($initial)guard($saved===null,'Backup exists; inspect outcome');else guard($saved&&$saved['status']==='published'&&$saved['manifest_sha256']===hash_file('sha256',__DIR__.'/manifest.json'),'Backup mismatch');
 if(in_array($mode,['--apply','--rollback'],true)){
  $rollback=$mode==='--rollback';if(!$rollback){$saved=['status'=>'prepared','utc'=>gmdate('c'),'manifest_sha256'=>hash_file('sha256',__DIR__.'/manifest.json'),'baseline'=>$b];guard(add_option($key,$saved,'',false),'Backup collision');}
  guard($wpdb->query('START TRANSACTION')!==false,'Transaction start failed');try{
   $ids=implode(',',array_map('intval',$scope['target_ids']));$wpdb->get_results("SELECT ID FROM {$wpdb->posts} WHERE ID IN ($ids) ORDER BY ID FOR UPDATE");$wpdb->get_results("SELECT meta_id FROM {$wpdb->postmeta} WHERE post_id IN ($ids) ORDER BY meta_id FOR UPDATE");$wpdb->get_results("SELECT id FROM $table WHERE object_type='post' AND object_id IN ($ids) ORDER BY id FOR UPDATE");check_state($m,$rollback);
   foreach($m['products'] as $p){$id=$p['id'];[$old,$new,$oldex,$newex]=$candidates[$id];$expected=$rollback?$new:$old;$replacement=$rollback?$old:$new;$expected_ex=$rollback?$newex:$oldex;$replacement_ex=$rollback?$oldex:$newex;
    guard($wpdb->query($wpdb->prepare("UPDATE {$wpdb->posts} SET post_content=%s,post_modified=%s,post_modified_gmt=%s WHERE ID=%d AND BINARY post_content=BINARY %s AND BINARY post_excerpt=BINARY %s",$replacement,current_time('mysql'),current_time('mysql',true),$id,$expected,$expected_ex))===1,'Conditional content write failed '.$id);clean_post_cache($id);
    clean_post_cache($id);
   }
   check_state($m,!$rollback);guard($wpdb->query('COMMIT')!==false,'Commit failed');
  }catch(Throwable $error){$wpdb->query('ROLLBACK');foreach($scope['target_ids'] as $id)clean_post_cache($id);throw $error;}
  $saved['status']=$rollback?'rolled-back':'published';$saved['updated_at']=gmdate('c');guard(update_option($key,$saved,false)!==false,'Backup status update failed');
  foreach($m['products'] as $p){clean_post_cache($p['id']);if(function_exists('rocket_clean_files'))rocket_clean_files([$p['url']]);do_action('litespeed_purge_url',$p['url']);}
 }
 echo json_encode(['ok'=>true,'mode'=>$mode,'utc'=>gmdate('c'),'products'=>count($m['products']),'seo_pairs_changed'=>count(array_filter($m['products'],fn($p)=>$p['before']!==$p['after'])),'preserved_records'=>count($m['prior']),'protected_fields_preserved'=>true,'indexables_match'=>true,'backup_key'=>$key,'backup_status'=>$saved['status']??null],JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";
}catch(Throwable $error){echo json_encode(['ok'=>false,'reason'=>$error instanceof RuntimeException?$error->getMessage():'Internal failure'])."\n";exit(1);}
