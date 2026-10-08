from pathlib import Path
import json,re,hashlib,shutil
root=Path(__file__).parent;old=root.parent/'Next Model Sliders 2026-10-08';repo=Path('J:/1. My Vault/90 Migration/shustrik-maps-seo');out=repo/'next-lunar-slider-release-20261008'
base=json.loads((root/'baseline.json').read_text(encoding='utf-8-sig'));defs=json.loads((root/'defs.json').read_text(encoding='utf-8-sig'));rows=[]
g='[woodmart_gallery images="{{IMAGE_IDS}}" view="carousel" img_size="large" caption="0" lazy_loading="yes" spacing="0" slides_per_view="1" slides_per_view_mobile="1" carousel_arrows_position="together" wrap="no" autoheight="no" autoplay="no" hide_prev_next_buttons="no" hide_pagination_control="no" hide_pagination_control_tablet="no" hide_pagination_control_mobile="no"]'
notice='[vc_column_text]<p style="text-align: center;"><strong>AI-generated application concepts.</strong></p>[/vc_column_text]'
for b,(id,slug,name) in zip(base['rows'],defs):
 text=b['content'];targets=re.findall(r'\[woodmart_image\b[^\]]*\]',text);assert len(targets)==1;after=text.replace(targets[0],g+notice,1)
 assert 'AI-generated' not in text
 for tag in ['vc_column_text','woodmart_text_block']:
  before=re.findall(r'\['+tag+r'[^\]]*\](.*?)\[/'+tag+r'\]',text,re.S);post=[x for x in re.findall(r'\['+tag+r'[^\]]*\](.*?)\[/'+tag+r'\]',after,re.S) if 'AI-generated application concepts.' not in x];assert before==post
 title=name+' STL | Moon Terrain for 3D Print & CNC'
 meta='Download the '+name.split()[0]+' lunar crater 3D model in STL and C4D formats, with textures listed. Explore Moon terrain display, gift and education concepts.'
 assert len(title)<=65 and 130<=len(meta)<=165,(len(title),len(meta))
 rows.append({'id':id,'slug':slug,'name':name,'url':b['url'],'h1_preserved':b['title'],'gallery_preserved':b['gallery'],'before_content_sha256':hashlib.sha256(text.encode()).hexdigest(),'before_seo_title':b['seo_title'],'before_meta_description':b['meta_description'],'before_excerpt_sha256':hashlib.sha256(b['excerpt'].encode()).hexdigest(),'baseline_protected':b['protected'],'seo_title':title,'meta_description':meta,'description':after,'illustration_target':targets[0],'base_listed':'closed' if id==16728 else 'not specified'})
(root/'manifest.json').write_text(json.dumps({'site_profile':'shustrik-maps','publication_authorized':True,'rows':rows},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for filename in ['release.php','backup-export.php','deliver.py','verify-preservation.py','public-qa.py']:
 s=(old/filename).read_text(encoding='utf-8-sig').replace('next-model-slider-release-20261008','next-lunar-slider-release-20261008').replace('next_models','next_lunar').replace('next-models','next-lunar').replace('[15527,20192,20199]','[16696,16728]').replace('count($assets)!==12','count($assets)!==8').replace('passed3/3','passed2/2');(root/filename).write_text(s,encoding='utf-8')
brief='# Lunar Page Briefs — approved owner workflow\n\nSite profile shustrik-maps, English, Google, USA. Update existing digital paid models. Primary clusters: Copernicus lunar crater STL and Theophilus lunar crater STL; support Moon terrain 3D print/CNC, lunar relief STL. Exclude Mars crater, Moon globe, generic gaming terrain, physical product purchase, free identical STL and research accuracy promises. No measured volume, US positions or difficulty. Public Google SERPs saved; actual location Unknown. Original C4D/STL/textures facts, base, prose, all links/HTML blocks/Internet ideas gallery and sample renders retained literally. Replace only the first standalone illustration with four own-reference AI concepts. No new base/readiness/precision/license promise.\n'
for r in rows:brief+='\n'+r['url']+'\n\nSEO title: '+r['seo_title']+'\n\nMeta: '+r['meta_description']+'\n\nH1 retained: '+r['h1_preserved']+'\n'
brief+='\nAcceptance: protected text/commerce/files/gallery exact, all8trueJPEG1500x1000/AI titles/alts/hashes, HTTP/SEO/canonical/robots/schema/CTA, all4slides on desktop/mobile, guarded backup/rollback preview, exact pushed archive, runtime unchanged. Original astronomical statements are preserved without independent scientific validation; application concepts do not verify the mesh.\n'
(root/'Page Briefs.md').write_text(brief,encoding='utf-8')
(root/'semantic-review.json').write_text(json.dumps({'site_profile':'shustrik-maps','language':'English','engine':'Google','market':'USA','new_metrics_collected':False,'us_rank_verified':False,'editorial_clusters':[{'product_id':r['id'],'primary':r['name']+' STL','supporting':['lunar crater 3D print','Moon relief CNC'],'volume':None,'rank':None} for r in rows],'decision':'validate first','note':'Later demand experiment only; publication of existing goods already authorized. Free NASA/derivative files, physical products and generic lunar game terrain are separate intents.'},indent=2)+'\n')
for p in root.iterdir():
 if p.is_file() and p.suffix in ['.php','.py','.json','.md','.jpg','.png','.txt']:shutil.copy2(p,out/p.name)
print([(r['id'],len(r['seo_title']),len(r['meta_description'])) for r in rows])
