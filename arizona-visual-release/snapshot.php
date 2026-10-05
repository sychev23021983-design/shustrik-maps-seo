<?php
ini_set('display_errors','0');define('WP_USE_THEMES',false);ob_start();require '/var/www/html/wp-load.php';ob_end_clean();
if(PHP_SAPI!=='cli'||rtrim(home_url(),'/')!=='https://shustrik-maps.com')exit(1);
$id=9520;$p=get_post($id);if(!$p||$p->post_type!=='product'||$p->post_name!=='state-of-arizona-stl-model')exit(1);
$protected=[];foreach(['_price','_regular_price','_sale_price','_sku','_stock','_stock_status','_downloadable','_virtual','_downloadable_files','_thumbnail_id','_product_image_gallery','_yoast_wpseo_canonical','_yoast_wpseo_meta-robots-noindex','_yoast_wpseo_meta-robots-nofollow'] as $key)$protected[$key]=hash('sha256',serialize(get_post_meta($id,$key,true)));
echo json_encode(['id'=>$id,'url'=>get_permalink($id),'title'=>$p->post_title,'excerpt'=>$p->post_excerpt,'content'=>$p->post_content,'seo_title'=>get_post_meta($id,'_yoast_wpseo_title',true),'meta_description'=>get_post_meta($id,'_yoast_wpseo_metadesc',true),'gallery'=>get_post_meta($id,'_product_image_gallery',true),'protected'=>$protected],JSON_PRETTY_PRINT|JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE);
