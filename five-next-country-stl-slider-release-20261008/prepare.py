import json,re,csv,hashlib
from pathlib import Path
root=Path(__file__).parent;repo=Path('J:/1. My Vault/90 Migration/shustrik-maps-seo');defs=json.loads((root/'defs.json').read_text(encoding='utf-8'));baseline=json.loads((root/'baseline.json').read_text(encoding='utf-8'))
assert [r['id'] for r in baseline['rows']]==[d[0] for d in defs]
core=root.parent/'2026-10-05--arizona-stl/processed';wanted=['GEO-'+d[1]+'-stl-cnc' for d in defs]
semantic={'market':'USA','language':'English','new_metrics_collected':False,'us_rank_verified':False,'existing_clusters':[r for r in csv.DictReader((core/'Current Cluster Map.csv').open(encoding='utf-8-sig')) if r['cluster_id'] in wanted],'existing_keywords':[r for r in csv.DictReader((core/'Current Semantic Core.csv').open(encoding='utf-8-sig')) if r['clean_cluster'] in wanted],'editorial_clusters':[],'note':'All five exact STL clusters are absent from the saved core: editorial product mapping only. Proposed paid digital-file queries are editorial hypotheses, not measured expansion. Existing elevation/vector clusters must not be reassigned to STL.'}
gallery='[woodmart_gallery images="{{IMAGE_IDS}}" view="carousel" img_size="large" caption="0" lazy_loading="yes" spacing="0" slides_per_view="1" slides_per_view_mobile="1" carousel_arrows_position="together" wrap="no" autoheight="no" autoplay="no" hide_prev_next_buttons="no" hide_pagination_control="no" hide_pagination_control_tablet="no" hide_pagination_control_mobile="no"]'
notice='[vc_column_text]<p style="text-align: center;"><strong>AI-generated application concepts.</strong></p>[/vc_column_text]';rows=[];refs={}
for before,(id,slug,name) in zip(baseline['rows'],defs):
 b=before['content'];target='[html_block id="9586"]'
 if target not in b:
  imgs=re.findall(r'\[woodmart_image\b[^\]]*\]',b)
  if len(imgs)==1:target=imgs[0]
  else:
   assert id==9384 and not imgs
   target='[/vc_column_text][/vc_column_inner][/vc_row_inner]'
 assert b.count(target)==1 and 'AI-generated application concepts.' not in b
 old=re.findall(r'\[vc_column_text[^\]]*\](.*?)\[/vc_column_text\]',b,re.S)
 replacement=gallery+notice
 if id==9384:replacement='[/vc_column_text]'+replacement+'[/vc_column_inner][/vc_row_inner]'
 after=b.replace(target,replacement)
 assert [t for t in re.findall(r'\[vc_column_text[^\]]*\](.*?)\[/vc_column_text\]',after,re.S) if 'AI-generated application concepts.' not in t]==old
 for tag in ['vc_section','vc_row','vc_column','vc_column_text','vc_row_inner','vc_column_inner']:assert len(re.findall(r'\['+tag+r'(?:\s|\])',after))==after.count('[/'+tag+']')
 bases=re.findall(r'Base: (.*?)</li>',before['excerpt']);base=bases[0].lower() if bases else ('closed' if 'Base: Closed' in before['excerpt'] else 'not stated')
 title=f'{name} Topographic Map STL | 3D Print & CNC'
 if slug=='north-america-lambert':title='North America Lambert STL | Topographic Map for 3D Print'
 desc=f'Download the {name} topographic STL model for 3D printing and CNC projects. Explore desk, wall and gift ideas for this digital terrain file.'
 if base=='open':desc=f'Download the {name} topographic STL model for 3D printing and CNC projects. Explore display ideas; the listed open-base mesh may need preparation.'
 desc=desc.replace('a Ukraine','a Ukraine').replace('a Ireland','an Ireland').replace('a Oregon','an Oregon').replace('a Idaho','an Idaho').replace('a Ohio','an Ohio').replace('a Arkansas','an Arkansas').replace('a Alabama','an Alabama').replace('a Indiana','an Indiana').replace('a Iowa','an Iowa').replace('a Oklahoma','an Oklahoma')
 assert 35<=len(title)<=65 and 130<=len(desc)<=165
 rows.append({'id':id,'slug':slug,'name':name,'url':before['url'],'h1_preserved':before['title'],'gallery_preserved':before['gallery'],'before_content_sha256':hashlib.sha256(b.encode()).hexdigest(),'seo_title':title,'meta_description':desc,'title_chars':len(title),'meta_chars':len(desc),'description':after,'primary_cluster':'GEO-'+slug+'-stl-cnc','base_listed':base,'illustration_target':target,'before_seo_title':before['seo_title'],'before_meta_description':before['meta_description'],'before_excerpt_sha256':hashlib.sha256(before['excerpt'].encode()).hexdigest(),'baseline_protected':before['protected']})
 semantic['editorial_clusters'].append({'cluster_id':'GEO-'+slug+'-stl-cnc','product_id':id,'primary':name+' topographic map STL','supporting':[name+' terrain STL',name+' relief map STL',name+' map 3D print',name+' CNC terrain model'],'measured_frequency':None,'rank':None,'status':'editorial product mapping; USA Google English intent; each geographic entity is a country; market remains USA'});refs[slug]=[i['id'] for i in before['images'][:2]]
 print(id,name,'base',base,'refs',refs[slug],'target',target[:90])
