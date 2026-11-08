from pathlib import Path
import json,hashlib,re
r=Path(__file__).resolve().parent;b=json.loads((r/'baseline.json').read_text(encoding='utf-8-sig'));content=b['content']
start=content.index('<p>Compare the file format, mesh and preview of each USA product before purchasing.')
end=content.index('</p>',start)+4;old=content[start:end]
links=[
 ('50-state C4D collection','https://shustrik-maps.com/product/50-united-states-of-america-3d-model/'),
 ('Contiguous 48-state collection','https://shustrik-maps.com/product/contiguous-48-usa-states/'),
 ('50-state STL collection','https://shustrik-maps.com/product/complete-usa-50-states-topographic-map-3d-model-for-3d-printing-cnc-carving/')
]
rows=[
 ['USA terrain package (this product)','C4D and OBJ: LOD100, LOD50, LOD25','Terrain model with material and texture files; open base.'],
 [f'<a href="{links[0][1]}">{links[0][0]}</a>','C4D; OBJ/FBX export on request','50 separate state meshes with individual satellite textures; open base.'],
 [f'<a href="{links[1][1]}">{links[1][0]}</a>','C4D and OBJ','48 contiguous state meshes; closed base.'],
 [f'<a href="{links[2][1]}">{links[2][0]}</a>','STL','50 state meshes with closed bases for print/CNC preparation.']
]
paras=[
 'Choose by the supplied formats and whether you need a terrain asset or separate state meshes. The collections below are separate products.',
 'LOD100, LOD50 and LOD25 identify detail versions of this terrain model; they do not mean sets of 100, 50 or 25 states.',
 'Check the preview of each product for the geographic area shown. For printing or CNC, compare the STL collection and prepare the selected files for your machine and scale.'
]
table='<div role="region" aria-label="Compare USA terrain and state collections" tabindex="0" style="overflow-x:auto;max-width:100%;"><table><thead><tr><th scope="col">Product</th><th scope="col">Supplied model formats</th><th scope="col">Model and base</th></tr></thead><tbody>'
table+=''.join('<tr>'+''.join('<td>'+cell+'</td>' for cell in row)+'</tr>' for row in rows)+'</tbody></table></div>'
new='<p>'+paras[0]+'</p>\n'+table+'\n'+'\n'.join('<p>'+p+'</p>' for p in paras[1:])
after=content[:start]+new+content[end:]
sha=lambda s:hashlib.sha256(s.encode('utf-8')).hexdigest()
assert re.findall(r'\[[^\]]+\]',content)==re.findall(r'\[[^\]]+\]',after)
m=dict(id=10102,slug=b['slug'],url=b['url'],backup_key='_shustrik_usa_comparison_backup_20261108',invariant=b['invariant'],prior=b['prior'],before_sha256=sha(content),after_sha256=sha(after),excerpt_sha256=sha(b['excerpt']),edit=dict(at_bytes=len(content[:start].encode('utf-8')),old=old,text=new),approved_paragraphs=paras,added_links=[dict(text=t,url=u) for t,u in links],metadata={'_yoast_wpseo_title':b['title'],'_yoast_wpseo_metadesc':b['meta_description']},indexables=b['indexables'])
assert b['id']==10102 and b['title_count']==1 and len(b['indexables'])==2
for file,data in [('baseline.json',b),('manifest.json',m)]:
 (r/file).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
(r/'10102-after.txt').write_bytes(after.encode('utf-8'))
for file in ['deploy.sh','.gitattributes','.gitignore']:
 s=(r.parent/'japan-copy-release-20261108'/file).read_text(encoding='utf-8').replace('11358','10102').replace('japan-copy','usa-copy')
 (r/file).write_text(s,encoding='utf-8',newline='\n')
print(json.dumps({'id':10102,'description_replacements':1,'comparison_products':4,'new_links':3,'metadata_preserved':True,'yoast_rows_preserved':len(b['indexables'])}))
