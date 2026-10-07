import json,re,urllib.request,concurrent.futures
from pathlib import Path
from html.parser import HTMLParser
root=Path(__file__).parent
raw=(root/'verify.json').read_text(encoding='utf-8-sig')
v=json.loads(next(x for x in raw.splitlines() if x.startswith('{')))
assert v['ok']
class P(HTMLParser):
 def __init__(self):super().__init__();self.title='';self.it=False;self.h1=[];self.ih=False;self.meta={};self.canonical='';self.ld=[];self.il=False
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if t=='title':self.it=True
  if t=='h1':self.ih=True;self.h1.append('')
  if t=='meta':self.meta[a.get('name','')]=a.get('content','')
  if t=='link' and a.get('rel')=='canonical':self.canonical=a.get('href')
  if t=='script' and a.get('type')=='application/ld+json':self.il=True;self.ld.append('')
 def handle_endtag(self,t):
  if t=='title':self.it=False
  if t=='h1':self.ih=False
  if t=='script':self.il=False
 def handle_data(self,s):
  if self.it:self.title+=s
  if self.ih:self.h1[-1]+=s
  if self.il:self.ld[-1]+=s
def check(arg):
 r,uncached=arg;u=r['url']+('?ten_eurasia_qa=20261007' if uncached else '')
 with urllib.request.urlopen(u,timeout=35) as response:s=response.read().decode();status=response.status
 p=P();p.feed(s);notice=re.findall(r'<p style="text-align: center;">\s*<strong>AI-generated application concepts\.</strong>(.*?)</p>',s,re.S)
 checks={'http':status==200,'title':p.title==r['seo_title'],'meta':p.meta.get('description')==r['meta_description'],'h1':[re.sub(r'\s+',' ',x).strip() for x in p.h1]==[r['h1'].replace(' - ',' – ')],'canonical':p.canonical==r['url'],'indexable':'noindex' not in p.meta.get('robots',''),'schema':any('"Product"' in x for x in p.ld),'short_centered_notice':notice==[''],'four_new_images':all(m['url'].split('/')[-1].split('.jpg')[0] in s and m['alt'] in s for m in r['media']),'own_slider':all(m['url'].split('/')[-1].split('.jpg')[0] in s for m in r['media']),'no_raw_shortcodes':not re.search(r'\[(vc_|woodmart_)',s),'cart_button':'single_add_to_cart_button' in s}
 return {'id':r['id'],'url':u,'checks':checks,'pass':all(checks.values())}
def media_check(m):
 with urllib.request.urlopen(urllib.request.Request(m['url'],method='HEAD'),timeout=35) as r:return {'id':m['id'],'url':m['url'],'http':r.status,'mime':r.headers.get('Content-Type'),'pass':r.status==200 and r.headers.get('Content-Type')=='image/jpeg'}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as e:
 rows=list(e.map(check,[(r,u) for r in v['rows'] for u in [False,True]]))
 media=list(e.map(media_check,[m for r in v['rows'] for m in r['media']]))
out={'rows':rows,'media':media,'pass':all(x['pass'] for x in rows+media)}
(root/'public-qa.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps({'pass':out['pass'],'pages':len(rows),'media':len(media)}));assert out['pass']
# Persist normalized media IDs/URLs in the project registry after verified upload.
registry=json.loads((root/'media.json').read_text(encoding='utf-8'))
for r in v['rows']:
 for orig,uploaded in zip([m for m in registry if m['product_id']==r['id']],r['media']):orig.update({'attachment_id':uploaded['id'],'url':uploaded['url']})
(root/'uploaded-media.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2),encoding='utf-8')
