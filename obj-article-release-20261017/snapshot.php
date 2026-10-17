<?php
require __DIR__.'/common.php';$p=get_post(14581);if(!$p||$p->post_type!=='post'||$p->post_name!=='understanding-the-obj-file-format-a-simple-explanation'||$p->post_status!=='publish')throw new RuntimeException('Wrong article');
$prior=[];foreach([14594,14596,15849,15631,20707,11517,16110,18062] as $id)$prior[$id]=invariant($id,false);
echo json_encode(['utc'=>gmdate('c'),'id'=>14581,'url'=>get_permalink(14581),'slug'=>$p->post_name,'content'=>$p->post_content,'invariant'=>invariant(14581),'before'=>values(14581),'counts'=>counts(14581),'indexables'=>indexable(),'prior'=>$prior],JSON_UNESCAPED_UNICODE|JSON_PRETTY_PRINT);
