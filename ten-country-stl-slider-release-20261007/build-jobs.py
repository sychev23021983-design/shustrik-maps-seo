import json,ast
from pathlib import Path
root=Path(__file__).parent
old=root.parent/'Ten Next STL Sliders 2026-10-06/build-jobs.py'
tree=ast.parse(old.read_text(encoding='utf-8'))
scenes=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='scenes' for t in n.targets))
geo={
'afghanistan':'Preserve the wide irregular Afghanistan outline and long narrow northeastern Wakhan corridor exactly; rugged central and northeastern Hindu Kush ridges and gentler southwestern plains.',
'crete':'Preserve the long narrow east-west Crete island outline, western peninsulas, mountain groups and ALL small islands shown in the SKU reference in their relative locations. All islands secured flush to the same backing.',
'corsica':'Preserve the tall Corsica island silhouette, narrow northern Cap Corse projection, rugged central-western mountains and gentler eastern coast. Any small coastal fragments fixed to same backing.',
'algeria':'Preserve the broad polygonal Algeria outline, northern Mediterranean coast and Atlas ridges, broad subdued Sahara and southeastern highland group. No invented mountain chain across central desert.',
'andorra':'Preserve the exact small irregular Andorra country outline and dense Pyrenees mountain ridges and deep branching valleys from the SKU render.',
'angola':'Preserve Angola main polygon outline with Atlantic coast west, southern border step and detached Cabinda fragment northwest EXACTLY as shown. Cabinda fully fixed to the same backing; western-central uplands and gentler eastern plains.',
'armenia':'Preserve exact Armenia outline with diagonal northwest-southeast body, rugged volcanic highlands, lake/valley depressions and narrow southern extent; every separate fragment shown fixed to the same backing.',
'azerbaijan':'Preserve exact Azerbaijan main silhouette, northeastern Greater Caucasus, central lowlands, western mountains, eastern Caspian peninsula and southern projection. Include detached Nakhchivan southwest and every small fragment shown, all fixed to the common backing in exact relative locations.',
'bangladesh':'Preserve exact Bangladesh outline, mostly LOW FLAT river delta with intricate southern estuary channels and many small islands, only narrow southeastern Chittagong hill ridges. All delta fragments attached on common continuous backing; no invented mountain belt across the flat country.',
'dominica':'Dominica Caribbean island, NOT Dominican Republic. Preserve tall narrow island outline and rugged central volcanic mountain spine, all shown coastal shape details.'}
jobs=[]
for id,slug,name in json.loads((root/'defs.json').read_text(encoding='utf-8')):
 for scene,details in scenes.items():
  prompt=f'Use case: product-mockup. Create ONE photorealistic AI application concept for {name} topographic STL. Landscape 3:2 aspect ratio, 1536x1024 preferred, later JPEG1500x1000. Input image is actual SKU geography reference: preserve silhouette, proportions, orientation, coverage and relative relief positions. {geo[slug]} North up, no mirroring. Replace yellow reference material with requested material. {details} Physically plausible support everywhere. No text, labels, logo, watermark, people, collage or multiple views. Refined editorial product photography; illustrative concept, not a photograph of an existing product.'
  jobs.append({'id':id,'slug':slug,'name':name,'scene':scene,'ref':str(root/(slug+'-source-1.jpg')),'prompt':prompt})
(root/'generation-jobs.json').write_text(json.dumps(jobs,ensure_ascii=False,indent=2),encoding='utf-8')
print('40 own geography prompts saved')
