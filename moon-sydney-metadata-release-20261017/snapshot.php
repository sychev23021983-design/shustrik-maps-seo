<?php
require __DIR__.'/common.php';$rows=[];global $wpdb;
foreach([16110=>'moon-3d-model',18062=>'sydney-opera-house-3d-model'] as $id=>$slug){
 $p=get_post($id);if(!$p||$p->post_name!==$slug||$p->post_type!=='product'||$p->post_status!=='publish')throw new RuntimeException('Wrong product');
 $rows[]=['id'=>$id,'slug'=>$slug,'url'=>get_permalink($id),'before'=>meta_values($id),'invariant'=>invariant($id)];
}
$prior=[];foreach([14594,14581,15849,14596,15631,20707,11517] as $id)$prior[$id]=invariant($id,false);
$table=$wpdb->prefix.'yoast_indexable';$exists=$wpdb->get_var($wpdb->prepare('SHOW TABLES LIKE %s',$table))===$table;
$indexables=$exists?$wpdb->get_results("SELECT object_id,title,description FROM $table WHERE object_type='post' AND object_id IN (16110,18062)",ARRAY_A):[];
$tables=$wpdb->get_results("SHOW TABLE STATUS WHERE Name IN ('{$wpdb->postmeta}','{$wpdb->options}')",ARRAY_A);$engines=[];foreach($tables as $t)$engines[$t['Name']]=$t['Engine'];
echo json_encode(['utc'=>gmdate('c'),'posts'=>$rows,'prior'=>$prior,'tables'=>$engines,'yoast_indexable_builder'=>class_exists('Yoast\\WP\\SEO\\Builders\\Indexable_Builder'),'indexables'=>$indexables],JSON_UNESCAPED_UNICODE|JSON_PRETTY_PRINT);
