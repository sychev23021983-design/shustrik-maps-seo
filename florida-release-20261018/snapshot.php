<?php
require __DIR__.'/common.php';$p=get_post(17465);if(!$p||$p->post_type!=='product'||$p->post_name!=='florida-satellite-map'||$p->post_status!=='publish')throw new RuntimeException('Wrong article');
$prior=[];foreach([17615,17495,17364,14594,14581,14596,15849,15631,20707,11517,16110,18062] as $id)$prior[$id]=invariant($id,false);
echo json_encode(['utc'=>gmdate('c'),'id'=>17465,'url'=>get_permalink(17465),'slug'=>$p->post_name,'content'=>$p->post_content,'excerpt'=>$p->post_excerpt,'invariant'=>invariant(17465),'before'=>values(17465),'counts'=>counts(17465),'indexables'=>indexable(),'prior'=>$prior],JSON_UNESCAPED_UNICODE|JSON_PRETTY_PRINT);
