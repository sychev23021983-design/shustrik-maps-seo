<?php
require __DIR__.'/common.php';
try {
 $mode=$argv[1]??'--preview';if(!in_array($mode,['--preview','--apply','--verify','--rollback-preview','--rollback'],true))throw new RuntimeException('Wrong mode');
 $path='/var/www/html/.htaccess';$backup='/tmp/shustrik-satellite-variants-htaccess-backup-20261018';$before=file_get_contents(__DIR__.'/htaccess-before.txt');$after=file_get_contents(__DIR__.'/htaccess-after.txt');$expected=$before;
 foreach(['australia','georgia','spain'] as $slug){$line='Redirect 301 /product/'.$slug.'-satellite-map-2/ https://shustrik-maps.com/product/'.$slug.'-satellite-map/'."\n";if(substr_count($expected,$line)!==1)throw new RuntimeException('Rule multiplicity');$expected=str_replace($line,'',$expected);}
 if($expected!==$after||!str_contains($after,'Redirect 301 /product/greece-3d-model-terrain-2/'))throw new RuntimeException('Diff beyond three rules');
 $oldstate=in_array($mode,['--preview','--apply'],true);$current=file_get_contents($path);if($current!==($oldstate?$before:$after))throw new RuntimeException('Routing file drift');
 if(in_array($mode,['--apply','--rollback'],true)){
  $rollback=$mode==='--rollback';if(!$rollback){$handle=fopen($backup,'x');if(!$handle)throw new RuntimeException('Backup exists');if(fwrite($handle,$before)!==strlen($before))throw new RuntimeException('Backup write failed');fclose($handle);chmod($backup,0600);}else if(!is_file($backup)||file_get_contents($backup)!==$before)throw new RuntimeException('Backup mismatch');
  $replacement=$rollback?$before:$after;$temp=$path.'.shustrik-variants-20261018.tmp';$handle=fopen($temp,'x');if(!$handle)throw new RuntimeException('Temporary file exists');if(fwrite($handle,$replacement)!==strlen($replacement))throw new RuntimeException('Temporary file write failed');fclose($handle);chmod($temp,fileperms($path)&0777);chown($temp,fileowner($path));chgrp($temp,filegroup($path));
  if(file_get_contents($path)!==($rollback?$after:$before))throw new RuntimeException('Routing concurrent drift');if(!rename($temp,$path))throw new RuntimeException('Atomic replacement failed');if(file_get_contents($path)!==$replacement)throw new RuntimeException('Readback mismatch');
 }
 echo json_encode(['ok'=>true,'mode'=>$mode,'utc'=>gmdate('c'),'file'=>$path,'sha256'=>hash_file('sha256',$path),'rules_removed'=>3,'greece_rule_preserved'=>true,'wordpress_block_preserved'=>true,'backup'=>$backup,'restart'=>false])."\n";
}catch(Throwable $error){echo json_encode(['ok'=>false,'reason'=>$error instanceof RuntimeException?$error->getMessage():'Internal failure'])."\n";exit(1);}
