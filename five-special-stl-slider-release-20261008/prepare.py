import json,re,csv,hashlib
from pathlib import Path
root=Path(__file__).parent;repo=Path('J:/1. My Vault/90 Migration/shustrik-maps-seo');defs=json.loads((root/'defs.json').read_text());baseline=json.loads((root/'baseline.json').read_text(encoding='utf-8'))
core=root.parent/'2026-10-05--arizona-stl/processed'
clusters=list(csv.DictReader((core/'Current Cluster Map.csv').open(encoding='utf-8-sig')));keywords=list(csv.DictReader((core/'Current Semantic Core.csv').open(encoding='utf-8-sig')))
mapping={10140:('Antarctica with Ice STL | Topographic Terrain 3D Model','Download the Antarctica with ice terrain model in C4D and STL formats. Explore relief display concepts for this digital polar stereographic model.'),10324:('Dymaxion World Map STL | Fuller Projection Terrain Model','Download the Dymaxion world terrain model in OBJ and STL formats. The listing has an open base; display and fabrication concepts need added support.'),16379:('Zion Canyon Trail STL | Open-Base Terrain Model for CNC','Download the Zion Canyon Trail model with an additional open-base STL for CNC. Preparing it for 3D printing requires closing the bottom and checking the mesh.'),21381:('New Zealand Kiwi Medallion STL | Flag Relief 3D Model','Download the New Zealand Kiwi medallion STL featuring a wavy flag and bird relief. Explore desktop, wall and gift concepts for this digital model.'),18721:('Nautilus Pendant STL | Maori-Style Spiral Relief Model','Download the Nautilus pendant STL with a Maori-style shell and central spiral. Explore 3D printing, CNC, desktop, wall and gift application concepts.')}
support={10140:['Antarctica terrain STL','Antarctica with ice 3D model','polar stereographic relief STL'],10324:['Dymaxion STL','Fuller world terrain model','unfolded world map STL'],16379:['Zion Canyon Trail STL','Zion CNC terrain model','Zion open base relief'],21381:['New Zealand medallion STL','kiwi bird relief STL','New Zealand flag 3D print'],18721:['Nautilus pendant STL','Maori style pendant 3D model','spiral pendant CNC relief']}
gallery='[woodmart_gallery images="{{IMAGE_IDS}}" view="carousel" img_size="large" caption="0" lazy_loading="yes" spacing="0" slides_per_view="1" slides_per_view_mobile="1" carousel_arrows_position="together" wrap="no" autoheight="no" autoplay="no" hide_prev_next_buttons="no" hide_pagination_control="no" hide_pagination_control_tablet="no" hide_pagination_control_mobile="no"]'
notice='[vc_column_text]<p style="text-align: center;"><strong>AI-generated application concepts.</strong></p>[/vc_column_text]';rows=[];refs={}
for before,(id,slug,name) in zip(baseline['rows'],defs):
 assert before['id']==id
 b=before['content'];title,desc=mapping[id]
 if id in [10140,10324,16379]:
  target=next(x for x in re.findall(r'\[woodmart_image\b[^\]]*\]',b) if 'img_id="'+str({10140:10158,10324:10340,16379:16386}[id])+'"' in x)
  assert b.count(target)==1;after=b.replace(target,gallery+notice)
 elif id==21381:
  # Preserve all right-column prose verbatim and append the absent illustration before its closing tag.
  target='[/woodmart_text_block][/vc_column][/vc_row][vc_row][vc_column][vc_message'
  assert b.count(target)==1;after=b.replace(target,'[/woodmart_text_block]'+gallery+notice+'[/vc_column][/vc_row][vc_row][vc_column][vc_message')
 else:
  assert id==18721 and b.startswith('[vc_row][vc_column]') and b.endswith('[/vc_column][/vc_row]')
  target='new right column (no previous Description illustration)'
  after=b.replace('[vc_row][vc_column]','[vc_row][vc_column width="1/2"]',1)
  after=after[:-len('[/vc_column][/vc_row]')]+'[/vc_column][vc_column width="1/2"]'+gallery+notice+'[/vc_column][/vc_row]'
 for tag in ['vc_column_text','woodmart_text_block']:
  old=re.findall(r'\['+tag+r'[^\]]*\](.*?)\[/'+tag+r'\]',b,re.S)
  new=[t for t in re.findall(r'\['+tag+r'[^\]]*\](.*?)\[/'+tag+r'\]',after,re.S) if 'AI-generated application concepts.' not in t];assert old==new
 assert 'AI-generated application concepts.' not in b and after.count('{{IMAGE_IDS}}')==1
 for tag in ['vc_section','vc_row','vc_column','vc_column_text','vc_row_inner','vc_column_inner','woodmart_text_block']:assert len(re.findall(r'\['+tag+r'(?:\s|\])',after))==after.count('[/'+tag+']'),(id,tag)
 bases=re.findall(r'Base: (.*?)</li>',before['excerpt']);base=bases[0].lower() if bases else 'not stated'
 assert 35<=len(title)<=65 and 130<=len(desc)<=165,(id,len(title),len(desc))
 rows.append({'id':id,'slug':slug,'name':name,'url':before['url'],'h1_preserved':before['title'],'gallery_preserved':before['gallery'],'before_content_sha256':hashlib.sha256(b.encode()).hexdigest(),'seo_title':title,'meta_description':desc,'title_chars':len(title),'meta_chars':len(desc),'description':after,'primary_cluster':'MODEL-'+slug+'-stl','base_listed':base,'illustration_target':target,'before_seo_title':before['seo_title'],'before_meta_description':before['meta_description'],'before_excerpt_sha256':hashlib.sha256(before['excerpt'].encode()).hexdigest(),'baseline_protected':before['protected']})
 refs[slug]=[i['id'] for i in before['images'][:2]]
 print(id,name,'refs',refs[slug],'base',base,'SEO lengths',len(title),len(desc))
