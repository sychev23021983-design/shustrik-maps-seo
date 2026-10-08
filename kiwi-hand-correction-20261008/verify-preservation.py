from pathlib import Path
import json,re,subprocess
root=Path('J:/1. My Vault/01 Projects/WordPress/shustrik-maps.com/Kiwi Hand Correction 2026-10-08')
def remote(s):return subprocess.check_output(['ssh','vpsadmin@10.66.66.1',s],text=True,encoding='utf-8')
d=json.loads((root/'deployment.json').read_text());p=d['wp_source']+'/release.php'
for mode,name in [('snapshot','after.json'),('backup-export','backup-export.json')]:
 (root/name).write_text(remote('sudo -n docker exec shustrik-maps-wordpress-1 php '+p+' --'+mode),encoding='utf-8')
b=json.loads((root/'baseline.json').read_text());a=json.loads((root/'after.json').read_text());saved=json.loads((root/'backup-export.json').read_text());v=json.loads((root/'verify.json').read_text())
assert saved['ok'] and saved['backup']['before']==b['state'] and saved['journal']['status']=='published'
new=v['rows'][0]['media'][0]['id']; assert new==saved['backup']['media_id'] and saved['journal']['ids']==[new]
assert a['state']['content']==b['state']['content'].replace('images="22766,22767,22768,22769"','images="'+str(new)+',22767,22768,22769"')
assert all(a['state'][k]==b['state'][k] for k in b['state'] if k!='content')
for old in b['old_media']: assert any(x==old for x in saved['backup']['old_media'])
assert a['old_media'][1:]==b['old_media'][1:]
for tag in ['woodmart_text_block','vc_column_text']:
 assert re.findall(r'\['+tag+r'[^\]]*\](.*?)\[/'+tag+r'\]',a['state']['content'],re.S)==re.findall(r'\['+tag+r'[^\]]*\](.*?)\[/'+tag+r'\]',b['state']['content'],re.S)
rt=remote("sudo -n docker inspect --format '{{.Name}} {{.State.Status}} {{.RestartCount}} {{.State.StartedAt}} {{json .HostConfig.PortBindings}}' shustrik-maps-wordpress-1 shustrik-maps-db-1")
(root/'runtime-after.txt').write_text(rt,encoding='utf-8');assert rt==(root/'runtime-before.txt').read_text(encoding='utf-8')
out={'pass':True,'product_id':21381,'new_media_id':new,'old_media_id_retained':22766,'only_one_gallery_id_replaced':True,'all_product_metadata_exact':True,'seo_exact':True,'original_text_exact':True,'h1_url_excerpt_gallery_exact':True,'other_four_product_hashes_exact':True,'other_three_slide_media_exact':True,'old_four_media_unchanged_verified_by_release':True,'backup_matches':True,'runtime_unchanged':True}
(root/'preservation-qa.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
s=(root.parent/'Kiwi Nautilus Use Cases Revision 2026-10-08'/'public-qa.py').read_text(encoding='utf-8')
s=s.split('# Persist normalized media')[0].replace('kiwi_nautilus_usecases_qa','kiwi_hand_fix_qa')
(root/'public-qa.py').write_text(s,encoding='utf-8')
print(json.dumps(out))
