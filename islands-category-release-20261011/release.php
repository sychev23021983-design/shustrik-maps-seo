<?php
ini_set('display_errors','0'); define('WP_USE_THEMES',false); ob_start(); require '/var/www/html/wp-load.php'; ob_end_clean();
function fail_release($message){throw new RuntimeException($message);}
function protected_state(){
 $p=get_post(21178);$t=get_term(27,'product_cat');$m=get_term_meta(27);foreach(['wd_page_css_files','xts-term-27-status','product_count_product_cat'] as $k)unset($m[$k]);
 $products=[];foreach(get_posts(['post_type'=>'product','post_status'=>'publish','numberposts'=>-1,'tax_query'=>[['taxonomy'=>'product_cat','field'=>'term_id','terms'=>[27],'include_children'=>false]]]) as $catalogue_product){$v=$catalogue_product;if(!$v)fail_release('Product missing');$products[$v->ID]=hash('sha256',serialize([$v,get_post_meta($v->ID)]));}
 return ['continents_block_hash'=>hash('sha256',serialize([get_post(21175),get_post_meta(21175)])),'countries_block_hash'=>hash('sha256',serialize([get_post(21176),get_post_meta(21176)])),'usa_block_hash'=>hash('sha256',serialize([get_post(21177),get_post_meta(21177)])),'parent_block_hash'=>hash('sha256',serialize([get_post(14417),get_post_meta(14417)])),'block'=>hash('sha256',serialize([$p->post_title,$p->post_name,$p->post_status,$p->post_excerpt,get_post_meta(21178)])),'term'=>hash('sha256',serialize([$t,$m])),'products'=>$products];
}
function assert_protected($actual,$baseline){
 if($actual['continents_block_hash']!==$baseline['continents_block_hash'])fail_release('Continents category block drift');
 if($actual['countries_block_hash']!==$baseline['countries_block_hash'])fail_release('Countries category block drift');
 if($actual['usa_block_hash']!==$baseline['usa_block_hash'])fail_release('USA States category block drift');
 if($actual['parent_block_hash']!==$baseline['parent_block_hash'])fail_release('Parent category block drift');
 if($actual['block']!==$baseline['block']['protected_hash']||$actual['term']!==$baseline['term']['protected_hash'])fail_release('Protected category/block drift');
 foreach($baseline['products'] as $p)if(($actual['products'][$p['id']]??'')!==$p['state_hash'])fail_release('Protected product drift');
}
function check_usage(){global $wpdb;
 $terms=$wpdb->get_results($wpdb->prepare("SELECT term_id,meta_key FROM {$wpdb->termmeta} WHERE meta_value=%s",'21178'),ARRAY_A);
 if(count($terms)!==1||(int)$terms[0]['term_id']!==27||$terms[0]['meta_key']!=='category_extra_description_html_block')fail_release('Shared category block');
 $refs=(int)$wpdb->get_var($wpdb->prepare("SELECT COUNT(*) FROM {$wpdb->posts} WHERE post_status NOT IN ('trash','auto-draft') AND post_type!='revision' AND post_content LIKE %s",'%21178%'));
 if($refs)fail_release('Shared post block');
 $refs=(int)$wpdb->get_var($wpdb->prepare("SELECT COUNT(*) FROM {$wpdb->postmeta} WHERE meta_value=%s",'21178'));if($refs)fail_release('Shared post meta block');
}
function refresh_category($url){clean_post_cache(21178);clean_term_cache(27,'product_cat');if(function_exists('rocket_clean_files'))rocket_clean_files([$url]);do_action('litespeed_purge_url',$url);}
try{
 if(PHP_SAPI!=='cli'||rtrim(home_url(),'/')!=='https://shustrik-maps.com')fail_release('Wrong site');
 $mode=$argv[1]??'--preview';if(!in_array($mode,['--preview','--apply','--verify','--rollback-preview','--rollback']))fail_release('Mode');
 $manifest=json_decode(file_get_contents(__DIR__.'/manifest.json'),true,512,JSON_THROW_ON_ERROR);$baseline=json_decode(file_get_contents(__DIR__.'/baseline.json'),true,512,JSON_THROW_ON_ERROR);
 if($manifest['block_id']!==21178||$manifest['term_id']!==27||count($manifest['assets'])!==4)fail_release('Scope');
 $template=file_get_contents(__DIR__.'/category.html');if(hash('sha256',$template)!==$manifest['template_sha256'])fail_release('Template hash');
 foreach($manifest['assets'] as $m)if($m['mode']==='new'&&hash_file('sha256',__DIR__.'/assets/'.$m['file'])!==$m['sha256'])fail_release('Asset hash');
 check_usage();assert_protected(protected_state(),$baseline);
 $backup_key='_shustrik_islands_category_backup_20261011';$journal_key='_shustrik_islands_category_media_20261011';$backup=get_option($backup_key,null);$current=get_post(21178)->post_content;
 $published_modes=['--verify','--rollback-preview','--rollback'];
 if(in_array($mode,$published_modes)){if(!$backup||$current!==$backup['after'])fail_release('Published content drift or missing backup');}
 else{if($backup!==null||get_option($journal_key,null)!==null)fail_release('Existing release journal; inspect before retry');if(hash('sha256',$current)!==$manifest['before_sha256'])fail_release('Baseline content drift');}
 $ids=[];$reuse=[];
 foreach($manifest['assets'] as $m){if($m['mode']==='reuse'){$aid=attachment_url_to_postid($m['url']);if(!$aid||wp_get_attachment_url($aid)!==$m['url']||!is_file(get_attached_file($aid)))fail_release('Reused asset missing');$ids[$m['key']]=$aid;$reuse[$m['key']]=$aid;}}
 if($mode==='--apply'){
  $protected=protected_state();$uploaded=[];
  if(!add_option($backup_key,['utc'=>gmdate('c'),'before'=>$current,'baseline'=>$baseline,'status'=>'prepared'],'',false))fail_release('Backup collision');
  if(!add_option($journal_key,['status'=>'importing','ids'=>[]],'',false))fail_release('Media journal collision');
  require_once ABSPATH.'wp-admin/includes/file.php';require_once ABSPATH.'wp-admin/includes/media.php';require_once ABSPATH.'wp-admin/includes/image.php';
  foreach($manifest['assets'] as $m){if($m['mode']!=='new')continue;$tmp=wp_tempnam($m['file']);if(!copy(__DIR__.'/assets/'.$m['file'],$tmp))fail_release('Asset staging');
   $aid=media_handle_sideload(['name'=>$m['file'],'tmp_name'=>$tmp],21178,$m['caption']);if(is_wp_error($aid))fail_release('Media import failed');$ids[$m['key']]=$aid;$uploaded[]=$aid;
   update_option($journal_key,['status'=>'importing','ids'=>$uploaded],false);
   $result=wp_update_post(wp_slash(['ID'=>$aid,'post_title'=>$m['title'],'post_excerpt'=>$m['caption'],'post_content'=>$m['caption']]),true);if(is_wp_error($result))fail_release('Media metadata');update_post_meta($aid,'_wp_attachment_image_alt',wp_slash($m['alt']));
  }
  foreach($manifest['assets'] as $m){$image=wp_get_attachment_image($ids[$m['key']],'large',false,['alt'=>$m['alt'],'loading'=>'lazy','decoding'=>'async','class'=>'cnc-application-photo']);if(!$image)fail_release('Image render');$template=str_replace('{{IMAGE:'.$m['key'].'}}',$image,$template);}
  if(strpos($template,'{{')!==false)fail_release('Unresolved placeholder');
  $after='[vc_row type="boxed" max_width="1600"][vc_column][vc_raw_html]'.base64_encode(rawurlencode($template)).'[/vc_raw_html][/vc_column][/vc_row]';
  $backup=['utc'=>gmdate('c'),'before'=>$current,'after'=>$after,'baseline'=>$baseline,'ids'=>$ids,'new_media'=>$uploaded,'status'=>'ready'];update_option($backup_key,$backup,false);
  global $wpdb;$wpdb->query('START TRANSACTION');
  try{$wpdb->get_var($wpdb->prepare("SELECT ID FROM {$wpdb->posts} WHERE ID=%d FOR UPDATE",21178));clean_post_cache(21178);if(get_post(21178)->post_content!==$current||protected_state()!==$protected)fail_release('Concurrent edit');
   $changed=$wpdb->query($wpdb->prepare("UPDATE {$wpdb->posts} SET post_content=%s,post_modified=%s,post_modified_gmt=%s WHERE ID=%d AND post_content=%s",$after,current_time('mysql'),current_time('mysql',true),21178,$current));if($changed!==1)fail_release('Conditional write failed');clean_post_cache(21178);if(get_post(21178)->post_content!==$after)fail_release('Written content mismatch');assert_protected(protected_state(),$baseline);$wpdb->query('COMMIT');
  }catch(Throwable $e){$wpdb->query('ROLLBACK');clean_post_cache(21178);throw $e;}
  $backup['status']='published';update_option($backup_key,$backup,false);update_option($journal_key,['status'=>'published','ids'=>$uploaded],false);refresh_category($manifest['url']);
 }
 if($mode==='--rollback'){
  global $wpdb;$changed=$wpdb->query($wpdb->prepare("UPDATE {$wpdb->posts} SET post_content=%s,post_modified=%s,post_modified_gmt=%s WHERE ID=%d AND post_content=%s",$backup['before'],current_time('mysql'),current_time('mysql',true),21178,$backup['after']));if($changed!==1)fail_release('Conditional rollback failed');refresh_category($manifest['url']);$backup['status']='rolled-back';update_option($backup_key,$backup,false);assert_protected(protected_state(),$baseline);
 }
 $media=[];if(in_array($mode,['--apply','--verify','--rollback-preview'])){$b=get_option($backup_key);foreach($manifest['assets'] as $m){$aid=$b['ids'][$m['key']];$data=wp_get_attachment_metadata($aid);if(!$data||$data['width']<1000||$data['height']<600)fail_release('Image dimensions');if($m['mode']==='new'&&(hash_file('sha256',get_attached_file($aid))!==$m['sha256']||get_post_meta($aid,'_wp_attachment_image_alt',true)!==$m['alt']))fail_release('Media verification');$media[]=['key'=>$m['key'],'id'=>$aid,'url'=>wp_get_attachment_url($aid),'mode'=>$m['mode'],'width'=>$data['width'],'height'=>$data['height']];}}
 assert_protected(protected_state(),$baseline);
 echo json_encode(['ok'=>true,'mode'=>$mode,'utc'=>gmdate('c'),'url'=>$manifest['url'],'block_id'=>21178,'protected_preserved'=>true,'reuse'=>$reuse,'media'=>$media,'content_sha256'=>hash('sha256',get_post(21178)->post_content),'rollback_backup'=>$backup_key],JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE)."\n";
}catch(Throwable $e){echo json_encode(['ok'=>false,'reason'=>$e instanceof RuntimeException?$e->getMessage():'Internal error'])."\n";exit(1);}
