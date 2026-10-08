from pathlib import Path
from datetime import datetime,timezone,timedelta
import json,re,shutil
base=Path('J:/1. My Vault');project=base/'01 Projects/WordPress/shustrik-maps.com';old=project/'Five Special STL Sliders 2026-10-08';root=project/'Kiwi Nautilus Use Cases Revision 2026-10-08';repo=base/'90 Migration/shustrik-maps-seo';oldout=repo/'five-special-stl-slider-release-20261008';out=repo/'kiwi-nautilus-usecases-revision-20261008'
def read(n):return json.loads((root/n).read_text(encoding='utf-8-sig'))
for n in ['verify.json','rollback-preview.json','apply.json']:assert read(n)['ok']
for n in ['preservation-qa.json','old-media-preservation.json','final-five-state-qa.json','final-five-public-qa.json','final-five-browser-qa.json','visual-review.json']:assert read(n)['pass']
assert len(read('final-five-verify.json')['rows'])==5 and len(read('browser-qa.json')['samples'])==16 and len(read('final-five-browser-qa.json')['samples'])==40
assert (root/'nautilus-published-proof.png').exists() and len(list(root.glob('*-original.png')))==8
d=read('deployment.json');initial=json.loads((old/'deployment.json').read_text(encoding='utf-8'));stamp=datetime.now(timezone(timedelta(hours=3))).strftime('%Y-%m-%d %H:%M');source=d['commit']
report=f'''---
type: seo-live-qa
site_profile: shustrik-maps
project_id: shustrik-maps-seo
status: published-check-passed
created_at: 2026-10-08
market: USA
language: English
sources: [final-five-state-qa.json, final-five-public-qa.json, final-five-browser-qa.json, deployment.json]
next_action: "Keep P1 recovery/consent and index check10.10; measure SEO only under a separate plan"
---

# Пять STL опубликованы — итог с правкой Kiwi и Nautilus

Проверено {stamp} МСК. Antarctica with Ice, Dymaxion World Map, Zion Canyon Trail, New Zealand Kiwi Medallion, Nautilus Pendant. Пять карточек завершены с учётом уточнения владельца: сувениры показаны по своему назначению.

## Итоговые сцены

Antarctica/Dymaxion/Zion: четыре own-reference сцены каждого — ivory plastic на сплошной подложке, небольшая картина, подарок, grey concrete инсталляция. Все три terrain модели и выступы полностью поддерживаются сплошной подложкой. Для Antarctica сохранён круглый polar ice-and-ocean-floor tile, Dymaxion angular Fuller net, Zion narrow corridor. Первоначальный source {initial['commit']}, архив {initial['archive_sha256']}, доставка {initial['wp_source']}. [[../Five Special STL Sliders 2026-10-08/Initial Release Report]].

Kiwi21381: небольшой медальон в руке, в прозрачной коллекционной капсуле, в подарочном футляре, с дорожным suede-мешочком. Сохранены круглый rim, Kiwi head/beak left, Union Jack и четыре звезды. Первая сцена ivory plastic; остальные antique brass/bronze finish — AI-финиш, не обещание готовой металлической монеты или legal tender.

Nautilus18721: ivory plastic подвеска на тёмном шнуре на шее взрослой девушки, брелок на рюкзаке, брелок на связке ключей, подарок с кольцом в коробке. Сохранены асимметричная форма, central spiral/cutouts и существующее отверстие; шнур/кольцо входят в него. Это сценарии использования, не статуэтки, картины или бетон. Hardware/cord/packaging/fabrication — дополнительная адаптация.

Восемь новых отдельных native ImageGen результатов осмотрены; 8originalPNG,4ownrefs,8prompts/registry сохранены в этой папке. Все прежние20originals/prompts сохранены в первоначальной папке. Живые слайдеры содержат20 настоящих RGB JPEG1500×1000:12terrain+8revised. Title/alt соответствуют фактическому материалу и явно обозначают AI-generated concept. Старые8 заменённых media сохранены по ID/title/alt/URL/SHA256, глобальные HTML и прежние рендеры не удалены. [[visual-review.json]] / [[generation-jobs.json]] / [[uploaded-media.json]] / [[old-media-preservation.json]].

## Товары и новые media

| Товар | ID | Текущие media IDs | URL |
|---|---:|---|---|
'''
for x in read('final-five-verify.json')['rows']:
 name=next(z['name'] for z in json.loads((old/'manifest.json').read_text(encoding='utf-8'))['rows'] if z['id']==x['id'])
 report+='| '+name+' | '+str(x['id'])+' | '+', '.join(str(z['id']) for z in x['media'])+' | '+x['url']+' |\n'
