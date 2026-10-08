import json,re,subprocess
from pathlib import Path
root=Path(__file__).parent;repo=Path('J:/1. My Vault/90 Migration/shustrik-maps-seo');host='vpsadmin@10.66.66.1'
def read(n):
 s=(root/n).read_text(encoding='utf-8-sig')
 try:return json.loads(s)
 except json.JSONDecodeError:return json.loads(next(x for x in s.splitlines() if x.startswith('{')))
def run(args):
 r=subprocess.run(args,capture_output=True,text=True,encoding='utf-8',errors='replace');assert r.returncode==0,r.stderr;return r.stdout
run(['scp',str(root/'backup-export.php'),host+':/tmp/five-mixed-backup-export.php'])
run(['ssh',host,'sudo -n docker cp /tmp/five-mixed-backup-export.php shustrik-maps-wordpress-1:/tmp/five-mixed-backup-export.php'])
out=run(['ssh',host,'sudo -n docker exec shustrik-maps-wordpress-1 php /tmp/five-mixed-backup-export.php'])
(root/'backup-export.json').write_text(out,encoding='utf-8')
after=run(['ssh',host,'sudo -n docker exec shustrik-maps-wordpress-1 php /tmp/five-mixed-snapshot.php'])
(root/'after.json').write_text(after,encoding='utf-8')
base=read('baseline.json');after=read('after.json');backups=read('backup-export.json');v=read('verify.json');m=read('manifest.json');rows=[]
for b,a,backup,verified,t in zip(base['rows'],after['rows'],backups['rows'],v['rows'],m['rows']):
 assert b['id']==a['id']==backup['id']==verified['id']==t['id']
 assert all(b[k]==a[k] for k in ['slug','url','title','excerpt','gallery','protected','images'])
 expected=t['description'].replace('{{IMAGE_IDS}}',','.join(str(x['id']) for x in verified['media']))
 assert a['content']==expected and a['seo_title']==t['seo_title'] and a['meta_description']==t['meta_description']
 saved=backup['backup']['before']
 assert all(saved[k]==b[k] for k in ['content','excerpt','url','gallery','seo_title','meta_description']) and saved['h1']==b['title']
 assert backup['journal']['status']=='published' and backup['journal']['ids']==backup['backup']['media_ids']
 rows.append({'id':a['id'],'source_prose_and_protected':True,'old_media_preserved':len(b['images']),'backup_matches_baseline':True})
rt=run(['ssh',host,"sudo -n docker inspect --format '{{.Name}} {{.State.Status}} {{.RestartCount}} {{.State.StartedAt}} {{json .HostConfig.PortBindings}}' shustrik-maps-wordpress-1 shustrik-maps-db-1"])
(root/'runtime-after.txt').write_text(rt,encoding='utf-8');assert rt==(root/'runtime-before.txt').read_text(encoding='utf-8')
(root/'preservation-qa.json').write_text(json.dumps({'pass':True,'rows':rows,'runtime_unchanged':True},indent=2),encoding='utf-8')
print('Protected fields, original prose, original galleries, backups and runtime passed5/5')
