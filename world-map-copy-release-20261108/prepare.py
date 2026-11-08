from pathlib import Path
import json,hashlib,re
root=Path(__file__).resolve().parent
b=json.loads((root/'baseline.json').read_text(encoding='utf-8-sig'))
intro='Create rendered world maps with a rectangular 3D terrain model in C4D, FBX and OBJ formats. The map uses a geographic projection and includes a TIF satellite texture.'
paras=[
 'The rectangular layout shows terrain across the world on a map surface. Open the model in your 3D software to compose an overview or choose an angled camera view for map illustrations, presentation graphics and animated scenes.',
 'The C4D, FBX and OBJ files are supplied with UV mapping and a 21600 x 10800 px TIF satellite texture. The mesh has an open base. Before 3D printing or CNC machining, check and prepare the geometry for your intended workflow.',
 'This product combines the terrain model and satellite texture in a C4D/FBX/OBJ package. For a bundle with height, normal and water maps, compare the separate World Earth Map 3D Model linked below.'
]
headings=['A world map with raised terrain','Included formats and satellite texture','Choosing between the World models']
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
m=dict(id=10238,slug=b['slug'],url=b['url'],backup_key='_shustrik_world_map_copy_backup_20261108',invariant=b['invariant'],prior=b['prior'],before_sha256=sha(content),after_sha256=sha(after),excerpt_sha256=sha(b['excerpt']),edits=edits,approved_paragraphs=[intro]+paras,approved_headings=headings,indexable_before=b['indexables'][0],
 before={'_yoast_wpseo_title':b['title'],'_yoast_wpseo_metadesc':b['meta_description']},
 after={'_yoast_wpseo_title':'World Map 3D Model — C4D, FBX & OBJ Terrain','_yoast_wpseo_metadesc':'Rectangular world terrain model in C4D, FBX and OBJ, with UV mapping and a TIF satellite texture. Create rendered maps, illustrations and animated scenes.'})
assert b['id']==10238 and b['title_count']==1 and len(b['indexables'])==1
(root/'10238-after.txt').write_bytes(after.encode('utf-8'))
for name,data in [('baseline.json',b),('manifest.json',m)]:
 (root/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
for file in ['release.php','deploy.sh','.gitattributes','.gitignore']:
 s=(root.parent/'japan-copy-release-20261108'/file).read_text(encoding='utf-8')
 s=s.replace('11358','10238').replace('japan-copy','world-map-copy').replace('_shustrik_japan_copy','_shustrik_world_map_copy')
 if file=='release.php':
  old=" $before=$b['content'];$after=file_get_contents(__DIR__.'/10238-after.txt');$e=$m['edit'];\n guard(substr($before,$e['at_bytes'],strlen($e['old']))===$e['old'],'Edit mismatch');\n guard(substr_replace($before,$e['text'],$e['at_bytes'],strlen($e['old']))===$after,'Candidate edit drift');"
  new=" $before=$b['content'];$after=file_get_contents(__DIR__.'/10238-after.txt');$candidate=$before;$edits=$m['edits'];usort($edits,fn($a,$b)=>$b['at_bytes']<=>$a['at_bytes']);\n foreach($edits as $e){guard(substr($candidate,$e['at_bytes'],strlen($e['old']))===$e['old'],'Edit mismatch');$candidate=substr_replace($candidate,$e['text'],$e['at_bytes'],strlen($e['old']));}\n guard($candidate===$after,'Candidate edit drift');"
  assert old in s;s=s.replace(old,new)
 (root/file).write_text(s,encoding='utf-8',newline='\n')
print(json.dumps({'id':m['id'],'title':m['after']['_yoast_wpseo_title'],'meta_length':len(m['after']['_yoast_wpseo_metadesc']),'description_blocks':len(edits),'protected_previous_products':list(m['prior'])}))
