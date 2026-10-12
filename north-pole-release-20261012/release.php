<?php
ini_set('display_errors','0');define('WP_USE_THEMES',false);ob_start();require '/var/www/html/wp-load.php';ob_end_clean();
function fail_release($s){throw new RuntimeException($s);}
function protected_state(){
 $t=get_term(67,'product_cat');$m=get_term_meta(67);foreach(['wd_page_css_files','xts-term-67-status','product_count_product_cat','category_extra_description_text'] as $k)unset($m[$k]);
 $products=[];foreach(get_posts(['post_type'=>'product','post_status'=>'publish','numberposts'=>-1,'tax_query'=>[['taxonomy'=>'product_cat','field'=>'term_id','terms'=>[67],'include_children'=>true]]]) as $p){$pm=get_post_meta($p->ID);unset($pm['wd_page_css_files']);$products[$p->ID]=hash('sha256',serialize([$p,$pm]));}
 $blocks=[];foreach([14416,14417,21177,21176,21175,21178,21162,22817,22822,22827,22832,16359,17235,18122,22853,22858,15975] as $id)$blocks[$id]=hash('sha256',serialize([get_post($id),get_post_meta($id)]));
 return ['term'=>hash('sha256',serialize([$t,$m])),'products'=>$products,'blocks'=>$blocks,'inventory_counts'=>['attachments'=>(array)wp_count_posts('attachment'),'blocks'=>(array)wp_count_posts('cms_block')]];
}
function assert_protected($a,$b){
 if($a['term']!==$b['term']['protected_hash']||$a['blocks']!==$b['previous_blocks']||$a['inventory_counts']!==$b['inventory_counts'])fail_release('Protected term/block/inventory drift');
 if(count($a['products'])!==count($b['products']))fail_release('Catalogue drift');foreach($b['products'] as $p)if(($a['products'][$p['id']]??'')!==$p['state_hash'])fail_release('Product drift');
}
function text_state(){return get_term_meta(67,'category_extra_description_text',true);}
function write_text($before,$after,$baseline){global $wpdb;$wpdb->query('START TRANSACTION');try{
 $wpdb->get_var($wpdb->prepare("SELECT term_id FROM {$wpdb->terms} WHERE term_id=%d FOR UPDATE",67));$wpdb->get_results($wpdb->prepare("SELECT meta_id FROM {$wpdb->termmeta} WHERE term_id=%d FOR UPDATE",67));wp_cache_delete(67,'term_meta');assert_protected(protected_state(),$baseline);if(text_state()!==$before)fail_release('Concurrent text edit');
 $changed=$wpdb->query($wpdb->prepare("UPDATE {$wpdb->termmeta} SET meta_value=%s WHERE term_id=%d AND meta_key=%s AND meta_value=%s",$after,67,'category_extra_description_text',$before));if($changed!==1)fail_release('Conditional text write');wp_cache_delete(67,'term_meta');if(text_state()!==$after)fail_release('Text verification');assert_protected(protected_state(),$baseline);$wpdb->query('COMMIT');
 }catch(Throwable $e){$wpdb->query('ROLLBACK');wp_cache_delete(67,'term_meta');throw $e;}}
function refresh_category($url){clean_term_cache(67,'product_cat');if(function_exists('rocket_clean_files'))rocket_clean_files([$url]);do_action('litespeed_purge_url',$url);}
try{
 if(PHP_SAPI!=='cli'||rtrim(home_url(),'/')!=='https://shustrik-maps.com')fail_release('Wrong site');$mode=$argv[1]??'--preview';if(!in_array($mode,['--preview','--apply','--verify','--rollback-preview','--rollback']))fail_release('Mode');
 $m=json_decode(file_get_contents(__DIR__.'/manifest.json'),true,512,JSON_THROW_ON_ERROR);$baseline=json_decode(file_get_contents(__DIR__.'/baseline.json'),true,512,JSON_THROW_ON_ERROR);$after=file_get_contents(__DIR__.'/category.html');
 if($m['term_id']!==67||$m['assets']!==[]||$m['block_id']!==null||get_term(67,'product_cat')->slug!=='north-pole'||get_term_meta(67,'category_extra_description_type',true)!=='text'||get_term_meta(67,'category_extra_description_html_block',true)!==''||hash('sha256',$after)!==$m['template_sha256'])fail_release('Text-only scope');
 $before=$baseline['term']['meta']['category_extra_description_text'][0]??null;if($before!=='')fail_release('Expected empty bottom text');assert_protected(protected_state(),$baseline);
 $key='_shustrik_north_pole_text_backup_20261012';$b=get_option($key,null);
 if(in_array($mode,['--verify','--rollback-preview','--rollback'])){if(!$b||$b['status']!=='published'||$b['after']!==$after||text_state()!==$after)fail_release('Published text drift');}
 else{if($b!==null||text_state()!==$before)fail_release('Existing release or text drift');}
 if($mode==='--apply'){
  $b=['utc'=>gmdate('c'),'before'=>$before,'after'=>$after,'status'=>'prepared'];if(!add_option($key,$b,'',false))fail_release('Backup collision');write_text($before,$after,$baseline);$b['status']='published';$b['published_at']=gmdate('c');update_option($key,$b,false);refresh_category($m['url']);
 }
 if($mode==='--rollback'){write_text($b['after'],$b['before'],$baseline);$b['status']='rolled-back';update_option($key,$b,false);refresh_category($m['url']);}
 assert_protected(protected_state(),$baseline);echo json_encode(['ok'=>true,'mode'=>$mode,'utc'=>gmdate('c'),'url'=>$m['url'],'term_id'=>67,'block_id'=>null,'protected_preserved'=>true,'inventory_counts_preserved'=>true,'media'=>[],'content_sha256'=>hash('sha256',text_state()),'rollback_backup'=>$key],JSON_UNESCAPED_SLASHES)."\n";
}catch(Throwable $e){echo json_encode(['ok'=>false,'reason'=>$e instanceof RuntimeException?$e->getMessage():'Internal error'])."\n";exit(1);}
