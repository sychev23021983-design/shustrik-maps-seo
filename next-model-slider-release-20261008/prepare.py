from pathlib import Path
import json,re,hashlib,shutil
root=Path('J:/1. My Vault/01 Projects/WordPress/shustrik-maps.com/Next Model Sliders 2026-10-08');repo=Path('J:/1. My Vault/90 Migration/shustrik-maps-seo');out=repo/'next-model-slider-release-20261008'
defs=json.loads((root/'defs.json').read_text());baseline=json.loads((root/'baseline.json').read_text(encoding='utf-8'))
mapping={15527:('Sheikh Zayed Bust STL | Portrait Model for 3D Print & CNC','Download the Sheikh Zayed portrait bust STL with open and closed base options listed. Explore display and gift concepts for this digital sculpture.'),20192:('Troll Face Skull STL | Whole & Split 3D Print Models','Download the Troll Face skull STL in whole and split versions, with its stand design. Explore 3D printing, display and gift concepts for this digital model.'),20199:('Zombie Monster Box STL | 3D Printable Storage Container','Download the Zombie Monster storage box STL with separate parts for assembly using plastic glue. Explore desk storage and gift concepts for this digital file.')}
support={15527:['Sheikh Zayed bust STL','Sheikh Zayed portrait 3D model','Sheikh Zayed sculpture CNC'],20192:['troll face skull STL','trollface skull 3D print','troll face skull with stand STL'],20199:['zombie monster box STL','monster storage box 3D print','Halloween storage box STL']}
exclude={15527:['Sheikh Zayed Grand Mosque','Sheikh Mohamed bin Zayed','physical ready-made bust','free STL'],20192:['plain Trollface flat meme','anatomical medical skull','commercial license','free identical file'],20199:['Zombicide organizer','Kingdom Death storage','humanoid zombie figure','food-safe container']}
g='[woodmart_gallery images="{{IMAGE_IDS}}" view="carousel" img_size="large" caption="0" lazy_loading="yes" spacing="0" slides_per_view="1" slides_per_view_mobile="1" carousel_arrows_position="together" wrap="no" autoheight="no" autoplay="no" hide_prev_next_buttons="no" hide_pagination_control="no" hide_pagination_control_tablet="no" hide_pagination_control_mobile="no"]'
notice='[vc_column_text]<p style="text-align: center;"><strong>AI-generated application concepts.</strong></p>[/vc_column_text]';rows=[]
for b,(id,slug,name) in zip(baseline['rows'],defs):
 assert b['id']==id and 'AI-generated' not in b['content'];title,meta=mapping[id];text=b['content']
 if id==15527:
  sections=re.findall(r'\[vc_section\b[^\]]*\].*?\[/vc_section\]',text,re.S)
  target=next(s for s in sections if 'image="15536"' in s);assert target.count('[vc_single_image')==1 and '[vc_column_text' not in target
  after=text.replace(target,'',1);intro=sections[0];assert intro in after and intro.count('[vc_column]')==1 and intro.count('[/vc_column][/vc_row]')==1
  revised=intro.replace('[vc_column]','[vc_column width="1/2"]',1).replace('[/vc_column][/vc_row]','[/vc_column][vc_column width="1/2"]'+g+notice+'[/vc_column][/vc_row]',1);after=after.replace(intro,revised,1)
 else:
  target='[/vc_column_text][/vc_column_inner][/vc_row_inner]';assert text.count(target)==1
  after=text.replace(target,'[/vc_column_text]'+g+notice+'[/vc_column_inner][/vc_row_inner]',1)
 for tag in ['vc_column_text','woodmart_text_block']:
  old=re.findall(r'\['+tag+r'[^\]]*\](.*?)\[/'+tag+r'\]',text,re.S);new=[x for x in re.findall(r'\['+tag+r'[^\]]*\](.*?)\[/'+tag+r'\]',after,re.S) if 'AI-generated application concepts.' not in x];assert old==new,(id,tag)
 for tag in ['vc_section','vc_row','vc_column','vc_column_text','vc_row_inner','vc_column_inner','woodmart_text_block']:assert len(re.findall(r'\['+tag+r'(?:\s|\])',after))==after.count('[/'+tag+']'),(id,tag)
 assert 35<=len(title)<=65 and 130<=len(meta)<=165,(id,len(title),len(meta))
 rows.append({'id':id,'slug':slug,'name':name,'url':b['url'],'h1_preserved':b['title'],'gallery_preserved':b['gallery'],'before_content_sha256':hashlib.sha256(text.encode()).hexdigest(),'before_seo_title':b['seo_title'],'before_meta_description':b['meta_description'],'before_excerpt_sha256':hashlib.sha256(b['excerpt'].encode()).hexdigest(),'baseline_protected':b['protected'],'seo_title':title,'meta_description':meta,'title_chars':len(title),'meta_chars':len(meta),'description':after,'illustration_target':target,'base_listed':'open/closed' if id==15527 else 'stand / assembly model','primary_cluster':'MODEL-'+slug+'-stl','supporting':support[id],'excluded':exclude[id]})
