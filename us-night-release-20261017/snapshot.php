<?php
require __DIR__.'/common.php';$p=get_post(17364);if(!$p||$p->post_type!=='product'||$p->post_name!=='united-states-night-satellite-map'||$p->post_status!=='publish')throw new RuntimeException('Wrong article');
$prior=[];foreach([14594,14581,14596,15849,15631,20707,11517,16110,18062] as $id)$prior[$id]=invariant($id,false);
echo json_encode(['utc'=>gmdate('c'),'id'=>17364,'url'=>get_permalink(17364),'slug'=>$p->post_name,'content'=>$p->post_content,'excerpt'=>$p->post_excerpt,'invariant'=>invariant(17364),'before'=>values(17364),'counts'=>counts(17364),'indexables'=>indexable(),'prior'=>$prior],JSON_UNESCAPED_UNICODE|JSON_PRETTY_PRINT);