(root/'semantic-review.json').write_text(json.dumps(semantic,ensure_ascii=False,indent=2),encoding='utf-8');(root/'manifest.json').write_text(json.dumps({'site_profile':'shustrik-maps','publication_authorized':True,'rows':rows},ensure_ascii=False,indent=2),encoding='utf-8')
s='<?php\nini_set("display_errors","0");define("WP_USE_THEMES",false);ob_start();require "/var/www/html/wp-load.php";ob_end_clean();\nforeach('+json.dumps(refs).replace('{','[').replace('}',']').replace(':','=>')+' as $slug=>$ids){foreach($ids as $i=>$aid){if(!copy(get_attached_file($aid),"/tmp/".$slug."-source-".($i+1).".jpg"))exit(1);}}';(repo/'.codex-work/five-next-country-refs.php').write_text(s,encoding='utf-8')
lines=['---','type: seo-page-brief','site_profile: shustrik-maps','status: approved','created_at: 2026-10-08','market: USA','language: English','---','','# '+', '.join(d[2] for d in defs),'','Owner authorized next five complete product updates and publication. Main prose, H1, URLs, excerpts/specifications, upper galleries, commerce and protected metadata preserved. Only selected illustration and two Yoast fields change. Four JPEG1500x1000 each: ivory plastic desktop, small framed wall art, kraft gift, huge grey concrete installation. Own native carousel; one slide desktop/mobile, manual arrows/dots, no autoplay. Only bold centered AI-generated application concepts notice. Original source media not deleted.','','Semantic limitations: All five exact STL clusters are absent from the saved core. Proposed product query groups are editorial hypotheses with no measured frequencies/ranks. No reassigning elevation or vector intent to STL. Broad public search supports paid digital-file intent but does not establish US-local ranks or demand. New groups saved in semantic-review.json; original core retained.']
for r in rows:lines+=['',f'## {r["name"]} / {r["id"]}',r['url'],f'Primary: {r["name"]} topographic map STL. Support: terrain STL / relief map STL / 3D print / CNC terrain. Exclude free/physical-only/ordinary maps/vector/elevation-data and county/city-only intent.',f'SEO title: {r["seo_title"]}',f'Meta description: {r["meta_description"]}',f'Listed base: {r["base_listed"]}. Mesh accuracy/readiness/archive not validated by this content release.']
lines+=['','Validation: source commit/push/archive SHA, lint/preview/concurrency backup, protected hashes, 20media JPEG/title/alt/dimensions, public10URLchecks, canonical/H1/indexability/Product/CTA, browser40samples, runtime, guarded rollback-preview, report and canonical docs.']
(root/'Page Briefs.md').write_text('\n\n'.join(lines),encoding='utf-8')
