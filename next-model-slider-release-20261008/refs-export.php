<?php
ini_set("display_errors","0");define("WP_USE_THEMES",false);ob_start();require "/var/www/html/wp-load.php";ob_end_clean();
foreach(["sheikh-zayed"=> [15530, 15531], "troll-skull"=> [20193, 20194], "zombie-box"=> [20206, 20205]] as $slug=>$ids){foreach($ids as $i=>$aid){if(!copy(get_attached_file($aid),"/tmp/".$slug."-source-".($i+1).".jpg"))exit(1);}}
