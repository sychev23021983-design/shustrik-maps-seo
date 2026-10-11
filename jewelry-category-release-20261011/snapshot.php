<?php
ini_set('display_errors','0'); define('WP_USE_THEMES',false); ob_start(); require '/var/www/html/wp-load.php'; ob_end_clean();
if(PHP_SAPI!=='cli'||rtrim(home_url(),'/')!=='https://shustrik-maps.com')exit(1);
global $wpdb;
$block=null; $term=get_term(246,'product_cat');
if(!$term||is_wp_error($term)||$term->slug!=='jewelry-pendant')exit(2);
$products=[];
$parent_block_hash=hash('sha256',serialize([get_post(14417),get_post_meta(14417)]));
foreach(get_posts(['post_type'=>'product','post_status'=>'publish','numberposts'=>-1,'tax_query'=>[['taxonomy'=>'product_cat','field'=>'term_id','terms'=>[246],'include_children'=>true]]]) as $catalogue_product){
 $slug=$catalogue_product->post_name;$p=$catalogue_product; if(!$p)exit(3); $images=[];
 foreach(array_unique(array_merge([get_post_thumbnail_id($p->ID)],explode(',',get_post_meta($p->ID,'_product_image_gallery',true)))) as $aid){if(!$aid)continue;$images[]=['id'=>(int)$aid,'url'=>wp_get_attachment_url($aid)];}
 preg_match_all('/images="([0-9,]+)"/',$p->post_content,$body_galleries);foreach($body_galleries[1] as $gallery){foreach(explode(',',$gallery) as $aid){$images[]=['id'=>(int)$aid,'url'=>wp_get_attachment_url($aid),'alt'=>get_post_meta($aid,'_wp_attachment_image_alt',true),'kind'=>'body-gallery'];}}
 $product_meta=get_post_meta($p->ID);unset($product_meta['wd_page_css_files']);
 $products[]=['id'=>$p->ID,'slug'=>$slug,'url'=>get_permalink($p->ID),'term_ids'=>wp_get_post_terms($p->ID,'product_cat',['fields'=>'ids']),'state_hash'=>hash('sha256',serialize([$p,$product_meta])),'images'=>$images];
}
$term_meta=get_term_meta(246); foreach(['wd_page_css_files','xts-term-246-status','product_count_product_cat'] as $key)unset($term_meta[$key]);
$usage=['terms'=>[],'post_refs'=>[],'post_meta_refs'=>[]];
if(!empty($term_meta['category_extra_description_html_block'][0])||!empty($term_meta['category_description_html_block'][0])||$term->description!=='')exit(4);
$protected_meta=$term_meta;unset($protected_meta['category_extra_description_type'],$protected_meta['category_extra_description_html_block']);
echo json_encode(['utc'=>gmdate('c'),'block'=>null,'term'=>['id'=>246,'slug'=>$term->slug,'name'=>$term->name,'description'=>$term->description,'meta'=>$term_meta,'protected_hash'=>hash('sha256',serialize([$term,$protected_meta]))],'art_block_hash'=>hash('sha256',serialize([get_post(22822),get_post_meta(22822)])),'satellites_block_hash'=>hash('sha256',serialize([get_post(22817),get_post_meta(22817)])),'planets_block_hash'=>hash('sha256',serialize([get_post(21162),get_post_meta(21162)])),'islands_block_hash'=>hash('sha256',serialize([get_post(21178),get_post_meta(21178)])),'continents_block_hash'=>hash('sha256',serialize([get_post(21175),get_post_meta(21175)])),'countries_block_hash'=>hash('sha256',serialize([get_post(21176),get_post_meta(21176)])),'usa_block_hash'=>hash('sha256',serialize([get_post(21177),get_post_meta(21177)])),'parent_block_hash'=>$parent_block_hash,'usage'=>$usage,'products'=>$products],JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE|JSON_PRETTY_PRINT);
