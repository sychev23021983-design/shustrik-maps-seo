from pathlib import Path
import json,hashlib,re
root=Path(__file__).resolve().parent
b=json.loads((root/'baseline.json').read_text(encoding='utf-8-sig'))
intro='Build rendered world maps in Cinema 4D with a rectangular terrain model and a set of surface maps. The download is supplied in C4D format; OBJ export is available on request.'
paras=[
 'Use the 16-bit TIF height map to drive displacement on a surface in your 3D software. The normal map helps show fine relief detail, while the satellite texture provides the color imagery. Map dimensions and bit depths are listed in the specification above.',
 'The package also includes a water map, a pseudo-color elevation map and a boundary mask. These give you additional inputs for building your scene: the pseudo-color map represents elevation with color, and the boundary mask can be used with your background.',
 'The model uses a geographic projection and has an open base. Set your camera, lighting and materials in your 3D software for map illustrations, presentations or animation. Before 3D printing or CNC machining, check and prepare the geometry for your intended workflow.'
]
headings=['Height, normal and satellite maps','Water, elevation color and boundary maps','Working with the terrain model']
detail='\r\n'+'\r\n'.join('<h2>'+h+'</h2>\r\n<p>'+p+'</p>' for h,p in zip(headings,paras))
content=b['content'];prefix='[vc_column_text css="" woodmart_inline="no" text_larger="no"]'
matches=list(re.finditer(re.escape(prefix),content));assert len(matches)==2
edits=[]
for match,new in zip(matches,[intro,detail]):
 start=match.end();end=content.index('[/vc_column_text]',start)
 edits.append(dict(at_bytes=len(content[:start].encode('utf-8')),old=content[start:end],text=new))
after=content.encode('utf-8')
for e in sorted(edits,key=lambda x:x['at_bytes'],reverse=True):
 at=e['at_bytes'];old=e['old'].encode('utf-8');after=after[:at]+e['text'].encode('utf-8')+after[at+len(old):]
after=after.decode('utf-8')
assert re.findall(r'\[[^\]]+\]',content)==re.findall(r'\[[^\]]+\]',after)
sha=lambda s:hashlib.sha256(s.encode('utf-8')).hexdigest()
m=dict(id=15954,slug=b['slug'],url=b['url'],backup_key='_shustrik_world_earth_copy_backup_20261108',invariant=b['invariant'],prior=b['prior'],before_sha256=sha(content),after_sha256=sha(after),excerpt_sha256=sha(b['excerpt']),edits=edits,approved_paragraphs=[intro]+paras,approved_headings=headings,indexable_before=b['indexables'][0],
 before={'_yoast_wpseo_title':b['title'],'_yoast_wpseo_metadesc':b['meta_description']},
 after={'_yoast_wpseo_title':'World Earth Map 3D — C4D with Height & Texture Maps','_yoast_wpseo_metadesc':'Rectangular world terrain model for Cinema 4D, with height, normal, satellite and water maps. OBJ export on request for your visualization workflow.'})
assert b['id']==15954 and b['title_count']==1 and len(b['indexables'])==1
(root/'15954-after.txt').write_bytes(after.encode('utf-8'))
for name,data in [('baseline.json',b),('manifest.json',m)]:
 (root/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
for file in ['release.php','deploy.sh','.gitattributes','.gitignore','public-dom.py','public-qa.py']:
 s=(root.parent/'world-map-copy-release-20261108'/file).read_text(encoding='utf-8')
 if file!='public-dom.py':
  s=s.replace('10238','15954').replace('world-map-copy','world-earth-copy').replace('_shustrik_world_map_copy','_shustrik_world_earth_copy')
 if file=='public-qa.py':
  s=s.replace("'https://shustrik-maps.com/product/world-3d-model/'","'https://shustrik-maps.com/product/world-map-3d-model/'")
  s=s.replace("['interactive globe','stunning accuracy','spatial analysis','global dataset']","['interactive','accurate','precision','geospatial data','The Best']")
 (root/file).write_text(s,encoding='utf-8',newline='\n')
print(json.dumps({'id':m['id'],'title':m['after']['_yoast_wpseo_title'],'meta_length':len(m['after']['_yoast_wpseo_metadesc']),'description_blocks':len(edits),'protected_previous_products':list(m['prior'])}))
