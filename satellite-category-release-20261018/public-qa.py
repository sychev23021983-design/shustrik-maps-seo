from pathlib import Path
import importlib.util,json,sys,concurrent.futures,re,html,unicodedata
ROOT=Path(__file__).resolve().parent;spec=importlib.util.spec_from_file_location('dom',ROOT/'public-dom.py');dom=importlib.util.module_from_spec(spec);spec.loader.exec_module(dom)
m=json.loads((ROOT/'manifest.json').read_text(encoding='utf8'));targets={p['id']:p for p in m['products']};baseline=json.loads((ROOT/'public-before.json').read_text(encoding='utf8'));before={r['id']:r['public'] for r in baseline};mode=sys.argv[1]
def norm(s):return re.sub(r'\s+',' ',unicodedata.normalize('NFKC',html.unescape(s)).translate(str.maketrans({'’':"'",'‘':"'",'–':'-','—':'-'}))).strip()
def body_text(s):
 d=dom.DOM();d.feed(s);return norm(d.root.text())
def enrich(row,raw):
 schemas=[json.loads(x) for x in re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',raw,re.S)];nodes=[]
 def walk(x):
  if isinstance(x,dict):
   nodes.append(x)
   for v in x.values():walk(v)
  elif isinstance(x,list):
   for v in x:walk(v)
 for s in schemas:walk(s)
 ps=[x for x in nodes if x.get('@type')=='Product' or isinstance(x.get('@type'),list) and 'Product' in x['@type']];assert len(ps)==1,'Product count'
 row['commerce_schema']={k:ps[0].get(k) for k in ['@id','name','sku','offers']};assert ps[0].get('offers'),'No offer'
 row['purchase_cta_present']='single_add_to_cart_button' in raw and 'Add to cart' in raw;assert row['purchase_cta_present'],'No purchase CTA'
 return row
if mode=='baseline':
 source=ROOT.parent.parent.parent/'01 Projects/WordPress/shustrik-maps.com/Satellite Category Audit 2026-10-18/html'
 for row in baseline:
  p=row['public'];raw=(source/('product--'+p['url'].rstrip('/').split('/')[-1]+'.html')).read_text(encoding='utf8');enrich(p,raw)
 (ROOT/'public-before.json').write_text(json.dumps(baseline,ensure_ascii=False,indent=2),encoding='utf8',newline='\n');print(json.dumps({'baseline':len(baseline),'commerce_schema_parsed':True}));sys.exit()
assert mode=='verify';(ROOT/'html').mkdir(exist_ok=True)
def one(item):
 id=item['id'];old=item['public'];checks=[]
 try:
  new=dom.fetch(old['url']);raw=(ROOT/'html'/('product--'+old['url'].rstrip('/').split('/')[-1]+'.html')).read_text(encoding='utf8');enrich(new,raw)
  assert new['http']==200,'HTTP';assert old['final_url']==new['final_url'],'Redirect destination drift'
  # Redirected variants remain deferred: their destination is another edited product.
  if id in [17585,17717,17876]:return {'id':id,'ok':True,'status':'deferred-redirect','public':new}
  for f in ['h1','canonical','robots','schema_types','commerce_schema','purchase_cta_present']:assert old[f]==new[f],f
  assert new['final_url']==new['url'] and new['canonical']==new['url'] and len(new['h1'])==1 and 'noindex' not in new['robots'],'Indexability'
  images=lambda r:[{k:v for k,v in x.items() if k not in ['loading','classes','context']} for x in r['images'] if x['region'] in ['gallery','description']]
  assert images(old)==images(new),'Authored images'
  assert old['description_links']==new['description_links'],'Description links'
  if id in targets:
   p=targets[id];assert new['title']==p['after']['_yoast_wpseo_title'] and new['meta_description']==p['after']['_yoast_wpseo_metadesc'],'Metadata not current'
   summary=norm(new['summary_text']);old_summary=norm(old['summary_text']);e=p['excerpt_edit'];old_lead=body_text(e['old']);new_lead=body_text(e['text'])
   if old_lead:expected=old_summary.replace(old_lead,new_lead,1);assert old_lead in old_summary,'Old lead missing'
   else:
    assert id==19462;start=old_summary.index('Format:');expected=old_summary[:start]+new_lead+' '+old_summary[start:]
   assert summary==expected,'Summary/specifications changed beyond lead'
   desc=norm(new['description_text'])
   for text in p['paragraphs']:assert norm(text) in desc,'New paragraph missing'
   if id!=19462:
    at=old['description_text'].index('FAQ');assert norm(old['description_text'][at:])==desc[desc.index('FAQ'):],'FAQ or authored tail changed'
   else:
    for caption in ['Source map in AuthaGraph projection','Triangular map with Antarctica in the center','Map with the North Pole in the center','A map with Africa in the center','Color Map with country names','Color Map with Borders']:assert norm(caption) in desc,'Example caption missing'
  else:
   for f in ['title','meta_description','description_text','summary_text']:assert old[f]==new[f],f
  return {'id':id,'ok':True,'status':'published-check-passed' if id in targets else 'preserved','public':new}
 except Exception as e:return {'id':id,'ok':False,'reason':str(e),'public':locals().get('new')}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:rows=list(pool.map(one,baseline))
result={'ok':all(r['ok'] for r in rows),'urls_checked':len(rows),'edited_checked':sum(r['ok'] and r['status']=='published-check-passed' for r in rows),'preserved_checked':sum(r['ok'] and r['status']=='preserved' for r in rows),'deferred_redirects':sum(r['ok'] and r['status']=='deferred-redirect' for r in rows),'failures':[{k:v for k,v in r.items() if k!='public'} for r in rows if not r['ok']]}
(ROOT/'public-after.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8',newline='\n');(ROOT/'public-qa.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8',newline='\n');print(json.dumps(result));sys.exit(0 if result['ok'] else 1)
