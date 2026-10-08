from pathlib import Path
import json,shutil
from urllib.parse import quote_plus
root=Path(__file__).parent;out=Path('J:/1. My Vault/90 Migration/shustrik-maps-seo/five-mixed-stl-slider-release-20261008')
queries={'israel':'Israel topographic map STL','israel-extended':'Israel extended coverage terrain STL','zimbabwe':'Zimbabwe terrain map STL','geoid':'artistic geoid height STL','modular-earth':'modular Earth globe STL dodecahedron'}
obs={'israel':'Paid STL marketplace listings and free Printables files observed. Country STL digital intent supported; reference-specific outline retained.','israel-extended':'Paid author STL result with125MB specification alongside free terrain, broader surrounding-area files and unrelated simulation terrain. Extended coverage is an editorial SKU distinction supported by the own listing, not measured keyword demand. Keep separate file/reference; no territorial expansion.','zimbabwe':'Paid own/author STL listings, free Thingiverse terrain and ordinary relief/elevation maps observed. Target digital terrain file, not physical model or ordinary map.','geoid':'Paid artistic geoid author/own listings alongside free geophysical globe and geodesy/elevation outputs. Retain artistic conceptual scope, no scientific precision claims.','modular-earth':'Own12-part STL and other modular/rhombic globe, paper-polyhedron and ordinary globe results observed. Preserve own regular-dodecahedron12part listing; exclude paper and rhombic alternatives. AI Overview claims ignored.'}
m=json.loads((root/'manifest.json').read_text(encoding='utf-8'));rows=[]
for r in m['rows']:
 slug=r['slug'];raw=(root/('google-'+slug+'.txt')).read_text(encoding='utf-8');assert 'Search Results' in raw and queries[slug] in raw and 'Unknown' in raw
 rows.append({'product_id':r['id'],'query':queries[slug],'url':'https://www.google.com/search?q='+quote_plus(queries[slug])+'&hl=en&gl=us&pws=0','google_raw':'google-'+slug+'.txt','observation':obs[slug],'primary_source':r['url'],'frequency':None,'rank':None,'actual_us_location_confirmed':False})
e={'date':'2026-10-08','market':'USA','language':'English','parameters':{'hl':'en','gl':'us','pws':0},'location_footer':'Unknown / cannot determine location','metrics_measured':False,'rows':rows}
(root/'intent-evidence.json').write_text(json.dumps(e,ensure_ascii=False,indent=2),encoding='utf-8')
s=json.loads((root/'semantic-review.json').read_text(encoding='utf-8'));s.update(fresh_intent_evidence='intent-evidence.json',google_results_observed=5,location_confirmed=False);(root/'semantic-review.json').write_text(json.dumps(s,ensure_ascii=False,indent=2),encoding='utf-8')
t='# Intent Review — five distinct STL products\n\nGoogle English / USA parameters. Actual location Unknown; frequency and rank not measured. Existing saved core checked; editorial mappings only. Sources and original own listing snapshots support file scope.\n'
for r in m['rows']:t+='\n## '+r['name']+'\n\n'+obs[r['slug']]+'\n\nSource: ['+r['name']+']('+r['url']+'); saved original content [[baseline.json]]. Google evidence: [[google-'+r['slug']+'.txt]].\n'
(root/'Intent Review.md').write_text(t,encoding='utf-8')
for n in ['semantic-review.json','intent-evidence.json','Intent Review.md','finish-semantic-mixed.py']+['google-'+r['slug']+'.txt' for r in m['rows']]:shutil.copy2(root/n,out/n)
print('Five observed Google intent checks saved; no measured frequencies/ranks')
