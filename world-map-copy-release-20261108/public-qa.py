from pathlib import Path
import importlib.util,json,concurrent.futures
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('dom',ROOT/'public-dom.py');dom=importlib.util.module_from_spec(spec);spec.loader.exec_module(dom)
m=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
urls=[m['url'],'https://shustrik-maps.com/product/world-3d-model/']
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:rows=list(pool.map(dom.fetch,urls))
baselines=[json.loads((ROOT/name).read_text(encoding='utf-8')) for name in ['public-baseline.json','other-world-baseline.json']]
for b,r in zip(baselines,rows):
 assert r['http']==200 and r['canonical']==r['url'] and len(r['h1'])==1 and 'noindex' not in (r['robots'] or '')
 for field in ['h1','canonical','robots','summary_text','description_links','schema_types']:assert b[field]==r[field],(r['url'],field)
 media=lambda row:[{k:x[k] for k in ['src','alt','html_title','width','height']} for x in row['images'] if x['region'] in ['gallery','description']]
 assert media(b)==media(r),(r['url'],'authored media')
b,r=baselines[0],rows[0]
assert r['title']==m['after']['_yoast_wpseo_title'] and r['meta_description']==m['after']['_yoast_wpseo_metadesc']
for p in m['approved_paragraphs']:assert r['description_text'].count(p)==1,p
for h in m['approved_headings']:assert any(n=={'tag':'h2','text':h} for n in r['headings']),h
marker='In addition to the 3D terrain model of the World'
assert b['description_text'][b['description_text'].index(marker):]==r['description_text'][r['description_text'].index(marker):]
for phrase in ['interactive globe','stunning accuracy','spatial analysis','global dataset']:assert phrase not in r['description_text'],phrase
for field in ['title','meta_description','description_text']:assert baselines[1][field]==rows[1][field],('other World changed',field)
for name,row in zip(['public-after.json','other-world-after.json'],rows):(ROOT/name).write_text(json.dumps(row,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
result=dict(ok=True,http_200=2,title_meta_match=True,one_h1=True,canonical_robots_preserved=True,paragraphs_headings_match=True,summary_specs_price_buttons_preserved=True,authored_media_preserved=True,description_links_preserved=True,lower_sections_preserved=True,schema_types_preserved=True,other_world_preserved=True)
(ROOT/'public-qa.json').write_text(json.dumps(result,indent=2),encoding='utf-8',newline='\n')
print(json.dumps(result))
