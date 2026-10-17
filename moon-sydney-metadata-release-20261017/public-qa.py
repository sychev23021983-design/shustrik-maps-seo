from pathlib import Path
import importlib.util,json,sys,concurrent.futures,html
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('public_dom',ROOT/'public-dom.py');dom=importlib.util.module_from_spec(spec);spec.loader.exec_module(dom)
mode=sys.argv[1];assert mode in ['baseline','verify'];(ROOT/'html').mkdir(exist_ok=True)
m=json.loads((ROOT/'manifest.json').read_text(encoding='utf8'));urls=[p['url'] for p in m['posts']]+['https://shustrik-maps.com/product/earth-3d-model-terrain-without-water/']
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:rows=list(ex.map(dom.fetch,urls))
for row in rows:assert row['http']==200 and row['canonical']==row['url'] and len(row['h1'])==1 and 'noindex' not in row['robots']
if mode=='baseline':(ROOT/'public-baseline.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8',newline='\n')
else:
 before=json.loads((ROOT/'public-baseline.json').read_text(encoding='utf8'))
 for i,(old,new) in enumerate(zip(before,rows)):
  for field in ['h1','canonical','robots','summary_text','description_text','description_links','schema_types']:assert old[field]==new[field],(new['url'],field)
  media=lambda r:[{k:x[k] for k in ['src','alt','html_title','width','height']} for x in r['images'] if x['region'] in ['gallery','description']]
  assert media(old)==media(new),(new['url'],'authored media')
  if i<2:
   assert new['title']==m['posts'][i]['after']['_yoast_wpseo_title'],(new['url'],'title')
   assert new['meta_description']==m['posts'][i]['after']['_yoast_wpseo_metadesc'],(new['url'],'description')
  else:assert old['title']==new['title'] and old['meta_description']==new['meta_description']
 (ROOT/'public-after.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8',newline='\n')
 (ROOT/'public-qa.json').write_text(json.dumps(dict(ok=True,urls_checked=3,metadata_exact=True,content_h1_summary_media_links_canonical_robots_preserved=True,earth_preserved=True,schema_type_presence_preserved=True),indent=2),encoding='utf8',newline='\n')
print(json.dumps(dict(ok=True,mode=mode,urls=3)))
