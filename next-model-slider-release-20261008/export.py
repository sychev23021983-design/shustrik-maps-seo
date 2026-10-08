from pathlib import Path
from PIL import Image
import json,shutil,hashlib
root=Path(__file__).parent;out=Path('J:/1. My Vault/90 Migration/shustrik-maps-seo/next-model-slider-release-20261008')
reg=json.loads((root/'native-registry.json').read_text());media=[];reviews=[]
scenes=['desk','wall','gift','commercial']
labels=['Desktop Display','Small Wall Display','Gift Box','Grey Concrete Exhibition']
subjects={'sheikh-zayed':'Sheikh Zayed portrait bust with draped headdress and patterned robe','troll-skull':'Troll Face skull with exaggerated toothy grin on a dark support post and rectangular base','zombie-box':'rectangular Zombie Monster storage box with large glasses, round eyes, square teeth and two block feet'}
for r in reg:
 j=r['job'];s=j['slug'];scene=j['scene'];src=Path(r['path']);stem=s+'-'+scene+'-1500x1000'
 shutil.copy2(src,root/(stem+'-original.png'));im=Image.open(src).convert('RGB');assert im.width*2==im.height*3
 jpg=root/(stem+'.jpg');im.resize((1500,1000),Image.Resampling.LANCZOS).save(jpg,format='JPEG',quality=95,subsampling=0,optimize=True)
 with Image.open(jpg) as c:assert c.format=='JPEG' and c.size==(1500,1000)
 subject=subjects[s]
 contexts={'desk':'fully supported on a solid desktop base','wall':'on a solid shelf in a small oak wall display','gift':'supported in an open gift box with a fitted insert','commercial':'enlarged in grey concrete at a design exhibition with adults for scale'}
 if s=='zombie-box' and scene=='wall':contexts[scene]='with coral glasses and keys in its open storage cavity on an oak wall shelf'
 if s=='zombie-box' and scene=='gift':contexts[scene]='with coral glasses in a kraft gift box with a green fitted insert'
 alt='AI-generated concept of '+('an ivory plastic ' if scene!='commercial' else 'a ')+subject+' '+contexts[scene]+'.'
 caption='AI-generated application concept. Digital STL model only; fabrication, materials, support, finishing, display cabinet, packaging and enlargement are additional project work.'
 if scene=='commercial':caption+=' This concept grants no commercial fabrication rights.'
 m={'product_id':j['id'],'slug':s,'scene':scene,'file':jpg.name,'title':'AI-generated '+j['name']+' - '+labels[scenes.index(scene)]+' Concept','alt':alt,'caption':caption,'width':1500,'height':1000,'bytes':jpg.stat().st_size,'sha256':hashlib.sha256(jpg.read_bytes()).hexdigest()};media.append(m)
 reviews.append({'index':r['index'],'original':src.name,'pass':True,'review':'Individually inspected: own reference silhouette and recognisable details retained, complete subject, distinct setting, plausible support; no unwanted text or hand defects. Desktop base fully supported. Zombie wall/gift coral glasses accurately described in alt.'})
 shutil.copy2(jpg,out/jpg.name)
assert len(media)==12
(root/'media.json').write_text(json.dumps(media,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(root/'visual-review.json').write_text(json.dumps(reviews,indent=2)+'\n')
old=root.parent/'Five Special STL Sliders 2026-10-08';revision=root.parent/'Kiwi Nautilus Use Cases Revision 2026-10-08'
for name in ['verify-preservation.py','public-qa.py']:
 text=(old/name).read_text().replace('five-special','next-models').replace('five_special_qa','next_models_qa').replace('passed5/5','passed3/3');(root/name).write_text(text,encoding='utf-8')
(root/'backup-export.php').write_text((revision/'backup-export.php').read_text().replace('[21381,18721]','[15527,20192,20199]').replace('kiwi_nautilus_usecases','next_models'),encoding='utf-8')
e=json.loads((root/'intent-evidence.json').read_text())
for row in e:
 for k,val in list(row.items()):
  if isinstance(val,str) and val.endswith('.txt') and 'google-sheikh-bust' not in val:row[k]=val[:-4]+'-full.txt'
(root/'intent-evidence.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(root/'Intent Review.md').write_text('# Google intent review — 2026-10-08\n\nEnglish queries, Google hl=en/gl=us/pws=0. Google footer could not determine location: these are intent observations, not verified US rankings. No measured volume, difficulty, positions or forecasts. Five full accessibility snapshots retained.\n\nSheikh Zayed bust queries mix this portrait STL with Grand Mosque models and a different Sheikh Mohamed bin Zayed. Use portrait/bust terms. Troll Face skull queries include this digital model, physical gifts, other creators and free aggregators; retain whole/split STL intent and the existing non-commercial license. Zombie Monster storage box queries include the same face/glasses/tooth-row model and unrelated tabletop-game organisers; avoid Zombicide, Kingdom Death and humanoid-zombie intent.\n\nNo demand threshold claimed. Publication is the owner-authorized update of existing goods; any later SEO experiment requires a measured baseline and indexation review. Original claims and anomalous Sheikh Zayed dimensions retained for separate validation.\n',encoding='utf-8')
for p in root.iterdir():
 if p.is_file() and (p.suffix in ['.py','.php','.json','.md','.png','.jpg','.txt']) and p.name not in ['runtime-before.txt','server-runtime-before.txt']:
  shutil.copy2(p,out/p.name)
for p in out.iterdir():
 if p.suffix in ['.py','.php','.json','.md','.txt']:p.write_text(p.read_text(encoding='utf-8-sig').rstrip()+'\n',encoding='utf-8',newline='\n')
print('Exported 12 true RGB JPEG1500x1000, originals/prompts/references, guarded source and QA tools')
