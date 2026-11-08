from pathlib import Path
import runpy,json,concurrent.futures
from collections import Counter
root=Path(__file__).resolve().parent
fetch=runpy.run_path(str(root/'public-dom.py'))['fetch']
m=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
baselines=json.loads((root/'public-baseline.json').read_text(encoding='utf-8'))
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool: rows=list(pool.map(fetch,[r['url'] for r in baselines]))
for b,r in zip(baselines,rows):
 assert r['http']==200 and r['canonical']==r['url'] and len(r['h1'])==1 and 'noindex' not in (r['robots'] or '')
 for field in ['h1','canonical','robots','summary_text','schema_types']:assert b[field]==r[field],(r['url'],field)
 media=lambda row:[{k:x[k] for k in ['src','alt','html_title','width','height']} for x in row['images'] if x['region'] in ['gallery','description']]
 assert media(b)==media(r),(r['url'],'authored media')
b,r=baselines[0],rows[0]
assert r['title']==m['after']['_yoast_wpseo_title'] and r['meta_description']==m['after']['_yoast_wpseo_metadesc']
for p in m['approved_paragraphs']:assert r['description_text'].count(p)==1,p
for h in m['approved_headings']:assert any(n=={'tag':'h2','text':h} for n in r['headings']),h
marker='Note: The boundary outline'
assert b['description_text'][b['description_text'].index(marker):]==r['description_text'][r['description_text'].index(marker):]
links=lambda xs:Counter((x['url'],x['text'],x['rel']) for x in xs)
assert links(b['description_links'])+links(m['added_links'])==links(r['description_links'])
for phrase in ['unparalleled','immersive','meticulously']:assert phrase not in r['description_text'],phrase
for b,r in zip(baselines[1:],rows[1:]):
 for field in ['title','meta_description','description_text','description_links']:assert b[field]==r[field],(r['url'],field)
(root/'public-after.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
result=dict(ok=True,http_200=3,title_meta_match=True,one_h1=True,canonical_robots_preserved=True,paragraphs_headings_match=True,summary_specs_price_buttons_preserved=True,authored_media_preserved=True,old_links_preserved=True,one_stl_link_added=True,boundary_warning_lower_sections_preserved=True,schema_types_preserved=True,two_related_products_preserved=True)
(root/'public-qa.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result))
