from pathlib import Path
import json,re,ast,shutil
root=Path(__file__).parent
repo=Path('J:/1. My Vault/90 Migration/shustrik-maps-seo')
defs=json.loads((root/'defs.json').read_text())
folder=repo/'ten-eurasia-stl-slider-release-20261007';folder.mkdir(exist_ok=True)
s=(repo/'ten-more-country-stl-slider-release-20261007/release.php').read_text(encoding='utf-8').replace('ten_more_country','ten_eurasia')
s=s.replace('[9403,9406,9408,9409,9410,9411,9412,9420,9421,9422]',json.dumps([d[0] for d in defs],separators=(',',':')))
(folder/'release.php').write_text(s,encoding='utf-8')
m=json.loads((root/'manifest.json').read_text(encoding='utf-8'));b=json.loads((root/'baseline.json').read_text(encoding='utf-8'))
for before,r in zip(b['rows'],m['rows']):
 strip=re.sub(r'\[woodmart_gallery[^\]]*\]\[vc_column_text\]<p style="text-align: center;"><strong>AI-generated application concepts.</strong></p>\[/vc_column_text\]','',r['description'])
 assert strip==before['content'].replace(r['illustration_target'],'')
 assert r['description'].count('[woodmart_gallery')==1
 if r['slug']=='north-america-lambert':
  r['seo_title']='North America Lambert STL | Topographic Map for 3D Print'
  r['meta_description']='Download a North America topographic STL in Lambert Conformal Conic projection for 3D printing and CNC projects. Explore desk, wall and gift concepts.'
  r['title_chars']=len(r['seo_title']);r['meta_chars']=len(r['meta_description'])
 if r['id']==9481:
  assert '• Base: Closed' in before['excerpt'];r['base_listed']='closed'
 print(r['id'],r['title_chars'],r['meta_chars'],'prose preserved',r['base_listed'])
