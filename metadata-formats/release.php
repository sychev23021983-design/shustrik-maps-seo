<?php
error_reporting(0);ob_start();require '/var/www/html/wp-load.php';ob_end_clean();
$scope=in_array('--three',$argv,true)?'three':(in_array('--eight',$argv,true)?'eight':null);
if(!$scope)throw new Exception('Explicit approved scope --three or --eight is required');
$apply=in_array('--apply',$argv,true);$rollback=in_array('--rollback',$argv,true);
$key='_shustrik_format_metadata_backup_20261003_'.$scope;
$rows=json_decode(file_get_contents(__DIR__.'/proposals.json'),true);
if(!is_array($rows)||count($rows)!==8)throw new Exception('Unexpected proposal package');
if($scope==='three')$rows=array_slice($rows,0,3);
$prepared=[];
foreach($rows as $r){
 $id=url_to_postid($r['url']);$p=get_post($id);
 if(!$p||$p->post_type!=='product'||$p->post_status!=='publish'||get_permalink($id)!==$r['url'])throw new Exception('Public product identity guard failed');
 $r['id']=$id;$r['content_sha256']=hash('sha256',$p->post_content);$r['h1']=$p->post_title;$r['price']=get_post_meta($id,'_price',true);$prepared[]=$r;
}
$backup=get_option($key);
if($rollback){
 if(!is_array($backup)||count($backup['rows'])!==count($prepared))throw new Exception('Rollback backup guard failed');
 foreach($backup['rows'] as $r){
  if(get_permalink($r['id'])!==$r['url']||!in_array(get_post_meta($r['id'],'_yoast_wpseo_title',true),[$r['title'],$r['old_title']],true)||!in_array(get_post_meta($r['id'],'_yoast_wpseo_metadesc',true),[$r['description'],$r['old_description']],true))throw new Exception('Rollback metadata drift');
 }
 foreach($backup['rows'] as $r){
  foreach(['_yoast_wpseo_title'=>'old_title','_yoast_wpseo_metadesc'=>'old_description'] as $meta=>$field){
   if($r[$field.'_exists'])update_post_meta($r['id'],$meta,$r[$field]);else delete_post_meta($r['id'],$meta);
  }
 }
 echo json_encode(['mode'=>'rollback','count'=>count($prepared),'utc'=>gmdate('c')]);exit;
}
foreach($prepared as $r){
 if(get_post_meta($r['id'],'_yoast_wpseo_title',true)!==$r['expected_title']||get_post_meta($r['id'],'_yoast_wpseo_metadesc',true)!==$r['expected_description'])throw new Exception('Preflight metadata drift; no writes');
}
if(!$apply){echo json_encode(['mode'=>'preview','scope'=>$scope,'count'=>count($prepared),'all_current_values_match'=>true,'backup_exists'=>is_array($backup)]);exit;}
if($backup)throw new Exception('Backup exists; refusing repeat apply');
foreach($prepared as &$r){$r['old_title']=get_post_meta($r['id'],'_yoast_wpseo_title',true);$r['old_title_exists']=metadata_exists('post',$r['id'],'_yoast_wpseo_title');$r['old_description']=get_post_meta($r['id'],'_yoast_wpseo_metadesc',true);$r['old_description_exists']=metadata_exists('post',$r['id'],'_yoast_wpseo_metadesc');}unset($r);
if(!add_option($key,['utc'=>gmdate('c'),'rows'=>$prepared],'',false))throw new Exception('Backup write failed');
foreach($prepared as $r){update_post_meta($r['id'],'_yoast_wpseo_title',$r['title']);update_post_meta($r['id'],'_yoast_wpseo_metadesc',$r['description']);}
foreach($prepared as $r){$p=get_post($r['id']);if(get_post_meta($r['id'],'_yoast_wpseo_title',true)!==$r['title']||get_post_meta($r['id'],'_yoast_wpseo_metadesc',true)!==$r['description'])throw new Exception('Metadata write verification failed; use guarded rollback');if(hash('sha256',$p->post_content)!==$r['content_sha256']||$p->post_title!==$r['h1']||get_post_meta($r['id'],'_price',true)!==$r['price'])throw new Exception('Untouched-field verification failed; use guarded rollback');}
echo json_encode(['mode'=>'apply','scope'=>$scope,'count'=>count($prepared),'utc'=>gmdate('c'),'content_h1_price_unchanged'=>true]);
