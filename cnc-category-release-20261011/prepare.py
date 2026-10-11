from pathlib import Path
import json,hashlib,re
from PIL import Image
ROOT=Path(__file__).parent
def sha(b): return hashlib.sha256(b).hexdigest()
assets=[]
items=[
 dict(key='print',mode='reuse',url='https://shustrik-maps.com/wp-content/uploads/2022/05/arizona-desk-ivory-plastic-1500x1000-v2.jpg',title='3D-printed terrain map',alt='AI-generated concept of an ivory Arizona terrain relief on a separate wooden desk stand.'),
 dict(key='globe',mode='new',original='modular-earth-original.png',file='cnc-category-modular-earth-20261011.webp',title='Modular Earth globe',alt='AI-generated concept of a spherical Earth relief globe assembled from colored curved sections on a shelf.'),
 dict(key='wood',mode='new',original='arizona-wood-original.png',file='cnc-category-arizona-walnut-20261011.webp',title='CNC-carved wooden map',alt='AI-generated concept of an Arizona terrain relief carved in walnut on a separate wooden wall backing.'),
 dict(key='troll',mode='reuse',url='https://shustrik-maps.com/wp-content/uploads/2025/05/troll-skull-desk-1500x1000-1.jpg',title='3D-printed Troll Face skull',alt='AI-generated concept of the Troll Face skull with its wide grin and stand on a wooden desk.')
]
for m in items:
 if m['mode']=='new':
  with Image.open(ROOT/'assets'/m['original']) as image:
   image.convert('RGB').save(ROOT/'assets'/m['file'],'WEBP',quality=88,method=6)
   m.update(width=image.width,height=image.height)
  m['sha256']=sha((ROOT/'assets'/m['file']).read_bytes())
 m['caption']='AI-generated application concept; not a photograph of a customer project.'
 assets.append(m)
baseline=json.loads((ROOT/'baseline.json').read_text(encoding='utf-8-sig'))
html=(ROOT/'category.html').read_text(encoding='utf-8')
assert len(re.findall(r'<h1\b',html))==1 and html.count('{{IMAGE:')==4
assert 'Decorative CNC relief' not in html and 'troll-face-3d-model/' in html
manifest={'site':'https://shustrik-maps.com','url':'https://shustrik-maps.com/product-category/cnc-models/','term_id':16,'block_id':14417,'before_sha256':baseline['block']['content_sha256'],'template_sha256':sha(html.encode()),'assets':assets,'authorization':'Owner approved the category mockup and explicitly requested replacing the decorative panel with Troll Face and publishing to the site on 2026-10-11.'}
(ROOT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'assets':len(assets),'new_media':2,'reused_media':2,'bytes':sum((ROOT/'assets'/m['file']).stat().st_size for m in assets if m['mode']=='new'),'h1':1}))
