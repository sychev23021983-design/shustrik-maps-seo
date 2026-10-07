from pathlib import Path
import json,re,ast,shutil
root=Path(__file__).parent
repo=Path('J:/1. My Vault/90 Migration/shustrik-maps-seo')
defs=json.loads((root/'defs.json').read_text(encoding='utf-8'))
folder=repo/'ten-more-country-stl-slider-release-20261007';folder.mkdir(exist_ok=True)
s=(repo/'ten-country-stl-slider-release-20261007/release.php').read_text(encoding='utf-8').replace('ten_country','ten_more_country')
s=s.replace('[9382,9384,9387,9397,9398,9399,9400,9401,9402,9404]',json.dumps([x[0] for x in defs],separators=(',',':')))
(folder/'release.php').write_text(s,encoding='utf-8')
m=json.loads((root/'manifest.json').read_text(encoding='utf-8'));b=json.loads((root/'baseline.json').read_text(encoding='utf-8'))
for before,r in zip(b['rows'],m['rows']):
    strip=re.sub(r'\[woodmart_gallery[^\]]*\]\[vc_column_text\]<p style="text-align: center;"><strong>AI-generated application concepts.</strong></p>\[/vc_column_text\]','',r['description'])
    assert strip==before['content'].replace(r['illustration_target'],'')
    assert r['description'].count('[woodmart_gallery')==1
    assert r['base_listed']=='closed'
    print(r['id'],r['seo_title'],r['title_chars'],r['meta_chars'],'prose preserved')
semantic=json.loads((root/'semantic-review.json').read_text(encoding='utf-8'))
semantic['note']='All ten exact STL clusters are absent in the saved Google/English/USA core 2026-10-05. Editorial paid digital-file mapping; no measured frequency/rank or controlled Google US SERP observation.'
for r in semantic['editorial_clusters']:r['status']='editorial country/island digital STL mapping; intended Google/English/USA market; frequency/rank unmeasured'
(root/'semantic-review.json').write_text(json.dumps(semantic,ensure_ascii=False,indent=2),encoding='utf-8')
lines=['---','type: seo-page-brief','site_profile: shustrik-maps','status: approved','created_at: 2026-10-07','market: USA','language: English','---','','# Ten more country and island STL product briefs','','Owner authorized this batch through the instruction “Следующие десять.” SEO title and meta only; original Description prose, H1, URL, excerpt/specs, commerce, downloads and upper galleries preserved. Replace the sole common 9586 illustration insert with a product-specific carousel. Shared blocks/media remain.','','Intent: paid downloadable country/island terrain STL; excludes ordinary maps, free files, physical products, city-only miniatures, coins/tokens, non-STL multi-format terrain, and DEM/DTM/vector datasets. No accuracy, mesh-readiness, license or compatibility promises added. Existing canonical/robots/schema/cart/internal links preserved. All listed bases closed; actual meshes/archives not inspected.']
for r in m['rows']:
    lines+=['',f'## {r["name"]} / {r["id"]}',r['url'],f'Primary: {r["name"]} topographic map STL. Supporting: terrain STL / relief map STL / map 3D print / CNC terrain model.',f'Title: {r["seo_title"]}',f'Meta: {r["meta_description"]}',f'H1 preserved: {r["h1_preserved"]}', 'Acceptance: exact source prose/protected hashes; four own JPEG 1500x1000 with AI title/alt; continuous desktop support; single-slide carousel desktop/mobile, arrows/dots, no autoplay; centered bold short AI caption; one-time apply with baseline/backup/journal guards; DB/public/browser/runtime/rollback-preview QA.']
lines+=['','Cannibalization: Jordan means the country, not people or basketball shoes; Jamaica means the whole island, not Kingston city; Kazakhstan means the country, not Astana; Kuwait includes the islands in its own SKU render, not Salmiya city; Liberia is not a coin/token; Libya is distinct from Liberia. Belarus excluded. No new URLs/hubs.']
(root/'Page Briefs.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
geo={
'belgium':'Exact broad irregular Belgium outline from the reference, gentle northern/western lowland and stronger dissected relief in the southeast. No alpine mountains across the flat north.',
'jamaica':'Exact long east-west Jamaica island coastline, western rounded end, southern projections, rolling central terrain and rugged eastern mountain group. Whole Jamaica island, not Kingston city.',
'jordan':'Exact Jordan outline: tall western body with rugged western escarpment, long northeastern triangular projection, distinctive deep angular eastern notch and subdued eastern desert. Preserve sharp geometric borders.',
'kazakhstan':'Exact very wide Kazakhstan national silhouette with deep southwest border step, irregular northern edge, mainly flat/subdued western and central plains, rugged far eastern and southeastern ridges. No invented mountains across the whole country.',
'kosovo':'Exact Kosovo irregular vertical outline, northern protrusion and narrow southern tip, central lower basins surrounded by rugged western/southern ridges; preserve all contour details.',
'kuwait':'Exact Kuwait silhouette with broad almost flat interior and deep northeastern Kuwait Bay opening. Preserve ALL islands and coastal fragments shown, especially the large northeastern island and small offshore pieces, in correct relative positions. Every fragment fully bonded to the same continuous backing. Gentle relief, no invented alpine peaks.',
'kyrgyzstan':'Exact wide Kyrgyzstan silhouette with irregular western projections, strong rugged mountain ridges and a smooth elongated northeast lake basin. Preserve geographic orientation and all shown contour fragments.',
'laos':'Exact long Laos outline: broad mountainous northern body, narrow curved southeastern tail, rugged central/eastern ridges and smoother southern basin. Preserve the northern projecting lobe and long narrow tail.',
'liberia':'Exact Liberia outline running northwest to southeast, Atlantic coast along southwest, two irregular northern lobes with deep notch between, subdued coastal plain and textured inland ridges. Not Libya.',
'libya':'Exact broad Libya polygon with northern Mediterranean coastline and deep central Gulf of Sidra curve, mostly subdued desert plateau, northern uplands and isolated southern/western relief. Straight east edge and southern angular border. Not Liberia.'}
tree=ast.parse((root.parent/'Ten Next STL Sliders 2026-10-06/build-jobs.py').read_text(encoding='utf-8'))
scenes=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='scenes' for t in n.targets))
jobs=[]
for id,slug,name in defs:
    for scene,detail in scenes.items():
        prompt=f'Use case: product-mockup. Create ONE photorealistic AI application concept for {name} topographic STL. Landscape 3:2 aspect ratio, 1536x1024 preferred, later JPEG1500x1000. The input image is the actual SKU geography reference: preserve its silhouette, proportions, orientation, coverage and relative relief positions. {geo[slug]} North up; no mirroring or rotation of the map. Replace the reference yellow material with the requested material. {detail} Whole map and backing must remain in frame. Physically plausible support everywhere. No text, labels, logos, watermark, people, collage or multiple views. Refined editorial product photography; illustrative fabrication concept, not a photograph of an existing physical product.'
        jobs.append({'id':id,'slug':slug,'name':name,'scene':scene,'ref':str(root/(slug+'-source-1.jpg')),'prompt':prompt})
(root/'generation-jobs.json').write_text(json.dumps(jobs,ensure_ascii=False,indent=2),encoding='utf-8')
for n in ['baseline.json','manifest.json','semantic-review.json','Page Briefs.md','generation-jobs.json','build-release.py','deliver.py','public-qa.py','verify-preservation.py','backup-export.php','export.py','defs.json','selection.json']:
    shutil.copy2(root/n,folder/n)
print('Guarded source and 40 own-reference prompts prepared; no content published')
