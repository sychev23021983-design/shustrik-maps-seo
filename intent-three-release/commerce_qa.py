import json,re,time,urllib.request,urllib.parse,http.cookiejar
from pathlib import Path
from html.parser import HTMLParser
root=Path(__file__).parent;base='https://shustrik-maps.com';headers={'User-Agent':'ShustrikPortfolioQA/1.0'}
class Links(HTMLParser):
 def __init__(self):super().__init__();self.remove=[]
 def handle_starttag(self,t,a):
  a=dict(a)
  if t=='a' and 'remove' in a.get('class','').split():self.remove.append(a['href'])
jar=http.cookiejar.CookieJar();opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar));steps=[]
def get(url,label):
 with opener.open(urllib.request.Request(url,headers=headers),timeout=40) as r:
  body=r.read().decode();steps.append({'step':label,'http':r.status,'cache':r.headers.get('X-Page-Cache','')});return body
assert 'cart-empty' in get(base+'/cart/','initial empty isolated cart')
remove=None
try:
 get(base+'/product/illinois-satellite-map/?add-to-cart=17483','add Illinois')
 body=get(base+'/cart/','one product cart');p=Links();p.feed(body);assert len(p.remove)==1;remove=p.remove[0]
 assert 'Illinois Satellite Map' in body and '15.00' in body
 body=get(base+'/checkout/','checkout before payment');assert re.search(r'<form[^>]*class="[^"]*checkout',body) and 'payment_methods' in body
finally:
 if remove:
  assert urllib.parse.urlsplit(remove).hostname=='shustrik-maps.com';get(remove,'remove test item')
 body=get(base+'/cart/','final empty cart');assert 'cart-empty' in body
media=[]
for row in json.loads((root/'public-after.json').read_text())['rows']:
 name={17483:'illinois',16047:'jupiter',15996:'mercury'}[row['id']]
 url=next(u for u in row['images'] if name in u.lower() and '-300x300' not in u)
 with urllib.request.urlopen(urllib.request.Request(url,headers=headers,method='HEAD'),timeout=30) as r:
  media.append({'id':row['id'],'http':r.status,'type':r.headers.get('Content-Type')});assert r.status==200 and r.headers.get('Content-Type','').startswith('image/')
out={'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'ok':True,'steps':steps,'media':media,'cart_final_empty':True,'order_created':False,'payment_submitted':False,'customer_data_entered':False,'payment_js_tested':False}
(root/'commerce-media.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print(json.dumps(out))