(root/'manifest.json').write_text(json.dumps({'site_profile':'shustrik-maps','publication_authorized':True,'rows':rows},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
semantic={'site_profile':'shustrik-maps','language':'English','market':'USA','engine':'Google','new_metrics_collected':False,'us_rank_verified':False,'editorial_clusters':[{'product_id':r['id'],'primary':support[r['id']][0],'supporting':support[r['id']][1:],'excluded':exclude[r['id']],'frequency':None,'rank':None} for r in rows],'decision':'validate first','note':'Publication already authorized by owner workflow; validate first refers only to a later demand/SEO measurement. Exact digital STL intent, known assortment and public SERPs reviewed. Google location Unknown despite hl=en/gl=us/pws=0. No keyword-service metrics collected.'}
(root/'semantic-review.json').write_text(json.dumps(semantic,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
brief='---\ntype: seo-page-brief\nsite_profile: shustrik-maps\nstatus: approved\ncreated_at: 2026-10-08\nmarket: USA\nlanguage: English\nsources: [baseline.json, semantic-review.json, intent-evidence.json]\nnext_action: Publish the owner-authorized remaining STL products and verify\n---\n\n# Remaining STL Page Briefs\n\nOwner workflow authorizes full cycle; retain original Description, H1, URL, specifications, commerce, files, upper gallery, existing canonicals/robots/Product schema/CTA and internal links. Optimize only SEO title/meta and one own-reference native carousel. No new format/coverage/accuracy/readiness/licensing claim. Four separate concepts per model, AI title/alt, true JPEG1500x1000; manual single-slide carousel, bold centered notice only.\n'
for r in rows:
 brief+='\n## '+r['name']+' / '+str(r['id'])+'\n\n'+r['url']+'\n\nPrimary/support: '+', '.join(support[r['id']])+'\n\nExclude: '+', '.join(exclude[r['id']])+'\n\nSEO title: '+r['seo_title']+'\n\nMeta description: '+r['meta_description']+'\n\nH1 unchanged: '+r['h1_preserved']+'\n\nSource: baseline SKU. Self canonical, robots, Product schema and Add to cart/Buy now CTA preserved and verified after publication.\n'
brief+='\nExisting facts needing separate validation: Sheikh Zayed dimensions76x48x68 m; original accuracy/production-ready claims and copied chat CSS retained literally. Troll license is non-commercial in original prose; enlarged exhibition is an AI fabrication concept and grants no commercial rights. Zombie glue assembly retained; no food-contact or child-safety promise. Mesh/archive not tested.\n\nAcceptance: exact SEO/prose/protected fields; all12media hashes/title/alt/JPEG/size; HTTP/H1/canonical/robots/schema/CTA; all4slides desktop/mobile; runtime unchanged; new guarded backup/rollback; pushed source and exact archive.\n'
(root/'Page Briefs.md').write_text(brief,encoding='utf-8')
old=repo/'kiwi-nautilus-usecases-revision-20261008'
release=(old/'release.php').read_text(encoding='utf-8').replace('kiwi_nautilus_usecases','next_models').replace('[21381,18721]','[15527,20192,20199]').replace('count($assets)!==8','count($assets)!==12')
(root/'release.php').write_text(release,encoding='utf-8');shutil.copy2(root/'release.php',out/'release.php')
delivery=(old/'deliver.py').read_text(encoding='utf-8').replace('kiwi-nautilus-usecases-revision-20261008','next-model-slider-release-20261008').replace('kiwi-nautilus-usecases','next-models')
(root/'deliver.py').write_text(delivery,encoding='utf-8')
for n in ['manifest.json','Page Briefs.md','semantic-review.json','baseline.json','defs.json','delivery.py']:
 p=root/n
 if p.exists():shutil.copy2(p,out/p.name)
print([(r['id'],r['title_chars'],r['meta_chars']) for r in rows])
