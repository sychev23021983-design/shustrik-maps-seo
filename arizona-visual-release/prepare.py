from pathlib import Path
import json,re,hashlib
from PIL import Image
r=Path(__file__).resolve().parent
assets=Path('J:/1. My Vault/01 Projects/WordPress/shustrik-maps.com/Visual Pilot 2026-10-05')
b=json.loads((r/'baseline.json').read_text(encoding='utf-8-sig'))
items=[('desk','Arizona Terrain STL — Desk Display Concept','AI-generated concept of an ivory Arizona terrain relief on a separate wooden desk stand.','Desk display idea','arizona-desk-ai-concept-v1.png'),('gift','Arizona Terrain STL — Personal Gift Concept','AI-generated concept of an Arizona terrain relief in a kraft gift box with ribbon.','Personal gift idea','arizona-gift-ai-concept-v1.png'),('hotel','Arizona Terrain STL — Hotel Reception Concept','AI-generated commercial concept of a bronze-finished Arizona terrain wall panel behind a hotel reception desk.','Commercial interior idea','arizona-hotel-commercial-ai-concept-v1.png')]
media=[]
for slug,title,alt,heading,source in items:
 name=f'arizona-terrain-{slug}-ai-concept.webp'
 im=Image.open(assets/source); im.save(r/name,'WEBP',quality=88,method=6)
 media.append(dict(file=name,title=title,alt=alt,heading=heading,caption='AI-generated application concept. Digital STL model only; fabrication, finish, stand, packaging and mounting are not included.'+(' Commercial use requires separately agreed permission.' if slug=='hotel' else ''),sha256=hashlib.sha256((r/name).read_bytes()).hexdigest(),width=im.width,height=im.height))
blocks=list(re.finditer(r'(\[vc_column_text[^\]]*\])(.*?)(\[/vc_column_text\])',b['content'],re.S))
assert len(blocks)==2
intro='''<h2>Arizona topographic map STL for 3D printing and CNC projects</h2>
<p>This digital <strong>Arizona topographic map STL</strong> provides a 3D terrain relief of the state, with mountains, plateaus and canyon features. Use it as the starting point for a physical relief map, a desktop display or a decorative terrain project.</p>
<p>The product is an <strong>STL model download</strong>, not a finished printed object or a standalone GeoTIFF/DEM dataset. Prepare the file in your own slicing or CAM workflow, and check scale, material and fabrication settings for your equipment before production.</p>'''
detail='''<h2>Plan your Arizona terrain project</h2>
<ul><li>Digital STL terrain model for 3D-printing and CNC workflows.</li><li>Arizona-wide relief for display, personal creative projects and terrain visualization.</li><li>Physical fabrication, finishing, packaging and display accessories are separate.</li></ul>
<h3>Choose the right file for your workflow</h3>
<p>This page offers the Arizona STL terrain model. For a different 3D-model workflow or a dedicated Grand Canyon model, use the related product links below and check each product’s own file formats.</p>
<p>Review the technical panel before purchase. Need clarification about model dimensions, projection or your intended workflow? <a href="mailto:shustrikmaps@gmail.com">Ask about this Arizona STL model</a>.</p>
<h3>Use and licensing</h3>
<p>The standard licence is for personal use. Commercial display and other commercial uses require separately agreed permission. <a href="https://shustrik-maps.com/terms-of-service/">Review the usage terms</a> or contact us before buying for a commercial project.</p>'''
body=b['content']
for match,html in reversed(list(zip(blocks,[intro,detail]))):body=body[:match.start(2)]+ '\n'+html+'\n'+body[match.end(2):]
body+='[vc_row][vc_column][vc_column_text]<section id="arizona-ai-application-concepts"><h2>Ideas for your Arizona terrain model</h2><p>Explore three display ideas based on the Arizona relief: a desk piece, a personal gift and a commercial interior installation. These AI-generated scenes illustrate styling and fabrication concepts; they are not photographs of tested prints.</p>{{AI_FIGURES}}</section>[/vc_column_text][/vc_column][/vc_row]'
assert '<h1' not in body
manifest=dict(product_id=9520,owner_instruction='2026-10-05: three images including commercial, title/alt, upload to product, check semantics and make relevant changes if needed',before_content_sha256=hashlib.sha256(b['content'].encode()).hexdigest(),seo_title=b['seo_title'],meta_description='Arizona topographic map STL for 3D printing and CNC terrain projects. Explore relief display ideas and check file details before buying this digital model.',content_template=body,media=media)
(r/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'media':[{k:m[k] for k in ['file','title','alt']} for m in media],'webp_bytes':[ (r/m['file']).stat().st_size for m in media],'content_blocks_preserved':True}))
