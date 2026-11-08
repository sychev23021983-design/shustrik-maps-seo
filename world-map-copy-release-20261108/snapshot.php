<?php
require __DIR__.'/common.php';
$p=get_post(10238);guard($p&&$p->post_type==='product'&&$p->post_name==='world-map-3d-model'&&$p->post_status==='publish','Identity mismatch');
$prior=[];foreach([11358,11013,11517,16110,10102,15954] as $id)$prior[$id]=invariant($id,false);
$archives=[];
foreach((array)get_post_meta(10238,'_downloadable_files',true) as $f){
 $path=parse_url($f['file']??'',PHP_URL_PATH);$local=$path?realpath(ABSPATH.ltrim($path,'/')):false;
 $a=['name'=>basename($path??''),'local_verified'=>false];
 if($local&&str_starts_with($local,realpath(ABSPATH).DIRECTORY_SEPARATOR)&&is_file($local)){
  $a['local_verified']=true;$a['bytes']=filesize($local);$a['modified_utc']=gmdate('c',filemtime($local));
  if(class_exists('ZipArchive')&&strtolower(pathinfo($local,PATHINFO_EXTENSION))==='zip'){
   $z=new ZipArchive();if($z->open($local)===true){$a['entries']=[];for($i=0;$i<$z->numFiles;$i++){$a['entries'][]=$z->getNameIndex($i);} $z->close();}
  }
 }
 $archives[]=$a;
}
echo json_encode(['utc'=>gmdate('c'),'id'=>10238,'url'=>get_permalink(10238),'slug'=>$p->post_name,'content'=>$p->post_content,'excerpt'=>$p->post_excerpt,'invariant'=>invariant(10238),'title'=>product_title(),'title_count'=>count(get_post_meta(10238,'_yoast_wpseo_title',false)),'meta_description'=>get_post_meta(10238,'_yoast_wpseo_metadesc',true),'indexables'=>indexable(),'prior'=>$prior,'archives'=>$archives],JSON_UNESCAPED_UNICODE|JSON_PRETTY_PRINT|JSON_UNESCAPED_SLASHES);