semantic={'market':'USA','language':'English','engine':'Google','new_metrics_collected':False,'us_rank_verified':False,'existing_clusters':[r for r in clusters if any(s in json.dumps(r).lower() for s in ['antarctica','dymaxion','zion','kiwi','nautilus'])],'existing_keywords':[r for r in keywords if any(s in json.dumps(r).lower() for s in ['antarctica','dymaxion','zion','kiwi','nautilus'])],'editorial_clusters':[{'product_id':i,'cluster_id':'MODEL-'+s+'-stl','primary':support[i][0],'supporting':support[i][1:],'frequency':None,'rank':None} for i,s,n in defs],'note':'Exact SKU/format intent must be separated from heightmap/GIS, physical goods, bedrock Antarctica, foldable globe or puzzle Dymaxion, full park Zion, live birds, currency and Nautilus submarines. Existing metrics retained as source data only.'}
(root/'semantic-review.json').write_text(json.dumps(semantic,ensure_ascii=False,indent=2),encoding='utf-8')
(root/'manifest.json').write_text(json.dumps({'site_profile':'shustrik-maps','publication_authorized':True,'rows':rows},ensure_ascii=False,indent=2),encoding='utf-8')
s='<?php\nini_set("display_errors","0");define("WP_USE_THEMES",false);ob_start();require "/var/www/html/wp-load.php";ob_end_clean();\nforeach('+json.dumps(refs).replace('{','[').replace('}',']').replace(':','=>')+' as $slug=>$ids){foreach($ids as $i=>$aid){if(!copy(get_attached_file($aid),"/tmp/".$slug."-source-".($i+1).".jpg"))exit(1);}}'
(repo/'.codex-work/five-special-refs.php').write_text(s,encoding='utf-8')
lines=['---','type: seo-page-brief','site_profile: shustrik-maps','status: approved','created_at: 2026-10-08','market: USA','language: English','sources: [baseline.json, semantic-review.json, intent-evidence.json]','next_action: "Publish authorized five existing STL products and verify"','---','','# Five Special STL Page Briefs','','Owner instruction authorizes full cycle and publication under STL Product Update Workflow. Audience: US English digital-model buyers. One paid digital file intent per SKU; editorial phrases have no new measured frequency or rank. Preserve original main text/H1/URLs/specs/commerce/upper galleries/all non-target blocks. Four own-reference concepts, true JPEG1500x1000, native manual carousel; only bold centered AI notice. New column added only where original Description has no illustration. No new manufacture readiness, precision, licensing or format promises.']
for r in rows:
 lines+=['',f'## {r["name"]} / {r["id"]}',r['url'],f'Primary/support: {", ".join(support[r["id"]])}',f'SEO title: {r["seo_title"]}',f'Meta description: {r["meta_description"]}',f'H1 unchanged: {r["h1_preserved"]}',f'Canonical: preserve self URL {r["url"]}. Robots: preserve baseline indexability. Product schema and CTA Add to cart/Buy now remain existing, verified publicly. Internal links and sections unchanged.',f'Base claim in excerpt: {r["base_listed"]}; mesh and archive not validated. Source: baseline.json SKU {r["id"]}.']
lines+=['','Acceptance: exact SEO; original prose including woodmart_text_block; protected fields; 20media hashes/title/alt/jpeg/size; HTTP/canonical/robots/H1/Product/CTA; all4slides desktop/mobile; runtime unchanged; guard backups/rollback; source commit pushed and exact archive delivered. Research decision validate first is only the later demand/SEO measurement, not a publication veto.']
(root/'Page Briefs.md').write_text('\n\n'.join(lines),encoding='utf-8')
