<?php
require __DIR__.'/common.php';
$s=json_decode(file_get_contents(__DIR__.'/scope.json'),true,512,JSON_THROW_ON_ERROR);$rows=[];$preserved=[];
foreach($s['attachment_ids'] as $id){clean_post_cache($id);$p=get_post($id);must($p&&$p->post_type==='attachment','Wrong attachment');$rows[]=['id'=>$id,'url'=>wp_get_attachment_url($id),'before'=>values($id),'alt_rows'=>altrows($id),'invariant'=>invariant($id,true)];}
foreach($s['preserve_ids'] as $id){clean_post_cache($id);$preserved[$id]=invariant($id);}
echo json_encode(['utc'=>gmdate('c'),'attachments'=>$rows,'preserved'=>$preserved,'indexables_hash'=>indexable_hash(array_merge($s['attachment_ids'],$s['preserve_ids']))],JSON_UNESCAPED_UNICODE|JSON_PRETTY_PRINT);
