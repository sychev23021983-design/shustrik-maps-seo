<?php
/** Plugin Name: Shustrik Maps - scoped catalog navigation */
defined('ABSPATH') || exit;

function shustrik_catalog_term_empty($term_id) {
    static $empty=[];
    if(!array_key_exists($term_id,$empty)) {
        $term=get_term($term_id,'product_cat');
        // Missing taxonomy data must leave the menu intact.
        if(!$term || is_wp_error($term)) return false;
        $ids=get_posts(['post_type'=>'product','post_status'=>'publish','numberposts'=>1,'fields'=>'ids','no_found_rows'=>true,
            'tax_query'=>[['taxonomy'=>'product_cat','field'=>'term_id','terms'=>[$term_id],'include_children'=>true]]]);
        $empty[$term_id]=empty($ids);
    }
    return $empty[$term_id];
}

function shustrik_catalog_filter_menu($items) {
    $targets=['https://shustrik-maps.com/product-category/fantasy-maps'=>84,
        'https://shustrik-maps.com/product-category/3d-renders/elevation-maps'=>206];
    return array_values(array_filter($items,static function($item) use($targets) {
        $url=rtrim($item->url,'/');
        return !isset($targets[$url]) || !shustrik_catalog_term_empty($targets[$url]);
    }));
}
add_filter('wp_nav_menu_objects','shustrik_catalog_filter_menu',20);

function shustrik_catalog_models_heading() {
    static $rendered=false;
    if($rendered || !function_exists('is_product_category') || !is_product_category('3d-models')) return;
    $rendered=true;
    echo '<h1 class="shustrik-catalog-heading">3D Models</h1>';
}
// Woodmart places this hook before the catalog toolbar and product grid.
add_action('woodmart_before_shop_page','shustrik_catalog_models_heading',5);
