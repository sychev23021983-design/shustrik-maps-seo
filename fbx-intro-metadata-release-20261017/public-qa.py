from pathlib import Path
import importlib.util,json,sys,concurrent.futures
ROOT=Path(__file__).resolve().parent;spec=importlib.util.spec_from_file_location('dom',ROOT/'public-dom.py');dom=importlib.util.module_from_spec(spec);spec.loader.exec_module(dom)
mode=sys.argv[1];assert mode in ['baseline','verify'];(ROOT/'html').mkdir(exist_ok=True);m=json.loads((ROOT/'manifest.json').read_text(encoding='utf8'))
urls=[m['url'],'https://shustrik-maps.com/product-category/3d-models/','https://shustrik-maps.com/product/moon-3d-model/','https://shustrik-maps.com/product/sydney-opera-house-3d-model/']
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:rows=list(ex.map(dom.fetch,urls))
for r in rows:assert r['http']==200 and r['canonical']==r['url'] and len(r['h1'])==1 and 'noindex' not in r['robots']
if mode=='baseline':(ROOT/'public-baseline.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8',newline='\n')
else:
 before=json.loads((ROOT/'public-baseline.json').read_text(encoding='utf8'))
 for i,(old,new) in enumerate(zip(before,rows)):
  for field in ['h1','canonical','robots','summary_text','main_links','schema_types']:
   if i>0 and field=='main_links':continue
   assert old[field]==new[field],(new['url'],field)
  if i==0:
   assert new['title']==m['after']['_yoast_wpseo_title'] and new['meta_description']==m['after']['_yoast_wpseo_metadesc'],'New title/meta not yet visible'
   for para in m['approved_paragraphs']:assert new['main_text'].count(para)==1,para
   assert old['main_text'][old['main_text'].index('CAPABILITIES AND FEATURES'):]==new['main_text'][new['main_text'].index('CAPABILITIES AND FEATURES'):],'Remainder public text changed'
   assert [x['src'] for x in old['images']]==[x['src'] for x in new['images']],'Article images changed'
   assert any(x['text']=='3D terrain model catalog' and x['url']==urls[1] for x in new['main_links'])
  else:
   for field in ['title','meta_description','description_text']:assert old[field]==new[field],(new['url'],field)
 (ROOT/'public-after.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8',newline='\n')
 (ROOT/'public-qa.json').write_text(json.dumps(dict(ok=True,urls_checked=4,metadata_intro_exact=True,h1_body_remainder_images_links_canonical_robots_preserved=True,previous_moon_sydney_metadata_preserved=True,schema_type_presence_preserved=True),indent=2),encoding='utf8',newline='\n')
print(json.dumps(dict(ok=True,mode=mode,urls=4)))