report+=f'''
## Сохранность, SEO и публикация

Only SEO title/meta и выбранные иллюстрации Description. Основные vc_column_text/woodmart_text_block, H1/URL, excerpt/specs, prices/files/downloads, upper gallery и прочие metadata сохранены дословно. В редакции Kiwi/Nautilus titles не менялись; meta descriptions убирают старые desktop/wall сценарии, отражают медальон/necklace/keychain/gift. Слайдер/подпись неизменны: один слайд desktop/mobile, две ручные стрелки, четыре точки, autoplay=no/wrap=no; под ним только жирная центрованная **AI-generated application concepts.** [[manifest.json]] / [[preservation-qa.json]] / [[final-five-state-qa.json]].

Выбор по полному516published catalog и точным SKU, прошлые партии/Беларусь/prepayment/convert-on-request-only исключены. Google/English/USA ядро05.10 и пять SERP проверены в первоначальном выпуске. Существующие Antarctica-clusters не считаются измеренными метриками отдельного ice SKU; новые exact-product группы редакционные. hl=en/gl=us/pws=0, footer Unknown: US-local rank/location не подтверждены, новых частотностей/позиций нет. Kiwi медальон и Nautilus pendant/keychain не смешаны с физической валютой, свободными файлами или submarine STL. [[../Five Special STL Sliders 2026-10-08/Intent Review]] / [[owner-revision]].

GitHub-first перед каждым выпуском: SSH remote/main/fetch/upstream0:0; прежние dirty/untracked и незавершённый evidence первого выпуска сохранены. Редакция source {source} committed/pushed до публикации. Archive SHA256 {d['archive_sha256']} local/VPS совпал, exact source доставлен в {d['wp_source']}. Lint/preview2/2 passed. Новый apply выполнен один раз с отдельными backup/journal, transactional/concurrency guard. Первоначальный apply не повторялся. [[deployment.json]] / [[preview.json]] / [[apply.json]] / [[source-git-receipt.json]].

DB2/2 редакции / media8/8 / guarded rollback-preview2/2 passed. Свежий final DB5/5 совпал с ожидаемым: три terrain unchanged, две revised. Public final HTTP10/10 (обычный+query URL каждой) и20media HTTP200/image/jpeg: SEO/H1/self-canonical/indexability/Product schema/CTA/notice/raw shortcodes passed. Query сам по себе не доказывает bypass. Nautilus curly quotes — обычный WordPress typography: один H1 и исходный DB title сохранены, QA нормализует только кавычки. [[verify.json]] / [[final-five-state-qa.json]] / [[final-five-public-qa.json]].

Browser final40/40: desktop1440×1000/mobile390×844, четыре слайда пяти карточек. Три неизменных terrain используют ранее выполненные24 проверки; две revised заново прошли16. На всех10 видах Next/Previous/first&last dots passed; одна видимая/загруженная картинка, exact alt, arrows2/dots4, centered bold notice, no overflow. Все14 screenshots (10initial+4revision) и новый published proof осмотрены. [[final-five-browser-qa.json]] / [[nautilus-published-proof.png]].

SSH WireGuard vpsadmin@10.66.66.1 / sudo Docker available. WP/DB running/restart0/StartedAt/ports before/after совпали; WP127.0.0.1:8083,DB безpublished ports. Никакого build/restart/local runtime change, secrets/.env не читались. [[runtime-before.txt]] / [[runtime-after.txt]].

## Откат

Current guarded rollback-preview2/2 passed. Backup _shustrik_kiwi_nautilus_usecases_stl_slider_backup_20261008_ID, journal _shustrik_kiwi_nautilus_usecases_stl_slider_media_20261008_ID. Перед откатом повторить:

```sh
sudo -n docker exec shustrik-maps-wordpress-1 php {d['wp_source']}/release.php --rollback-preview
```

После отсутствия drift — --rollback. Это вернёт две карточки к первоначальному выпуску08.10, все медиа сохраняются. Для полного возврата пяти к исходному состоянию: сначала откатить эту редакцию, затем заново preview первоначального {initial['wp_source']}/release.php и только после успешного guard выполнить его --rollback. Его preview5/5 был проверен ДО редакции; сейчас два товара намеренно отличаются, слепой preview/apply/rollback исходного выпуска не допустим. Actual rollback не выполнялся. [[backup-export.json]] / [[rollback-preview.json]].

Исходные спорные specs Kiwi/Nautilus (одинаковые размеры/объём/полигонность) и старые Zion headings Grand Canyon DEM/Texture сохранены по поручению; отдельная проверка владельцем до исправления. Mesh/archive/readiness/accuracy/rights не проверялись. Existing P1 analytics/recovery/consent, индекс-контроль10.10, yellow/degraded сохраняются, рост SEO/продаж не заявляется.
'''
(root/'Release Report.md').write_text(report,encoding='utf-8')
assert not (old/'Initial Release Report.md').exists();shutil.copy2(old/'Release Report.md',old/'Initial Release Report.md');shutil.copy2(old/'Release Report.md',oldout/'Initial Release Report.md')
(old/'Release Report.md').write_text(report.replace('[[../Five Special STL Sliders 2026-10-08/Initial Release Report]]','[[Initial Release Report]]')+'\nПолные доказательства редакции: [[../Kiwi Nautilus Use Cases Revision 2026-10-08/Release Report]].\n',encoding='utf-8');shutil.copy2(old/'Release Report.md',oldout/'Release Report.md')
workflow=project/'STL Product Update Workflow.md';s=workflow.read_text(encoding='utf-8');heading='## Декоративные STL — уточнение владельца08.10.2026';assert heading not in s
workflow.write_text(s+'\n'+heading+'\n\nДля Kiwi показывать небольшой памятный медальон/монетку в руке, капсуле, подарочном футляре или дорожном мешочке. Для Nautilus — подвеску на шее девушки либо брелок на рюкзаке/ключах и в подарке. Не применять к этим двум шаблон статуэтка/картина/огромная бетонная инсталляция. Использовать собственную форму/отверстия, сохранять4разные сцены/AI-mark/title/alt/JPEG1500×1000, single-slide manual carousel и исходные тексты. Эта правка владельца заменяет generic terrain scene template для двух декоративных товаров. [[Kiwi Nautilus Use Cases Revision 2026-10-08/Release Report]].\n',encoding='utf-8')
note=f'''## Итог пяти STL с правкой Kiwi/Nautilus — {stamp} МСК

Antarctica with Ice, Dymaxion World Map, Zion Canyon Trail, Kiwi Medallion, Nautilus: опубликованы и проверены20liveJPEG/SEO. Kiwi — памятный медальон (рука/capsule/gift/pouch); Nautilus — necklace/backpack/keys/gift, без картин/статуэток/бетона. Terrain12media исходного source466394c, decorative8media revised source {source}, оба точных архива доставлены. Fresh DB5/5,HTTP10/10,media20/20,final browser40/40 passed; исходные тексты/commerce/upper galleries и старыеmedia сохранены. Current rollback-preview2/2 passed, полный откат пяти — сначала revision, затем guarded initial. [[Five Special STL Sliders 2026-10-08/Release Report]].

WP/DB runtime unchanged, SSH/sudoDocker available, restart/build нет. P1 analytics/recovery/consent, индекс10.10,yellow/degraded сохраняются; метрики SEO не измерены. [[STL Product Update Workflow#Декоративные STL — уточнение владельца08.10.2026]].

'''
for n in ['Shustrik Maps SEO - Overview.md','Shustrik Maps SEO - Next Actions.md']:
 p=project/n;parts=p.read_text(encoding='utf-8').split('---',2);parts[1]=re.sub(r'last_reviewed: .*','last_reviewed: 2026-10-08',parts[1]);assert '## Итог пяти STL с правкой Kiwi/Nautilus' not in parts[2]
 if n.endswith('Overview.md'):parts[1]=re.sub(r'current_commit: .*','current_commit: '+source,parts[1]);parts[1]=re.sub(r'last_runtime_check: .*','last_runtime_check: '+stamp,parts[1])
 p.write_text('---'+parts[1]+'---\n'+note+parts[2].lstrip('\n'),encoding='utf-8');shutil.copy2(p,out/(Path(n).stem+' snapshot.md'))
