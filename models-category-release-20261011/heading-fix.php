<?php
ini_set('display_errors','0');define('WP_USE_THEMES',false);ob_start();require '/var/www/html/wp-load.php';ob_end_clean();
function fail_release($message){throw new RuntimeException($message);}
function protected_state(){
 $t=clone get_term(26,'product_cat');$t->description='';$m=get_term_meta(26);foreach(['wd_page_css_files','xts-term-26-status','product_count_product_cat'] as $k)unset($m[$k]);
 $products=[];foreach(get_posts(['post_type'=>'product','post_status'=>'publish','numberposts'=>-1,'tax_query'=>[['taxonomy'=>'product_cat','field'=>'term_id','terms'=>[26],'include_children'=>true]]]) as $p){$pm=get_post_meta($p->ID);unset($pm['wd_page_css_files']);$products[$p->ID]=hash('sha256',serialize([$p,$pm]));}
 $blocks=[];foreach([14416, 14417, 21177, 21176, 21175, 21178, 21162, 22817, 22822, 22827] as $id)$blocks[$id]=hash('sha256',serialize([get_post($id),get_post_meta($id)]));
 return ['term'=>hash('sha256',serialize([$t,$m])),'products'=>$products,'blocks'=>$blocks];
}
function assert_protected($a,$b){
 if($a['term']!==$b['term']['protected_hash'])fail_release('Protected category drift');
 if(count($a['products'])!==count($b['products']))fail_release('Catalogue membership drift');
 foreach($b['products'] as $p)if(($a['products'][$p['id']]??'')!==$p['state_hash'])fail_release('Protected product drift');
 if($a['blocks']!==$b['previous_blocks'])fail_release('Existing shared/category block drift');
}
function placement_state(){return ['description'=>get_term(26,'product_cat')->description];}
function assert_placement($expected){if(placement_state()!==$expected)fail_release('Category placement drift');}
function check_usage($id){global $wpdb;
 $terms=$wpdb->get_results($wpdb->prepare("SELECT term_id FROM {$wpdb->term_taxonomy} WHERE description LIKE %s",'%'.$id.'%'),ARRAY_A);
 if(count($terms)!==1||(int)$terms[0]['term_id']!==26)fail_release('Shared category block');
 if((int)$wpdb->get_var($wpdb->prepare("SELECT COUNT(*) FROM {$wpdb->termmeta} WHERE meta_value=%s",(string)$id)))fail_release('Shared term meta block');
 if((int)$wpdb->get_var($wpdb->prepare("SELECT COUNT(*) FROM {$wpdb->posts} WHERE post_status NOT IN ('trash','auto-draft') AND post_type!='revision' AND post_content LIKE %s",'%'.$id.'%')))fail_release('Shared post block');
 if((int)$wpdb->get_var($wpdb->prepare("SELECT COUNT(*) FROM {$wpdb->postmeta} WHERE meta_value=%s",(string)$id)))fail_release('Shared post meta block');
}
function verify_block($b){$p=get_post($b['block_id']);if(!$p||$p->post_type!=='cms_block'||$p->post_status!=='publish'||$p->post_name!=='models-category-applications-20261011'||$p->post_content!==$b['after'])fail_release('Published block drift');}
function refresh_category($url,$id){clean_post_cache($id);clean_term_cache(26,'product_cat');if(function_exists('rocket_clean_files'))rocket_clean_files([$url]);do_action('litespeed_purge_url',$url);}
try{
 if(PHP_SAPI!=='cli'||rtrim(home_url(),'/')!=='https://shustrik-maps.com')fail_release('Wrong site');
 $mode=$argv[1]??'--preview';if(!in_array($mode,['--preview','--apply']))fail_release('Mode');
 $m=json_decode(file_get_contents(__DIR__.'/manifest.json'),true);$baseline=json_decode(file_get_contents(__DIR__.'/baseline.json'),true);$key='_shustrik_models_category_backup_20261011';$b=get_option($key);if(!$b||$b['status']!=='published')fail_release('Missing backup');
 assert_protected(protected_state(),$baseline);assert_placement($b['placement_after']);verify_block($b);check_usage($b['block_id']);
 if(hash('sha256',$b['after'])!=='dfa2f61b16b7120960cd982c33606648b0b681f9f214ddd7f9a0d323b3c0e700'||isset($b['heading_before']))fail_release('Heading revision drift');
 $template=file_get_contents(__DIR__.'/category.html');if(hash('sha256',$template)!==$m['template_sha256'])fail_release('Template hash');
 foreach($m['assets'] as $asset){$image=wp_get_attachment_image($b['ids'][$asset['key']],'large',false,['alt'=>$asset['alt'],'loading'=>'lazy','decoding'=>'async','class'=>'cnc-application-photo']);$template=str_replace('{{IMAGE:'.$asset['key'].'}}',$image,$template);}
 preg_match('/\[vc_raw_html\]([^[]+)\[\/vc_raw_html\]/',$b['after'],$match);$old=rawurldecode(base64_decode($match[1]));$modified=str_replace(['<h1 id="models-category-title">','</h1>'],['<h2 id="models-category-title">','</h2>'],$old);if($modified!==$template)fail_release('Change exceeds heading-only scope');
 $after='[vc_row type="boxed" max_width="1600"][vc_column][vc_raw_html]'.base64_encode(rawurlencode($template)).'[/vc_raw_html][/vc_column][/vc_row]';
 if($mode==='--apply'){
  global $wpdb;$wpdb->query('START TRANSACTION');try{$wpdb->get_var($wpdb->prepare("SELECT ID FROM {$wpdb->posts} WHERE ID=%d FOR UPDATE",$b['block_id']));clean_post_cache($b['block_id']);verify_block($b);assert_protected(protected_state(),$baseline);assert_placement($b['placement_after']);$changed=$wpdb->query($wpdb->prepare("UPDATE {$wpdb->posts} SET post_content=%s,post_modified=%s,post_modified_gmt=%s WHERE ID=%d AND post_content=%s",$after,current_time('mysql'),current_time('mysql',true),$b['block_id'],$b['after']));if($changed!==1)fail_release('Conditional heading write');$wpdb->query('COMMIT');}catch(Throwable $e){$wpdb->query('ROLLBACK');throw $e;}
  $b['heading_before']=$b['after'];$b['after']=$after;$b['heading_updated_at']=gmdate('c');update_option($key,$b,false);refresh_category($m['url'],$b['block_id']);verify_block($b);assert_protected(protected_state(),$baseline);
 }
 echo json_encode(['ok'=>true,'mode'=>$mode,'utc'=>gmdate('c'),'block_id'=>$b['block_id'],'term_id'=>26,'heading_only'=>true,'no_media_created'=>true,'protected_preserved'=>true,'content_sha256'=>hash('sha256',$after)],JSON_UNESCAPED_SLASHES)."\n";
}catch(Throwable $e){echo json_encode(['ok'=>false,'reason'=>$e->getMessage()])."\n";exit(1);}
