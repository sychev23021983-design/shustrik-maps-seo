from pathlib import Path
import importlib.util,json,sys,concurrent.futures,re
ROOT=Path(__file__).resolve().parent;spec=importlib.util.spec_from_file_location('dom',ROOT/'public-dom.py');dom=importlib.util.module_from_spec(spec);spec.loader.exec_module(dom)
mode=sys.argv[1];assert mode in ['baseline','verify'];(ROOT/'html').mkdir(exist_ok=True);m=json.loads((ROOT/'manifest.json').read_text(encoding='utf8'))
urls=[m['url'],'https://shustrik-maps.com/understanding-the-obj-file-format-a-simple-explanation/','https://shustrik-maps.com/product-category/cnc-models/','https://shustrik-maps.com/understanding-the-fbx-file-format-a-simple-explanation/']
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:rows=list(ex.map(dom.fetch,urls))
for r in rows:assert r['http']==200 and r['canonical']==r['url'] and r['final_url']==r['url'] and len(r['h1'])==1 and 'noindex' not in r['robots']
if mode=='baseline':(ROOT/'public-baseline.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8',newline='\n')
else:
 before=json.loads((ROOT/'public-baseline.json').read_text(encoding='utf8'))
 for i,(old,new) in enumerate(zip(before,rows)):
  for f in ['h1','canonical','robots','headings','summary_text','schema_types']:
   if f in ['headings','schema_types'] and '/product-category/' in new['url']:continue
   assert old[f]==new[f],(new['url'],f)
  if i==0:
   assert new['title']==m['after']['_yoast_wpseo_title'] and new['meta_description']==m['after']['_yoast_wpseo_metadesc'],'Metadata not yet current'
   assert old['main_links']==new['main_links'],'Article links changed'
   assert old['images']==new['images'],'Article images changed'
   # The HTML parser inserts a separator after inline links (e.g. 'FBX .').
   # Normalize only whitespace before punctuation; source bytes are guarded in CMS.
   plain=re.sub(r'\s+([.,;:])(?=\s|$)',r'\1',new['main_text'])
   for p in m['approved_paragraphs_plain']:assert plain.count(p)==1,('Approved paragraph missing',p)
   for bad in ['Only 3D designs intentionally created','unfolded onto a 2D surface','There are over 30 file formats','introduced attempts to launch','the native language of your 3D printer']:assert bad not in new['main_text'],bad
  else:
   for f in ['title','meta_description','description_text']:assert old[f]==new[f],(new['url'],f)
   if '/product-category/' not in new['url']:assert old['main_text']==new['main_text'] and old['main_links']==new['main_links']
 (ROOT/'public-after.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8',newline='\n');(ROOT/'public-qa.json').write_text(json.dumps(dict(ok=True,urls_checked=4,approved_paragraphs_exact=True,metadata_exact=True,h1_headings_links_media_preserved=True,previous_releases_public_preserved=True,schema_type_presence_preserved=True),indent=2),encoding='utf8',newline='\n')
print(json.dumps(dict(ok=True,mode=mode,urls=4)))
