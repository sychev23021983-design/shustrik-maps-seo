<?php
// Narrow owner-authorized help text update. CLI only; no orders or settings read.
ini_set('display_errors','0');
ob_start(); require '/var/www/html/wp-load.php'; ob_end_clean();
function stop_release($m) { throw new RuntimeException($m); }
function protected_state($id,$target) {
    $p=get_post($id,ARRAY_A); if(!$p) stop_release('Missing scoped post');
    if($target) unset($p['post_content'],$p['post_modified'],$p['post_modified_gmt']);
    $meta=get_post_meta($id); ksort($meta);
    return ['post'=>hash('sha256',serialize($p)),'meta'=>hash('sha256',serialize($meta))];
}
function replace_copy($content,$row) {
    foreach($row['changes'] as $c) {
        if(isset($c['old'])) {
            if(substr_count($content,$c['old'])!==1) stop_release('Exact fragment guard failed');
            $content=str_replace($c['old'],$c['text'],$content);
        } else {
            if(substr_count($content,$c['start'])!==1) stop_release('Section start guard failed');
            $s=strpos($content,$c['start'])+strlen($c['start']); $e=strpos($content,$c['end'],$s);
            if($e===false) stop_release('Section end missing');
            $content=substr($content,0,$s).$c['text'].substr($content,$e);
        }
    } return $content;
}
try {
    if(PHP_SAPI!=='cli'||rtrim(home_url(),'/')!=='https://shustrik-maps.com') stop_release('CLI/site guard');
    $mode=$argv[1]??'--preview'; if(!in_array($mode,['--snapshot','--preview','--apply','--verify','--rollback'],true)) stop_release('Invalid mode');
    $rows=json_decode(file_get_contents(__DIR__.'/proposals.json'),true,512,JSON_THROW_ON_ERROR);
    if(array_column($rows,'id')!==[10438,651,10018]) stop_release('Scope mismatch');
    $ids=[10438,651,10018,608,11517,19462,15954]; $states=[]; $contents=[];
    foreach($ids as $id) {
        $p=get_post($id); $target=in_array($id,[10438,651,10018],true);
        $states[$id]=['protected'=>protected_state($id,$target),'content'=>hash('sha256',$p->post_content)];
        if($target) $contents[$id]=['before'=>$p->post_content,'modified'=>$p->post_modified,'modified_gmt'=>$p->post_modified_gmt];
    }
    foreach($rows as $r) {
        $p=get_post($r['id']); if($p->post_type!==$r['type']||$p->post_status!=='publish'||($r['slug']!==null&&$p->post_name!==$r['slug'])) stop_release('Identity drift');
    }
    if($mode==='--snapshot') { echo json_encode($states,JSON_PRETTY_PRINT|JSON_UNESCAPED_SLASHES)."\n"; exit; }
    $baseline=json_decode(file_get_contents(__DIR__.'/baseline.json'),true,512,JSON_THROW_ON_ERROR);
    $key='_shustrik_help_copy_backup_20261004'; $backup=get_option($key,null);
    $after=[];
    if(in_array($mode,['--preview','--apply'],true)) {
        if($states!==$baseline) stop_release('Baseline drift; no writes');
        if($backup!==null) stop_release('Backup already exists; no repeat apply');
        foreach($rows as $r) $after[$r['id']]=replace_copy($contents[$r['id']]['before'],$r);
    } else {
        if(!is_array($backup)||$backup['baseline']!==$baseline||$backup['proposals']!==$rows) stop_release('Backup mismatch');
        $contents=$backup['contents']; $after=$backup['after'];
        foreach($ids as $id) {
            if($states[$id]['protected']!==$baseline[$id]['protected']) stop_release('Protected field drift');
            $expected=isset($after[$id])?hash('sha256',$after[$id]):$baseline[$id]['content'];
            if($states[$id]['content']!==$expected) stop_release('Content drift; no writes');
        }
    }
    if($mode==='--preview'||$mode==='--verify') {
        echo json_encode(['mode'=>$mode,'ok'=>true,'targets'=>3,'fragments'=>4,'protected_posts'=>4,'utc'=>gmdate('c')])."\n"; exit;
    }
    if($mode==='--apply'&&!add_option($key,['baseline'=>$baseline,'proposals'=>$rows,'contents'=>$contents,'after'=>$after,'utc'=>gmdate('c')],'',false)) stop_release('Backup save failed');
    global $wpdb;
    $wpdb->query('START TRANSACTION');
    // Lock the scoped posts and recheck content; bypass broad post-save filters.
    foreach($ids as $id) {
        $locked=$wpdb->get_row($wpdb->prepare("SELECT post_content FROM {$wpdb->posts} WHERE ID=%d FOR UPDATE",$id),ARRAY_A);
        if(!$locked||hash('sha256',$locked['post_content'])!==$states[$id]['content']) { $wpdb->query('ROLLBACK'); stop_release('Concurrent content edit'); }
    }
    foreach($rows as $r) {
        $id=$r['id']; $data=$mode==='--apply'?['post_content'=>$after[$id],'post_modified'=>current_time('mysql'),'post_modified_gmt'=>current_time('mysql',true)]:['post_content'=>$contents[$id]['before'],'post_modified'=>$contents[$id]['modified'],'post_modified_gmt'=>$contents[$id]['modified_gmt']];
        if($wpdb->update($wpdb->posts,$data,['ID'=>$id],['%s','%s','%s'],['%d'])===false) { $wpdb->query('ROLLBACK'); stop_release('Write failed; transaction rolled back'); }
    }
    // Read raw rows before commit so content mismatch remains reversible.
    foreach($rows as $r) {
        $actual=$wpdb->get_var($wpdb->prepare("SELECT post_content FROM {$wpdb->posts} WHERE ID=%d",$r['id']));
        $expected=$mode==='--apply'?$after[$r['id']]:$contents[$r['id']]['before'];
        if($actual!==$expected) { $wpdb->query('ROLLBACK'); stop_release('Exact write mismatch'); }
    }
    $wpdb->query('COMMIT'); foreach($rows as $r) clean_post_cache($r['id']);
    foreach($ids as $id) if(protected_state($id,in_array($id,[10438,651,10018],true))!==$baseline[$id]['protected']) stop_release('Post-commit protected drift; inspect before rollback');
    echo json_encode(['mode'=>$mode,'ok'=>true,'targets'=>3,'fragments'=>4,'protected_posts'=>4,'backup_retained'=>true,'utc'=>gmdate('c')])."\n";
} catch(Throwable $e) { fwrite(STDERR,'RELEASE_REFUSED: '.$e->getMessage()."\n"); exit(1); }
