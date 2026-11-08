from pathlib import Path
import json,hashlib,re,shutil
root=Path(__file__).resolve().parent
b=json.loads((root/'baseline.json').read_text(encoding='utf-8-sig'));content=b['content']
blocks=[
'<h2>48 contiguous states in C4D and OBJ</h2>\r\n<p>Explore the terrain of the 48 contiguous United States with separate state meshes supplied in C4D and OBJ. The collection includes TIF maps for building terrain visualizations, educational scenes and presentations.</p>',
'<h2>Formats and terrain maps</h2>\r\n<p>The package lists 48 polygonal state meshes with closed bases. The model uses a Lambert Conformal Conic projection and a vertical scale factor of 3. The specification lists 11,586,716 polygons in total; performance depends on your software, hardware and scene settings.</p>\r\n<p>The listed TIF maps include satellite, pseudo-color elevation, water and normal maps, with frontal UV mapping. Check the file specifications above for package sizes and format details.</p>',
'<h2>Using the collection</h2>\r\n<p>Use the models as assets in a 3D workflow that supports the supplied C4D or OBJ files. Import behavior, materials and performance depend on the application and version. The closed bases do not by themselves establish print or CNC readiness: inspect and prepare the geometry for your equipment, material and scale.</p>\r\n<p>The contiguous collection excludes Alaska and Hawaii. For a separate collection covering all 50 states, see the existing 50-state product link below; its supplied formats and base differ.</p>'
]
prefix='[vc_column_text css="" woodmart_inline="no" text_larger="no"]'
matches=list(re.finditer(re.escape(prefix),content));assert len(matches)>=5
edits=[]
for match,new in zip(matches[:3],blocks):
 start=match.end();end=content.index('[/vc_column_text]',start)
 edits.append(dict(at_bytes=len(content[:start].encode()),old=content[start:end],text='\r\n'+new+'\r\n'))
old='Optimized low-polygon mesh';assert content.count(old)==1
start=content.index(old);edits.append(dict(at_bytes=len(content[:start].encode()),old=old,text='State terrain mesh'))
after=content.encode()
for e in sorted(edits,key=lambda x:x['at_bytes'],reverse=True):
 at=e['at_bytes'];o=e['old'].encode();assert after[at:at+len(o)]==o;after=after[:at]+e['text'].encode()+after[at+len(o):]
after=after.decode();assert re.findall(r'\[[^\]]+\]',content)==re.findall(r'\[[^\]]+\]',after)
sha=lambda s:hashlib.sha256(s.encode()).hexdigest()
m=dict(id=19313,slug=b['slug'],url=b['url'],backup_key='_shustrik_usa48_copy_backup_20261108',invariant=b['invariant'],prior=b['prior'],before_sha256=sha(content),after_sha256=sha(after),excerpt_sha256=sha(b['excerpt']),edits=edits,indexable_before=b['indexables'][0],before={'_yoast_wpseo_title':b['title'],'_yoast_wpseo_metadesc':b['meta_description']},after={'_yoast_wpseo_title':'Contiguous 48 US States 3D Model — C4D & OBJ Terrain','_yoast_wpseo_metadesc':'Explore 48 contiguous US state terrain meshes in C4D and OBJ, with TIF maps and closed bases. View the mesh and file specifications.'})
assert b['id']==19313 and b['title_count']==1 and len(b['indexables'])==1
(root/'19313-after.txt').write_bytes(after.encode())
for name,data in [('baseline.json',b),('manifest.json',m)]:(root/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for f in ['release.php','deploy.sh','.gitattributes','.gitignore']:
 s=(root.parent/'world-earth-copy-release-20261108'/f).read_text(encoding='utf-8').replace('15954','19313').replace('world-earth-copy','usa48-copy').replace('_shustrik_world_earth_copy','_shustrik_usa48_copy')
 (root/f).write_text(s,encoding='utf-8',newline='\n')
shutil.copy2(root.parent/'usa50-c4d-copy-release-20261108'/'public-dom.py',root/'public-dom.py')
print(json.dumps({'ok':True,'edits':len(edits),'protected':len(b['prior'])}))
