from pathlib import Path
import subprocess,json,hashlib,difflib
root=Path(__file__).parent
r=subprocess.run(['ssh','vpsadmin@10.66.66.1','sudo -n docker exec shustrik-maps-wordpress-1 php /tmp/next-lunar-snapshot.php'],capture_output=True,text=True,encoding='utf-8');assert r.returncode==0,r.stderr
current=json.loads(r.stdout);(root/'preapply-drift-snapshot.json').write_text(json.dumps(current,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');base=json.loads((root/'baseline.json').read_text(encoding='utf-8-sig'));manifest=json.loads((root/'manifest.json').read_text(encoding='utf-8-sig'))
for b,c,t in zip(base['rows'],current['rows'],manifest['rows']):
 for k in ['content','excerpt','seo_title','meta_description','protected','gallery','title','url']:
  if b[k]!=c[k]:print('Changed',b['id'],k,str(b[k])[:100],str(c[k])[:100])
 print(b['id'],'hashes',hashlib.sha256(c['excerpt'].encode()).hexdigest(),t['before_excerpt_sha256'],'SEO',c['seo_title']==t['before_seo_title'],c['meta_description']==t['before_meta_description'])
 print('Excerpt repr trailing',repr(c['excerpt'][-50:]),repr(b['excerpt'][-50:]))
