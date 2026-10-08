<?php
ini_set("display_errors","0");define("WP_USE_THEMES",false);ob_start();require "/var/www/html/wp-load.php";ob_end_clean();
foreach(["copernicus-crater"=> [16697, 16699], "theophilus-crater"=> [16740, 16738]] as $slug=>$ids){foreach($ids as $i=>$aid){if(!copy(get_attached_file($aid),"/tmp/".$slug."-source-".($i+1).".jpg"))exit(1);}}
