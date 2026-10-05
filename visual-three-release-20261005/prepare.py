from pathlib import Path
import json,re,hashlib,shutil
from PIL import Image
r=Path(__file__).parent
vault=Path('J:/1. My Vault/01 Projects/WordPress/shustrik-maps.com/Visual Batch 2026-10-05')
generated=Path('C:/Users/syche/.codex/generated_images/01a10ad1-15b1-7223-901f-a61919ea4763')
b=json.loads((r/'baseline.json').read_text(encoding='utf-8-sig'))
files={
 'california':['exec-b8f3939f-1144-43c8-a7bc-8fab1428d003.png','exec-ca201cbc-76ea-4531-95d1-021aa966ac25.png','exec-9363338f-e1ff-4b32-a8d9-41b5212a5929.png'],
 'new-york':['exec-b6cc7518-1389-4d33-bde4-a19e535bb26d.png','exec-75aec824-300e-4961-b672-10dfc13db1db.png','exec-4ac32517-70a8-4279-9999-b80a5c14a718.png'],
 'grand-canyon':['exec-562f82a7-c261-4f3a-af09-11b669c3a9cc.png','exec-5672d253-6652-4b5d-8227-5d488ba410f7.png','exec-7b5cfdaa-142c-450c-851c-addb8dec9b6a.png']}
alts={
 'california':['AI-generated concept of an ivory California terrain relief on a separate walnut desk stand.','AI-generated concept of a California terrain relief in a kraft gift box with green tissue paper.','AI-generated commercial concept of a bronze-finished California terrain wall relief in a hotel lounge.'],
 'new-york':['AI-generated concept of a New York State terrain relief on a separate oak backing panel on a home shelf.','AI-generated concept of a New York State terrain relief in a dark gift box with fitted foam.','AI-generated commercial concept of a New York State terrain relief on a walnut panel in a museum gallery.'],
 'grand-canyon':['AI-generated concept of a sandstone-coloured Grand Canyon terrain relief on a separate walnut display base.','AI-generated concept of a Grand Canyon terrain relief and separate supporting base in gift packaging.','AI-generated commercial concept of a framed Grand Canyon terrain relief in a visitor-centre exhibition.']}
