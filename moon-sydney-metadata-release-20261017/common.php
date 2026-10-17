<?php
ini_set('display_errors','0');define('WP_USE_THEMES',false);ob_start();require '/var/www/html/wp-load.php';ob_end_clean();
if(PHP_SAPI!=='cli'||rtrim(home_url(),'/')!=='https://shustrik-maps.com')throw new RuntimeException('Wrong runtime');
function invariant($id,$target=true){
 $post=(array)get_post($id);$meta=get_post_meta($id);unset($meta['wd_page_css_files']);
 if($target){unset($meta['_yoast_wpseo_title'],$meta['_yoast_wpseo_metadesc']);}
 ksort($meta);$terms=wp_get_object_terms($id,get_object_taxonomies(get_post($id)->post_type),['fields'=>'all']);
 usort($terms,function($a,$b){$n=strcasecmp($a->name,$b->name);return $n!==0?$n:($a->term_id<=>$b->term_id);});
 return hash('sha256',serialize([$post,$meta,$terms]));
}
function meta_values($id){return ['_yoast_wpseo_title'=>get_post_meta($id,'_yoast_wpseo_title',true),'_yoast_wpseo_metadesc'=>get_post_meta($id,'_yoast_wpseo_metadesc',true)];}
