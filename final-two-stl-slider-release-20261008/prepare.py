from pathlib import Path
import json,re,hashlib,shutil
root=Path(__file__).parent;old=root.parent/'Next Lunar Sliders 2026-10-08';out=Path('J:/1. My Vault/90 Migration/shustrik-maps-seo/final-two-stl-slider-release-20261008')
base=json.loads((root/'baseline.json').read_text(encoding='utf-8-sig'));defs=json.loads((root/'defs.json').read_text(encoding='utf-8-sig'));rows=[]
g='[woodmart_gallery images="{{IMAGE_IDS}}" view="carousel" img_size="large" caption="0" lazy_loading="yes" spacing="0" slides_per_view="1" slides_per_view_mobile="1" carousel_arrows_position="together" wrap="no" autoheight="no" autoplay="no" hide_prev_next_buttons="no" hide_pagination_control="no" hide_pagination_control_tablet="no" hide_pagination_control_mobile="no"]'
notice='[vc_column_text]<p style="text-align: center;"><strong>AI-generated application concepts.</strong></p>[/vc_column_text]'
for b,(id,slug,name) in zip(base['rows'],defs):
 text=b['content'];assert 'AI-generated' not in text
 if id==16743:
  targets=[x for x in re.findall(r'\[woodmart_image\b[^\]]*\]',text) if 'img_id="16744"' in x];assert len(targets)==1
  after=text.replace(targets[0],g+notice,1);target=targets[0]
  title='Moon Surface STL | Lunar Terrain 3D Model'
  meta='Download the Moon Surface 3D model in STL and C4D formats, with textures listed. Explore lunar terrain relief concepts for desktop displays, wall art and gifts.'
 else:
  targets=[x for x in re.findall(r'\[vc_section\b[^\]]*\].*?\[/vc_section\]',text,re.S) if 'image="16813"' in x];assert len(targets)==1
  target=targets[0];assert not re.search(r'\[(?:vc_column_text|woodmart_text_block)',target)
  after=text.replace(target,'',1)
  intro=re.search(r'\[vc_section\b[^\]]*\].*?\[/vc_section\]',after,re.S).group()
  assert '[vc_column]' in intro and intro.count('[/vc_column]')==1
  newintro=intro.replace('[vc_column]','[vc_column width="1/2"]',1).replace('[/vc_column][/vc_row]','[/vc_column][vc_column width="1/2"]'+g+notice+'[/vc_column][/vc_row]',1)
  after=after.replace(intro,newintro,1)
  title='Abstract Female Face STL | Geometric Relief 3D Model'
  meta='Download an abstract female face silhouette STL model with geometric relief details. Explore desktop display, framed wall art and gift presentation concepts.'
 assert len(title)<=65 and 130<=len(meta)<=165,(len(title),len(meta))
 for tag in ['vc_column_text','woodmart_text_block']:
  before=re.findall(r'\['+tag+r'[^\]]*\](.*?)\[/'+tag+r'\]',text,re.S);post=[x for x in re.findall(r'\['+tag+r'[^\]]*\](.*?)\[/'+tag+r'\]',after,re.S) if 'AI-generated application concepts.' not in x];assert before==post
 for tag in ['woodmart_gallery','vc_single_image','html_block','idcore','woodmart_button','woodmart_title']:
  before=re.findall(r'\['+tag+r'\b[^\]]*\]',text);post=re.findall(r'\['+tag+r'\b[^\]]*\]',after)
  if tag=='woodmart_gallery':assert post==[g]+before
  elif tag=='vc_single_image' and id==16812:assert post==[x for x in before if 'image="16813"' not in x]
  else:assert before==post,(id,tag)
 rows.append({'id':id,'slug':slug,'name':name,'url':b['url'],'h1_preserved':b['title'],'gallery_preserved':b['gallery'],'before_content_sha256':hashlib.sha256(text.encode()).hexdigest(),'before_seo_title':b['seo_title'],'before_meta_description':b['meta_description'],'before_excerpt_sha256':hashlib.sha256(b['excerpt'].encode()).hexdigest(),'baseline_protected':b['protected'],'seo_title':title,'meta_description':meta,'description':after,'illustration_target':target,'base_listed':'closed' if id==16743 else 'open'})
