from pathlib import Path
import json,re,shutil
from datetime import datetime,timezone,timedelta
root=Path(__file__).parent
out=Path('J:/1. My Vault/90 Migration/shustrik-maps-seo/five-asia-country-stl-slider-release-20261008')
def read(n):
 s=(root/n).read_text(encoding='utf-8-sig')
 try:return json.loads(s)
 except json.JSONDecodeError:return json.loads(next(x for x in s.splitlines() if x.startswith('{')))
m=read('manifest.json');v=read('verify.json');d=read('deployment.json');samples=[]
assert len(m['rows'])==len(v['rows'])==5 and v['ok']
for r in m['rows']:
 for mode in ['desktop','mobile']:
  records=read(r['slug']+'-'+mode+'-qa.json')
  assert [x['slide'] for x in records]==[1,2,3,4]
  for x in records:
   assert x['id']==r['id'] and x['mode']==mode and x['align']=='center' and not x['overflow']
   assert len(x['active'])==1 and x['active'][0]['loaded'] and x['active'][0]['alt']==x['expected_alt']
   assert x['visible_count']==1 and x['dots']==4 and x['arrows']==2 and int(x['bold'])>=600
   assert x['viewport']==(390 if mode=='mobile' else 1440)
  samples+=records
  assert read(r['slug']+'-'+mode+'-controls.json')['pass']
assert len(samples)==40 and len(list(root.glob('*-controls.json')))==10
for n,k in [('apply.json','ok'),('rollback-preview.json','ok'),('public-qa.json','pass'),('preservation-qa.json','pass'),('visual-review.json','pass')]:assert read(n)[k]
assert sum(len(x['media']) for x in v['rows'])==20
assert len(read('public-qa.json')['rows'])==10 and len(read('public-qa.json')['media'])==20
assert len(list(root.glob('*-1500x1000-original.png')))==20
assert (root/'nepal-published-proof.png').exists()
(root/'browser-qa.json').write_text(json.dumps({'pass':True,'desktop':'1440x1000','mobile':'390x844','next_previous_and_dots_passed':10,'screenshots_visually_reviewed':True,'samples':samples},ensure_ascii=False,indent=2),encoding='utf-8')
now=datetime.now(timezone(timedelta(hours=3)));stamp=now.strftime('%Y-%m-%d %H:%M');date=now.strftime('%Y-%m-%d')
commit=d['commit'];names=', '.join(r['name'] for r in m['rows']);oldmedia=sum(r['old_media_preserved'] for r in read('preservation-qa.json')['rows'])
report=f'''---
type: work-log
project_id: shustrik-maps-seo
status: completed
date: {date}
market: USA
language: English
---

# Следующие пять country STL опубликованы и проверены

{names}. Завершено {stamp} МСК по поручению «делай следующие 5».

## Выбор и семантика

Выбраны по возрастанию ID следующих country listings после Oman/Peru/Paraguay/Panama/Pakistan; India уже обработана и пропущена. Журналы и fresh live inventory сверены: ни у одного из пяти не было собственного AI-слайдера, у каждого была одна ссылка на общий HTML-блок9586. Предыдущие партии исключены, Беларусь не рассматривается. [[selection.json]] / [[baseline.json]].

Сохранённое ядро Google/English/USA05.10 не содержит точных пяти STL-кластеров. Primary: place topographic map STL; support: terrain STL, relief map STL, map 3D print, CNC terrain model. Новые группы редакционные, frequency/rank=null. Фактически осмотрены пять Google выдач с hl=en/gl=us/pws=0. Footer Unknown / cannot determine location: US-local rank и фактическая локация не подтверждены. Частотности и позиции не измерялись. Paid whole-country STL intent отделён от free/physical/ordinary/GIS/vector/city/coin/outline intent. Сохранены собственные контуры и рельеф каждого товара; сохранены горная полоса Nepal, острова North Korea/Iran, широкая Mongolia и равнинный Iraq по собственным референсам. Острова и фрагменты закреплены на общей подложке. Google AI Overview claims не переносились в карточки. [[Intent Review]] / [[intent-evidence.json]] / [[semantic-review.json]] / [[Page Briefs]]. Решение validate first относится к последующему измерению SEO-эффекта; порученная публикация существующих товаров выполнена.

## Публикация и сохранность

Изменены только SEO title/meta и выбранная иллюстрационная вставка Description: ссылка9586 заменена собственным native Woodmart carousel. Все прежние vc_column_text/main prose сохранены дословно. H1, URL, excerpt/specs, цены, downloads/files, thumbnail, верхняя галерея, прочие productmeta защищены. Общий блок9586 сохранён без изменений; {oldmedia} прежних media сохранены по ID/title/URL. [[preservation-qa.json]] / [[backup-export.json]] / [[after.json]].

20 отдельных native ImageGen вызовов, четыре разные сцены по собственному референсу каждого товара: ivory plastic desktop, небольшая картина, подарок в kraft-коробке, крупная инсталляция из серого бетона. Каждый результат визуально осмотрен. Все настольные рельефы полностью на цельной сплошной walnut-подложке, включая острова и выступы. Сохранены20 оригиналов PNG,10 собственных референсов, prompts/registry. Географические особенности закреплены в [[geography-notes.json]]; точное совпадение с mesh не заявляется. [[generation-jobs.json]] / [[generated-registry.json]] / [[visual-review.json]].

20 настоящих RGB JPEG1500×1000 с описательными title/alt и явной AI-concept маркировкой. Один слайд desktop/mobile, две ручные стрелки вместе внутри доступной области блока, четыре точки, autoplay=no/wrap=no. Под слайдером только жирная центрованная **AI-generated application concepts.** Media caption не выводится в gallery. [[uploaded-media.json]].

Все пять listings указывают base=closed. Mesh/archive/readiness не проверялись; прежние claims сохранены, новых обещаний готовности/точности/совместимости/лицензии не добавлено. Подложки, рамы, упаковка, concrete fabrication и коммерческие permissions — отдельная проектная работа.

## Товары

| Товар | ID | Media IDs | URL |
|---|---:|---|---|
'''
for r in v['rows']:
 name=next(x['name'] for x in m['rows'] if x['id']==r['id'])
 report+='| '+name+' | '+str(r['id'])+' | '+', '.join(str(a['id']) for a in r['media'])+' | '+r['url']+' |\n'