(root/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
sem=json.loads((root/'semantic-review.json').read_text(encoding='utf-8'))
assert not sem['existing_clusters'] and not sem['existing_keywords']
sem['note']='Exact ten STL clusters absent from saved Google/English/USA core. Editorial digital-file intent, no measured frequency/rank and no controlled Google US SERP. Lambert has separate projection-specific intent; broad North America relief metrics are not inherited.'
for x in sem['editorial_clusters']:
 x['status']='editorial country/continent STL mapping; intended Google/English/USA; unmeasured'
 if x['product_id']==9475:x['primary']='North America Lambert Conformal Conic STL';x['supporting']=['North America Lambert topographic STL','Lambert terrain STL','North America Lambert map 3D print','North America Lambert CNC model']
(root/'semantic-review.json').write_text(json.dumps(sem,ensure_ascii=False,indent=2),encoding='utf-8')
lines=['---','type: seo-page-brief','site_profile: shustrik-maps','status: approved','created_at: 2026-10-07','market: USA','language: English','sources: [baseline.json, semantic-review.json, Intent Review.md]','next_action: Publish authorized scope and verify','---','','# Ten Eurasia and atlas STL product briefs','','Owner authorized full cycle with “Следующие десять.” Audience: US users seeking paid digital STL terrain for 3D printing/CNC. Preserve original prose/H1/URL/excerpt/specs/prices/files/gallery. Change two Yoast fields and sole common illustration insert. Existing canonical/indexability/Product schema/CTA/internal links preserved.','','Exclude free files, physical-only products, coins/tokens, city-only models, maps of other formats, DEM/vector data. No new accuracy/readiness/compatibility/license claims. All ten listed bases closed; Luxembourg uses legacy bullet markup. No actual mesh inspection.']
for r in m['rows']:
 lines+=['',f'## {r["name"]} / {r["id"]}',r['url'],f'Primary: {next(x["primary"] for x in sem["editorial_clusters"] if x["product_id"]==r["id"])}',f'SEO title: {r["seo_title"]}',f'Meta description: {r["meta_description"]}',f'H1 preserved: {r["h1_preserved"]}',f'Listed base: {r["base_listed"]}.', 'Acceptance: exact source/protected preservation; four own true JPEG 1500x1000/AI title/alt; solid desktop backing behind every fragment; manual native carousel one slide desktop/mobile with arrows/dots; centered bold short AI notice; backup/journal/concurrent-edit guards; one-time apply; DB/public/browser/runtime/rollback-preview QA.']
lines+=['','Cannibalization: Myanmar includes Burma naming intent; Turkey means country, not bird. Ireland SKU coverage follows own reference. Czech Republic/Czechia are same country; avoid Prague-only intent. North America9475 explicitly Lambert Conformal Conic, distinct from9392. Luxembourg country distinct from city miniature. Belarus excluded. No new URLs.']
(root/'Page Briefs.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
geo={
'myanmar':'Exact tall Myanmar silhouette, broad northern mountainous body, long narrow southern coastal tail with all shown offshore fragments, lower central north-south basin and western/eastern mountain belts. Preserve every thin coastal piece on common backing.',
'turkey':'Exact very wide Turkey silhouette, small northwest European section across the straits, deeply notched western coastline and shown islands; northern and southern mountain belts and stronger eastern relief, smoother central plateau. All separate pieces fixed to common panel.',
'ukraine':'Exact Ukraine silhouette and coverage shown in this SKU, including southern peninsula and all coastal pieces. Low rolling plains with strongest relief in southwest and small southern mountain belt. Do not replace or crop the reference outline; no invented mountain chains across plains.',
'finland':'Exact tall Finland silhouette with hooked northwest projection, broad southern body and northern uplands, mainly subtle low relief. Preserve all small coastal fragments on common backing. No exaggerated alpine mountains across flat southern body.',
'ireland':'Exact Ireland SKU outline in the reference, including its distinctive northeast indentation and northern lobe. Do not fill the northeast cutout or substitute a whole-island outline. Central lowland, southwest coastal ridges and southeastern uplands. Preserve western coastal fragments.',
'sweden':'Exact tall Sweden silhouette, mountainous northwest/northern spine, gentle southern lowland; preserve the narrow southeast offshore island and larger eastern island in their own relative positions. Every offshore piece bonded to common continuous panel.',
'north-america-lambert':'Exact North America Lambert Conformal Conic projection and coverage of this SKU: Alaska upper left, Greenland upper right, ALL Arctic archipelago, western mountain chain, central plains, eastern uplands, Mexico, Central America and Caribbean islands. Preserve projection and separate fragments, all bonded to one common continuous backing. Do not substitute Mercator or omit Greenland.',
'romania':'Exact broad Romania silhouette with eastern coastal projection and southeast coast. Strong curved Carpathian mountain arc around central lower basin, southern/eastern lowlands and separate western uplands. Preserve shape and relative ridge positions.',
'czech-republic':'Exact Czech Republic broad west-east silhouette, rounded western body and eastern projecting lobe; raised border mountains surrounding lower central basins. Preserve subtle relative relief, no invented alpine peaks.',
'luxembourg':'Exact tall compact Luxembourg silhouette, distinctive narrow northern neck, broad southern body and southeast projection; dissected northern hills and gentle southern plateau. No invented alpine peaks.'}
tree=ast.parse((root.parent/'Ten Next STL Sliders 2026-10-06/build-jobs.py').read_text(encoding='utf-8'))
scenes=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='scenes' for t in n.targets))
jobs=[]
for id,slug,name in defs:
 for scene,detail in scenes.items():
  prompt=f'Use case: product-mockup. Create ONE photorealistic AI application concept for {name} topographic STL. Landscape 3:2 aspect ratio, 1536x1024 preferred, later JPEG1500x1000. Input is actual SKU geography reference: preserve silhouette, proportions, orientation, coverage and relief positions. {geo[slug]} North up, no mirroring or rotation. Replace yellow reference material with requested material. {detail} Entire map and backing fully visible. Physically plausible support everywhere. No text, labels, logo, watermark, people, collage or multiple views. Refined editorial product photography; illustrative fabrication concept.'
  jobs.append({'id':id,'slug':slug,'name':name,'scene':scene,'ref':str(root/(slug+'-source-1.jpg')),'prompt':prompt})
(root/'generation-jobs.json').write_text(json.dumps(jobs,ensure_ascii=False,indent=2),encoding='utf-8')
for n in ['baseline.json','manifest.json','semantic-review.json','Page Briefs.md','generation-jobs.json','build-release.py','deliver.py','public-qa.py','verify-preservation.py','backup-export.php','export.py','defs.json','selection.json']:
 shutil.copy2(root/n,folder/n)
print('Guarded ten-card source and 40 prompts prepared')