(root/'manifest.json').write_text(json.dumps({'site_profile':'shustrik-maps','publication_authorized':True,'rows':rows},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for filename in ['release.php','backup-export.php','deliver.py','verify-preservation.py','public-qa.py']:
 s=(old/filename).read_text(encoding='utf-8-sig').replace('next-lunar-slider-release-20261008','final-two-stl-slider-release-20261008').replace('next_lunar','final_two_stl').replace('next-lunar','final-two-stl').replace('[16696,16728]','[16743,16812]')
 s=s.replace(".read_text()",".read_text(encoding='utf-8-sig')")
 (root/filename).write_text(s,encoding='utf-8',newline='\n')
clusters=[{'product_id':16743,'primary':'Moon Surface STL','supporting':['lunar terrain STL','Moon relief 3D model'],'exclude':['Moon globe','free identical files','generic game terrain','scientific accuracy promises']},{'product_id':16812,'primary':'abstract female face STL','supporting':['geometric face relief','female face wall panel STL'],'exclude':['anatomical head scans','female bust','free identical files','physical goods']}]
(root/'semantic-review.json').write_text(json.dumps({'site_profile':'shustrik-maps','language':'English','engine':'Google','market':'USA','new_metrics_collected':False,'us_rank_verified':False,'editorial_clusters':clusters,'decision':'validate first','note':'Existing products publication authorized. Google hl=en/gl=us/pws=0, actual footer location Unknown; no measured demand, positions or mesh validation.'},indent=2)+'\n',encoding='utf-8')
intent=[{'query':'moon surface terrain STL 3D model','file':'google-moon-surface.txt','observations':'Lunar terrain digital download intent mixed with free terrain generators, Moon globes, NASA assets and tabletop game terrain.'},{'query':'abstract female face relief STL','file':'google-female-face.txt','observations':'Paid decorative relief/CNC digital download intent mixed with free sculptures and busts. Our geometric portrait panel is the relevant format.'}]
(root/'intent-evidence.json').write_text(json.dumps(intent,indent=2)+'\n',encoding='utf-8')
brief='# Final Two STL Page Briefs\n\nOwner-authorized external WordPress content publication. English, Google, USA; Belarus excluded. Fresh catalog516 leaves exactly these2 eligible explicitly listed STL products after excluding already processed Denmark. No C4D-only substitutions.\n\nEditorial clusters and observed public Google SERPs saved separately. No measured frequency/rank/difficulty; actual search footer location Unknown. Moon retains listed STL/C4D/textures and closed base. Female Face retains STL/open base: concept backing is additional fabrication. Meshes not printed or scientifically validated. All original prose/excerpts, H1, URL, commerce/downloads/specs, upper gallery, sample renders, Internet ideas galleries and shared HTML blocks retained. Only first own illustration replaced by a four-slide gallery and short centered bold AI notice.\n'
for r in rows:brief+='\n'+r['url']+'\n\nSEO title: '+r['seo_title']+'\n\nMeta description: '+r['meta_description']+'\n\nH1 retained: '+r['h1_preserved']+'\n'
brief+='\nAcceptance: true JPEG1500x1000 own-reference8 images/AI titles/alts/SHA, guarded preflight/backup/rollback, exact pushed archive, all4slides desktop/mobile, original fields exact, runtime unchanged. Existing P1/yellow/degraded and10October index check retained.\n'
(root/'Page Briefs.md').write_text(brief,encoding='utf-8')
for p in root.iterdir():
 if p.is_file() and p.suffix in ['.php','.py','.json','.md','.jpg','.png','.txt']:shutil.copy2(p,out/p.name)
print([(r['id'],len(r['seo_title']),len(r['meta_description'])) for r in rows])
