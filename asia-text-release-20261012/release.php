<?php
ini_set('display_errors','0');define('WP_USE_THEMES',false);ob_start();require '/var/www/html/wp-load.php';ob_end_clean();
function fail_release($message){throw new RuntimeException($message);}
function protected_state(){
 $t=clone get_term(162,'product_cat');$t->description='';$m=get_term_meta(162);foreach(['wd_page_css_files','xts-term-162-status','product_count_product_cat'] as $k)unset($m[$k]);
 $products=[];foreach(get_posts(['post_type'=>'product','post_status'=>'publish','numberposts'=>-1,'tax_query'=>[['taxonomy'=>'product_cat','field'=>'term_id','terms'=>[162],'include_children'=>true]]]) as $p){$pm=get_post_meta($p->ID);unset($pm['wd_page_css_files']);$products[$p->ID]=hash('sha256',serialize([$p,$pm]));}
 $blocks=[];foreach([14416, 14417, 21177, 21176, 21175, 21178, 21162, 22817, 22822, 22827, 22832, 16359, 17235, 18122, 22853, 22858, 15975, 14991, 18211, 20008, 20525, 22867, 15267, 15269, 15271, 15364, 15346, 15361, 14996, 15273, 15031, 15195, 15193, 15191, 15189, 15197, 15244, 15238, 15221, 15218, 15200, 15418] as $id)$blocks[$id]=hash('sha256',serialize([get_post($id),get_post_meta($id)]));
 $previous_terms=[];foreach([63,67,68,159,160,161] as $prior_id){$prior_meta=get_term_meta($prior_id);foreach(['wd_page_css_files','xts-term-'.$prior_id.'-status','product_count_product_cat'] as $k)unset($prior_meta[$k]);$previous_terms[$prior_id]=hash('sha256',serialize([get_term($prior_id,'product_cat'),$prior_meta]));}
 return ['previous_terms'=>$previous_terms,'term'=>hash('sha256',serialize([$t,$m])),'products'=>$products,'blocks'=>$blocks];
}
function assert_protected($a,$b){
 if($a['previous_terms']!==$b['previous_terms']||$a['term']!==$b['term']['protected_hash'])fail_release('Protected category drift');
 if(count($a['products'])!==count($b['products']))fail_release('Catalogue membership drift');
 foreach($b['products'] as $p)if(($a['products'][$p['id']]??'')!==$p['state_hash'])fail_release('Protected product drift');
 if($a['blocks']!==$b['previous_blocks'])fail_release('Existing shared/category block drift');
}
function placement_state(){return ['description'=>get_term(162,'product_cat')->description];}
function assert_placement($expected){if(placement_state()!==$expected)fail_release('Category placement drift');}
function check_usage($id){global $wpdb;
 $description_terms=$wpdb->get_results($wpdb->prepare("SELECT term_id,description FROM {$wpdb->term_taxonomy} WHERE description LIKE %s",'%'.$id.'%'),ARRAY_A);if(count($description_terms)!==1||(int)$description_terms[0]['term_id']!==162||$description_terms[0]['description']!=='[html_block id="15264"]')fail_release('Shared description block');
 $terms=$wpdb->get_results($wpdb->prepare("SELECT term_id,meta_key FROM {$wpdb->termmeta} WHERE meta_value=%s",(string)$id),ARRAY_A);if(count($terms)!==0)fail_release('Shared category meta block');
 foreach($wpdb->get_results($wpdb->prepare("SELECT ID,post_content FROM {$wpdb->posts} WHERE post_status NOT IN ('trash','auto-draft') AND post_type!='revision' AND post_content LIKE %s",'%'.$id.'%'),ARRAY_A) as $row){preg_match_all('/'.get_shortcode_regex(['html_block']).'/s',$row['post_content'],$matches,PREG_SET_ORDER);foreach($matches as $match){$atts=shortcode_parse_atts($match[3]);if(is_array($atts)&&(string)($atts['id']??'')===(string)$id)fail_release('Shared post block');}}
 if((int)$wpdb->get_var($wpdb->prepare("SELECT COUNT(*) FROM {$wpdb->postmeta} WHERE meta_value=%s",(string)$id)))fail_release('Shared post meta block');
}
function text_structure($s){
 $s=preg_replace('/(\[woodmart_title\b[^\]]*?\btitle=")ASIA(")/','$1__TITLE__$2',$s);
 $s=preg_replace('/(\[woodmart_title\b[^\]]*?\btitle=")Asia 3D Model for Renders and Animation(")/','$1__TITLE__$2',$s);
 $s=preg_replace('/(\[woodmart_title\b[^\]]*?\bsubtitle=")[^"]*(")/','$1__SUBTITLE__$2',$s);
 return preg_replace('/(\[woodmart_text_block\b[^\]]*\]).*?(\[\/woodmart_text_block\])/s','$1__COPY__$2',$s);
}
function assert_text_scope($before,$after){
 if(text_structure($before)!==text_structure($after))fail_release('Non-text shortcode/layout drift');
 if(substr_count($after,'[woodmart_text_block ')!==1||substr_count($after,'[woodmart_title ')!==1)fail_release('Unexpected text scope');
 if(strpos($after,'title="Asia 3D Model for Renders and Animation"')===false||strpos($after,'id="asia-category-copy"')===false)fail_release('Missing approved copy');
}
function verify_block($b){$p=get_post($b['block_id']);if(!$p||$p->post_type!=='cms_block'||$p->post_status!=='publish'||$p->post_content!==$b['after'])fail_release('Published block drift');}
function refresh_category($url,$id){clean_post_cache($id);clean_term_cache(162,'product_cat');if(function_exists('rocket_clean_files'))rocket_clean_files([$url]);do_action('litespeed_purge_url',$url);}
function assert_block_base($baseline){$p=get_post(15264);if(!$p||hash('sha256',serialize([$p->post_title,$p->post_name,$p->post_status,$p->post_excerpt,get_post_meta(15264)]))!==$baseline['block']['protected_hash'])fail_release('Protected block metadata drift');}
function write_content($expected,$replacement,$baseline){global $wpdb;$wpdb->query('START TRANSACTION');try{$wpdb->get_var("SELECT ID FROM {$wpdb->posts} WHERE ID=15264 FOR UPDATE");clean_post_cache(15264);assert_block_base($baseline);assert_protected(protected_state(),$baseline);assert_placement(['description'=>$baseline['term']['description']]);check_usage(15264);$changed=$wpdb->query($wpdb->prepare("UPDATE {$wpdb->posts} SET post_content=%s,post_modified=%s,post_modified_gmt=%s WHERE ID=15264 AND post_content=%s",$replacement,current_time('mysql'),current_time('mysql',true),$expected));if($changed!==1)fail_release('Conditional content write');clean_post_cache(15264);assert_block_base($baseline);assert_protected(protected_state(),$baseline);$wpdb->query('COMMIT');}catch(Throwable $e){$wpdb->query('ROLLBACK');clean_post_cache(15264);throw $e;}}
try{
 if(PHP_SAPI!=='cli'||rtrim(home_url(),'/')!=='https://shustrik-maps.com')fail_release('Wrong site');$mode=$argv[1]??'--preview';if(!in_array($mode,['--preview','--apply','--verify','--rollback-preview','--rollback']))fail_release('Mode');
 $m=json_decode(file_get_contents(__DIR__.'/manifest.json'),true,512,JSON_THROW_ON_ERROR);$baseline=json_decode(file_get_contents(__DIR__.'/baseline.json'),true,512,JSON_THROW_ON_ERROR);if($m['term_id']!==162||$m['block_id']!==15264||count($m['assets'])!==0||get_term(162,'product_cat')->slug!=='asia')fail_release('Scope');
 $template=file_get_contents(__DIR__.'/category-shortcodes.txt');if(hash('sha256',$template)!==$m['template_sha256'])fail_release('Template hash');foreach($m['assets'] as $asset)if($asset['mode']!=='new'||hash_file('sha256',__DIR__.'/assets/'.$asset['file'])!==$asset['sha256'])fail_release('Asset scope/hash');
 $backup_key='_shustrik_asia_text_backup_20261012';$journal_key='_shustrik_asia_text_media_20261012';$b=get_option($backup_key,null);assert_protected(protected_state(),$baseline);assert_placement(['description'=>$baseline['term']['description']]);assert_block_base($baseline);check_usage(15264);
 if(in_array($mode,['--verify','--rollback-preview','--rollback'])){if(!$b||$b['status']!=='published')fail_release('Missing published backup');verify_block($b);}
 else{if($b!==null||get_option($journal_key,null)!==null)fail_release('Existing release; inspect before retry');if(get_post(15264)->post_content!==$baseline['block']['content']||hash('sha256',$baseline['block']['content'])!==$m['before_sha256'])fail_release('Original content drift');}
 assert_text_scope($baseline['block']['content'],$template);
 if($mode==='--apply'){
  $b=['utc'=>gmdate('c'),'block_id'=>15264,'before'=>$baseline['block']['content'],'status'=>'prepared'];if(!add_option($backup_key,$b,'',false)||!add_option($journal_key,['ids'=>[],'status'=>'importing'],'',false))fail_release('Backup collision');$ids=[];
  $after=$template;$b=array_merge($b,['after'=>$after,'ids'=>$ids,'status'=>'ready']);update_option($backup_key,$b,false);write_content($b['before'],$after,$baseline);$b['status']='published';$b['published_at']=gmdate('c');update_option($backup_key,$b,false);update_option($journal_key,['ids'=>$ids,'status'=>'published'],false);refresh_category($m['url'],15264);verify_block($b);
 }
 if($mode==='--rollback'){write_content($b['after'],$b['before'],$baseline);$b['status']='rolled-back';update_option($backup_key,$b,false);refresh_category($m['url'],15264);}
 $media=[];if(in_array($mode,['--apply','--verify','--rollback-preview'])){foreach($m['assets'] as $asset){$aid=$b['ids'][$asset['key']];$data=wp_get_attachment_metadata($aid);if(!$data||$data['width']!==$asset['width']||$data['height']!==$asset['height']||hash_file('sha256',get_attached_file($aid))!==$asset['sha256']||get_post_meta($aid,'_wp_attachment_image_alt',true)!==$asset['alt'])fail_release('Media verification');$media[]=['key'=>$asset['key'],'id'=>$aid,'url'=>wp_get_attachment_url($aid),'width'=>$data['width'],'height'=>$data['height']];}}
 assert_protected(protected_state(),$baseline);assert_block_base($baseline);assert_placement(['description'=>$baseline['term']['description']]);echo json_encode(['ok'=>true,'mode'=>$mode,'utc'=>gmdate('c'),'url'=>$m['url'],'term_id'=>162,'block_id'=>15264,'protected_preserved'=>true,'media'=>$media,'content_sha256'=>isset($b['after'])?hash('sha256',$b['after']):null,'rollback_backup'=>$backup_key],JSON_UNESCAPED_SLASHES)."\n";
}catch(Throwable $e){echo json_encode(['ok'=>false,'reason'=>$e instanceof RuntimeException?$e->getMessage():'Internal error'])."\n";exit(1);}
