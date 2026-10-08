from pathlib import Path
import json,shutil
root=Path(__file__).parent
defs=json.loads((root/'defs.json').read_text())
observations=[
 ('Paid terrain STL/CNC listings versus free outline/claim-inclusive maps, ordinary elevation maps and GIS relief data. Preserve the supplied product outline, no geographic claim expansion.','https://www.etsy.com/listing/1458469211/venezuela-topographical-relief-map-3d'),
 ('Paid whole-geography STL terrain versus free relief images, map-to-STL tools, collector coins and city models.','https://www.etsy.com/listing/1471233145/uzbekistan-hd-topographic-terrain-3d'),
 ('Paid STL terrain versus free continent-country packs, outline cutters and ordinary printed/GIS maps.','https://www.etsy.com/listing/1432143632/uruguay-topographic-map-3d-model-file'),
 ('Whole UAE / United Arab Emirates terrain STL versus Dubai city infrastructure, building miniatures, physical shaded-relief prints and free map data.','https://www.cgtrader.com/3d-print-models/miniatures/other/3d-topographical-map-of-the-united-arab-emirates'),
 ('Paid Taiwan terrain STL versus free island relief, Taipei city miniatures, physical shaded-relief posters and ordinary GIS maps.','https://www.etsy.com/ca/listing/1755322830/taiwan-topographic-map-3d-model-file-stl')]
evidence={'date':'2026-10-08','market':'USA','language':'English','google_parameters':'hl=en&gl=us&pws=0','location':'Unknown / cannot determine location; US physical location and local ranking not verified','measured_frequency':None,'measured_rank':None,'rows':[]}
lines=['# Google English / USA intent review — 2026-10-08','','Five own product queries observed in Google, qualitative intent only. Saved semantic core has no exact five STL clusters. New clusters are editorial product mappings; no new demand or rank measurement. Belarus excluded. Google AI Overview product claims are not adopted. Publication is authorized by the owner; later SEO impact measurement remains separate.','']
for (id,slug,name),(note,url) in zip(defs,observations):
 evidence['rows'].append({'id':id,'query':name+' topographic map STL','google_url':'https://www.google.com/search?q='+name.replace(' ','+')+'+topographic+map+STL&hl=en&gl=us&pws=0','raw_snapshot':'google-'+slug+'.txt','intent_inference':note,'primary_seller_source':url})
 lines+=['## '+name,'',note+' This is an inference from the observed result mix, not measured demand. [Primary seller listing]('+url+').','']
assert all((root/r['raw_snapshot']).exists() for r in evidence['rows'])
(root/'intent-evidence.json').write_text(json.dumps(evidence,indent=2),encoding='utf-8')
(root/'Intent Review.md').write_text('\n'.join(lines),encoding='utf-8')
# Taiwan is a geographic product entity; no political classification is needed.
p=root/'semantic-review.json';s=json.loads(p.read_text())
for r in s['editorial_clusters']:r['status']='editorial product mapping; Google English USA intent; whole geographic entity, market remains USA'
uae=next(r for r in s['editorial_clusters'] if r['product_id']==19891);uae['supporting']+=['United Arab Emirates topographic STL','United Arab Emirates terrain STL']
p.write_text(json.dumps(s,indent=2),encoding='utf-8')
out=Path('J:/1. My Vault/90 Migration/shustrik-maps-seo/five-country-stl-slider-release-20261008')
for n in ['Intent Review.md','intent-evidence.json','finish-semantic-oct8.py']:
 shutil.copy2(root/n,out/n)
for p in root.glob('google-*.txt'):
 (out/p.name).write_text('\n'.join(l.rstrip() for l in p.read_text(encoding='utf-8').splitlines())+'\n',encoding='utf-8')
print('Five Google observations and primary seller examples saved; no measured frequencies or ranks')
