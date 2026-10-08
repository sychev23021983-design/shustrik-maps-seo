from pathlib import Path
import json,re,hashlib
from PIL import Image
root=Path(__file__).parent;out=Path('J:/1. My Vault/90 Migration/shustrik-maps-seo/five-country-stl-slider-release-20261008')
m=json.loads((out/'manifest.json').read_text(encoding='utf-8'));b=json.loads((out/'baseline.json').read_text(encoding='utf-8'))
assert [r['id'] for r in m['rows']]==[19867,19875,19883,19891,19908]
for x,y in zip(m['rows'],b['rows']):
 assert x['id']==y['id']
 old=re.findall(r'\[vc_column_text[^\]]*\](.*?)\[/vc_column_text\]',y['content'],re.S)
 new=[t for t in re.findall(r'\[vc_column_text[^\]]*\](.*?)\[/vc_column_text\]',x['description'],re.S) if 'AI-generated application concepts.' not in t]
 assert old==new and x['h1_preserved']==y['title'] and x['url']==y['url']
 assert 'carousel_arrows_position="together"' in x['description'] and x['description'].count('[woodmart_gallery')==1
 assert 35<=len(x['seo_title'])<=65 and 130<=len(x['meta_description'])<=165
media=json.loads((out/'media.json').read_text(encoding='utf-8'));assert len(media)==20
for a in media:
 with Image.open(out/a['file']) as im:assert im.format=='JPEG' and im.size==(1500,1000)
 assert 'AI-generated' in a['title'] and 'AI-generated' in a['alt']
 assert a['sha256']==hashlib.sha256((out/a['file']).read_bytes()).hexdigest()
for p in out.iterdir():
 if p.suffix in ['.json','.md','.py','.php','.txt']:
  s=p.read_text(encoding='utf-8-sig');p.write_text('\n'.join(l.rstrip() for l in s.splitlines()).rstrip()+'\n',encoding='utf-8',newline='\n')
for n in ['deliver.py','export.py','public-qa.py','verify-preservation.py','package-next.py']:compile((root/n).read_text(encoding='utf-8'),n,'exec')
print('Preflight:5 exact manifests, preserved prose/H1/URL,20 true JPEGs, title/alt/hashes and helper syntax passed')
