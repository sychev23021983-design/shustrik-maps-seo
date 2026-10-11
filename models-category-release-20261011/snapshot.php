<?php
ini_set('display_errors','0'); define('WP_USE_THEMES',false); ob_start(); require '/var/www/html/wp-load.php'; ob_end_clean();
if(PHP_SAPI!=='cli'||rtrim(home_url(),'/')!=='https://shustrik-maps.com')exit(1);
global $wpdb;
$block=get_post(14416); $term=get_term(26,'product_cat');
if(!$block||$block->post_type!=='cms_block'||!$term||is_wp_error($term)||$term->slug!=='3d-models')exit(2);
$products=[];
foreach(get_posts(['post_type'=>'product','post_status'=>'publish','numberposts'=>-1,'tax_query'=>[['taxonomy'=>'product_cat','field'=>'term_id','terms'=>[26],'include_children'=>true]]]) as $p){
 $slug=$p->post_name; if(!$p)exit(3); $images=[];
 foreach(array_unique(array_merge([get_post_thumbnail_id($p->ID)],explode(',',get_post_meta($p->ID,'_product_image_gallery',true)))) as $aid){if(!$aid)continue;$images[]=['id'=>(int)$aid,'url'=>wp_get_attachment_url($aid)];}
 $products[]=['id'=>$p->ID,'slug'=>$slug,'url'=>get_permalink($p->ID),'state_hash'=>hash('sha256',serialize([$p,array_diff_key(get_post_meta($p->ID),array_flip(['wd_page_css_files']))])),'images'=>$images];
}
$previous_blocks=[];foreach([14416, 14417, 21177, 21176, 21175, 21178, 21162, 22817, 22822, 22827] as $id)$previous_blocks[$id]=hash('sha256',serialize([get_post($id),get_post_meta($id)]));
$term_meta=get_term_meta(26); foreach(['wd_page_css_files','xts-term-26-status','product_count_product_cat'] as $key)unset($term_meta[$key]);
$usage=['terms'=>$wpdb->get_results($wpdb->prepare("SELECT term_id,meta_key FROM {$wpdb->termmeta} WHERE meta_value=%s",'14416'),ARRAY_A),'post_refs'=>$wpdb->get_results($wpdb->prepare("SELECT ID,post_type,post_name FROM {$wpdb->posts} WHERE post_status NOT IN ('trash','auto-draft') AND post_type!='revision' AND post_content LIKE %s",'%14416%'),ARRAY_A),'post_meta_refs'=>$wpdb->get_results($wpdb->prepare("SELECT post_id,meta_key FROM {$wpdb->postmeta} WHERE meta_value=%s",'14416'),ARRAY_A)];
$protected_term=clone $term;$protected_term->description='';
echo json_encode(['utc'=>gmdate('c'),'block'=>['id'=>14416,'title'=>$block->post_title,'content'=>$block->post_content,'content_sha256'=>hash('sha256',$block->post_content),'protected_hash'=>hash('sha256',serialize([$block->post_title,$block->post_name,$block->post_status,$block->post_excerpt,get_post_meta(14416)]))],'term'=>['id'=>26,'slug'=>$term->slug,'name'=>$term->name,'description'=>$term->description,'meta'=>$term_meta,'protected_hash'=>hash('sha256',serialize([$protected_term,$term_meta]))],'usage'=>$usage,'products'=>$products,'previous_blocks'=>$previous_blocks],JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE|JSON_PRETTY_PRINT);
