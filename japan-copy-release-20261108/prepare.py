from pathlib import Path
import json, hashlib, re, shutil
root=Path(__file__).resolve().parent
b=json.loads((root/'baseline.json').read_text(encoding='utf-8-sig'))
paras=[
 'Use this Japan terrain model to create rendered maps, landscape illustrations and scenes. The model is supplied in C4D format with a TIF satellite texture; OBJ or FBX export is available on request.',
 'The mesh has an open base. Before 3D printing or CNC machining, check and prepare the geometry for your intended workflow. For an STL version, see the separate Japan STL product linked below.'
]
content=b['content'];prefix='[vc_column_text woodmart_inline="no" text_larger="no"]'
start=content.index(prefix)+len(prefix);end=content.index('[/vc_column_text]',start)
old=content[start:end];new='\r\n\r\n'.join(paras);after=content[:start]+new+content[end:]
assert re.findall(r'\[[^\]]+\]',content)==re.findall(r'\[[^\]]+\]',after)
sha=lambda s:hashlib.sha256(s.encode('utf-8')).hexdigest()
m=dict(id=11358,slug=b['slug'],url=b['url'],backup_key='_shustrik_japan_copy_backup_20261108',invariant=b['invariant'],prior=b['prior'],before_sha256=sha(content),after_sha256=sha(after),excerpt_sha256=sha(b['excerpt']),edit=dict(at_bytes=len(content[:start].encode('utf-8')),old=old,text=new),approved_paragraphs=paras,indexable_before=b['indexables'][0],
 before={'_yoast_wpseo_title':b['title'],'_yoast_wpseo_metadesc':b['meta_description']},
 after={'_yoast_wpseo_title':'Japan Terrain 3D Model — C4D with Satellite Texture','_yoast_wpseo_metadesc':'Japan terrain model in C4D with a TIF satellite texture for visualization. OBJ/FBX export on request. Prepare the mesh for your printing or CNC workflow.'})
assert b['title_count']==1 and len(b['indexables'])==1
(root/'11358-after.txt').write_bytes(after.encode('utf-8'))
(root/'baseline.json').write_text(json.dumps(b,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
(root/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
shutil.copyfile(root.parent/'moon-description-release-20261017/public-dom.py',root/'public-dom.py')
print(json.dumps({'id':m['id'],'title':m['after']['_yoast_wpseo_title'],'description_length':len(m['after']['_yoast_wpseo_metadesc']),'shortcodes_preserved':True},ensure_ascii=False))
