<?php
require __DIR__.'/common.php';$p=get_post(14594);if(!$p||$p->post_type!=='post'||$p->post_name!=='what-is-an-stl-file-explaining-the-stl-format'||$p->post_status!=='publish')throw new RuntimeException('Wrong article');
$prior=[];foreach([14581,14596,15849,15631,20707,11517,16110,18062] as $id)$prior[$id]=invariant($id,false);
echo json_encode(['utc'=>gmdate('c'),'id'=>14594,'url'=>get_permalink(14594),'slug'=>$p->post_name,'content'=>$p->post_content,'invariant'=>invariant(14594),'before'=>values(14594),'counts'=>counts(14594),'indexables'=>indexable(),'prior'=>$prior],JSON_UNESCAPED_UNICODE|JSON_PRETTY_PRINT);
