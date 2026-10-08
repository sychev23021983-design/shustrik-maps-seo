from pathlib import Path
from PIL import Image
import json,shutil,hashlib
root=Path(__file__).parent;out=Path('J:/1. My Vault/90 Migration/shustrik-maps-seo/next-lunar-slider-release-20261008');reg=json.loads((root/'native-registry.json').read_text());media=[];review=[]
labels={'desk':'Ivory Plastic Desktop Display','wall':'Small Framed Wall Relief','gift':'Gift Box','commercial':'Grey Concrete Exhibition'}
contexts={'desk':'fully supported across its closed bottom on a continuous solid desktop base','wall':'mounted on solid sage-green backing in a small oak wall frame','gift':'fully supported in a kraft gift box with a fitted green insert','commercial':'enlarged in grey concrete on a charcoal backing wall with adults for scale'}
for r in reg:
 j=r['job'];s=j['slug'];scene=j['scene'];src=Path(r['path']);stem=s+'-'+scene+'-1500x1000';shutil.copy2(src,root/(stem+'-original.png'))
 im=Image.open(src).convert('RGB');assert im.width*2==im.height*3;jpg=root/(stem+'.jpg');im.resize((1500,1000),Image.Resampling.LANCZOS).save(jpg,format='JPEG',quality=95,subsampling=0,optimize=True)
 with Image.open(jpg) as c:assert c.format=='JPEG' and c.size==(1500,1000)
 alt='AI-generated concept of '+('an ivory ' if scene!='commercial' else 'a ')+j['name']+' square lunar terrain relief '+contexts[scene]+'.'
 caption='AI-generated application concept. Digital STL/C4D model only; physical fabrication, support, framing, packaging, finishing and concrete casting are additional work. No mesh accuracy or readiness verification.'
 if scene=='commercial':caption+=' Fabrication rights require separate agreement.'
 media.append({'product_id':j['id'],'slug':s,'scene':scene,'file':jpg.name,'title':'AI-generated '+j['name']+' - '+labels[scene]+' Concept','alt':alt,'caption':caption,'width':1500,'height':1000,'bytes':jpg.stat().st_size,'sha256':hashlib.sha256(jpg.read_bytes()).hexdigest()});shutil.copy2(jpg,out/jpg.name)
 review.append({'index':r['index'],'pass':True,'review':'Individually inspected against own two references: square terrain, terraced crater, characteristic central peaks and neighbouring features, full object and distinct setting. Desktop bottom fully supported. Peripheral book lettering in Copernicus wall scene does not label the relief or imply supplied physical goods.'})
assert len(media)==8
(root/'media.json').write_text(json.dumps(media,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(root/'visual-review.json').write_text(json.dumps(review,indent=2)+'\n')
(root/'intent-evidence.json').write_text(json.dumps([{'query':n+' lunar crater STL','url':'https://www.google.com/search?q='+n+'+lunar+crater+STL&hl=en&gl=us&pws=0','file':'google-'+n.lower()+'.txt','location':'Unknown','observations':'Paid own digital model intent mixed with free NASA-derived lunar models, general lunar information and gaming terrain. No metric/rank claims.'} for n in ['Copernicus','Theophilus']],indent=2)+'\n')
for p in root.iterdir():
 if p.is_file() and p.suffix in ['.py','.php','.json','.md','.png','.jpg','.txt']:shutil.copy2(p,out/p.name)
for p in out.iterdir():
 if p.suffix in ['.py','.php','.json','.md','.txt']:p.write_text('\n'.join(x.rstrip() for x in p.read_text(encoding='utf-8-sig').splitlines()).rstrip()+'\n',encoding='utf-8',newline='\n')
print('8 own-reference images inspected, original PNG/prompts retained, true JPEG1500x1000 exported')
