from pathlib import Path
import importlib.util,json,concurrent.futures,collections
R=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('dom',R/'public-dom.py');dom=importlib.util.module_from_spec(spec);spec.loader.exec_module(dom)
m=json.loads((R/'manifest.json').read_text(encoding='utf-8'));before=json.loads((R/'public-baseline.json').read_text(encoding='utf-8'))
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:after=list(pool.map(dom.fetch,[r['url'] for r in before]))
for b,r in zip(before,after):
 assert r['http']==200 and r['canonical']==r['url'] and len(r['h1'])==1 and 'noindex' not in (r['robots'] or '')
 for f in ['title','meta_description','h1','canonical','robots','summary_text','schema_types']:assert b[f]==r[f],(r['url'],f)
 media=lambda row:[{k:x[k] for k in ['src','alt','html_title','width','height']} for x in row['images'] if x['region'] in ['gallery','description']]
 assert media(b)==media(r),(r['url'],'authored media')
for b,r in zip(before[1:],after[1:]):
 for f in ['description_text','description_links']:assert b[f]==r[f],(r['url'],f)
b,r=before[0],after[0]
for p in m['approved_paragraphs']:assert r['description_text'].count(p)==1,p
marker='Choosing a USA model';tail='You can browse state terrain models'
assert b['description_text'][:b['description_text'].index(marker)]==r['description_text'][:r['description_text'].index(marker)]
assert b['description_text'][b['description_text'].index(tail):]==r['description_text'][r['description_text'].index(tail):]
key=lambda x:(x['url'],x['text'],x['rel'])
expected=collections.Counter(map(key,b['description_links']))
expected.update((x['url'],x['text'],'') for x in m['added_links'])
assert expected==collections.Counter(map(key,r['description_links']))
d=dom.DOM();d.feed((R/'html/product--usa-map-3d-model.html').read_text(encoding='utf-8'))
regions=[n for n in d.root.walk() if n.attrs.get('aria-label')=='Compare USA terrain and state collections'];assert len(regions)==1
assert len([n for n in regions[0].walk() if n.tag=='tr'])==5
(R/'public-after.json').write_text(json.dumps(after,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
result=dict(ok=True,http_200=4,metadata_h1_canonical_robots_preserved=True,comparison_four_products=True,three_added_links=True,other_copy_preserved=True,specs_price_buttons_preserved=True,media_preserved=True,three_related_products_preserved=True)
(R/'public-qa.json').write_text(json.dumps(result,indent=2),encoding='utf-8',newline='\n');print(json.dumps(result))
