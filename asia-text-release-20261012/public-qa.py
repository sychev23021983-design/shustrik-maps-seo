from pathlib import Path
import json,sys,urllib.request
from lxml import html
ROOT=Path(__file__).parent;URL='https://shustrik-maps.com/product-category/3d-models/continents-3d-models/asia/'
def fetch(url):
 request=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
 with urllib.request.urlopen(request,timeout=35) as response:return {'http':response.status,'url':response.url,'body':response.read()}
def has_class(name):return "contains(concat(' ',normalize-space(@class),' '),' "+name+" ')"
def text(node):return ' '.join(node.text_content().split())
def first(nodes):return nodes[0] if nodes else None
def page_state(url):
 response=fetch(url);tree=html.fromstring(response['body'].decode('utf-8'));cards=[]
 for card in tree.xpath('//main//*['+has_class('product-grid-item')+']'):
  heading=first(card.xpath('.//*['+has_class('wd-entities-title')+' or '+has_class('woocommerce-loop-product__title')+']'));link=first(heading.xpath('.//a')) if heading is not None else None;price=first(card.xpath('.//*['+has_class('price')+']'))
  if link is not None:cards.append({'url':link.get('href'),'title':text(heading),'price':text(price) if price is not None else ''})
 schema=[]
 for script in tree.xpath('//script[@type="application/ld+json"]'):
  try:payload=json.loads(script.text or '')
  except ValueError:continue
  graph=payload.get('@graph',[payload]) if isinstance(payload,dict) else payload
  schema.extend(entry.get('@type') for entry in graph if isinstance(entry,dict))
 def attr(xpath,name):node=first(tree.xpath(xpath));return node.get(name) if node is not None else None
 state={'http':response['http'],'url':response['url'],'title':' '.join(tree.xpath('//title/text()')),'description':attr('//meta[@name="description"]','content'),'canonical':attr('//link[@rel="canonical"]','href'),'robots':attr('//meta[@name="robots"]','content'),'h1':[text(h) for h in tree.xpath('//h1')],'cards':cards,'schema_types':schema,'pagination_present':bool(tree.xpath('//*['+has_class('woocommerce-pagination')+' or '+has_class('wd-pagination')+']'))}
 state['main_images']=[{'url':i.get('data-src') or i.get('src'),'alt':i.get('alt'),'width':i.get('width'),'height':i.get('height')} for i in tree.xpath('//main//img')]
 state['retained_links']=[a.get('href') for a in tree.xpath('//main//a[not(ancestor::*[@id="asia-category-copy"])]')]
 state['retained_country_headings']=[text(h) for h in tree.xpath('//main//h4')]
 return response,tree,state
mode=sys.argv[1];response,tree,state=page_state(URL)
if mode=='baseline':
 assert len(state['cards'])==1 and state['h1']==['ASIA']
 (ROOT/'public-baseline.json').write_text(json.dumps(state,indent=2)+'\n',encoding='utf-8',newline='\n');print(json.dumps({'mode':mode,'http':state['http'],'cards':1,'h1':state['h1'],'images':len(state['main_images']),'headings':len(state['retained_country_headings'])}))
else:
 assert mode=='verify';baseline=json.loads((ROOT/'public-baseline.json').read_text());checks={}
 for field in ['title','description','canonical','robots','cards','schema_types','pagination_present','retained_country_headings','main_images','retained_links']:checks[field+'_preserved']=state[field]==baseline[field]
 checks['h1']=state['h1']==['Asia 3D Model for Renders and Animation'];copy=first(tree.xpath('//*[@id="asia-category-copy"]'));checks['copy_exists']=copy is not None
 expected=html.fromstring((ROOT/'category.html').read_text(encoding='utf-8'));checks['copy_matches']=copy is not None and text(copy)==text(expected)
 checks['three_paragraphs']=copy is not None and len(copy.xpath('./p'))==3
 checks['no_added_images']=copy is not None and not copy.xpath('.//img')
 checks['old_copy_removed']='Welcome to our page featuring 3D models of Asia for sale' not in text(tree)
 checks['no_added_h1']=len(state['h1'])==1
 links={}
 if copy is not None:
  for url in sorted(set(copy.xpath('.//a/@href'))):links[url]=fetch(url)['http']
 checks['links_http']=len(links)==3 and all(code==200 for code in links.values())
 health={}
 for path in ['','cart/','checkout/']:
  r=fetch('https://shustrik-maps.com/'+path);health[path or 'home']={'http':r['http'],'final_url':r['url']}
 checks['health']=all(h['http']==200 for h in health.values())
 result={'ok':all(checks.values()),'checks':checks,'state':state,'links':links,'health':health,'scope':'Text only; existing images and all country links preserved; no media imported.'}
 (ROOT/'public-qa.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');print(json.dumps({'ok':result['ok'],'checks':checks,'cards':1}));assert result['ok']
