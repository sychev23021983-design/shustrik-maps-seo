<?php
require __DIR__.'/common.php';
function check_state($m,$after){
 foreach($m['attachments'] as $a){$id=$a['id'];clean_post_cache($id);$p=get_post($id);must($p&&$p->post_type==='attachment'&&wp_get_attachment_url($id)===$a['url'],'Attachment identity drift '.$id);must(invariant($id,true)===$a['invariant'],'Protected attachment drift '.$id);must(values($id)===$a[$after?'after':'before'],'Media values drift '.$id);$rows=altrows($id);must(count($rows)===($after?1:count($a['alt_rows'])),'Alt row count drift '.$id);if(!$after)must($rows===$a['alt_rows'],'Original alt rows drift '.$id);}
 foreach($m['preserved'] as $id=>$hash){clean_post_cache((int)$id);must(invariant((int)$id)===$hash,'Protected post drift '.$id);}
 must(indexable_hash(array_merge(array_column($m['attachments'],'id'),array_keys($m['preserved'])))===$m['indexables_hash'],'Indexables drift');
}
try{
 $mode=$argv[1]??'--preview';must(in_array($mode,['--preview','--apply','--verify','--rollback-preview','--rollback'],true),'Wrong mode');
 $m=json_decode(file_get_contents(__DIR__.'/manifest.json'),true,512,JSON_THROW_ON_ERROR);$b=json_decode(file_get_contents(__DIR__.'/baseline.json'),true,512,JSON_THROW_ON_ERROR);$s=json_decode(file_get_contents(__DIR__.'/scope.json'),true,512,JSON_THROW_ON_ERROR);
 must($m['site_profile']==='shustrik-maps'&&$m['backup_key']==='_shustrik_satellite_image_metadata_backup_20261018'&&count($m['attachments'])===427&&count($m['preserved'])===138,'Wrong scope');
 must(array_column($m['attachments'],'id')===$s['attachment_ids']&&array_column($b['attachments'],'id')===$s['attachment_ids'],'Allowlist mismatch');
 foreach($m['attachments'] as $i=>$a){must(array_diff_key($a,array_flip(['after','products']))===$b['attachments'][$i],'Baseline mismatch');must(array_keys($a['after'])===['title','alt']&&$a['after']['title']!==''&&$a['after']['alt']!==''&&strlen($a['after']['alt'])<300&&strlen($a['after']['title'])<180,'Invalid copy');}
 global $wpdb;$eng=$wpdb->get_results("SHOW TABLE STATUS WHERE Name IN ('{$wpdb->posts}','{$wpdb->postmeta}','{$wpdb->options}')",ARRAY_A);must(count($eng)===3,'Missing tables');foreach($eng as $x)must($x['Engine']==='InnoDB','Nontransactional table');
 $initial=in_array($mode,['--preview','--apply'],true);check_state($m,!$initial);$key=$m['backup_key'];$saved=get_option($key,null);
 if($initial)must($saved===null,'Backup exists; inspect outcome');else must($saved&&$saved['status']==='published'&&$saved['manifest_sha256']===hash_file('sha256',__DIR__.'/manifest.json'),'Backup mismatch');
 if(in_array($mode,['--apply','--rollback'],true)){
  $rollback=$mode==='--rollback';if(!$rollback){$saved=['status'=>'prepared','utc'=>gmdate('c'),'manifest_sha256'=>hash_file('sha256',__DIR__.'/manifest.json'),'baseline'=>$b];must(add_option($key,$saved,'',false),'Backup collision');}
  must($wpdb->query('START TRANSACTION')!==false,'Transaction start failed');try{
   $ids=implode(',',array_map('intval',$s['attachment_ids']));$wpdb->get_results("SELECT ID FROM {$wpdb->posts} WHERE ID IN ($ids) ORDER BY ID FOR UPDATE");$wpdb->get_results("SELECT meta_id FROM {$wpdb->postmeta} WHERE post_id IN ($ids) ORDER BY meta_id FOR UPDATE");check_state($m,$rollback);
   foreach($m['attachments'] as $a){$id=$a['id'];$old=$a[$rollback?'after':'before'];$new=$a[$rollback?'before':'after'];
    must($wpdb->query($wpdb->prepare("UPDATE {$wpdb->posts} SET post_title=%s,post_modified=%s,post_modified_gmt=%s WHERE ID=%d AND post_type='attachment' AND BINARY post_title=BINARY %s",$new['title'],current_time('mysql'),current_time('mysql',true),$id,$old['title']))===1,'Conditional title write failed '.$id);
    $rows=altrows($id);if($rollback&&count($a['alt_rows'])===0){must(count($rows)===1,'Inserted alt missing');must($wpdb->query($wpdb->prepare("DELETE FROM {$wpdb->postmeta} WHERE meta_id=%d AND post_id=%d AND meta_key='_wp_attachment_image_alt' AND BINARY meta_value=BINARY %s",$rows[0]['meta_id'],$id,$old['alt']))===1,'Alt rollback failed');}
    elseif(count($rows)===1){must($wpdb->query($wpdb->prepare("UPDATE {$wpdb->postmeta} SET meta_value=%s WHERE meta_id=%d AND post_id=%d AND meta_key='_wp_attachment_image_alt' AND BINARY meta_value=BINARY %s",$new['alt'],$rows[0]['meta_id'],$id,$old['alt']))===1,'Conditional alt write failed '.$id);}
    else{must(!$rollback&&count($rows)===0,'Alt rows drift');must($wpdb->insert($wpdb->postmeta,['post_id'=>$id,'meta_key'=>'_wp_attachment_image_alt','meta_value'=>$new['alt']],['%d','%s','%s'])===1,'Alt insert failed '.$id);}
    clean_post_cache($id);
   }
   check_state($m,!$rollback);must($wpdb->query('COMMIT')!==false,'Commit failed');
  }catch(Throwable $e){$wpdb->query('ROLLBACK');foreach($s['attachment_ids'] as $id)clean_post_cache($id);throw $e;}
  $saved['status']=$rollback?'rolled-back':'published';$saved['updated_at']=gmdate('c');must(update_option($key,$saved,false)!==false,'Backup status update failed');foreach($s['attachment_ids'] as $id)clean_post_cache($id);
  foreach($s['product_urls'] as $url){if(function_exists('rocket_clean_files'))rocket_clean_files([$url]);do_action('litespeed_purge_url',$url);}
 }
 echo json_encode(['ok'=>true,'mode'=>$mode,'utc'=>gmdate('c'),'attachments'=>427,'title_fields_changed'=>427,'alt_fields_changed'=>427,'preserved_posts'=>138,'product_content_metadata_preserved'=>true,'attachment_files_metadata_preserved'=>true,'indexables_preserved'=>true,'backup_key'=>$key,'backup_status'=>$saved['status']??null],JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";
}catch(Throwable $e){echo json_encode(['ok'=>false,'reason'=>$e instanceof RuntimeException?$e->getMessage():'Internal failure'])."\n";exit(1);}
