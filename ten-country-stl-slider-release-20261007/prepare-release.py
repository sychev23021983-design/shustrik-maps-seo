from pathlib import Path
import json,re,shutil,hashlib
root=Path(__file__).parent;repo=Path('J:/1. My Vault/90 Migration/shustrik-maps-seo')
defs=json.loads((root/'defs.json').read_text(encoding='utf-8'));ids=[x[0] for x in defs]
folder=repo/'ten-country-stl-slider-release-20261007';folder.mkdir(exist_ok=True)
s=(repo/'ten-next-stl-slider-release-20261006/release.php').read_text(encoding='utf-8')
s=s.replace('[9416,9417,9418,9448,9450,9455,10743,10763,9392,9393]',json.dumps(ids,separators=(',',':'))).replace('ten_next','ten_country').replace('20261006','20261007')
(folder/'release.php').write_text(s,encoding='utf-8')
p=root/'backup-export.php';s=p.read_text(encoding='utf-8').replace('[9416,9417,9418,9448,9450,9455,10743,10763,9392,9393]',json.dumps(ids,separators=(',',':')));p.write_text(s,encoding='utf-8')
b=json.loads((root/'baseline.json').read_text(encoding='utf-8'));m=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
for before,after in zip(b['rows'],m['rows']):
 target=after['illustration_target'];prefix,suffix=before['content'].split(target)
 assert after['description'].startswith(prefix) and after['description'].endswith(suffix)
 strip=re.sub(r'\[woodmart_gallery[^\]]*\]\[vc_column_text\]<p style="text-align: center;"><strong>AI-generated application concepts.</strong></p>\[/vc_column_text\]','',after['description'])
 if after['id']==9384:assert strip==before['content']
 else:assert strip==before['content'].replace(target,'')
 assert after['description'].count('[woodmart_gallery')==1
 assert all(x in after['description'] for x in ['slides_per_view="1"','slides_per_view_mobile="1"','autoplay="no"','hide_prev_next_buttons="no"','hide_pagination_control_mobile="no"'])
 print(after['id'],after['seo_title'],after['title_chars'],after['meta_chars'],'preserved')
 # Correct grammar without adding factual claims.
 after['meta_description']=re.sub(r'\ba (Afghanistan|Algeria|Andorra|Angola|Armenia|Azerbaijan)\b',r'an \1',after['meta_description'])
 after['meta_chars']=len(after['meta_description'])
(root/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
# Fresh page briefs replace prior batch boilerplate.
lines=['---','type: seo-page-brief','site_profile: shustrik-maps','status: approved','created_at: 2026-10-07','market: USA','language: English','sources: [baseline.json, semantic-review.json, Intent Review.md]','next_action: "Publish authorized batch and verify"','---','','# Ten country and island STL product briefs','','Owner requested next ten full workflow updates, including publication. All original prose/H1/URL/excerpt/specifications/prices/downloads/upper galleries preserved. Nine common9586 illustration inserts replaced; Crete has no existing illustration, so its carousel is added after unchanged Applications text in the right column. Shared blocks and media retained.','','Intent: paid digital country/island terrain STL files for English-speaking US buyers. Not physical products, free files, educational maps, DEM/TIF/OBJ/C4D products or city-only areas. Frequency/rank unknown. No accuracy, mesh readiness, licensing rights or compatibility invented. Canonical, robots, existing Product schema, commerce CTA and internal links preserved.']
for r in m['rows']:
 lines+=['',f'## {r["name"]} / {r["id"]}',r['url'],f'Primary: {r["name"]} topographic map STL. Support: terrain STL / relief map STL / map 3D print / CNC terrain model.',f'Title: {r["seo_title"]}',f'Meta: {r["meta_description"]}',f'H1 preserved: {r["h1_preserved"]}',f'Listed base: {r["base_listed"]}. Digital STL composition from baseline, no physical fabricated item.', 'Acceptance: exact original content outside visual insertion; one native carousel/four own JPEG1500x1000; one slide/desktop/mobile/manual arrows+dots/no autoplay; only centered bold AI caption; protected metadata preserved; backup/rollback guards; HTTP/SEO/schema/media/browser QA.']
lines+=['','Cannibalization: Crete separated from Crete relief without water SKU; Dominica separated from Dominican Republic; Armenia/Azerbaijan STL separate from multi-format terrain SKU. Only actual SKU coverage from own renders illustrated. No new hubs/URLs.']
(root/'Page Briefs.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
semantic=json.loads((root/'semantic-review.json').read_text(encoding='utf-8'))
assert not semantic['existing_clusters'] and not semantic['existing_keywords']
semantic['note']='Ten exact GEO-place-stl-cnc clusters absent in saved core05.10. Editorial mapping only; USA Google English intended market. No measured frequency/ranks or claim of controlled US Google SERP observation. Existing non-STL clusters not reassigned.'
for r in semantic['editorial_clusters']:r['status']='editorial paid digital STL intent; Google/English/USA intended market; no measured metrics'
(root/'semantic-review.json').write_text(json.dumps(semantic,ensure_ascii=False,indent=2),encoding='utf-8')
for n in ['baseline.json','manifest.json','semantic-review.json','Page Briefs.md','generation-jobs.json','prepare-release.py']:
 shutil.copy2(root/n,folder/n)
print('Guarded release source prepared, nothing published')
