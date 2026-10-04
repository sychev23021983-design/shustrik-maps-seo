<?php
/** Plugin Name: Shustrik responsive product thumbnails */
if (!defined('ABSPATH')) { exit; }
function shu_responsive_product_thumbnail($attr, $attachment, $size) {
    $class = $attr['class'] ?? '';
    $loop = strpos($class, 'attachment-woocommerce_thumbnail') !== false;
    $thumb = strpos($class, 'attachment-189x') !== false || strpos($class, 'attachment-woocommerce_gallery_thumbnail') !== false;
    if (!$loop && !$thumb) { return $attr; }
    if (!empty($attr['fetchpriority']) && $attr['fetchpriority'] === 'high') { return $attr; }
    $target = $loop ? 'woocommerce_thumbnail' : 'woocommerce_gallery_thumbnail';
    $image = wp_get_attachment_image_src($attachment->ID, $target);
    if (!$image) { return $attr; }
    // Keep responsive candidates in the initial HTML, avoiding a JS src/srcset race.
    $attr['src'] = $image[0];
    $attr['width'] = $image[1];
    $attr['height'] = $image[2];
    $srcset = wp_get_attachment_image_srcset($attachment->ID, $target);
    if ($srcset) { $attr['srcset'] = $srcset; }
    else { unset($attr['srcset']); }
    $attr['sizes'] = $loop ? '(max-width: 767px) 50vw, 300px' : '(max-width: 767px) 211px, 189px';
    $attr['loading'] = 'lazy';
    $attr['decoding'] = 'async';
    unset($attr['data-src'], $attr['data-srcset']);
    $attr['class'] = trim(preg_replace('/\b(?:wd-lazy-load|woodmart-lazy-load|wd-lazy-fade|wd-lazy-blur)\b/', '', $class));
    return $attr;
}
add_filter('wp_get_attachment_image_attributes', 'shu_responsive_product_thumbnail', 30, 3);
