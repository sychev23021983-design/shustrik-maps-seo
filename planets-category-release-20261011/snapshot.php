<?php
ini_set('display_errors','0'); define('WP_USE_THEMES',false); ob_start(); require '/var/www/html/wp-load.php'; ob_end_clean();
if(PHP_SAPI!=='cli'||rtrim(home_url(),'/')!=='https://shustrik-maps.com')exit(1);
global $wpdb;
$block=get_post(21162); $term=get_term(30,'product_cat');
if(!$block||$block->post_type!=='cms_block'||!$term||is_wp_error($term)||$term->slug!=='planets')exit(2);
$products=[];
$parent_block_hash=hash('sha256',serialize([get_post(14417),get_post_meta(14417)]));
foreach(get_posts(['post_type'=>'product','post_status'=>'publish','numberposts'=>-1,'tax_query'=>[['taxonomy'=>'product_cat','field'=>'term_id','terms'=>[30],'include_children'=>false]]]) as $catalogue_product){
 $slug=$catalogue_product->post_name;$p=$catalogue_product; if(!$p)exit(3); $images=[];
 foreach(array_unique(array_merge([get_post_thumbnail_id($p->ID)],explode(',',get_post_meta($p->ID,'_product_image_gallery',true)))) as $aid){if(!$aid)continue;$images[]=['id'=>(int)$aid,'url'=>wp_get_attachment_url($aid)];}
 preg_match_all('/images="([0-9,]+)"/',$p->post_content,$body_galleries);foreach($body_galleries[1] as $gallery){foreach(explode(',',$gallery) as $aid){$images[]=['id'=>(int)$aid,'url'=>wp_get_attachment_url($aid),'alt'=>get_post_meta($aid,'_wp_attachment_image_alt',true),'kind'=>'body-gallery'];}}
 $products[]=['id'=>$p->ID,'slug'=>$slug,'url'=>get_permalink($p->ID),'term_ids'=>wp_get_post_terms($p->ID,'product_cat',['fields'=>'ids']),'state_hash'=>hash('sha256',serialize([$p,get_post_meta($p->ID)])),'images'=>$images];
}
$term_meta=get_term_meta(30); foreach(['wd_page_css_files','xts-term-30-status','product_count_product_cat'] as $key)unset($term_meta[$key]);
$usage=['terms'=>$wpdb->get_results($wpdb->prepare("SELECT term_id,meta_key FROM {$wpdb->termmeta} WHERE meta_value=%s",'21162'),ARRAY_A),'post_refs'=>$wpdb->get_results($wpdb->prepare("SELECT ID,post_type,post_name FROM {$wpdb->posts} WHERE post_status NOT IN ('trash','auto-draft') AND post_type!='revision' AND post_content LIKE %s",'%21162%'),ARRAY_A),'post_meta_refs'=>$wpdb->get_results($wpdb->prepare("SELECT post_id,meta_key FROM {$wpdb->postmeta} WHERE meta_value=%s",'21162'),ARRAY_A)];
echo json_encode(['utc'=>gmdate('c'),'block'=>['id'=>21162,'title'=>$block->post_title,'content'=>$block->post_content,'content_sha256'=>hash('sha256',$block->post_content),'protected_hash'=>hash('sha256',serialize([$block->post_title,$block->post_name,$block->post_status,$block->post_excerpt,get_post_meta(21162)]))],'term'=>['id'=>30,'slug'=>$term->slug,'name'=>$term->name,'description'=>$term->description,'meta'=>$term_meta,'protected_hash'=>hash('sha256',serialize([$term,$term_meta]))],'islands_block_hash'=>hash('sha256',serialize([get_post(21178),get_post_meta(21178)])),'continents_block_hash'=>hash('sha256',serialize([get_post(21175),get_post_meta(21175)])),'countries_block_hash'=>hash('sha256',serialize([get_post(21176),get_post_meta(21176)])),'usa_block_hash'=>hash('sha256',serialize([get_post(21177),get_post_meta(21177)])),'parent_block_hash'=>$parent_block_hash,'usage'=>$usage,'products'=>$products],JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE|JSON_PRETTY_PRINT);
