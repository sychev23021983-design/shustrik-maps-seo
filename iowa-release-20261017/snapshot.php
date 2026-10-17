<?php
require __DIR__.'/common.php';$p=get_post(17495);if(!$p||$p->post_type!=='product'||$p->post_name!=='iowa-satellite-map'||$p->post_status!=='publish')throw new RuntimeException('Wrong article');
$prior=[];foreach([17364,14594,14581,14596,15849,15631,20707,11517,16110,18062] as $id)$prior[$id]=invariant($id,false);
echo json_encode(['utc'=>gmdate('c'),'id'=>17495,'url'=>get_permalink(17495),'slug'=>$p->post_name,'content'=>$p->post_content,'excerpt'=>$p->post_excerpt,'invariant'=>invariant(17495),'before'=>values(17495),'counts'=>counts(17495),'indexables'=>indexable(),'prior'=>$prior],JSON_UNESCAPED_UNICODE|JSON_PRETTY_PRINT);