report+=f'''
## Доставка и проверки

GitHub-first: starting HEAD9f2174f; SSH remote/main; fetch/prune, upstream0:0. Прежние dirty/untracked сохранены. Source {commit} committed/pushed и remote main подтверждён до apply. Exact archive SHA256 {d['archive_sha256']} local/VPS совпал; source доставлен в {d['wp_source']} внешнего WordPress https://shustrik-maps.com. Lint/preview5/5 прошли. Apply выполнен ровно один раз с уникальными backup/journal, transactional guard и защитой от параллельных изменений. [[deployment.json]] / [[preview.json]] / [[apply.json]].

DB5/5: точные SEO/Description, protected data, backup before совпал с baseline, journal status=published. Media20/20: SHA256/image/jpeg/1500×1000/title/alt/caption. Public HTTP10/10: обычный и query URL200, точные SEO, H1/self-canonical/indexability/Product schema/CTA, четыре новых media, краткая подпись, отсутствие raw shortcode. Media20/20 HTTP200/image/jpeg. Query не доказывает cache bypass. [[verify.json]] / [[public-qa.json]].

Browser40/40: четыре слайда каждого товара на1440×1000 и390×844. Один активный/видимый слайд, изображение загружено, alt точный; две стрелки/четыре точки/center/font-weight≥600/безoverflow. На всех10 видах Next/Previous/first&last dots прошли. Сохранены10 screenshots, контрольные JSON и отдельный proof. Все desktop/mobile screenshots и published proof осмотрены. [[browser-qa.json]] / [[nepal-published-proof.png]].

WireGuard SSH vpsadmin@10.66.66.1 и sudo Docker available, сервер/docker ps проверены до target WP/DB. Running/RestartCount0/StartedAt/ports before/after совпали: WP127.0.0.1:8083, DB безpublished ports. Build/restart/local runtime change нет; secrets/.env не читались. [[runtime-before.txt]] / [[runtime-after.txt]].

## Откат

Guarded rollback-preview5/5 passed, actual rollback не выполнялся. Backup _shustrik_five_asia_country_stl_slider_backup_20261008_ID; journal _shustrik_five_asia_country_stl_slider_media_20261008_ID. Перед откатом выполнить:

```sh
sudo -n docker exec shustrik-maps-wordpress-1 php {d['wp_source']}/release.php --rollback-preview
```

Затем --rollback только при отсутствии published drift. Восстанавливаются прежние Description/SEO; old/new media сохраняются. Apply неидемпотентен: при неизвестном результате читать journals/backups, слепой повтор запрещён. [[rollback-preview.json]].

Партия5/5 завершена. P1 analytics/recovery/consent, индекс-контроль10.10, yellow/degraded сохранены. Рост позиций/продаж не заявляется. [[../STL Product Update Workflow]].
'''
(root/'Release Report.md').write_text(report,encoding='utf-8')
note=f'''## Пять Asia country STL завершены 08.10 — {stamp} МСК

{names}: SEO title/meta и20JPEG1500×1000 опубликованы в собственных слайдерах. Один слайд desktop/mobile, ручные стрелки/точки безautoplay; только жирная центрованная AI-подпись. Настольные рельефы и острова полностью на сплошной подложке. Основные тексты/H1/URL/specs/commerce/верхние галереи и{oldmedia} прежних media сохранены. [[Five Asia Country STL Sliders 2026-10-08/Release Report]].

Source {commit} pushed и доставлен точным архивом. DB5/5,media20/20,HTTP10/10,browser40/40,guarded rollback-preview прошли. SSH/sudo Docker доступны; WP/DB running/restart0/StartedAt/ports неизменны. Пять Google English/gl=us intent observations, фактическая локация Unknown; частотности/позиции не измерялись. P1 analytics/recovery/consent,индекс10.10,yellow/degraded сохранены.

'''
for n in ['Shustrik Maps SEO - Overview.md','Shustrik Maps SEO - Next Actions.md']:
 p=root.parent/n;parts=p.read_text(encoding='utf-8').split('---',2);assert len(parts)==3
 parts[1]=re.sub(r'last_reviewed: .*','last_reviewed: '+date,parts[1])
 if n.endswith('Overview.md'):
  parts[1]=re.sub(r'current_commit: .*','current_commit: '+commit,parts[1]);parts[1]=re.sub(r'last_runtime_check: .*','last_runtime_check: '+stamp,parts[1])
 assert '## Пять Asia country STL завершены 08.10' not in parts[2]
 body=parts[2].lstrip('\n')
 if body.startswith('GitHub evidence commit '):
  prior_line,body=body.split('\n',1);body=body.lstrip('\n');heading,tail=body.split('\n',1);body=heading+'\n\n'+prior_line+'\n'+tail
 p.write_text('---'+parts[1]+'---\n'+note+body,encoding='utf-8')
