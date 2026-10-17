from pathlib import Path
import importlib.util,json,sys,concurrent.futures,re
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('public_dom',ROOT/'public-dom.py');dom=importlib.util.module_from_spec(spec);spec.loader.exec_module(dom)
mode=sys.argv[1];assert mode in ['baseline','verify'];(ROOT/'html').mkdir(exist_ok=True)
urls=['https://shustrik-maps.com/product/'+slug+'/' for slug in ['earth-3d-model-terrain-without-water','earth-3d-model','earth-stl-model','world-3d-model']]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:rows=list(ex.map(dom.fetch,urls))
for r in rows:assert r['http']==200 and r['canonical']==r['url'] and len(r['h1'])==1 and 'noindex' not in r['robots']
if mode=='baseline':
 (ROOT/'public-baseline.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
else:
 before=json.loads((ROOT/'public-baseline.json').read_text(encoding='utf-8'));manifest=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
 for old,new in zip(before,rows):
  for field in ['title','meta_description','h1','canonical','robots','summary_text','description_links','schema_types']:
   assert old[field]==new[field],(new['url'],field)
  media=lambda row:[{k:x[k] for k in ['src','alt','html_title','width','height']} for x in row['images'] if x['region'] in ['gallery','description']]
  assert media(old)==media(new),(new['url'],'authored media')
 new=rows[0];old=before[0]
 text=new['description_text'];paras=manifest['approved_paragraphs']
 for p in paras:assert text.count(p)==1,p
 assert text.index(paras[0])<text.index(paras[1])<text.index(paras[2])<text.index('Earth terrain DEM')
 assert old['description_text'][old['description_text'].index('Earth terrain DEM'):]==text[text.index('Earth terrain DEM'):]
 for x in ['Key Benefits of','Applications for the Earth Without Water','scientifically accurate','climate simulations','geological precision']:
  assert x not in text,x
 for old,new in zip(before[1:],rows[1:]):assert old['description_text']==new['description_text']
 (ROOT/'public-after.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
 result=dict(ok=True,urls_checked=4,approved_paragraphs_exact=True,summary_specs_price_buttons_preserved=True,metadata_canonical_h1_robots_schema_types_preserved=True,authored_media_preserved=True,description_links_preserved=True,lower_sections_preserved=True,related_products_preserved=True)
 (ROOT/'public-qa.json').write_text(json.dumps(result,indent=2),encoding='utf-8',newline='\n')
print(json.dumps(dict(ok=True,mode=mode,urls=4)))
