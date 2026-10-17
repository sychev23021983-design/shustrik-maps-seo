<?php
ini_set('display_errors','0');define('WP_USE_THEMES',false);ob_start();require '/var/www/html/wp-load.php';ob_end_clean();
if(PHP_SAPI!=='cli'||rtrim(home_url(),'/')!=='https://shustrik-maps.com')exit(1);
$slugs=['what-is-an-stl-file-explaining-the-stl-format','understanding-the-obj-file-format-a-simple-explanation','how-to-convert-a-model-from-c4d-to-obj'];$rows=[];
foreach($slugs as $slug){$p=get_page_by_path($slug,OBJECT,'post');if(!$p||$p->post_status!=='publish')exit(2);$protected=(array)$p;unset($protected['post_content'],$protected['post_modified'],$protected['post_modified_gmt']);$meta=get_post_meta($p->ID);unset($meta['wd_page_css_files']);$terms=wp_get_object_terms($p->ID,get_object_taxonomies('post'),['fields'=>'all']);
$rows[]=['id'=>$p->ID,'slug'=>$slug,'url'=>get_permalink($p->ID),'title'=>$p->post_title,'content'=>$p->post_content,'before_sha256'=>hash('sha256',$p->post_content),'protected_hash'=>hash('sha256',serialize([$protected,$meta,$terms])),'meta_keys'=>array_keys($meta)];}
global $wpdb;$engines=$wpdb->get_results("SHOW TABLE STATUS WHERE Name IN ('{$wpdb->posts}','{$wpdb->options}')",ARRAY_A);$tables=[];foreach($engines as $e)$tables[$e['Name']]=$e['Engine'];echo json_encode(['utc'=>gmdate('c'),'posts'=>$rows,'tables'=>$tables],JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE|JSON_PRETTY_PRINT);
