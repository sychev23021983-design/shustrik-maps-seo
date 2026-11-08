<?php
ini_set('display_errors','0');define('WP_USE_THEMES',false);ob_start();require '/var/www/html/wp-load.php';ob_end_clean();
if(PHP_SAPI!=='cli'||rtrim(home_url(),'/')!=='https://shustrik-maps.com')throw new RuntimeException('Wrong runtime');
function must($c,$m){if(!$c)throw new RuntimeException($m);}
function invariant($id,$target=false){$p=(array)get_post($id);must(!empty($p['ID']),'Missing post '.$id);$m=get_post_meta($id);unset($m['wd_page_css_files']);if($target){unset($p['post_title'],$p['post_modified'],$p['post_modified_gmt'],$m['_wp_attachment_image_alt']);}ksort($m);$t=wp_get_object_terms($id,get_object_taxonomies($p['post_type']),['fields'=>'all']);usort($t,fn($a,$b)=>$a->term_id<=>$b->term_id);return hash('sha256',serialize([$p,$m,$t]));}
function altrows($id){global $wpdb;return $wpdb->get_results($wpdb->prepare("SELECT meta_id,meta_value FROM {$wpdb->postmeta} WHERE post_id=%d AND meta_key='_wp_attachment_image_alt' ORDER BY meta_id",$id),ARRAY_A);}
function values($id){$p=get_post($id);return ['title'=>$p->post_title,'alt'=>get_post_meta($id,'_wp_attachment_image_alt',true)];}
function indexable_hash($ids){global $wpdb;$ids=implode(',',array_map('intval',$ids));return hash('sha256',serialize($wpdb->get_results("SELECT * FROM {$wpdb->prefix}yoast_indexable WHERE object_type='post' AND object_id IN ($ids) ORDER BY id",ARRAY_A)));}