runtime=root.parents[3]/'04 Operations/Runtime Status.md'
rt=f'''## Targeted Shustrik Maps — Five Asia Country STL, {stamp} МСК

External https://shustrik-maps.com; source {commit}; archive {d['archive_sha256']} local/VPS совпал. {names}: SEO и20JPEG опубликованы. DB5/5,media20/20,HTTP10/10,browser40/40,rollback-preview прошли; исходные тексты/данные сохранены. SSH WireGuard/sudo Docker доступны; WP/DB running/restart0/StartedAt/ports before/after совпали: WP127.0.0.1:8083,DB безpublished ports. Build/restart/local change нет. P1 analytics/recovery/consent,индекс10.10,yellow/degraded сохранены. Другие проекты не проверялись. [[01 Projects/WordPress/shustrik-maps.com/Five Asia Country STL Sliders 2026-10-08/Release Report]].

'''
runtime.write_text(rt+runtime.read_text(encoding='utf-8'),encoding='utf-8')
for n in ['Release Report.md','browser-qa.json','apply.json','verify.json','preview.json','rollback-preview.json','public-qa.json','uploaded-media.json','backup-export.json','preservation-qa.json','after.json','deployment.json','runtime-before.txt','runtime-after.txt','nepal-published-proof.png','finalize-asia.py']:
 shutil.copy2(root/n,out/n)
for pattern in ['*-desktop.png','*-mobile.png','*-qa.json','*-controls.json']:
 for p in root.glob(pattern):shutil.copy2(p,out/p.name)
for n in ['Shustrik Maps SEO - Overview.md','Shustrik Maps SEO - Next Actions.md']:shutil.copy2(root.parent/n,out/(Path(n).stem+' snapshot.md'))
shutil.copy2(runtime,out/'Runtime Status snapshot.md')
for p in out.iterdir():
 if p.suffix in ['.json','.md','.py','.php','.txt']:
  s=p.read_text(encoding='utf-8-sig');p.write_text('\n'.join(l.rstrip() for l in s.splitlines()).rstrip()+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'completed':5,'images':20,'browser_samples':40,'source':commit,'checked_moscow':stamp}))
