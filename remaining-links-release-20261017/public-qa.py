from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin,urlsplit,urlunsplit
import concurrent.futures,json,urllib.request,re

ROOT=Path(__file__).resolve().parent
class Node:
 def __init__(self,tag='',attrs=None,parent=None):self.tag=tag;self.attrs=dict(attrs or []);self.parent=parent;self.children=[];self.data=[];self.parts=[]
 def text(self):return re.sub(r'\s+',' ', ' '.join(p if isinstance(p,str) else p.text() for p in self.parts if isinstance(p,str) or p.tag not in ['script','style','noscript'])).strip()
 def walk(self):
  yield self
  for c in self.children:yield from c.walk()
 def ancestors(self):
  p=self
  while p:yield p;p=p.parent
class DOM(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.root=Node();self.current=self.root
 def handle_starttag(self,tag,attrs):
  n=Node(tag,attrs,self.current);self.current.children.append(n);self.current.parts.append(n)
  if tag not in ['img','input','meta','link','br','hr','source','area','base','embed','param','track','wbr']:self.current=n
 def handle_startendtag(self,tag,attrs):self.handle_starttag(tag,attrs);self.handle_endtag(tag)
 def handle_endtag(self,tag):
  p=self.current
  while p and p.tag!=tag:p=p.parent
  if p:self.current=p.parent or self.root
 def handle_data(self,data):self.current.data.append(data);self.current.parts.append(data)
def normalized(url):
 p=urlsplit(url);return urlunsplit((p.scheme,p.netloc,p.path,'',''))
def fetch(url):
 req=urllib.request.Request(url,headers={'User-Agent':'ShustrikPortfolioQA/1.0'})
 with urllib.request.urlopen(req,timeout=35) as r:raw=r.read().decode('utf-8',errors='replace');http=r.status;final=r.url
 slug=urlsplit(url).path.strip('/').replace('/','--') or 'home'
 (ROOT/'html'/(slug+'.html')).write_text(raw,encoding='utf-8')
 d=DOM();d.feed(raw);nodes=list(d.root.walk())
 main=next((n for n in nodes if n.tag=='main'),d.root)
 description=next((n for n in nodes if n.attrs.get('id')=='tab-description'),None)
 summary=next((n for n in nodes if 'summary' in n.attrs.get('class','').split()),None)
 def links(region):
  return [{'url':urljoin(url,n.attrs['href']),'text':n.text(),'rel':n.attrs.get('rel','')} for n in region.walk() if n.tag=='a' and n.attrs.get('href') and urlsplit(urljoin(url,n.attrs['href'])).netloc=='shustrik-maps.com']
 images=[]
 for n in main.walk():
  if n.tag!='img':continue
  ancestors=list(n.ancestors());classes=' '.join(p.attrs.get('class','') for p in ancestors)
  region='gallery' if any('woocommerce-product-gallery' in p.attrs.get('class','') for p in ancestors) else ('description' if description in ancestors else 'listing_or_related')
  images.append({'src':urljoin(url,n.attrs.get('data-src') or n.attrs.get('src','')),'srcset':n.attrs.get('srcset',''),'alt':n.attrs.get('alt'),'html_title':n.attrs.get('title'),
   'width':n.attrs.get('width'),'height':n.attrs.get('height'),'loading':n.attrs.get('loading'),'region':region,'classes':n.attrs.get('class',''),'context':classes[-300:]})
 row={'url':url,'http':http,'final_url':final,'title':next((n.text() for n in nodes if n.tag=='title'),''),
  'meta_description':next((n.attrs.get('content') for n in nodes if n.tag=='meta' and n.attrs.get('name')=='description'),None),
  'robots':next((n.attrs.get('content') for n in nodes if n.tag=='meta' and n.attrs.get('name')=='robots'),None),
  'canonical':next((n.attrs.get('href') for n in nodes if n.tag=='link' and n.attrs.get('rel')=='canonical'),None),
  'h1':[n.text() for n in nodes if n.tag=='h1'],'headings':[{'tag':n.tag,'text':n.text()} for n in main.walk() if n.tag in ['h2','h3']],
  'main_text':main.text(),'description_text':description.text() if description else '', 'summary_text':summary.text() if summary else '',
  'main_links':links(main),'description_links':links(description) if description else [],'images':images,
  'schema_types':re.findall(r'"@type"\s*:\s*"([^"\n]+)"',raw),'archive_description_nodes':sum('term-description' in n.attrs.get('class','') for n in nodes),
  'pagination':[normalized(urljoin(url,n.attrs['href'])) for n in main.walk() if n.tag=='a' and '/page/' in n.attrs.get('href','') and '/cnc-models/' in n.attrs.get('href','')]}
 return row

if __name__=='__main__':
 import sys
 mode=sys.argv[1]
 assert mode in ['baseline','verify']
 (ROOT/'html').mkdir(exist_ok=True)
 manifest=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
 targets=['https://shustrik-maps.com/product-category/3d-models/','https://shustrik-maps.com/product-category/cnc-models/','https://shustrik-maps.com/product/authagraph-world-map/','https://shustrik-maps.com/product/earth-3d-model-terrain-without-water/']
 prior=['https://shustrik-maps.com/what-is-an-stl-file-explaining-the-stl-format/','https://shustrik-maps.com/understanding-the-obj-file-format-a-simple-explanation/','https://shustrik-maps.com/how-to-convert-a-model-from-c4d-to-obj/']
 urls=[p['url'] for p in manifest['posts']]+targets+prior
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:rows=list(ex.map(fetch,urls))
 for row in rows:
  assert row['http']==200 and row['canonical']==row['url']
  assert len(row['h1'])==1 and 'noindex' not in row['robots']
 if mode=='baseline':
  (ROOT/'public-baseline.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
 else:
  before=json.loads((ROOT/'public-baseline.json').read_text(encoding='utf-8'))
  for old,new in zip(before,rows):
   for field in ['url','title','meta_description','canonical','robots','h1']:
    assert old[field]==new[field],(new['url'],field)
   assert [x['src'] for x in old['images']]==[x['src'] for x in new['images']]
   assert old['schema_types']==new['schema_types']
  tests=[(14596,'3D terrain model catalog',targets[0]),(15631,'3D terrain models',targets[0]),(15631,'terrain STL collection',targets[1]),(20707,'AuthaGraph world map image files (TIF/PSD)',targets[2]),(16110,'Earth terrain model without water',targets[3])]
  for id,anchor,url in tests:
   source=next(p['url'] for p in manifest['posts'] if p['id']==id)
   row=next(r for r in rows if r['url']==source)
   assert sum(l['url']==url and l['text']==anchor for l in row['main_links'])==1,(id,anchor)
  for source in prior:
   old=next(r for r in before if r['url']==source);new=next(r for r in rows if r['url']==source)
   assert old['main_text']==new['main_text'] and old['main_links']==new['main_links']
  (ROOT/'public-after.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
  (ROOT/'public-qa.json').write_text(json.dumps({'ok':True,'urls_checked':len(rows),'links_checked':5,'source_metadata_media_preserved':True,'schema_types_preserved':True,'previous_release_public_preserved':True,'checks':[{'id':id,'anchor':anchor,'target':url} for id,anchor,url in tests]},ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
 print(json.dumps({'ok':True,'mode':mode,'urls':len(rows)}))
