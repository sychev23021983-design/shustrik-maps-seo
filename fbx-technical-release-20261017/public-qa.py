from pathlib import Path
import importlib.util,json,sys,concurrent.futures
ROOT=Path(__file__).resolve().parent;spec=importlib.util.spec_from_file_location('dom',ROOT/'public-dom.py');dom=importlib.util.module_from_spec(spec);spec.loader.exec_module(dom)
mode=sys.argv[1];assert mode in ['baseline','verify'];(ROOT/'html').mkdir(exist_ok=True);m=json.loads((ROOT/'manifest.json').read_text(encoding='utf8'))
urls=[m['posts'][0]['url'],'https://shustrik-maps.com/understanding-the-obj-file-format-a-simple-explanation/','https://shustrik-maps.com/what-is-an-stl-file-explaining-the-stl-format/','https://shustrik-maps.com/product-category/3d-models/','https://shustrik-maps.com/product/moon-3d-model/','https://shustrik-maps.com/product/sydney-opera-house-3d-model/']
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:rows=list(ex.map(dom.fetch,urls))
for r in rows:assert r['http']==200 and r['canonical']==r['url'] and len(r['h1'])==1 and 'noindex' not in r['robots']
if mode=='baseline':(ROOT/'public-baseline.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8',newline='\n')
else:
 before=json.loads((ROOT/'public-baseline.json').read_text(encoding='utf8'))
 for i,(old,new) in enumerate(zip(before,rows)):
  for f in ['title','meta_description','h1','canonical','robots','headings','summary_text','schema_types']:assert old[f]==new[f],(new['url'],f)
  if i==0:
   assert old['main_links']==new['main_links'],'Article links changed'
   assert [x['src'] for x in old['images']]==[x['src'] for x in new['images']],'Article media changed'
   marker='CAPABILITIES AND FEATURES';assert old['main_text'][:old['main_text'].index(marker)]==new['main_text'][:new['main_text'].index(marker)],'Intro changed'
   for block in m['approved_blocks_plain']:assert new['main_text'].count(block)==1,'Approved block absent'
   for bad in ['all 3D object files can be 3D printed','boasts numerous useful features','topography data','Effects (e.g., fog)','featuring SDKs compatible with FBX files']:assert bad not in new['main_text'],bad
  elif '/product/' in new['url']:assert old['description_text']==new['description_text']
  elif i in [1,2]:assert old['main_text']==new['main_text'] and old['main_links']==new['main_links']
 (ROOT/'public-after.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8',newline='\n');(ROOT/'public-qa.json').write_text(json.dumps(dict(ok=True,urls_checked=6,five_blocks_exact=True,intro_metadata_h1_headings_links_media_preserved=True,previous_releases_public_preserved=True,schema_type_presence_preserved=True),indent=2),encoding='utf8',newline='\n')
print(json.dumps(dict(ok=True,mode=mode,urls=6)))
