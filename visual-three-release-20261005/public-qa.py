import json,urllib.request,re,datetime,concurrent.futures
from pathlib import Path
from html.parser import HTMLParser
root=Path(__file__).parent
baseline=json.loads((root/'baseline.json').read_text(encoding='utf-8-sig'))['rows']
manifest=json.loads((root/'manifest.json').read_text(encoding='utf-8'))['products']
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.stack=[];self.title=[];self.h1=[];self.meta=[];self.canonical=[];self.robots=[];self.ld=[];self.current=[];self.inld=False;self.text=[];self.images=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs);self.stack.append(tag)
  if tag=='h1':self.h1.append([])
  if tag=='meta' and a.get('name')=='description':self.meta.append(a.get('content',''))
  if tag=='meta' and a.get('name')=='robots':self.robots.append(a.get('content',''))
  if tag=='link' and a.get('rel')=='canonical':self.canonical.append(a.get('href'))
  if tag=='script' and a.get('type')=='application/ld+json':self.inld=True;self.current=[]
  if tag=='img':self.images.append(a)
 def handle_endtag(self,tag):
  if tag=='script' and self.inld:self.ld.append(''.join(self.current));self.inld=False
  if tag in self.stack:self.stack=self.stack[:len(self.stack)-1-self.stack[::-1].index(tag)]
 def handle_data(self,data):
  if self.inld:self.current.append(data)
  if 'title' in self.stack:self.title.append(data)
  if 'h1' in self.stack:self.h1[-1].append(data)
  if not any(t in self.stack for t in ['script','style']):self.text.append(data)
def fetch(url):
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Shustrik scoped visual release QA'}),timeout=40) as q:return q.status,q.url,q.headers,q.read()
def inspect(i,uncached):
 b=baseline[i];m=manifest[i];url=b['url']+('?visual_three_qa=20261005' if uncached else '')
 status,final,headers,raw=fetch(url);p=Parser();p.feed(raw.decode('utf-8','replace'));text=' '.join(' '.join(p.text).split())
 title=''.join(p.title).strip();h1=[''.join(x).strip() for x in p.h1]
 schemas=[]
 for t in p.ld:
  try:
   d=json.loads(t);schemas+=d.get('@graph',[d]) if isinstance(d,dict) else d
  except json.JSONDecodeError:pass
 products=[x for x in schemas if isinstance(x,dict) and x.get('@type') in ['Product','ProductGroup']]
 checks={'http':status==200,'path':final.split('?')[0]==b['url'],'title':title==m['seo_title'],'meta':p.meta==[m['meta_description']],'h1':h1==[b['title']],'canonical':p.canonical==[b['url']],'indexable':bool(p.robots) and not any('noindex' in x for x in p.robots) and 'noindex' not in headers.get('X-Robots-Tag',''),'product_schema':bool(products) and any(x.get('offers') for x in products),'ai_notice':'not a photograph of a tested print' in text,'licence':'Commercial use requires separately agreed permission' in text,'no_raw_shortcodes':not re.search(r'\[(?:vc_|woodmart_|html_block)',text),'cta':'Add to cart' in text,'scene_images':all(any(im.get('alt')==a['alt'] and im.get('title')==a['title'] for im in p.images) for a in m['media'])}
 if b['id']==10668:checks['open_base']='open base' in text and 'closed printable volume' in text
 return {'id':b['id'],'url':url,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':checks,'title':title,'h1':h1,'robots':p.robots,'pass':all(checks.values())}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:rows=list(pool.map(lambda a:inspect(*a),[(i,u) for i in range(3) for u in [False,True]]))
verify=json.loads((root/'verify.json').read_text(encoding='utf-8-sig'))
media=[]
for r in verify['rows']:
 for a in r['media']:
  s,u,h,data=fetch(a['url']);media.append({'id':a['id'],'http':s,'content_type':h.get('Content-Type'),'bytes':len(data),'pass':s==200 and h.get('Content-Type','').startswith('image/webp')})
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'rows':rows,'media':media,'pass':all(x['pass'] for x in rows+media),'scope':'HTTP/media only; browser layout and commerce checked separately'}
(root/'public-qa.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out,ensure_ascii=False,indent=2));assert out['pass'],'Public QA failed'
