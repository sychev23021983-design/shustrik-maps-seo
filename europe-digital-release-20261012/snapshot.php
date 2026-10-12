<?php
ini_set('display_errors','0'); define('WP_USE_THEMES',false); ob_start(); require '/var/www/html/wp-load.php'; ob_end_clean();
if(PHP_SAPI!=='cli'||rtrim(home_url(),'/')!=='https://shustrik-maps.com')exit(1);
global $wpdb;
$block=get_post(15197); $term=get_term(161,'product_cat');
if(!$block||$block->post_type!=='cms_block'||!$term||is_wp_error($term)||$term->slug!=='europe')exit(2);
$products=[];
foreach(get_posts(['post_type'=>'product','post_status'=>'publish','numberposts'=>-1,'tax_query'=>[['taxonomy'=>'product_cat','field'=>'term_id','terms'=>[161],'include_children'=>true]]]) as $p){
 $slug=$p->post_name; if(!$p)exit(3); $images=[];
 foreach(array_unique(array_merge([get_post_thumbnail_id($p->ID)],explode(',',get_post_meta($p->ID,'_product_image_gallery',true)))) as $aid){if(!$aid)continue;$images[]=['id'=>(int)$aid,'url'=>wp_get_attachment_url($aid)];}
 $products[]=['id'=>$p->ID,'slug'=>$slug,'url'=>get_permalink($p->ID),'state_hash'=>hash('sha256',serialize([$p,array_diff_key(get_post_meta($p->ID),array_flip(['wd_page_css_files']))])),'images'=>$images];
}
$previous_blocks=[];foreach([14416, 14417, 21177, 21176, 21175, 21178, 21162, 22817, 22822, 22827, 22832, 16359, 17235, 18122, 22853, 22858, 15975, 14991, 18211, 20008, 20525, 22867, 15267, 15269, 15271, 15364, 15346, 15361, 14996, 15273, 15031, 15195, 15193, 15191, 15189] as $id)$previous_blocks[$id]=hash('sha256',serialize([get_post($id),get_post_meta($id)]));
$term_meta=get_term_meta(161); foreach(['wd_page_css_files','xts-term-161-status','product_count_product_cat'] as $key)unset($term_meta[$key]);
$usage=['description_terms'=>$wpdb->get_results($wpdb->prepare("SELECT term_id,description FROM {$wpdb->term_taxonomy} WHERE description LIKE %s",'%15197%'),ARRAY_A),'terms'=>$wpdb->get_results($wpdb->prepare("SELECT term_id,meta_key FROM {$wpdb->termmeta} WHERE meta_value=%s",'15197'),ARRAY_A),'post_refs'=>$wpdb->get_results($wpdb->prepare("SELECT ID,post_type,post_name FROM {$wpdb->posts} WHERE post_status NOT IN ('trash','auto-draft') AND post_type!='revision' AND post_content LIKE %s",'%15197%'),ARRAY_A),'post_meta_refs'=>$wpdb->get_results($wpdb->prepare("SELECT post_id,meta_key FROM {$wpdb->postmeta} WHERE meta_value=%s",'15197'),ARRAY_A)];
$protected_term=clone $term;$protected_term->description='';
$previous_terms=[];foreach([63,67,68,159,160] as $prior_id){$prior_meta=get_term_meta($prior_id);foreach(['wd_page_css_files','xts-term-'.$prior_id.'-status','product_count_product_cat'] as $k)unset($prior_meta[$k]);$previous_terms[$prior_id]=hash('sha256',serialize([get_term($prior_id,'product_cat'),$prior_meta]));}
echo json_encode(['utc'=>gmdate('c'),'block'=>['id'=>15197,'title'=>$block->post_title,'content'=>$block->post_content,'content_sha256'=>hash('sha256',$block->post_content),'protected_hash'=>hash('sha256',serialize([$block->post_title,$block->post_name,$block->post_status,$block->post_excerpt,get_post_meta(15197)]))],'term'=>['id'=>161,'slug'=>$term->slug,'name'=>$term->name,'description'=>$term->description,'meta'=>$term_meta,'protected_hash'=>hash('sha256',serialize([$protected_term,$term_meta]))],'usage'=>$usage,'products'=>$products,'previous_terms'=>$previous_terms,'previous_blocks'=>$previous_blocks],JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE|JSON_PRETTY_PRINT);
