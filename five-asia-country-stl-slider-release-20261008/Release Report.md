---
type: work-log
project_id: shustrik-maps-seo
status: completed
date: 2026-10-08
market: USA
language: English
---

# Следующие пять country STL опубликованы и проверены

Nepal, North Korea, Mongolia, Iran, Iraq. Завершено 2026-10-08 09:47 МСК по поручению «делай следующие 5».

## Выбор и семантика

Выбраны по возрастанию ID следующих country listings после Oman/Peru/Paraguay/Panama/Pakistan; India уже обработана и пропущена. Журналы и fresh live inventory сверены: ни у одного из пяти не было собственного AI-слайдера, у каждого была одна ссылка на общий HTML-блок9586. Предыдущие партии исключены, Беларусь не рассматривается. [[selection.json]] / [[baseline.json]].

Сохранённое ядро Google/English/USA05.10 не содержит точных пяти STL-кластеров. Primary: place topographic map STL; support: terrain STL, relief map STL, map 3D print, CNC terrain model. Новые группы редакционные, frequency/rank=null. Фактически осмотрены пять Google выдач с hl=en/gl=us/pws=0. Footer Unknown / cannot determine location: US-local rank и фактическая локация не подтверждены. Частотности и позиции не измерялись. Paid whole-country STL intent отделён от free/physical/ordinary/GIS/vector/city/coin/outline intent. Сохранены собственные контуры и рельеф каждого товара; сохранены горная полоса Nepal, острова North Korea/Iran, широкая Mongolia и равнинный Iraq по собственным референсам. Острова и фрагменты закреплены на общей подложке. Google AI Overview claims не переносились в карточки. [[Intent Review]] / [[intent-evidence.json]] / [[semantic-review.json]] / [[Page Briefs]]. Решение validate first относится к последующему измерению SEO-эффекта; порученная публикация существующих товаров выполнена.

## Публикация и сохранность

Изменены только SEO title/meta и выбранная иллюстрационная вставка Description: ссылка9586 заменена собственным native Woodmart carousel. Все прежние vc_column_text/main prose сохранены дословно. H1, URL, excerpt/specs, цены, downloads/files, thumbnail, верхняя галерея, прочие productmeta защищены. Общий блок9586 сохранён без изменений; 35 прежних media сохранены по ID/title/URL. [[preservation-qa.json]] / [[backup-export.json]] / [[after.json]].

20 отдельных native ImageGen вызовов, четыре разные сцены по собственному референсу каждого товара: ivory plastic desktop, небольшая картина, подарок в kraft-коробке, крупная инсталляция из серого бетона. Каждый результат визуально осмотрен. Все настольные рельефы полностью на цельной сплошной walnut-подложке, включая острова и выступы. Сохранены20 оригиналов PNG,10 собственных референсов, prompts/registry. Географические особенности закреплены в [[geography-notes.json]]; точное совпадение с mesh не заявляется. [[generation-jobs.json]] / [[generated-registry.json]] / [[visual-review.json]].

20 настоящих RGB JPEG1500×1000 с описательными title/alt и явной AI-concept маркировкой. Один слайд desktop/mobile, две ручные стрелки вместе внутри доступной области блока, четыре точки, autoplay=no/wrap=no. Под слайдером только жирная центрованная **AI-generated application concepts.** Media caption не выводится в gallery. [[uploaded-media.json]].

Все пять listings указывают base=closed. Mesh/archive/readiness не проверялись; прежние claims сохранены, новых обещаний готовности/точности/совместимости/лицензии не добавлено. Подложки, рамы, упаковка, concrete fabrication и коммерческие permissions — отдельная проектная работа.

## Товары

| Товар | ID | Media IDs | URL |
|---|---:|---|---|
| Nepal | 20110 | 22686, 22687, 22688, 22689 | https://shustrik-maps.com/product/nepal-stl-model/ |
| North Korea | 20134 | 22690, 22691, 22692, 22693 | https://shustrik-maps.com/product/north-korea-stl-model/ |
| Mongolia | 20175 | 22694, 22695, 22696, 22697 | https://shustrik-maps.com/product/mongolia-stl-model/ |
| Iran | 20320 | 22698, 22699, 22700, 22701 | https://shustrik-maps.com/product/iran-stl-model/ |
| Iraq | 20329 | 22702, 22703, 22704, 22705 | https://shustrik-maps.com/product/iraq-stl-model/ |

## Доставка и проверки

GitHub-first: starting HEAD9f2174f; SSH remote/main; fetch/prune, upstream0:0. Прежние dirty/untracked сохранены. Source eed40cd9ca37f3403485a4ceae3a9fb60b0f5a4e committed/pushed и remote main подтверждён до apply. Exact archive SHA256 d5950ea7f191af4a1c17a68ba7d3ae9abbf1fd8de39cd959a48ae0fc5de0b269 local/VPS совпал; source доставлен в /tmp/five-asia-country-eed40cd внешнего WordPress https://shustrik-maps.com. Lint/preview5/5 прошли. Apply выполнен ровно один раз с уникальными backup/journal, transactional guard и защитой от параллельных изменений. [[deployment.json]] / [[preview.json]] / [[apply.json]].

DB5/5: точные SEO/Description, protected data, backup before совпал с baseline, journal status=published. Media20/20: SHA256/image/jpeg/1500×1000/title/alt/caption. Public HTTP10/10: обычный и query URL200, точные SEO, H1/self-canonical/indexability/Product schema/CTA, четыре новых media, краткая подпись, отсутствие raw shortcode. Media20/20 HTTP200/image/jpeg. Query не доказывает cache bypass. [[verify.json]] / [[public-qa.json]].

Browser40/40: четыре слайда каждого товара на1440×1000 и390×844. Один активный/видимый слайд, изображение загружено, alt точный; две стрелки/четыре точки/center/font-weight≥600/безoverflow. На всех10 видах Next/Previous/first&last dots прошли. Сохранены10 screenshots, контрольные JSON и отдельный proof. Все desktop/mobile screenshots и published proof осмотрены. [[browser-qa.json]] / [[nepal-published-proof.png]].

WireGuard SSH vpsadmin@10.66.66.1 и sudo Docker available, сервер/docker ps проверены до target WP/DB. Running/RestartCount0/StartedAt/ports before/after совпали: WP127.0.0.1:8083, DB безpublished ports. Build/restart/local runtime change нет; secrets/.env не читались. [[runtime-before.txt]] / [[runtime-after.txt]].

## Откат

Guarded rollback-preview5/5 passed, actual rollback не выполнялся. Backup _shustrik_five_asia_country_stl_slider_backup_20261008_ID; journal _shustrik_five_asia_country_stl_slider_media_20261008_ID. Перед откатом выполнить:

```sh
sudo -n docker exec shustrik-maps-wordpress-1 php /tmp/five-asia-country-eed40cd/release.php --rollback-preview
```

Затем --rollback только при отсутствии published drift. Восстанавливаются прежние Description/SEO; old/new media сохраняются. Apply неидемпотентен: при неизвестном результате читать journals/backups, слепой повтор запрещён. [[rollback-preview.json]].

Партия5/5 завершена. P1 analytics/recovery/consent, индекс-контроль10.10, yellow/degraded сохранены. Рост позиций/продаж не заявляется. [[../STL Product Update Workflow]].
