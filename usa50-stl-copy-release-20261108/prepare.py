from pathlib import Path
import json,hashlib,re,shutil
r=Path(__file__).resolve().parent;b=json.loads((r/'baseline.json').read_text(encoding='utf-8-sig'));content=b['content']
blocks=[
'<h2>50-state USA topographic STL set</h2>\r\n<p>This STL collection contains 50 separate state terrain meshes for projects such as raised relief displays, educational models and decorative maps. The states are listed as proportionally scaled for a puzzle-like assembly; check the fit at your chosen scale before making a full set.</p>',
'<h2>Files and fabrication planning</h2>\r\n<p>The product specification lists a 7.39 GB full archive, 50 meshes with closed bases, triangle geometry, Lambert conformal conic projection and vertical scale factor Z = 3. The archive contains terrain models, not a physical product.</p>\r\n<p>For 3D printing or CNC projects, inspect the files and prepare them for your software, equipment, material and chosen scale. Closed bases alone do not guarantee a successful print, toolpath or fit. Make a small test before producing a complete display.</p>\r\n<h2>Choosing a USA collection</h2>\r\n<p>This product covers all 50 states. For the separate 48-state STL collection, use the link below. The images beside this description are AI-generated application concepts, not photographs of fabricated models.</p>'
]
prefix='[vc_column_text css="" woodmart_inline="no" text_larger="no"]';matches=list(re.finditer(re.escape(prefix),content));assert len(matches)==2
edits=[]
for match,new in zip(matches,blocks):
 start=match.end();end=content.index('[/vc_column_text]',start);edits.append(dict(at_bytes=len(content[:start].encode()),old=content[start:end],text='\r\n'+new+'\r\n'))
after=content.encode()
for e in sorted(edits,key=lambda x:x['at_bytes'],reverse=True):
 at=e['at_bytes'];old=e['old'].encode();assert after[at:at+len(old)]==old;after=after[:at]+e['text'].encode()+after[at+len(old):]
after=after.decode();assert re.findall(r'\[[^\]]+\]',content)==re.findall(r'\[[^\]]+\]',after)
sha=lambda s:hashlib.sha256(s.encode()).hexdigest()
m=dict(id=18873,slug=b['slug'],url=b['url'],backup_key='_shustrik_usa50_stl_copy_backup_20261108',invariant=b['invariant'],prior=b['prior'],before_sha256=sha(content),after_sha256=sha(after),excerpt_sha256=sha(b['excerpt']),edits=edits,added_links=[],metadata={'_yoast_wpseo_title':b['title'],'_yoast_wpseo_metadesc':b['meta_description']},indexables=b['indexables'])
assert b['id']==18873 and b['title_count']==1 and len(b['indexables'])==2
for file,data in [('baseline.json',b),('manifest.json',m)]:(r/file).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(r/'18873-after.txt').write_bytes(after.encode())
s=(r.parent/'usa-copy-release-20261108'/'release.php').read_text(encoding='utf-8').replace('10102','18873').replace('_shustrik_usa_comparison_backup','_shustrik_usa50_stl_copy_backup')
old="$before=$b['content'];$after=file_get_contents(__DIR__.'/18873-after.txt');$e=$m['edit'];\n guard(substr($before,$e['at_bytes'],strlen($e['old']))===$e['old'],'Edit mismatch');\n guard(substr_replace($before,$e['text'],$e['at_bytes'],strlen($e['old']))===$after,'Candidate edit drift');"
new="$before=$b['content'];$after=file_get_contents(__DIR__.'/18873-after.txt');$candidate=$before;$edits=$m['edits'];usort($edits,fn($a,$b)=>$b['at_bytes']<=>$a['at_bytes']);\n foreach($edits as $e){guard(substr($candidate,$e['at_bytes'],strlen($e['old']))===$e['old'],'Edit mismatch');$candidate=substr_replace($candidate,$e['text'],$e['at_bytes'],strlen($e['old']));}\n guard($candidate===$after,'Candidate edit drift');"
assert old in s;s=s.replace(old,new);(r/'release.php').write_text(s,encoding='utf-8',newline='\n')
for f in ['deploy.sh','.gitattributes','.gitignore']:
 s=(r.parent/'usa-copy-release-20261108'/f).read_text(encoding='utf-8').replace('usa-copy','usa50-stl-copy').replace('10102','18873')
 if f=='.gitattributes':s+='\n*.sh text eol=lf\n'
 (r/f).write_text(s,encoding='utf-8',newline='\n')
shutil.copy2(r.parent/'usa48-copy-release-20261108'/'public-dom.py',r/'public-dom.py')
print(json.dumps({'ok':True,'edits':len(edits),'indexables':len(b['indexables'])}))
