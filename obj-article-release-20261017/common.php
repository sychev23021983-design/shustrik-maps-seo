<?php
ini_set('display_errors','0');define('WP_USE_THEMES',false);ob_start();require '/var/www/html/wp-load.php';ob_end_clean();
if(PHP_SAPI!=='cli'||rtrim(home_url(),'/')!=='https://shustrik-maps.com')throw new RuntimeException('Wrong runtime');
function invariant($id,$target=true){$p=(array)get_post($id);$m=get_post_meta($id);unset($m['wd_page_css_files']);if($target){unset($p['post_content'],$p['post_modified'],$p['post_modified_gmt'],$m['_yoast_wpseo_title'],$m['_yoast_wpseo_metadesc']);}ksort($m);$t=wp_get_object_terms($id,get_object_taxonomies(get_post($id)->post_type),['fields'=>'all']);usort($t,function($a,$b){$n=strcasecmp($a->name,$b->name);return $n!==0?$n:($a->term_id<=>$b->term_id);});return hash('sha256',serialize([$p,$m,$t]));}
function values($id){return ['_yoast_wpseo_title'=>get_post_meta($id,'_yoast_wpseo_title',true),'_yoast_wpseo_metadesc'=>get_post_meta($id,'_yoast_wpseo_metadesc',true)];}
function counts($id){return ['_yoast_wpseo_title'=>count(get_post_meta($id,'_yoast_wpseo_title',false)),'_yoast_wpseo_metadesc'=>count(get_post_meta($id,'_yoast_wpseo_metadesc',false))];}
function indexable(){global $wpdb;return $wpdb->get_results("SELECT id,title,description FROM {$wpdb->prefix}yoast_indexable WHERE object_type='post' AND object_id=14581",ARRAY_A);}
