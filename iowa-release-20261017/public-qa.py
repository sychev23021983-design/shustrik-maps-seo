from pathlib import Path
import importlib.util,json,sys,concurrent.futures,re
ROOT=Path(__file__).resolve().parent;spec=importlib.util.spec_from_file_location('dom',ROOT/'public-dom.py');dom=importlib.util.module_from_spec(spec);spec.loader.exec_module(dom)
mode=sys.argv[1];assert mode in ['baseline','verify'];(ROOT/'html').mkdir(exist_ok=True);m=json.loads((ROOT/'manifest.json').read_text(encoding='utf8'))
urls=[m['url'],'https://shustrik-maps.com/product/united-states-night-satellite-map/','https://shustrik-maps.com/product/china-satellite-map/','https://shustrik-maps.com/product/florida-satellite-map/']
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:rows=list(ex.map(dom.fetch,urls))
for r in rows:
 raw=(ROOT/'html'/('product--'+r['url'].rstrip('/').split('/')[-1]+'.html')).read_text(encoding='utf8')
 schemas=[json.loads(x) for x in re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',raw,re.S)]
 nodes=[]
 def walk(x):
  if isinstance(x,dict):
   nodes.append(x)
   for v in x.values():walk(v)
  elif isinstance(x,list):
   for v in x:walk(v)
 for s in schemas:walk(s)
 products=[x for x in nodes if x.get('@type')=='Product' or (isinstance(x.get('@type'),list) and 'Product' in x['@type'])]
 assert len(products)==1,'Expected one Product schema'
 product=products[0];r['commerce_schema']={k:product.get(k) for k in ['@id','name','sku','offers']}
 assert product.get('offers'),'Product offers missing'
 r['purchase_cta_present']='single_add_to_cart_button' in raw and 'Add to cart' in raw
 assert r['purchase_cta_present'],'Purchase CTA missing'
for r in rows:assert r['http']==200 and r['canonical']==r['url'] and r['final_url']==r['url'] and len(r['h1'])==1 and 'noindex' not in r['robots']
if mode=='baseline':(ROOT/'public-baseline.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8',newline='\n')
else:
 before=json.loads((ROOT/'public-baseline.json').read_text(encoding='utf8'))
 for i,(old,new) in enumerate(zip(before,rows)):
  for f in ['h1','canonical','robots','schema_types','commerce_schema','purchase_cta_present']:assert old[f]==new[f],(new['url'],f)
  if i==0:
   assert new['title']==m['after']['_yoast_wpseo_title'] and new['meta_description']==m['after']['_yoast_wpseo_metadesc'],'Metadata not yet current'
   assert old['summary_text'].replace(m['old_phrase_rendered'],m['short_phrase'],1)==new['summary_text'],'Summary changed beyond approved phrase'
   expected=' '.join(m['approved_paragraphs'])+' '+old['description_text'][old['description_text'].index('FAQ'):]
   assert new['description_text']==expected,'Description or FAQ mismatch'
   assert old['description_links']==new['description_links'],'Description links changed'
   images=lambda r:[x for x in r['images'] if x['region'] in ['gallery','description']]
   assert images(old)==images(new),'Authored images changed'
  else:
   for f in ['title','meta_description','description_text','summary_text']:assert old[f]==new[f],(new['url'],f)
 (ROOT/'public-after.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8',newline='\n');(ROOT/'public-qa.json').write_text(json.dumps(dict(ok=True,urls_checked=4,approved_description_exact=True,metadata_exact=True,short_phrase_exact=True,faq_specs_h1_links_authored_media_preserved=True,other_three_products_unchanged=True,schema_type_presence_preserved=True),indent=2),encoding='utf8',newline='\n')
print(json.dumps(dict(ok=True,mode=mode,urls=4)))
