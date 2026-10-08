import json,shutil,hashlib
from pathlib import Path
from PIL import Image
root=Path(__file__).parent
repo=Path('J:/1. My Vault/90 Migration/shustrik-maps-seo/five-special-stl-slider-release-20261008')
repo.mkdir(exist_ok=True)
jobs=json.loads((root/'generated-registry.json').read_text(encoding='utf-8'))
edits={r['key']:r for r in json.loads((root/'edits.json').read_text(encoding='utf-8'))} if (root/'edits.json').exists() else {}
titles={'desk':'Ivory Plastic Desktop Craft Concept','wall':'Small Framed Wall Art Concept','gift':'Gift Box Concept','commercial':'Concrete Commercial Installation Concept'}
base_by_id={r['id']:r['base_listed'] for r in json.loads((root/'manifest.json').read_text(encoding='utf-8'))['rows']}
media=[]
for j in jobs:
 slug=j['slug'];scene=j['scene'];name=j['name'];key=slug+'_'+scene;src=Path(j['generated_path']);stem=f'{slug}-{scene}-1500x1000'
 shutil.copy2(src,root/(stem+'-original.png'))
 if key in edits:src=Path(edits[key]['generated_path']);stem+='-v2';shutil.copy2(src,root/(stem+'-original.png'))
 im=Image.open(src).convert('RGB');assert im.width*2==im.height*3,'3:2 source required'
 im=im.resize((1500,1000),Image.Resampling.LANCZOS);jpg=root/(stem+'.jpg');im.save(jpg,format='JPEG',quality=95,subsampling=0,optimize=True)
 with Image.open(jpg) as check:assert check.format=='JPEG' and check.size==(1500,1000)
 subjects={'antarctica-ice':'circular Antarctica ice-and-ocean-floor terrain disc','dymaxion':'angular unfolded Dymaxion world terrain net','zion-trail':'tall narrow Zion Canyon Trail terrain tile','kiwi-medallion':'New Zealand flag medallion with kiwi bird head relief, left-pointing beak and four stars','nautilus':'Maori-style Nautilus pendant with spiral cutout and cord hole'}
 subject=subjects[slug]
 if scene=='desk':alt=f'AI-generated concept of an ivory plastic {subject} fully supported on a continuous solid walnut desktop backing panel.'
 elif scene=='wall':alt=f'AI-generated concept of a small ivory {subject} mounted on solid sage-green backing in an oak wall frame above a home console.'
 elif scene=='gift':alt=f'AI-generated concept of an ivory {subject} fully supported in a kraft gift box with forest-green tissue.'
 else:alt=f'AI-generated concept of a large grey concrete {subject} fixed to a charcoal backing wall in a museum lobby with visitors for scale.'
 if slug=='nautilus' and scene=='gift':alt=alt.replace('forest-green tissue','a forest-green fitted insert')
 if slug=='dymaxion' and scene=='wall':alt=alt.replace('small ivory','small warm tan')
 caption='AI-generated application concept. Digital STL model only; fabrication, material, finishing, supports, frames, packaging and concrete casting are additional project work.'
 if base_by_id[j['id']]=='open':caption+=' The listed STL has an open base; shown support is additional.'
 if base_by_id[j['id']]=='open / closed':caption+=' The listing states open / closed base; shown backing is additional.'
 if slug in ['nautilus','kiwi-medallion'] and scene in ['wall','commercial']:caption+=' Enlargement and framed wall presentation are additional fabrication adaptations, not supplied file claims.'
 if scene=='commercial':caption+=' Commercial use requires separately agreed permission.'
 if slug=='bermuda':alt=alt.replace('Bermuda terrain relief','Bermuda square marine terrain relief tile with a shallow bank and small island chain')
 r={'product_id':j['id'],'slug':slug,'scene':scene,'file':jpg.name,'title':f'AI-generated {name} - {titles[scene]}','alt':alt,'caption':caption,'width':1500,'height':1000,'bytes':jpg.stat().st_size,'sha256':hashlib.sha256(jpg.read_bytes()).hexdigest()}
 media.append(r);shutil.copy2(jpg,repo/jpg.name)
assert len(media)==20
(root/'media.json').write_text(json.dumps(media,ensure_ascii=False,indent=2),encoding='utf-8')
for name in ['manifest.json','media.json']:shutil.copy2(root/name,repo/name)
print(json.dumps([{'file':r['file'],'bytes':r['bytes']} for r in media]))
