<?php
require __DIR__.'/common.php';
function values(){return ['_yoast_wpseo_title'=>get_post_meta(10102,'_yoast_wpseo_title',true),'_yoast_wpseo_metadesc'=>get_post_meta(10102,'_yoast_wpseo_metadesc',true)];}
function check_state($m,$after){
 clean_post_cache(10102);$p=get_post(10102);
 guard($p&&$p->post_name===$m['slug']&&$p->post_type==='product'&&$p->post_status==='publish'&&get_permalink(10102)===$m['url'],'Identity drift');
 guard(invariant(10102)===$m['invariant'],'Protected fields drift');
 guard(hash('sha256',$p->post_content)===($after?$m['after_sha256']:$m['before_sha256']),'Content drift');
 guard(hash('sha256',$p->post_excerpt)===$m['excerpt_sha256'],'Excerpt drift');
 guard(values()===$m['metadata'],'Metadata drift');foreach(array_keys($m['metadata']) as $key)guard(count(get_post_meta(10102,$key,false))===1,'Metadata multiplicity drift');
 $rows=indexable();$expected=$m['indexables'];usort($rows,fn($a,$b)=>(int)$a['id']<=>(int)$b['id']);usort($expected,fn($a,$b)=>(int)$a['id']<=>(int)$b['id']);guard($rows===$expected,'Indexable drift');
 foreach($m['prior'] as $id=>$hash){clean_post_cache((int)$id);guard(invariant((int)$id,false)===$hash,'Prior product drift');}
}
try{
 $mode=$argv[1]??'--preview';guard(in_array($mode,['--preview','--apply','--verify','--rollback-preview','--rollback'],true),'Wrong mode');
 $m=json_decode(file_get_contents(__DIR__.'/manifest.json'),true,512,JSON_THROW_ON_ERROR);$b=json_decode(file_get_contents(__DIR__.'/baseline.json'),true,512,JSON_THROW_ON_ERROR);
 guard($m['id']===10102&&$m['backup_key']==='_shustrik_usa_comparison_backup_20261108','Wrong scope');
 $before=$b['content'];$after=file_get_contents(__DIR__.'/10102-after.txt');$e=$m['edit'];
 guard(substr($before,$e['at_bytes'],strlen($e['old']))===$e['old'],'Edit mismatch');
 guard(substr_replace($before,$e['text'],$e['at_bytes'],strlen($e['old']))===$after,'Candidate edit drift');
 guard(hash('sha256',$before)===$m['before_sha256']&&hash('sha256',$after)===$m['after_sha256'],'Candidate hash drift');
 preg_match_all('/\[[^\]]+\]/',$before,$l);preg_match_all('/\[[^\]]+\]/',$after,$r);guard($l[0]===$r[0],'Shortcode drift');
 $without_new=$after;foreach($m['added_links'] as $link){$anchor='<a href="'.$link['url'].'">'.$link['text'].'</a>';guard(substr_count($without_new,$anchor)===1,'Added link mismatch');$without_new=str_replace($anchor,$link['text'],$without_new);}
 preg_match_all('/<a\b[^>]*>.*?<\/a>/s',$before,$l);preg_match_all('/<a\b[^>]*>.*?<\/a>/s',$without_new,$r);guard($l[0]===$r[0],'Existing link markup drift');
 global $wpdb;$table=$wpdb->prefix.'yoast_indexable';$eng=$wpdb->get_results("SHOW TABLE STATUS WHERE Name IN ('{$wpdb->posts}','{$wpdb->postmeta}','{$wpdb->options}','$table')",ARRAY_A);
 guard(count($eng)===4,'Missing tables');foreach($eng as $x)guard($x['Engine']==='InnoDB','Nontransactional table');
 $initial=in_array($mode,['--preview','--apply'],true);check_state($m,!$initial);$key=$m['backup_key'];$saved=get_option($key,null);
 if($initial)guard($saved===null,'Backup exists; inspect first');else guard($saved&&$saved['status']==='published'&&$saved['manifest_sha256']===hash_file('sha256',__DIR__.'/manifest.json'),'Backup mismatch');
 if(in_array($mode,['--apply','--rollback'],true)){
  $rollback=$mode==='--rollback';if(!$rollback){$saved=['status'=>'prepared','utc'=>gmdate('c'),'manifest_sha256'=>hash_file('sha256',__DIR__.'/manifest.json'),'baseline'=>$b];guard(add_option($key,$saved,'',false),'Backup collision');}
  guard($wpdb->query('START TRANSACTION')!==false,'Cannot start transaction');try{
   $wpdb->get_results("SELECT ID FROM {$wpdb->posts} WHERE ID=10102 FOR UPDATE");$wpdb->get_results("SELECT meta_id FROM {$wpdb->postmeta} WHERE post_id=10102 ORDER BY meta_id FOR UPDATE");$wpdb->get_results("SELECT id FROM $table WHERE object_type='post' AND object_id=10102 ORDER BY id FOR UPDATE");check_state($m,$rollback);
   $expected=$rollback?$after:$before;$replacement=$rollback?$before:$after;
   guard($wpdb->query($wpdb->prepare("UPDATE {$wpdb->posts} SET post_content=%s,post_modified=%s,post_modified_gmt=%s WHERE ID=10102 AND BINARY post_content=BINARY %s",$replacement,current_time('mysql'),current_time('mysql',true),$expected))===1,'Conditional content write failed');
   clean_post_cache(10102);check_state($m,!$rollback);guard($wpdb->query('COMMIT')!==false,'Commit failed');
  }catch(Throwable $error){$wpdb->query('ROLLBACK');clean_post_cache(10102);throw $error;}
  $saved['status']=$rollback?'rolled-back':'published';$saved['updated_at']=gmdate('c');guard(update_option($key,$saved,false)!==false,'Backup status update failed');
  clean_post_cache(10102);if(function_exists('rocket_clean_files'))rocket_clean_files([$m['url']]);do_action('litespeed_purge_url',$m['url']);
 }
 echo json_encode(['ok'=>true,'mode'=>$mode,'utc'=>gmdate('c'),'id'=>10102,'content_sha256'=>hash('sha256',get_post(10102)->post_content),'fields'=>values(),'protected_preserved'=>true,'prior_preserved'=>true,'indexables_preserved'=>true,'backup_key'=>$key,'backup_status'=>$saved['status']??null],JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE)."\n";
}catch(Throwable $error){echo json_encode(['ok'=>false,'reason'=>$error instanceof RuntimeException?$error->getMessage():'Internal failure'])."\n";exit(1);}
