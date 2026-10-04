<?php
ini_set('display_errors','0');
ob_start(); require '/var/www/html/wp-load.php'; ob_end_clean();
if(PHP_SAPI!=='cli'||rtrim(home_url(),'/')!=='https://shustrik-maps.com') exit(1);
$out=['site'=>home_url(),'menus'=>[],'categories'=>[],'products'=>[]];
foreach(wp_get_nav_menus() as $menu) {
    $data=[];
    // Raw rows and post metadata, not the plugin-filtered navigation view.
    $ids=get_objects_in_term($menu->term_id,'nav_menu'); sort($ids);
    foreach($ids as $id) { $meta=get_post_meta($id);ksort($meta);$data[$id]=hash('sha256',serialize([get_post($id,ARRAY_A),$meta])); }
    $out['menus'][$menu->term_id]=hash('sha256',serialize($data));
}
foreach([26,84,206] as $id) {
    $meta=get_term_meta($id); ksort($meta);
    $out['categories'][$id]=hash('sha256',serialize([get_term($id,'product_cat',ARRAY_A),$meta]));
}
foreach([11517,19462,15954] as $id) { $meta=get_post_meta($id);ksort($meta); $out['products'][$id]=hash('sha256',serialize([get_post($id,ARRAY_A),$meta])); }
$out['archive_template_hash']=hash_file('sha256',get_template_directory().'/woocommerce/archive-product.php');
$mode=$argv[1]??'--snapshot';
if($mode==='--snapshot') echo json_encode($out,JSON_PRETTY_PRINT|JSON_UNESCAPED_SLASHES)."\n";
elseif($mode==='--verify') {
    $baseline=json_decode(file_get_contents(__DIR__.'/baseline.json'),true);
    if($out!==$baseline) { fwrite(STDERR,"Protected data drift; inspect\n");exit(1); }
    echo json_encode(['ok'=>true,'menus_preserved'=>count($out['menus']),'categories_preserved'=>3,'products_preserved'=>3,'template_preserved'=>true,'utc'=>gmdate('c')])."\n";
} else exit(1);
