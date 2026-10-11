<?php
ini_set('display_errors','0');define('WP_USE_THEMES',false);ob_start();require '/var/www/html/wp-load.php';ob_end_clean();
function fail_release($message){throw new RuntimeException($message);}
function protected_state(){
 $t=get_term(175,'product_cat');$m=get_term_meta(175);foreach(['wd_page_css_files','xts-term-175-status','product_count_product_cat','category_extra_description_type','category_extra_description_html_block'] as $k)unset($m[$k]);
 $products=[];foreach(get_posts(['post_type'=>'product','post_status'=>'publish','numberposts'=>-1,'tax_query'=>[['taxonomy'=>'product_cat','field'=>'term_id','terms'=>[175],'include_children'=>false]]]) as $p)$products[$p->ID]=hash('sha256',serialize([$p,get_post_meta($p->ID)]));
 $blocks=[];foreach([14417,21177,21176,21175,21178,21162] as $id)$blocks[$id]=hash('sha256',serialize([get_post($id),get_post_meta($id)]));
 return ['term'=>hash('sha256',serialize([$t,$m])),'products'=>$products,'blocks'=>$blocks];
}
function assert_protected($a,$b){
 if($a['term']!==$b['term']['protected_hash'])fail_release('Protected category drift');
 if(count($a['products'])!==count($b['products']))fail_release('Catalogue membership drift');
 foreach($b['products'] as $p)if(($a['products'][$p['id']]??'')!==$p['state_hash'])fail_release('Product drift');
 foreach([14417=>'parent',21177=>'usa',21176=>'countries',21175=>'continents',21178=>'islands',21162=>'planets'] as $id=>$key)if($a['blocks'][$id]!==$b[$key.'_block_hash'])fail_release('Existing category block drift');
}
function placement_state(){return ['type'=>get_term_meta(175,'category_extra_description_type',true),'block'=>get_term_meta(175,'category_extra_description_html_block',true)];}
function assert_placement($expected){if(placement_state()!==$expected)fail_release('Category placement drift');}
function check_usage($id){global $wpdb;
 $terms=$wpdb->get_results($wpdb->prepare("SELECT term_id,meta_key FROM {$wpdb->termmeta} WHERE meta_value=%s",(string)$id),ARRAY_A);
 if(count($terms)!==1||(int)$terms[0]['term_id']!==175||$terms[0]['meta_key']!=='category_extra_description_html_block')fail_release('Shared category block');
 if((int)$wpdb->get_var($wpdb->prepare("SELECT COUNT(*) FROM {$wpdb->posts} WHERE post_status NOT IN ('trash','auto-draft') AND post_type!='revision' AND post_content LIKE %s",'%'.$id.'%')))fail_release('Shared post block');
 if((int)$wpdb->get_var($wpdb->prepare("SELECT COUNT(*) FROM {$wpdb->postmeta} WHERE meta_value=%s",(string)$id)))fail_release('Shared post meta block');
}
function verify_block($b){$p=get_post($b['block_id']);if(!$p||$p->post_type!=='cms_block'||$p->post_status!=='publish'||$p->post_name!=='satellites-category-applications-20261011'||$p->post_content!==$b['after'])fail_release('Published block drift');}
function refresh_category($url,$id){clean_post_cache($id);clean_term_cache(175,'product_cat');if(function_exists('rocket_clean_files'))rocket_clean_files([$url]);do_action('litespeed_purge_url',$url);}
try{
 if(PHP_SAPI!=='cli'||rtrim(home_url(),'/')!=='https://shustrik-maps.com')fail_release('Wrong site');
 $mode=$argv[1]??'--preview';if(!in_array($mode,['--preview','--apply','--resume-prepared','--verify','--rollback-preview','--rollback']))fail_release('Mode');
 $m=json_decode(file_get_contents(__DIR__.'/manifest.json'),true,512,JSON_THROW_ON_ERROR);$baseline=json_decode(file_get_contents(__DIR__.'/baseline.json'),true,512,JSON_THROW_ON_ERROR);
 if($m['term_id']!==175||$m['block_id']!==null||count($m['assets'])!==4)fail_release('Scope');
 $template=file_get_contents(__DIR__.'/category.html');if(hash('sha256',$template)!==$m['template_sha256'])fail_release('Template hash');
 foreach($m['assets'] as $asset)if($asset['mode']!=='new'||hash_file('sha256',__DIR__.'/assets/'.$asset['file'])!==$asset['sha256'])fail_release('Asset scope/hash');
 $backup_key='_shustrik_satellites_category_backup_20261011';$journal_key='_shustrik_satellites_category_media_20261011';$b=get_option($backup_key,null);
 $before=['type'=>$baseline['term']['meta']['category_extra_description_type'][0],'block'=>$baseline['term']['meta']['category_extra_description_html_block'][0]];
 assert_protected(protected_state(),$baseline);
 if(in_array($mode,['--verify','--rollback-preview','--rollback'])){if(!$b||$b['status']!=='published')fail_release('Missing published backup');assert_placement($b['placement_after']);verify_block($b);check_usage($b['block_id']);}
 else{assert_placement($before);if($before!==['type'=>'text','block'=>'']||get_term_meta(175,'category_extra_description_text',true)!=='')fail_release('Not an empty bottom section');
  $draft=get_page_by_path('satellites-category-applications-20261011',OBJECT,'cms_block');
  if($mode==='--resume-prepared'){$j=get_option($journal_key,null);if(!$b||$b['status']!=='prepared'||isset($b['block_id'])||$b['placement_before']!==$before||$b['baseline']!==$baseline||$j!==['ids'=>[],'status'=>'importing']||!$draft||$draft->ID!==22817||$draft->post_status!=='draft'||$draft->post_content!==''||$draft->post_title!=='Satellites — Moon STL applications')fail_release('Prepared resume state mismatch');}
  elseif($b!==null||get_option($journal_key,null)!==null||$draft)fail_release('Existing release; inspect before retry');
 }
 if(in_array($mode,['--apply','--resume-prepared'])){
  $protected=protected_state();
  if($mode==='--apply'){$b=['utc'=>gmdate('c'),'placement_before'=>$before,'baseline'=>$baseline,'status'=>'prepared'];if(!add_option($backup_key,$b,'',false)||!add_option($journal_key,['ids'=>[],'status'=>'importing'],'',false))fail_release('Backup collision');
   $id=wp_insert_post(wp_slash(['post_type'=>'cms_block','post_status'=>'draft','post_title'=>'Satellites — Moon STL applications','post_name'=>'satellites-category-applications-20261011','post_content'=>'']),true);if(is_wp_error($id)||!$id)fail_release('Block creation');
  }else{$id=$draft->ID;$b['resumed_at']=gmdate('c');}
  $b['block_id']=$id;update_option($backup_key,$b,false);$ids=[];
  require_once ABSPATH.'wp-admin/includes/file.php';require_once ABSPATH.'wp-admin/includes/media.php';require_once ABSPATH.'wp-admin/includes/image.php';
  foreach($m['assets'] as $asset){$tmp=wp_tempnam($asset['file']);if(!copy(__DIR__.'/assets/'.$asset['file'],$tmp))fail_release('Media staging');$aid=media_handle_sideload(['name'=>$asset['file'],'tmp_name'=>$tmp],$id,$asset['caption']);if(is_wp_error($aid))fail_release('Media import');$ids[$asset['key']]=$aid;update_option($journal_key,['ids'=>$ids,'status'=>'importing'],false);
   $r=wp_update_post(wp_slash(['ID'=>$aid,'post_title'=>$asset['title'],'post_excerpt'=>$asset['caption'],'post_content'=>$asset['caption']]),true);if(is_wp_error($r))fail_release('Media metadata');update_post_meta($aid,'_wp_attachment_image_alt',wp_slash($asset['alt']));
   $image=wp_get_attachment_image($aid,'large',false,['alt'=>$asset['alt'],'loading'=>'lazy','decoding'=>'async','class'=>'cnc-application-photo']);if(!$image)fail_release('Image render');$template=str_replace('{{IMAGE:'.$asset['key'].'}}',$image,$template);
  }
  if(strpos($template,'{{')!==false)fail_release('Unresolved template');
  $after='[vc_row type="boxed" max_width="1600"][vc_column][vc_raw_html]'.base64_encode(rawurlencode($template)).'[/vc_raw_html][/vc_column][/vc_row]';
  $r=wp_update_post(wp_slash(['ID'=>$id,'post_status'=>'publish','post_content'=>$after]),true);if(is_wp_error($r))fail_release('Block publication');
  $b=array_merge($b,['after'=>$after,'ids'=>$ids,'placement_after'=>['type'=>'html_block','block'=>(string)$id],'status'=>'ready']);update_option($backup_key,$b,false);
  global $wpdb;$wpdb->query('START TRANSACTION');
  try{$wpdb->get_results($wpdb->prepare("SELECT meta_id FROM {$wpdb->termmeta} WHERE term_id=%d FOR UPDATE",175));wp_cache_delete(175,'term_meta');assert_placement($before);if(protected_state()!==$protected)fail_release('Concurrent protected edit');
   foreach(['category_extra_description_type'=>'html_block','category_extra_description_html_block'=>(string)$id] as $key=>$value){if(!update_term_meta(175,$key,$value))fail_release('Placement write');}
   wp_cache_delete(175,'term_meta');assert_placement($b['placement_after']);assert_protected(protected_state(),$baseline);verify_block($b);check_usage($id);$wpdb->query('COMMIT');
  }catch(Throwable $e){$wpdb->query('ROLLBACK');wp_cache_delete(175,'term_meta');throw $e;}
  $b['status']='published';$b['published_at']=gmdate('c');update_option($backup_key,$b,false);update_option($journal_key,['ids'=>$ids,'status'=>'published'],false);refresh_category($m['url'],$id);
 }
 if($mode==='--rollback'){
  global $wpdb;$wpdb->query('START TRANSACTION');try{$wpdb->get_results($wpdb->prepare("SELECT meta_id FROM {$wpdb->termmeta} WHERE term_id=%d FOR UPDATE",175));wp_cache_delete(175,'term_meta');assert_placement($b['placement_after']);verify_block($b);assert_protected(protected_state(),$baseline);
   update_term_meta(175,'category_extra_description_type',$b['placement_before']['type']);update_term_meta(175,'category_extra_description_html_block',$b['placement_before']['block']);wp_cache_delete(175,'term_meta');assert_placement($b['placement_before']);assert_protected(protected_state(),$baseline);$wpdb->query('COMMIT');
  }catch(Throwable $e){$wpdb->query('ROLLBACK');wp_cache_delete(175,'term_meta');throw $e;}$b['status']='rolled-back';update_option($backup_key,$b,false);refresh_category($m['url'],$b['block_id']);
 }
 $media=[];if(in_array($mode,['--apply','--resume-prepared','--verify','--rollback-preview'])){foreach($m['assets'] as $asset){$aid=$b['ids'][$asset['key']];$data=wp_get_attachment_metadata($aid);if(!$data||$data['width']<1000||$data['height']<600||hash_file('sha256',get_attached_file($aid))!==$asset['sha256']||get_post_meta($aid,'_wp_attachment_image_alt',true)!==$asset['alt'])fail_release('Media verification');$media[]=['key'=>$asset['key'],'id'=>$aid,'url'=>wp_get_attachment_url($aid),'mode'=>'new','width'=>$data['width'],'height'=>$data['height']];}}
 assert_protected(protected_state(),$baseline);echo json_encode(['ok'=>true,'mode'=>$mode,'utc'=>gmdate('c'),'url'=>$m['url'],'term_id'=>175,'block_id'=>$b['block_id']??null,'protected_preserved'=>true,'media'=>$media,'content_sha256'=>isset($b['after'])?hash('sha256',$b['after']):null,'rollback_backup'=>$backup_key],JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE)."\n";
}catch(Throwable $e){echo json_encode(['ok'=>false,'reason'=>$e instanceof RuntimeException?$e->getMessage():'Internal error'])."\n";exit(1);}
