from pathlib import Path
import json,sys,urllib.request
from lxml import html
ROOT=Path(__file__).parent;URL='https://shustrik-maps.com/product-category/cnc-models/other-cnc-models/jewelry-pendant/'
def fetch(url):
 request=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
 with urllib.request.urlopen(request,timeout=35) as response:return {'http':response.status,'url':response.url,'body':response.read()}
def has_class(name):return "contains(concat(' ',normalize-space(@class),' '),' "+name+" ')"
def text(node):return ' '.join(node.text_content().split())
def first(nodes):return nodes[0] if nodes else None
def page_state(url):
 response=fetch(url);tree=html.fromstring(response['body']);cards=[]
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
 return response,tree,state
mode=sys.argv[1];response,tree,state=page_state(URL)
if mode=='baseline':
 assert len(state['cards'])==2,{'cards':len(state['cards'])}
 (ROOT/'public-baseline.json').write_text(json.dumps(state,indent=2)+'\n',encoding='utf-8');print(json.dumps({'mode':mode,'http':state['http'],'cards':len(state['cards']),'h1':state['h1']}))
else:
 assert mode=='verify';baseline=json.loads((ROOT/'public-baseline.json').read_text());checks={}
 for field in ['title','description','canonical','robots','cards','schema_types','pagination_present']:checks[field+'_preserved']=state[field]==baseline[field]
 checks['h1']=state['h1']==['Jewelry & Pendant STL Models for 3D Printing & CNC'];block=first(tree.xpath('//*['+has_class('shustrik-jewelry-category')+']'));checks['block_exists']=block is not None
 checks['old_copy_removed']='UNUSED_PREVIOUS_HEADING' not in text(tree)
 checks['pagination_absent']=not state['pagination_present']
 checks['images']=block is not None and len(block.xpath('.//img'))==4
 checks['product_examples']=block is not None and len(block.xpath('.//article//a'))==8
 checks['disclosure']=block is not None and 'AI-generated application concepts' in text(block)
 links={};media={}
 if block is not None:
  for url in sorted(set(block.xpath('.//a/@href'))):links[url]=fetch(url)['http']
  for image in block.xpath('.//img'):
   url=image.get('data-src') or image.get('src');r=fetch(url);media[url]={'http':r['http'],'bytes':len(r['body']),'alt':image.get('alt'),'width':image.get('width'),'height':image.get('height')}
 checks['links_http']=bool(links) and all(code==200 for code in links.values());checks['media_http_alt']=len(media)==4 and all(m['http']==200 and m['alt'] for m in media.values())
 health={}
 for path in ['','cart/','checkout/']:
  r=fetch('https://shustrik-maps.com/'+path);health[path or 'home']={'http':r['http'],'final_url':r['url']}
 checks['health']=all(h['http']==200 for h in health.values())
 result={'ok':all(checks.values()),'checks':checks,'state':state,'links':links,'media':media,'health':health}
 (ROOT/'public-qa.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({'ok':result['ok'],'checks':checks,'cards':len(state['cards'])}));assert result['ok']
