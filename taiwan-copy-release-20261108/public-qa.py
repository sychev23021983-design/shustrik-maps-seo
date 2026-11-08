from pathlib import Path
import importlib.util,json,sys
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('public_dom',ROOT/'public-dom.py');dom=importlib.util.module_from_spec(spec);spec.loader.exec_module(dom)
mode=sys.argv[1];assert mode in ['baseline','verify'];(ROOT/'html').mkdir(exist_ok=True)
m=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
r=dom.fetch(m['url'])
assert r['http']==200 and r['canonical']==r['url'] and r['h1']==['Taiwan Terrain 3D model'] and 'noindex' not in (r['robots'] or '')
if mode=='baseline':
 (ROOT/'public-baseline.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
else:
 b=json.loads((ROOT/'public-baseline.json').read_text(encoding='utf-8'))
 assert r['title']==m['after']['_yoast_wpseo_title']
 assert r['meta_description']==m['after']['_yoast_wpseo_metadesc']
 for field in ['h1','canonical','robots','summary_text','description_links','schema_types']:assert b[field]==r[field],field
 media=lambda row:[{k:x[k] for k in ['src','alt','html_title','width','height']} for x in row['images'] if x['region'] in ['gallery','description']]
 assert media(b)==media(r),'Authored images changed'
 for p in m['approved_paragraphs']:assert r['description_text'].count(p)==1,p
 marker='Taiwan DEM'
 assert b['description_text'][b['description_text'].index(marker):]==r['description_text'][r['description_text'].index(marker):],'Lower sections changed'
 assert 'precision parts and components' not in r['description_text']
 (ROOT/'public-after.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
 (ROOT/'public-qa.json').write_text(json.dumps(dict(ok=True,http=200,title_meta_match=True,one_h1=True,canonical_robots_preserved=True,paragraphs_match=True,summary_specs_price_buttons_preserved=True,authored_media_preserved=True,description_links_preserved=True,lower_sections_preserved=True,schema_types_preserved=True),indent=2),encoding='utf-8',newline='\n')
print(json.dumps(dict(ok=True,mode=mode,url=r['url'],title=r['title']),ensure_ascii=False))
