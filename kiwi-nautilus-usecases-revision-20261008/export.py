from pathlib import Path
import json,shutil,hashlib,re
from PIL import Image
root=Path(__file__).parent;out=Path('J:/1. My Vault/90 Migration/shustrik-maps-seo/kiwi-nautilus-usecases-revision-20261008')
jobs=json.loads((root/'generated-registry.json').read_text(encoding='utf-8'));media=[]
labels={'handheld':'Ivory Plastic Handheld Medallion','capsule':'Antique Brass Collector Capsule','gift':'Small Gift Box','pouch':'Antique Brass Travel Keepsake','necklace':'Ivory Plastic Necklace on Woman','backpack':'Ivory Plastic Backpack Keychain','keys':'Ivory Plastic House Keys Keychain'}
alts={('kiwi-medallion','handheld'):'AI-generated concept of a small ivory plastic New Zealand flag and kiwi bird commemorative medallion resting in an adult hand.',('kiwi-medallion','capsule'):'AI-generated concept of an antique-brass-finish New Zealand kiwi and flag medallion in a clear collector capsule on a dark velvet tray.',('kiwi-medallion','gift'):'AI-generated concept of an antique-bronze-finish New Zealand kiwi and flag commemorative medallion in a small navy-blue gift presentation box.',('kiwi-medallion','pouch'):'AI-generated concept of a small antique-brass-finish New Zealand kiwi and flag medallion displayed with a suede travel keepsake pouch.',('nautilus','necklace'):'AI-generated concept of a small ivory plastic Maori-style Nautilus spiral pendant worn on a dark cord at the collarbone of an adult woman in a linen shirt.',('nautilus','backpack'):'AI-generated concept of an ivory plastic Maori-style Nautilus spiral keychain attached through its top hole to the zipper of an olive-green backpack.',('nautilus','keys'):'AI-generated concept of a small ivory plastic Maori-style Nautilus spiral keychain attached by a metal split ring to house keys beside a wallet.',('nautilus','gift'):'AI-generated concept of an ivory plastic Maori-style Nautilus spiral keychain with a metal split ring in a small kraft gift box with a forest-green insert.'}
for j in jobs:
 src=Path(j['generated_path']);stem=j['slug']+'-'+j['scene']+'-revision-1500x1000';shutil.copy2(src,root/(stem+'-original.png'))
 im=Image.open(src).convert('RGB');assert im.width*2==im.height*3
 jpg=root/(stem+'.jpg');im.resize((1500,1000),Image.Resampling.LANCZOS).save(jpg,format='JPEG',quality=95,subsampling=0,optimize=True)
 with Image.open(jpg) as im:assert im.format=='JPEG' and im.size==(1500,1000)
 caption='AI-generated application concept. Digital STL model only; fabrication, finishing, cords, rings, capsules and packaging are additional project adaptations.'
 if j['slug']=='kiwi-medallion':caption+=' Commemorative decorative medallion concept, not legal tender or a supplied physical coin.'
 media.append({'product_id':j['id'],'slug':j['slug'],'scene':j['scene'],'file':jpg.name,'title':'AI-generated '+j['name']+' - '+labels[j['scene']],'alt':alts[(j['slug'],j['scene'])],'caption':caption,'width':1500,'height':1000,'bytes':jpg.stat().st_size,'sha256':hashlib.sha256(jpg.read_bytes()).hexdigest()});shutil.copy2(jpg,out/jpg.name)
assert len(media)==8
(root/'media.json').write_text(json.dumps(media,ensure_ascii=False,indent=2),encoding='utf-8')
b=json.loads((root/'baseline.json').read_text(encoding='utf-8'));m=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
for x,y in zip(m['rows'],b['rows']):
 for tag in ['vc_column_text','woodmart_text_block']:
  assert re.findall(r'\['+tag+r'[^\]]*\](.*?)\[/'+tag+r'\]',x['description'],re.S)==re.findall(r'\['+tag+r'[^\]]*\](.*?)\[/'+tag+r'\]',y['content'],re.S)
 assert x['h1_preserved']==y['title'] and x['url']==y['url'] and x['description'].count('{{IMAGE_IDS}}')==1
for n in ['release.php']:
 s=(out/n).read_text(encoding='utf-8');assert '[21381,18721]' in s and 'count($assets)!==8' in s
for n in ['manifest.json','baseline.json','defs.json','media.json','owner-revision.md','generation-jobs.json','generated-registry.json','visual-review.json','export.py','deliver.py','backup-export.php','verify-preservation.py','public-qa.py']:shutil.copy2(root/n,out/n)
for p in out.iterdir():
 if p.suffix in ['.json','.md','.py','.php','.txt']:
  s=p.read_text(encoding='utf-8-sig');p.write_text('\n'.join(l.rstrip() for l in s.splitlines()).rstrip()+'\n',encoding='utf-8',newline='\n')
print('Two exact replacement manifests, source text unchanged, eight true JPEGs and AI metadata prepared')
