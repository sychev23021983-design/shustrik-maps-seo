from pathlib import Path
import json,hashlib,re
root=Path(__file__).resolve().parent
b=json.loads((root/'baseline.json').read_text(encoding='utf-8-sig'))
paras=[
 'Build terrain visualizations of Taiwan with a textured 3D model for rendered maps, landscape scenes and animations.',
 'The download includes a C4D model, OBJ versions at LOD100, LOD50 and LOD25, and a TIF satellite texture. Use the available detail levels to choose the mesh density that fits your scene; polygon counts and file sizes are listed above.',
 'The mesh has an open base. Before 3D printing or CNC machining, check and prepare the geometry for your intended workflow. For a different format or resolution, use the contact form below to discuss your requirements.'
]
content=b['content'];prefix='[vc_column_text woodmart_inline="no" text_larger="no"]'
start=content.index(prefix)+len(prefix);end=content.index('[/vc_column_text]',start)
old=content[start:end];new='\r\n\r\n'.join(paras);after=content[:start]+new+content[end:]
assert re.findall(r'\[[^\]]+\]',content)==re.findall(r'\[[^\]]+\]',after)
sha=lambda s:hashlib.sha256(s.encode('utf-8')).hexdigest()
m=dict(id=11013,slug=b['slug'],url=b['url'],backup_key='_shustrik_taiwan_copy_backup_20261108',invariant=b['invariant'],prior=b['prior'],before_sha256=sha(content),after_sha256=sha(after),excerpt_sha256=sha(b['excerpt']),edit=dict(at_bytes=len(content[:start].encode('utf-8')),old=old,text=new),approved_paragraphs=paras,indexable_before=b['indexables'][0],
 before={'_yoast_wpseo_title':b['title'],'_yoast_wpseo_metadesc':b['meta_description']},
 after={'_yoast_wpseo_title':'Taiwan Terrain 3D Model — C4D & OBJ with 3 LODs','_yoast_wpseo_metadesc':'Taiwan terrain 3D model in C4D and OBJ, with LOD100/50/25 meshes and a TIF satellite texture. For rendered maps, landscape scenes and visualizations.'})
assert b['id']==11013 and b['title_count']==1 and len(b['indexables'])==1
(root/'11013-after.txt').write_bytes(after.encode('utf-8'))
for file,data in [('baseline.json',b),('manifest.json',m)]:
 (root/file).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
for file in ['release.php','deploy.sh','.gitattributes','.gitignore','public-dom.py','public-qa.py']:
 s=(root.parent/'japan-copy-release-20261108'/file).read_text(encoding='utf-8')
 if file!='public-dom.py':s=s.replace('11358','11013').replace('japan','taiwan').replace('Japan','Taiwan')
 if file=='public-qa.py':
  s=s.replace("['Taiwan 3D model terrain']","['Taiwan Terrain 3D model']")
  s=s.replace('In addition to the 3D terrain of Taiwan','Taiwan DEM')
  s=s.replace('It is perfect for use in graphic design, 3D printing, and CNC milling.','precision parts and components')
 (root/file).write_text(s,encoding='utf-8',newline='\n')
print(json.dumps({'id':m['id'],'title':m['after']['_yoast_wpseo_title'],'meta_length':len(m['after']['_yoast_wpseo_metadesc']),'protected_previous_products':list(m['prior'])},ensure_ascii=False))
