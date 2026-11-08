<?php
ini_set('display_errors','0');
define('WP_USE_THEMES',false);
ob_start();require '/var/www/html/wp-load.php';ob_end_clean();
if(PHP_SAPI!=='cli'||rtrim(home_url(),'/')!=='https://shustrik-maps.com')throw new RuntimeException('Wrong runtime');
function guard($ok,$message){if(!$ok)throw new RuntimeException($message);}
function invariant($id,$target=true){
 $p=(array)get_post($id);$m=get_post_meta($id);unset($m['wd_page_css_files']);
 if($target){unset($p['post_content'],$p['post_modified'],$p['post_modified_gmt'],$m['_yoast_wpseo_title'],$m['_yoast_wpseo_metadesc']);}
 ksort($m);$t=wp_get_object_terms($id,get_object_taxonomies(get_post($id)->post_type),['fields'=>'all']);
 usort($t,function($a,$b){$c=strcasecmp($a->name,$b->name);return $c!==0?$c:($a->term_id<=>$b->term_id);});
 return hash('sha256',serialize([$p,$m,$t]));
}
function indexable(){global $wpdb;return $wpdb->get_results("SELECT id,title,description FROM {$wpdb->prefix}yoast_indexable WHERE object_type='post' AND object_id=15665",ARRAY_A);}
function product_title(){return get_post_meta(15665,'_yoast_wpseo_title',true);}
