import json,sys,re,html,time,urllib.request,urllib.parse
from pathlib import Path
from html.parser import HTMLParser
ROOT=Path(__file__).parent
rows=json.loads((ROOT/'proposals.json').read_text(encoding='utf-8-sig'))['products']
class Page(HTMLParser):
 def __init__(self):
  super().__init__(); self.meta={};self.canonical='';self.title='';self.h1=[];self.links=[];self.images=[];self.schema=[];self.cta=False;self.capture=None;self.buf=''
 def handle_starttag(self,t,a):
  a=dict(a)
  if t=='meta': self.meta[a.get('name','')]=a.get('content','')
  if t=='link' and a.get('rel')=='canonical': self.canonical=a.get('href','')
  if t=='a':self.links.append(a.get('href',''))
  if t=='img':self.images.append(a.get('src',''))
  if t=='button' and ('single_add_to_cart_button' in a.get('class','') or a.get('name')=='add-to-cart'):self.cta=True
  if t in ('title','h1') or t=='script' and a.get('type')=='application/ld+json':self.capture=t;self.buf=''
 def handle_data(self,s):
  if self.capture:self.buf+=s
 def handle_endtag(self,t):
  if self.capture==t:
   if t=='title':self.title=self.buf.strip()
   elif t=='h1':self.h1.append(' '.join(self.buf.split()))
   else:self.schema.append(json.loads(self.buf))
   self.capture=None
def product_schema(v):
 out=[]
 if isinstance(v,dict):
  if 'Product' in ([v.get('@type')] if isinstance(v.get('@type'),str) else v.get('@type',[])):
   out.append({k:v.get(k) for k in ('@id','sku','offers')})
  for x in v.values():out+=product_schema(x)
 elif isinstance(v,list):
  for x in v:out+=product_schema(x)
 return out
mode=sys.argv[1]; evidence=[]
for r in rows:
 url=r['url']+('?intent_release_qa=20261004' if mode=='uncached' else '')
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'ShustrikPortfolioQA/1.0'}),timeout=40) as response:
  raw=response.read().decode('utf-8');status=response.status;final=response.geturl()
 p=Page();p.feed(raw)
 text=' '.join(html.unescape(re.sub('<[^>]+>',' ',raw)).split())
 entry={'id':r['id'],'http':status,'final_path':urllib.parse.urlsplit(final).path,'title':p.title,'meta':p.meta.get('description'),'robots':p.meta.get('robots'),'canonical':p.canonical,'h1':p.h1,'links':p.links,'images':p.images,'products':product_schema(p.schema),'cta':p.cta,'intro_present':r['after']['first_paragraph_text'] in text}
 evidence.append(entry)
if mode!='before':
 before=json.loads((ROOT/'public-before.json').read_text())['rows']
 for e,r,b in zip(evidence,rows,before):
  # Related-product carousels rotate on render. Exact DB body verification protects existing authored links; compare full-size product imagery, excluding carousel thumbnails.
  e['checks']={'title':e['title']==r['after']['seo_title'],'meta':e['meta']==r['after']['meta_description'],'intro':e['intro_present'],'h1':e['h1']==[r['unchanged_h1']],'canonical':e['canonical']==r['url'],'indexable':'noindex' not in (e['robots'] or ''),'commerce_schema':e['products']==b['products'],'main_images':set(u for u in e['images'] if '-300x300' not in u)==set(u for u in b['images'] if '-300x300' not in u),'cta':e['cta'],'http':e['http']==200,'url':e['final_path']==urllib.parse.urlsplit(r['url']).path}
  assert all(e['checks'].values()),e['checks']
else:
 for e,r in zip(evidence,rows):assert e['http']==200 and e['title']==r['before']['seo_title'] and e['meta']==r['before']['meta_description'] and e['h1']==[r['unchanged_h1']] and e['cta'] and e['products']
out={'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'mode':mode,'ok':True,'rows':evidence}
(ROOT/('public-'+mode+'.json')).write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps({'mode':mode,'ok':True,'pages':len(evidence)}))
