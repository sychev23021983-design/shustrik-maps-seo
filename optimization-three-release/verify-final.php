<?php
// Exact owner-approved title/meta/intro release; no save filters or download URLs emitted.
ini_set('display_errors','0');
define('WP_USE_THEMES',false);
ob_start();require '/var/www/html/wp-load.php';ob_end_clean();
function stop_release($message){throw new RuntimeException($message);}
function invariant_three($id){
    $p=get_post($id);$hashes=[];
    foreach(['_price','_regular_price','_sale_price','_sku','_stock','_stock_status','_manage_stock','_downloadable','_virtual','_downloadable_files','_download_limit','_download_expiry','_thumbnail_id','_product_image_gallery','_tax_status','_tax_class'] as $k)$hashes[$k]=hash('sha256',serialize(get_post_meta($id,$k,true)));
    $cats=wp_get_post_terms($id,'product_cat',['fields'=>'ids']);if(is_wp_error($cats))stop_release('Category read failed');sort($cats);
    return ['url'=>get_permalink($id),'type'=>$p->post_type,'status'=>$p->post_status,'slug'=>$p->post_name,'h1'=>$p->post_title,'excerpt_sha256'=>hash('sha256',$p->post_excerpt),'commerce_hashes'=>$hashes,'categories'=>$cats,'currency'=>get_woocommerce_currency(),'robots'=>get_post_meta($id,'_yoast_wpseo_meta-robots-noindex',true),'follow'=>get_post_meta($id,'_yoast_wpseo_meta-robots-nofollow',true),'canonical'=>get_post_meta($id,'_yoast_wpseo_canonical',true)];
}
function current_three($id){$p=get_post($id);return ['seo_title'=>get_post_meta($id,'_yoast_wpseo_title',true),'meta_description'=>get_post_meta($id,'_yoast_wpseo_metadesc',true),'content_sha256'=>hash('sha256',$p->post_content)];}
function target_three($r,$body){
    if(substr_count($body,$r['before']['first_paragraph_source'])!==1)stop_release('Intro source not unique');
    return str_replace($r['before']['first_paragraph_source'],$r['after']['first_paragraph_text'],$body);
}
function invalidate_three($id){clean_post_cache($id);wp_cache_delete($id,'post_meta');}
function rebuild_three($id){
    invalidate_three($id);
    if(function_exists('YoastSEO')&&class_exists('Yoast\\WP\\SEO\\Builders\\Indexable_Builder'))YoastSEO()->classes->get('Yoast\\WP\\SEO\\Builders\\Indexable_Builder')->build_for_id_and_type($id,'post');
}
try {if(PHP_SAPI!=='cli'||rtrim(home_url(),'/')!=='https://shustrik-maps.com')stop_release('Site');$m=json_decode(file_get_contents(__DIR__.'/proposals.json'),true,512,JSON_THROW_ON_ERROR);$b=get_option('_shustrik_optimization_three_backup_20261005');if(!is_array($b)||$b['proposals']!==$m)stop_release('Backup');$rows=[];foreach($m['products'] as $r){$id=$r['id'];$expected=$r['after'];if($id===10102){$new=str_replace(['<table>','</table>'],['<div role="region" aria-label="Included C4D and OBJ files" tabindex="0" style="overflow-x:auto;max-width:100%;"><table>','</table></div>'],$r['content_after']);$expected['content_sha256']=hash('sha256',$new);if(get_option('_shustrik_optimization_table_backup_20261005')!==$r['content_after'])stop_release('Table backup');}invalidate_three($id);if(current_three($id)!==$expected||invariant_three($id)!==$r['invariants'])stop_release('Final fields/protected drift');$rows[]=['id'=>$id,'fields_match'=>true,'protected_match'=>true];}echo json_encode(['ok'=>true,'utc'=>gmdate('c'),'rows'=>$rows,'applied_backup_utc'=>$b['utc']])."\n";}catch(Throwable $e){echo json_encode(['ok'=>false,'reason'=>$e instanceof RuntimeException?$e->getMessage():'Internal error'])."\n";exit(1);}