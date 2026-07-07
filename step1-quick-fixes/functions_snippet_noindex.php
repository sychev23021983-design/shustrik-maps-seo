<?php
// Вставить в functions.php активной темы (или в code snippets плагин)
// Добавляет noindex,follow для списка служебных страниц (Prepayment/test) —
// это единственный надёжный способ убрать их из индекса Google.
// Если используете Yoast/RankMath — вместо этого проще прописать noindex
// через мета-поле SEO в каждой карточке или массово через их API/CLI.

function shustrik_noindex_junk_pages() {
    $junk_slugs = array(
        'florida-state-rendering-fee',
        'test',
        'prepayment-earth-regular-dodecaedron',
        'prepayment-for-3d-model-5',
        'prepayment-for-3d-model-4',
        'prepayment-for-3d-model-nc',
        'prepayment-for-3d-model',
        'prepayment-for-3d-model-2',
        'prepayment-for-3d-model-california',
        'prepayment-for-3d-model-ermoupolis',
        'prepayment-for-3d-model-globe',
        'prepayment-for-3d-model-hands',
        'prepayment-for-3d-model-isla-nublar-from-jurassic-park',
        'prepayment-for-3d-model-russia',
        'prepayment-for-3d-model-3',
        'prepayment-for-3d-model-buildings',
        'prepayment-for-3d-model-gaza',
        'prepayment-for-3d-model-moon',
        'prepayment-for-3d-model-table',
        'prepayment-for-3d-model-turkey-site',
        'prepayment-for-3d-modelvector',
        'prepayment-for-3d-models-3',
        'prepayment-for-3d-models-2',
        'prepayment-for-3d-models-gores12',
        'prepayment-for-3d-models-ukraine',
        'prepayment-for-3d-models_',
        'prepayment-for-3d-model-mexico',
        'prepayment-for-3d-models',
        'prepayment-for-add',
        'prepayment-for-earth-full-color-model',
        'prepayment-for-map',
        'prepayment-for-map3',
        'prepayment-for-python-script',
        'prepayment-for-render-2',
        'prepayment-for-renders-2',
        'prepayment-for-satellite-maps',
        'prepayment-for-renders',
        'prepayment-for-render',
        'prepayment-for-satellite-map',
    );
    if ( is_singular("product") && in_array( get_post_field("post_name"), $junk_slugs ) ) {
        echo '<meta name="robots" content="noindex,nofollow" />' . "\n";
    }
}
add_action( "wp_head", "shustrik_noindex_junk_pages", 1 );
