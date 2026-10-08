<?php
ini_set("display_errors","0");define("WP_USE_THEMES",false);ob_start();require "/var/www/html/wp-load.php";ob_end_clean();
foreach(["moon-surface"=> [16754, 16752], "female-face"=> [16814, 16819]] as $slug=>$ids){foreach($ids as $i=>$aid){if(!copy(get_attached_file($aid),"/tmp/".$slug."-source-".($i+1).".jpg"))exit(1);}}
