from pathlib import Path
import json,hashlib,re
root=Path(__file__).resolve().parent
b=json.loads((root/'baseline.json').read_text(encoding='utf-8-sig'))
headings=['50 separate states for Cinema 4D','Model formats and open bases','Choosing a USA collection']
paras=[
 'Build USA map scenes with 50 separate state terrain meshes in Cinema 4D. Each state has its own mesh, frontal UV mapping and TIF satellite texture. Show or hide individual states and adjust terrain, base elevation and boundary appearance in your scene.',
 'The supplied model format is C4D; OBJ and FBX export is available on request. The meshes have open bases. Before using them for 3D printing or CNC machining, check and prepare the geometry for your machine, material and scale.',
 'Choose this collection when you need separate state terrain objects with satellite textures for rendered maps, presentations or animation. For a collection supplied as STL with closed bases, compare the 50-state STL collection. It is a separate product and still requires preparation for your fabrication workflow.'
]
url='https://shustrik-maps.com/product/complete-usa-50-states-topographic-map-3d-model-for-3d-printing-cnc-carving/'
anchor='<a href="'+url+'">50-state STL collection</a>'
htmlparas=paras[:2]+[paras[2].replace('50-state STL collection',anchor)]
new='\r\n'+'\r\n'.join('<h2>'+h+'</h2>\r\n<p>'+p+'</p>' for h,p in zip(headings,htmlparas))+'\r\n'
content=b['content'];prefix='[vc_column_text woodmart_inline="no" text_larger="no"]'
assert content.count(prefix)==1
start=content.index(prefix)+len(prefix);end=content.index('[/vc_column_text]',start)
edits=[dict(at_bytes=len(content[:start].encode('utf-8')),old=content[start:end],text=new)]
after=content[:start]+new+content[end:]
assert re.findall(r'\[[^\]]+\]',content)==re.findall(r'\[[^\]]+\]',after)
sha=lambda s:hashlib.sha256(s.encode('utf-8')).hexdigest()
m=dict(id=15665,slug=b['slug'],url=b['url'],backup_key='_shustrik_usa50_c4d_copy_backup_20261108',invariant=b['invariant'],prior=b['prior'],before_sha256=sha(content),after_sha256=sha(after),excerpt_sha256=sha(b['excerpt']),edits=edits,approved_paragraphs=paras,approved_headings=headings,added_links=[{'url':url,'text':'50-state STL collection','rel':''}],added_anchors=[anchor],indexable_before=b['indexables'][0],before={'_yoast_wpseo_title':b['title'],'_yoast_wpseo_metadesc':b['meta_description']},after={'_yoast_wpseo_title':'50 US States 3D Model — C4D with Satellite Textures','_yoast_wpseo_metadesc':'50 separate US state terrain meshes in C4D, each with UV mapping and a TIF satellite texture. Open bases; OBJ/FBX export available on request.'})
assert b['id']==15665 and b['title_count']==1 and len(b['indexables'])==1
(root/'15665-after.txt').write_bytes(after.encode('utf-8'))
for name,data in [('baseline.json',b),('manifest.json',m)]:
 (root/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
for file in ['release.php','deploy.sh','.gitattributes','.gitignore']:
 s=(root.parent/'world-earth-copy-release-20261108'/file).read_text(encoding='utf-8').replace('15954','15665').replace('world-earth-copy','usa50-c4d-copy').replace('_shustrik_world_earth_copy','_shustrik_usa50_c4d_copy')
 if file=='release.php':
  old="preg_match_all('/<a\\b[^>]*>.*?<\\/a>/s',$before,$l);preg_match_all('/<a\\b[^>]*>.*?<\\/a>/s',$after,$r);guard($l[0]===$r[0],'Link markup drift');"
  newcode="foreach($m['added_anchors'] as $anchor)guard(substr_count($after,$anchor)===1&&substr_count($before,$anchor)===0,'Added anchor mismatch');\n $link_comparison=str_replace($m['added_anchors'],'',$after);\n preg_match_all('/<a\\b[^>]*>.*?<\\/a>/s',$before,$l);preg_match_all('/<a\\b[^>]*>.*?<\\/a>/s',$link_comparison,$r);guard($l[0]===$r[0],'Link markup drift');"
  assert old in s
  s=s.replace(old,newcode)
 (root/file).write_text(s,encoding='utf-8',newline='\n')
print(json.dumps({'id':m['id'],'title':m['after']['_yoast_wpseo_title'],'meta_length':len(m['after']['_yoast_wpseo_metadesc']),'description_blocks':len(edits),'protected_previous_products':list(m['prior'])},ensure_ascii=True))