products=[]; registry=[]
for base,slug,name,format in zip(b['rows'],files,['California','New York State','Grand Canyon'],['STL','STL','C4D / STL']):
    media=[]
    for i,(scene,src) in enumerate(zip(['desk','gift','commercial'],files[slug])):
        target=vault/f'{slug}-{scene}-ai-concept-v1.png';shutil.copy2(generated/src,target)
        webp=f'{slug}-{scene}-ai-concept.webp';im=Image.open(target);im.save(r/webp,'WEBP',quality=88,method=6)
        title=f'{name} Terrain — '+['Home Display Concept','Personal Gift Concept','Commercial Display Concept'][i]
        caption='AI-generated application concept, not a photograph of a tested print. Digital '+format+' model only; fabrication, colour finishing, support, packaging and mounting are not included.'
        if slug=='grand-canyon':caption+=' The listed STL has an open base; the support shown is additional.'
        if i==2:caption+=' Commercial use requires separately agreed permission.'
        a={'file':webp,'title':title,'alt':alts[slug][i],'caption':caption,'heading':['Home display idea','Personal gift idea','Commercial display idea'][i],'width':im.width,'height':im.height,'sha256':hashlib.sha256((r/webp).read_bytes()).hexdigest()}
        media.append(a);registry.append({'product_id':base['id'],'source_render':f'{slug}-source-overview.jpg','source_render_url':base['images'][0]['url'],'generated_original':str(generated/src),'selected_png':target.name,**a})
    content=base['content'];title=base['seo_title'];meta=base['meta_description']
    if slug=='grand-canyon':
        blocks=list(re.finditer(r'(\[vc_column_text[^\]]*\])(.*?)(\[/vc_column_text\])',content,re.S));assert len(blocks)==4
        texts=[
        '''<h2>Grand Canyon 3D model for terrain projects</h2><p>Explore a digital <strong>Grand Canyon 3D model</strong> for landscape visualization and relief-model projects. The listing specifies <strong>C4D and STL model formats</strong>, with a TIF texture. Choose the workflow that matches your software and the file details below.</p><p>This is a digital download. Fabrication, colour finishing, display bases and frames shown in application concepts are separate.</p>''',
        '''<h2>Choose a Grand Canyon terrain workflow</h2><h3>C4D landscape visualization</h3><p>Use the listed C4D format for a modelling or presentation workflow that supports it. Check texture paths and scene setup in your own software. A rendered texture is distinct from an automatically colour-printed object.</p><h3>Grand Canyon STL for a relief project</h3><p>The listing specifies an <strong>open base</strong>. Inspect the STL mesh, units and scale before fabrication; a closed printable volume, added base or other preparation may be needed. Prepare your own slicing or CAM settings for the equipment and material you plan to use.</p><h3>Check the product scope before purchase</h3><p>This is a dedicated Grand Canyon terrain asset, distinct from a whole-state Arizona model. The listed TIF is a texture; this page does not establish a standalone georeferenced DEM or GeoTIFF dataset, survey accuracy or a complete interactive map application.</p><p>Review the specifications, then use <strong>Add to cart</strong> to purchase the digital model. <a href="mailto:shustrikmaps@gmail.com">Ask about Grand Canyon files or your intended workflow</a> if you need clarification.</p>''',
        'This catalogue preview illustrates terrain shading. A standalone georeferenced elevation dataset is not established by this product listing.',
        'The product listing specifies a TIF texture. Display colours in the concepts represent additional finishing and are not an automatically colour-printed STL result.'
        ]
        for m,text in reversed(list(zip(blocks,texts))):content=content[:m.start(2)]+'\n'+text+'\n'+content[m.end(2):]
        title='Grand Canyon 3D Model | C4D & STL Terrain Files'
        meta='Download a Grand Canyon terrain model listed in C4D and STL formats with a TIF texture. Review the open-base STL and file details before planning your project.'
    commercial=['a hotel lounge wall panel','a museum terrain exhibit','a visitor-centre display'][list(files).index(slug)]
    if slug=='grand-canyon': useintro='Explore a tabletop relief, a personal gift and a visitor-centre installation. Coloured finishing and any closed supporting base are additional fabrication steps.'
    else: useintro=f'Explore how a {name} terrain relief could become a home display, a personal gift or {commercial}. Choose a material, scale and finish for your own project.'
    content+=f'''[vc_row][vc_column][vc_column_text]<section id="{slug}-ai-application-concepts"><h2>Ideas for your {name} terrain model</h2><p>{useintro}</p><p>These AI-generated scenes use catalogue renders as references. They illustrate possible styling and fabrication; they are not photographs of tested prints or a guarantee of final geometry.</p>{{{{AI_FIGURES}}}}<h3>Use and licensing</h3><p>The standard licence is for personal use. Commercial displays and other commercial projects require separately agreed permission. <a href="https://shustrik-maps.com/terms-of-service/">Review the usage terms</a> or <a href="mailto:shustrikmaps@gmail.com">ask about your intended use before buying</a>.</p></section>[/vc_column_text][/vc_column][/vc_row]'''
    assert '<h1' not in content and len(media)==3
    products.append({'product_id':base['id'],'slug':slug,'name':name,'before_content_sha256':hashlib.sha256(base['content'].encode()).hexdigest(),'seo_title':title,'meta_description':meta,'content_template':content,'media':media})
(r/'manifest.json').write_text(json.dumps({'owner_instruction':'2026-10-05: optimize several additional products; standing instruction three AI images including commercial/title/alt/upload and relevant product copy','market':'US only / English / Google','products':products},ensure_ascii=False,indent=2),encoding='utf-8')
(vault/'assets.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2),encoding='utf-8')
md='# Три товара — AI-сцены и семантика, 05.10.2026\n\nМодельный рендер — референс. AI-концепт не является техническим доказательством геометрии/печати. Показанные материалы, основания и упаковка дополнительные; коммерческие права отдельно. California и New York: сохранить опубликованный текст и metadata. Grand Canyon: C4D/STL + TIF по листингу, open-base preparation; не standalone DEM. География SEO — только США; узкие частотности и текущие ranks здесь не измерены заново.\n\n| Товар | Сцена | Title | Alt | PNG |\n|---|---|---|---|---|\n'
for a in registry:md+=f"| {a['product_id']} | {a['heading']} | {a['title']} | {a['alt']} | [[{a['selected_png']}]] |\n"
md+='\nПромпты: photorealistic square, supplied actual render as strict silhouette/terrain reference, physically supported object, no labels/logos, three distinct contexts (home/gift/commercial). NY is whole state, Long Island supported. California desk initial floating offshore fragments corrected; first attempt is not selected. Grand Canyon is rectangular terrain with additional support and conceptual colour finish.\n'
(vault/'README.md').write_text(md,encoding='utf-8')
print(json.dumps({'products':[p['product_id'] for p in products],'images':len(registry),'webp_total_bytes':sum((r/a['file']).stat().st_size for a in registry),'grand_canyon_title':title},ensure_ascii=False))
