from pathlib import Path
from urllib.parse import urlsplit,unquote
import importlib.util,json,re,concurrent.futures,sys
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('publicdom',ROOT.parent/'satellite-descriptions-release-20261018/public-dom.py');dom=importlib.util.module_from_spec(spec);spec.loader.exec_module(dom);dom.ROOT=ROOT
(ROOT/'html').mkdir(exist_ok=True)
m=json.loads((ROOT/'manifest.json').read_text(encoding='utf8'));s=json.loads((ROOT/'scope.json').read_text(encoding='utf8'))
def key(u):return re.sub(r'-\d+x\d+(?=\.[^.]+$)','',unquote(urlsplit(u).path))
target={key(a['url']):a for a in m['attachments']}
archives=['https://shustrik-maps.com/product-category/3d-renders/satellite-maps/','https://shustrik-maps.com/product-category/3d-renders/night-satellite-map/']
urls=s['product_urls']+archives
def products(raw):
 out=[]
 def walk(x):
  if isinstance(x,dict):
   if x.get('@type')=='Product' or isinstance(x.get('@type'),list) and 'Product' in x['@type']:out.append({k:x.get(k) for k in ['@id','name','sku','url','offers','image']})
   for v in x.values():walk(v)
  elif isinstance(x,list):
   for v in x:walk(v)
 for block in re.findall(r'<script[^>]*type=[\"\x27]application/ld\+json[\"\x27][^>]*>(.*?)</script>',raw,re.S|re.I):walk(json.loads(block))
 return out
def fetch(url):
 row=dom.fetch(url);slug=urlsplit(url).path.strip('/').replace('/','--');raw=(ROOT/'html'/(slug+'.html')).read_text(encoding='utf8');row['product_identity_offers']=products(raw);return row
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex: rows=list(ex.map(fetch,urls))
mode=sys.argv[1] if len(sys.argv)>1 else 'verify'
if mode=='baseline':
 assert all(x['http']==200 and x['final_url']==x['url'] for x in rows)
 (ROOT/'public-before.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(dict(baseline_urls=len(rows))));sys.exit()
before={x['url']:x for x in json.loads((ROOT/'public-before.json').read_text(encoding='utf8'))}
failures=[];seen=set();changes=0;titlechanges=0;own=0;archive_checks=0
for row in rows:
 old=before[row['url']];errors=[]
 if row['http']!=200 or row['url']!=row['final_url']:errors.append('HTTP/redirect')
 for k in ['h1','title','meta_description','robots','canonical','description_text','summary_text','description_links','product_identity_offers']:
  if row[k]!=old[k]:errors.append('Protected '+k)
 if row['url'] in s['product_urls']:
  if len(row['h1'])!=1 or not row['product_identity_offers']:errors.append('Product structure')
  oldimages=[x for x in old['images'] if x['region'] in ['gallery','description']];images=[x for x in row['images'] if x['region'] in ['gallery','description']]
  if len(images)!=len(oldimages):errors.append('Own image count')
  for a,b in zip(oldimages,images):
   own+=1
   for k in ['src','srcset','region','width','height']:
    if a[k]!=b[k]:errors.append('Image identity '+k)
   t=target.get(key(b['src']))
   if t:
    seen.add(t['id']);expected=t['after']['alt'];expectedtitle=t['after']['title'] if a['html_title'] is not None else None
   else:expected=a['alt'];expectedtitle=a['html_title']
   if b['alt']!=expected:errors.append('Alt '+b['src'])
   if b['html_title']!=expectedtitle:errors.append('Image title '+b['src'])
   changes+=a['alt']!=b['alt'];titlechanges+=a['html_title']!=b['html_title']
 else:
  for img in row['images']:
   t=target.get(key(img['src']))
   if t:
    archive_checks+=1
    if img['alt']!=t['after']['alt']:errors.append('Archive alt '+str(t['id']))
 if errors:failures.append(dict(url=row['url'],errors=sorted(set(errors))))
if seen!=set(s['attachment_ids']):failures.append(dict(coverage_missing=sorted(set(s['attachment_ids'])-seen)))
qa=dict(ok=not failures,urls_checked=len(rows),product_urls_checked=92,archive_urls_checked=2,attachments_seen=len(seen),own_img_elements=own,alt_occurrences_changed=changes,title_occurrences_changed=titlechanges,archive_image_checks=archive_checks,failures=failures)
(ROOT/'public-after.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8');(ROOT/'public-qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(qa,ensure_ascii=True));sys.exit(0 if qa['ok'] else 1)
