<?php
require __DIR__.'/common.php';$p=get_post(14596);if(!$p||$p->post_type!=='post'||$p->post_name!=='understanding-the-fbx-file-format-a-simple-explanation'||$p->post_status!=='publish')throw new RuntimeException('Wrong article');
$prior=[];foreach([14594,14581,15849,15631,20707,11517,16110,18062] as $id)$prior[$id]=invariant($id,false);
echo json_encode(['utc'=>gmdate('c'),'id'=>14596,'url'=>get_permalink(14596),'slug'=>$p->post_name,'content'=>$p->post_content,'invariant'=>invariant(14596),'before'=>values(14596),'counts'=>counts(14596),'indexables'=>indexable(),'prior'=>$prior],JSON_UNESCAPED_UNICODE|JSON_PRETTY_PRINT);
