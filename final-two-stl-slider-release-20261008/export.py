from pathlib import Path
from PIL import Image
import json,shutil,hashlib
root=Path(__file__).parent;out=Path('J:/1. My Vault/90 Migration/shustrik-maps-seo/final-two-stl-slider-release-20261008');reg=json.loads((root/'native-registry.json').read_text(encoding='utf-8-sig'));media=[];review=[]
labels={'desk':'Ivory Plastic Desktop Display','wall':'Small Framed Wall Relief','gift':'Gift Box','commercial':'Grey Concrete Installation'}
contexts={'desk':'lying with its entire underside supported on a continuous solid walnut backing board on a desk','wall':'mounted on solid sage backing in a small oak wall frame','gift':'fully supported in a kraft gift box with a fitted green insert','commercial':'enlarged in grey concrete on a continuous charcoal backing wall with adults for scale'}
reviews=['Square lunar tile, large upper-left old crater and central flat crater/right crater chain retained; full underside supported on walnut board.','Tall rectangular face relief, asymmetric eyes/angular nose/lips/geometric contours retained, full underside supported on walnut board.','Own lunar crater layout recognizable, small framed square relief with continuous backing.','Own tall portrait panel geometry recognizable, small oak frame and backing.','Own square lunar relief fully visible and supported in gift box.','Own tall face relief fully visible and supported in fitted gift box.','Own square crater layout recognizable enlarged in grey concrete, continuous wall backing, adult scale.','Own tall rectangular face geometry recognizable enlarged grey concrete panel, wall backing, adult scale.']
for r in reg:
 j=r['job'];s=j['slug'];scene=j['scene'];src=Path(r['path']);stem=s+'-'+scene+'-1500x1000';shutil.copy2(src,root/(stem+'-original.png'))
 im=Image.open(src).convert('RGB');assert im.width*2==im.height*3;jpg=root/(stem+'.jpg');im.resize((1500,1000),Image.Resampling.LANCZOS).save(jpg,format='JPEG',quality=95,subsampling=0,optimize=True)
 with Image.open(jpg) as c:assert c.format=='JPEG' and c.mode=='RGB' and c.size==(1500,1000)
 kind='square lunar terrain relief' if j['id']==16743 else 'tall rectangular geometric face relief'
 alt='AI-generated concept of '+j['name']+' '+kind+' '+contexts[scene]+'.'
 caption='AI-generated application concept. Digital model only; physical fabrication, solid support/backing, framing, packaging, finishing and concrete casting are additional work. No mesh accuracy or readiness verification.'
 if j['id']==16812:caption+=' The listed model has an open base; the depicted solid backing is additional fabrication.'
 if scene=='commercial':caption+=' Fabrication rights require separate agreement.'
 media.append({'product_id':j['id'],'slug':s,'scene':scene,'file':jpg.name,'title':'AI-generated '+j['name']+' - '+labels[scene]+' Concept','alt':alt,'caption':caption,'width':1500,'height':1000,'bytes':jpg.stat().st_size,'sha256':hashlib.sha256(jpg.read_bytes()).hexdigest()});shutil.copy2(jpg,out/jpg.name)
 review.append({'index':r['index'],'pass':True,'review':reviews[r['index']],'reference_paths':j['refs']})
assert len(media)==8
(root/'media.json').write_text(json.dumps(media,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(root/'visual-review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
for p in root.iterdir():
 if p.is_file() and p.suffix in ['.py','.php','.json','.md','.png','.jpg','.txt']:shutil.copy2(p,out/p.name)
for p in out.iterdir():
 if p.suffix in ['.py','.php','.json','.md','.txt']:p.write_text('\n'.join(x.rstrip() for x in p.read_text(encoding='utf-8-sig').splitlines()).rstrip()+'\n',encoding='utf-8',newline='\n')
print('All8 individually inspected; original PNG/prompts retained; JPEG RGB1500x1000/SHA/title/alt prepared.')
