<?php
ini_set('display_errors','0');define('WP_USE_THEMES',false);ob_start();require '/var/www/html/wp-load.php';ob_end_clean();
$rows=[];foreach([16696,16728] as $id){$key='_shustrik_next_lunar_stl_slider_backup_20261008_'.$id;$j='_shustrik_next_lunar_stl_slider_media_20261008_'.$id;$b=get_option($key,null);$journal=get_option($j,null);if(!$b||!$journal||$journal['status']!=='published')exit(1);$rows[]=['id'=>$id,'backup_key'=>$key,'journal_key'=>$j,'backup'=>$b,'journal'=>$journal];}echo json_encode(['utc'=>gmdate('c'),'rows'=>$rows],JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);