runtime=base/'04 Operations/Runtime Status.md';rt=f'''## Targeted Shustrik Maps — Five Special STL Revised, {stamp} МСК

External https://shustrik-maps.com; terrain source466394c, revised Kiwi/Nautilus source {source}, exact archive {d['archive_sha256']} local/VPS совпал. Five final DB5/5,HTTP10/10,media20/20,browser40/40 passed. Current revision rollback-preview2/2 passed. WireGuard SSH/sudoDocker available; WP/DB running/restart0/StartedAt/ports unchanged, WP127.0.0.1:8083/DB no published ports; build/restart/local runtime change нет. Исходные тексты/commerce/media сохранены. P1 analytics/recovery/consent,индекс10.10,yellow/degraded сохраняются. Другие проекты этим срезом не проверялись. [[01 Projects/WordPress/shustrik-maps.com/Five Special STL Sliders 2026-10-08/Release Report]].

''';runtime.write_text(rt+runtime.read_text(encoding='utf-8'),encoding='utf-8');(out/'Runtime Status snapshot.md').write_text(rt,encoding='utf-8');shutil.copy2(workflow,out/'STL Product Update Workflow snapshot.md')
# Copy release evidence and current QA helpers only; originals remain in the vault.
for p in root.iterdir():
 if p.suffix in ['.json','.md','.php','.py','.js','.txt'] or p.name.endswith('-desktop.png') or p.name.endswith('-mobile.png') or p.name=='nautilus-published-proof.png':shutil.copy2(p,out/p.name)
for n in ['source-git-receipt.json','server-runtime-before.txt','browser-live-runner.js','public-qa.py','public-qa-before-typography-fix.json','finish-evidence-next.py','git-receipt-next.py']:shutil.copy2(old/n,oldout/n)
shutil.copy2(Path(__file__),out/'finalize-special-revision.py')
print(json.dumps({'final_products':5,'live_images':20,'revision_images':8,'browser_samples':40,'source':source,'stamp':stamp}))
