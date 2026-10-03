<?php
error_reporting(0);
ob_start(); require '/var/www/html/wp-load.php'; ob_end_clean();
$key='_shustrik_two_junk_backup_20261003';
$opt='click5_sitemap_seo_blacklisted_array';
$slugs=['prepayment-for-kyrgyzstan-model','prepayment-for-authagraph-map'];
$mode=in_array('--rollback',$argv,true)?'rollback':(in_array('--apply',$argv,true)?'apply':'preview');
$posts=[];
foreach($slugs as $slug){$p=get_page_by_path($slug,OBJECT,'product');if(!$p||$p->post_status!=='publish')throw new Exception('Expected public product missing');$posts[]=$p;}
$old=get_option($opt);$blacklist=is_string($old)?json_decode($old,true):$old;
if(!is_array($blacklist))throw new Exception('Unexpected blacklist shape');
if($mode==='preview'){echo json_encode(['mode'=>$mode,'urls'=>array_map(fn($p)=>get_permalink($p),$posts),'blacklist_count'=>count($blacklist)]);exit;}
$backup=get_option($key);
if($mode==='rollback'){
 if(!is_array($backup)||hash('sha256',serialize(get_option($opt)))!==$backup['installed_blacklist_hash'])throw new Exception('Rollback drift or backup guard failed');
 foreach($backup['fields'] as $f){if(get_post_meta($f['id'],'_yoast_wpseo_meta-robots-noindex',true)!=='1')throw new Exception('Metadata drift');}
 foreach($backup['fields'] as $f){if($f['exists'])update_post_meta($f['id'],'_yoast_wpseo_meta-robots-noindex',$f['value']);else delete_post_meta($f['id'],'_yoast_wpseo_meta-robots-noindex');}
 update_option($opt,$backup['blacklist']);
}else{
 if($backup)throw new Exception('Backup already exists; refusing repeat apply');
 $backup=['utc'=>gmdate('c'),'blacklist'=>$old,'fields'=>[]];
 foreach($posts as $p){$backup['fields'][]=['id'=>$p->ID,'exists'=>metadata_exists('post',$p->ID,'_yoast_wpseo_meta-robots-noindex'),'value'=>get_post_meta($p->ID,'_yoast_wpseo_meta-robots-noindex',true)];}
 $ids=array_map(fn($r)=>(string)$r['ID'],$blacklist);
 foreach($posts as $p){if(!in_array((string)$p->ID,$ids,true))$blacklist[]=['ID'=>(int)$p->ID];}
 $new=wp_json_encode($blacklist);$backup['installed_blacklist_hash']=hash('sha256',serialize($new));
 if(!add_option($key,$backup,'',false))throw new Exception('Backup write failed');
 foreach($posts as $p){update_post_meta($p->ID,'_yoast_wpseo_meta-robots-noindex','1');}
 update_option($opt,$new);
}
if(!function_exists('click5_sitemap_generate_sitemap_XML_DoWork'))throw new Exception('Sitemap generator unavailable');
ob_start();$result=click5_sitemap_generate_sitemap_XML_DoWork();ob_end_clean();
echo json_encode(['mode'=>$mode,'utc'=>gmdate('c'),'products'=>count($posts),'sitemap_regenerated'=>true,'generator_result'=>$result]);
