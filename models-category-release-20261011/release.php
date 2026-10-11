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
 $mode=$argv[1]??'--preview';if(!in_array($mode,['--preview','--apply','--verify','--rollback-preview','--rollback']))fail_release('Mode');
 $m=json_decode(file_get_contents(__DIR__.'/manifest.json'),true,512,JSON_THROW_ON_ERROR);$baseline=json_decode(file_get_contents(__DIR__.'/baseline.json'),true,512,JSON_THROW_ON_ERROR);
 if($m['term_id']!==26||$m['block_id']!==null||count($m['assets'])!==4||get_term(26,'product_cat')->slug!=='3d-models')fail_release('Scope');
 $template=file_get_contents(__DIR__.'/category.html');if(hash('sha256',$template)!==$m['template_sha256'])fail_release('Template hash');
 foreach($m['assets'] as $asset)if($asset['mode']!=='new'||hash_file('sha256',__DIR__.'/assets/'.$asset['file'])!==$asset['sha256'])fail_release('Asset scope/hash');
 $backup_key='_shustrik_models_category_backup_20261011';$journal_key='_shustrik_models_category_media_20261011';$b=get_option($backup_key,null);
 $before=['description'=>$baseline['term']['description']];$before_exists=['description'=>true];
 assert_protected(protected_state(),$baseline);
 if(in_array($mode,['--verify','--rollback-preview','--rollback'])){if(!$b||$b['status']!=='published')fail_release('Missing published backup');assert_placement($b['placement_after']);verify_block($b);check_usage($b['block_id']);}
 else{assert_placement($before);if($before!==['description'=>'[html_block id="14416"]'])fail_release('Original category reference drift');if($b!==null||get_option($journal_key,null)!==null||get_page_by_path('models-category-applications-20261011',OBJECT,'cms_block'))fail_release('Existing release; inspect before retry');}
 if($mode==='--apply'){
  $protected=protected_state();$b=['utc'=>gmdate('c'),'placement_before'=>$before,'placement_before_exists'=>$before_exists,'baseline'=>$baseline,'status'=>'prepared'];
  if(!add_option($backup_key,$b,'',false)||!add_option($journal_key,['ids'=>[],'status'=>'importing'],'',false))fail_release('Backup collision');
  $id=wp_insert_post(wp_slash(['post_type'=>'cms_block','post_status'=>'draft','post_title'=>'3D Models — application concepts','post_name'=>'models-category-applications-20261011','post_content'=>'']),true);if(is_wp_error($id)||!$id)fail_release('Block creation');$b['block_id']=$id;update_option($backup_key,$b,false);$ids=[];
  require_once ABSPATH.'wp-admin/includes/file.php';require_once ABSPATH.'wp-admin/includes/media.php';require_once ABSPATH.'wp-admin/includes/image.php';
  foreach($m['assets'] as $asset){$tmp=wp_tempnam($asset['file']);if(!copy(__DIR__.'/assets/'.$asset['file'],$tmp))fail_release('Media staging');$aid=media_handle_sideload(['name'=>$asset['file'],'tmp_name'=>$tmp],$id,$asset['caption']);if(is_wp_error($aid))fail_release('Media import');$ids[$asset['key']]=$aid;update_option($journal_key,['ids'=>$ids,'status'=>'importing'],false);
   $r=wp_update_post(wp_slash(['ID'=>$aid,'post_title'=>$asset['title'],'post_excerpt'=>$asset['caption'],'post_content'=>$asset['caption']]),true);if(is_wp_error($r))fail_release('Media metadata');update_post_meta($aid,'_wp_attachment_image_alt',wp_slash($asset['alt']));
   $image=wp_get_attachment_image($aid,'large',false,['alt'=>$asset['alt'],'loading'=>'lazy','decoding'=>'async','class'=>'cnc-application-photo']);if(!$image)fail_release('Image render');$template=str_replace('{{IMAGE:'.$asset['key'].'}}',$image,$template);
  }
  if(strpos($template,'{{')!==false)fail_release('Unresolved template');
  $after='[vc_row type="boxed" max_width="1600"][vc_column][vc_raw_html]'.base64_encode(rawurlencode($template)).'[/vc_raw_html][/vc_column][/vc_row]';
  $b=array_merge($b,['after'=>$after,'ids'=>$ids,'placement_after'=>['description'=>'[html_block id="'.$id.'"]'],'status'=>'ready']);update_option($backup_key,$b,false);
  global $wpdb;$wpdb->query('START TRANSACTION');
  try{$wpdb->get_var($wpdb->prepare("SELECT ID FROM {$wpdb->posts} WHERE ID=%d FOR UPDATE",$id));$wpdb->get_var($wpdb->prepare("SELECT term_id FROM {$wpdb->term_taxonomy} WHERE term_id=%d AND taxonomy='product_cat' FOR UPDATE",26));$wpdb->get_results($wpdb->prepare("SELECT meta_id FROM {$wpdb->termmeta} WHERE term_id=%d FOR UPDATE",26));wp_cache_delete(26,'term_meta');clean_post_cache($id);assert_placement($before);if(protected_state()!==$protected)fail_release('Concurrent protected edit');
   $p=get_post($id);if($p->post_type!=='cms_block'||$p->post_status!=='draft'||$p->post_content!==''||$p->post_name!=='models-category-applications-20261011')fail_release('New draft drift');
   $changed=$wpdb->query($wpdb->prepare("UPDATE {$wpdb->posts} SET post_status='publish',post_content=%s,post_modified=%s,post_modified_gmt=%s WHERE ID=%d AND post_status='draft' AND post_content=''",$after,current_time('mysql'),current_time('mysql',true),$id));if($changed!==1)fail_release('Conditional block write');clean_post_cache($id);
   $changed=$wpdb->query($wpdb->prepare("UPDATE {$wpdb->term_taxonomy} SET description=%s WHERE term_id=26 AND taxonomy='product_cat' AND description=%s",$b['placement_after']['description'],$before['description']));if($changed!==1)fail_release('Conditional category reference write');clean_term_cache(26,'product_cat');
   wp_cache_delete(26,'term_meta');assert_placement($b['placement_after']);assert_protected(protected_state(),$baseline);verify_block($b);check_usage($id);$wpdb->query('COMMIT');
  }catch(Throwable $e){$wpdb->query('ROLLBACK');wp_cache_delete(26,'term_meta');clean_post_cache($id);throw $e;}
  $b['status']='published';$b['published_at']=gmdate('c');update_option($backup_key,$b,false);update_option($journal_key,['ids'=>$ids,'status'=>'published'],false);refresh_category($m['url'],$id);
 }
 if($mode==='--rollback'){
  global $wpdb;$wpdb->query('START TRANSACTION');try{$wpdb->get_var($wpdb->prepare("SELECT term_id FROM {$wpdb->term_taxonomy} WHERE term_id=%d AND taxonomy='product_cat' FOR UPDATE",26));$wpdb->get_results($wpdb->prepare("SELECT meta_id FROM {$wpdb->termmeta} WHERE term_id=%d FOR UPDATE",26));wp_cache_delete(26,'term_meta');assert_placement($b['placement_after']);verify_block($b);assert_protected(protected_state(),$baseline);
   $changed=$wpdb->query($wpdb->prepare("UPDATE {$wpdb->term_taxonomy} SET description=%s WHERE term_id=26 AND taxonomy='product_cat' AND description=%s",$b['placement_before']['description'],$b['placement_after']['description']));if($changed!==1)fail_release('Conditional reference rollback');clean_term_cache(26,'product_cat');
   wp_cache_delete(26,'term_meta');assert_placement($b['placement_before']);assert_protected(protected_state(),$baseline);$wpdb->query('COMMIT');
  }catch(Throwable $e){$wpdb->query('ROLLBACK');wp_cache_delete(26,'term_meta');throw $e;}$b['status']='rolled-back';update_option($backup_key,$b,false);refresh_category($m['url'],$b['block_id']);
 }
 $media=[];if(in_array($mode,['--apply','--verify','--rollback-preview'])){foreach($m['assets'] as $asset){$aid=$b['ids'][$asset['key']];$data=wp_get_attachment_metadata($aid);if(!$data||$data['width']<1000||$data['height']<600||hash_file('sha256',get_attached_file($aid))!==$asset['sha256']||get_post_meta($aid,'_wp_attachment_image_alt',true)!==$asset['alt'])fail_release('Media verification');$media[]=['key'=>$asset['key'],'id'=>$aid,'url'=>wp_get_attachment_url($aid),'mode'=>'new','width'=>$data['width'],'height'=>$data['height']];}}
 assert_protected(protected_state(),$baseline);echo json_encode(['ok'=>true,'mode'=>$mode,'utc'=>gmdate('c'),'url'=>$m['url'],'term_id'=>26,'block_id'=>$b['block_id']??null,'protected_preserved'=>true,'media'=>$media,'content_sha256'=>isset($b['after'])?hash('sha256',$b['after']):null,'rollback_backup'=>$backup_key],JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE)."\n";
}catch(Throwable $e){echo json_encode(['ok'=>false,'reason'=>$e instanceof RuntimeException?$e->getMessage():'Internal error'])."\n";exit(1);}
