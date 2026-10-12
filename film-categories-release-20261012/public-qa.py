from pathlib import Path
import json,sys,urllib.request,concurrent.futures
from lxml import html
ROOT=Path(__file__).parent
def fetch(url):
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=45) as r:return {'http':r.status,'url':r.url,'body':r.read()}
def cls(n):return "contains(concat(' ',normalize-space(@class),' '),' "+n+" ')"
def txt(n):return ' '.join(n.text_content().split())
def first(a):return a[0] if a else None
def state(c):
 r=fetch(c['url']);t=html.fromstring(r['body'].decode('utf-8'));cards=[]
 for card in t.xpath('//main//*['+cls('product-grid-item')+']'):
  h=first(card.xpath('.//*['+cls('wd-entities-title')+' or '+cls('woocommerce-loop-product__title')+']'));a=first(h.xpath('.//a')) if h is not None else None;p=first(card.xpath('.//*['+cls('price')+']'))
  if a is not None:cards.append({'url':a.get('href'),'title':txt(h),'price':txt(p) if p is not None else ''})
 schema=[]
 for script in t.xpath('//script[@type="application/ld+json"]'):
  try:payload=json.loads(script.text or '')
  except ValueError:continue
  graph=payload.get('@graph',[payload]) if isinstance(payload,dict) else payload
  schema.extend(e.get('@type') for e in graph if isinstance(e,dict))
 def attr(x,n):a=first(t.xpath(x));return a.get(n) if a is not None else None
 block=first(t.xpath('//*['+cls('shustrik-film-'+c['key']+'-category')+']'))
 retained_links=sorted(t.xpath('//main//a[not(ancestor::section['+cls('shustrik-film-'+c['key']+'-category')+'])]/@href'))
 retained_images=sorted(t.xpath('//main//img[not(ancestor::section['+cls('shustrik-film-'+c['key']+'-category')+'])]/@data-src')+t.xpath('//main//img[not(@data-src) and not(ancestor::section['+cls('shustrik-film-'+c['key']+'-category')+'])]/@src'))
 s={'http':r['http'],'url':r['url'],'title':' '.join(t.xpath('//title/text()')),'description':attr('//meta[@name="description"]','content'),'canonical':attr('//link[@rel="canonical"]','href'),'robots':attr('//meta[@name="robots"]','content'),'h1':[txt(h) for h in t.xpath('//h1')],'cards':cards,'schema_types':schema,'pagination_present':bool(t.xpath('//*['+cls('woocommerce-pagination')+' or '+cls('wd-pagination')+']')),'retained_h4':[txt(h) for h in t.xpath('//main//h4')],'retained_main_links':retained_links,'retained_main_images':retained_images}
 return t,block,s
mode=sys.argv[1]
if mode=='baseline':
 cats=json.loads((ROOT/'baseline.json').read_text(encoding='utf-8'))['categories'];keys={69:'islands',62:'countries',81:'states',91:'provinces'}
 for c in cats:c['key']=keys[c['term_id']]
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:out=list(pool.map(state,cats))
 result={c['key']:s for c,(_,_,s) in zip(cats,out)};assert all(s['http']==200 and s['cards'] for s in result.values())
 (ROOT/'public-baseline.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');print(json.dumps({k:{'http':s['http'],'cards':len(s['cards']),'h1':s['h1']} for k,s in result.items()}))
else:
 assert mode=='verify';m=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'));baseline=json.loads((ROOT/'public-baseline.json').read_text(encoding='utf-8'));results={};endpoints=set();media_urls={}
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:out=list(pool.map(state,m['categories']))
 for c,(t,block,s) in zip(m['categories'],out):
  checks={f+'_preserved':s[f]==baseline[c['key']][f] for f in ['title','description','canonical','robots','cards','schema_types','pagination_present','retained_h4']}
  checks['h1']=s['h1']==[c['h1']];checks['block_exists']=block is not None;checks['images']=block is not None and len(block.xpath('.//img'))==4;checks['article_links']=block is not None and len(block.xpath('.//article//a'))==8;checks['disclosure']=block is not None and 'These are still images' in txt(block);checks['bottom_position']=bool(block is not None and block.xpath('preceding::*['+cls('product-grid-item')+']'))
  if c['key']=='states':
   checks['shared_collection_links_preserved']=s['retained_main_links']==baseline['states']['retained_main_links'];checks['shared_collection_images_preserved']=s['retained_main_images']==baseline['states']['retained_main_images']
  urls=[]
  if block is not None:
   endpoints.update(block.xpath('.//a/@href'))
   for im in block.xpath('.//img'):
    u=im.get('data-src') or im.get('src');urls.append(u);media_urls[u]={'alt':im.get('alt'),'width':im.get('width'),'height':im.get('height')}
  results[c['key']]={'checks':checks,'state':s,'image_urls':urls}
 endpoints.update(media_urls);endpoints.update(['https://shustrik-maps.com/','https://shustrik-maps.com/cart/','https://shustrik-maps.com/checkout/'])
 def endpoint(u):r=fetch(u);return u,{'http':r['http'],'url':r['url'],'bytes':len(r['body'])}
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:responses=dict(pool.map(endpoint,sorted(endpoints)))
 for k,res in results.items():
  res['checks']['media_http_alt']=len(res['image_urls'])==4 and all(responses[u]['http']==200 and media_urls[u]['alt'] for u in res['image_urls']);res['ok']=all(res['checks'].values())
 health={u:responses[u] for u in ['https://shustrik-maps.com/','https://shustrik-maps.com/cart/','https://shustrik-maps.com/checkout/']};result={'ok':all(r['ok'] for r in results.values()) and all(r['http']==200 for r in responses.values()),'categories':results,'media':media_urls,'endpoints':responses,'health':health}
 (ROOT/'public-qa.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');print(json.dumps({'ok':result['ok'],'categories':{k:r['checks'] for k,r in results.items()},'endpoints':len(responses)}));assert result['ok']
