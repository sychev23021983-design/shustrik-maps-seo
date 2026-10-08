<?php
ini_set('display_errors','0');define('WP_USE_THEMES',false);ob_start();require '/var/www/html/wp-load.php';ob_end_clean();
$id=15536;$p=get_post($id);$file=get_attached_file($id);if(!$p||$p->post_type!=='attachment'||!is_file($file))exit(1);
echo json_encode(['retained'=>true,'id'=>$id,'title'=>$p->post_title,'url'=>wp_get_attachment_url($id),'file_sha256'=>hash_file('sha256',$file)],JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE);
