---
type: work-log
project_id: shustrik-maps-seo
status: completed
date: 2026-10-08
market: USA
language: English
---

# Следующие пять country STL опубликованы и проверены

Oman, Peru, Paraguay, Panama, Pakistan. Завершено 2026-10-08 09:17 МСК по поручению «делай следующие 5».

## Выбор и семантика

Выбраны по возрастанию ID следующих country listings после Tajikistan/Thailand/Turkmenistan/Saudi Arabia/Russia. Журналы и fresh live inventory сверены: ни у одного из пяти не было собственного AI-слайдера, у каждого была одна ссылка на общий HTML-блок9586. Предыдущие партии исключены, Беларусь не рассматривается. [[selection.json]] / [[baseline.json]].

Сохранённое ядро Google/English/USA05.10 не содержит точных пяти STL-кластеров. Primary: place topographic map STL; support: terrain STL, relief map STL, map 3D print, CNC terrain model. Новые группы редакционные, frequency/rank=null. Фактически осмотрены пять Google выдач с hl=en/gl=us/pws=0. Footer Unknown / cannot determine location: US-local rank и фактическая локация не подтверждены. Частотности и позиции не измерялись. Paid whole-country STL intent отделён от free/physical/ordinary/GIS/vector/city/coin/outline intent. Сохранены собственные контуры и рельеф каждого товара; сохранены северный эксклав Oman, острова Panama и собственный контур Pakistan без расширения claims. Острова и фрагменты закреплены на общей подложке. Google AI Overview claims не переносились в карточки. [[Intent Review]] / [[intent-evidence.json]] / [[semantic-review.json]] / [[Page Briefs]]. Решение validate first относится к последующему измерению SEO-эффекта; порученная публикация существующих товаров выполнена.

## Публикация и сохранность

Изменены только SEO title/meta и выбранная иллюстрационная вставка Description: ссылка9586 заменена собственным native Woodmart carousel. Все прежние vc_column_text/main prose сохранены дословно. H1, URL, excerpt/specs, цены, downloads/files, thumbnail, верхняя галерея, прочие productmeta защищены. Общий блок9586 сохранён без изменений; 28 прежних media сохранены по ID/title/URL. [[preservation-qa.json]] / [[backup-export.json]] / [[after.json]].

20 отдельных native ImageGen вызовов, четыре разные сцены по собственному референсу каждого товара: ivory plastic desktop, небольшая картина, подарок в kraft-коробке, крупная инсталляция из серого бетона. Каждый результат визуально осмотрен. Все настольные рельефы полностью на цельной сплошной walnut-подложке, включая острова и выступы. Сохранены20 оригиналов PNG,9 собственных референсов, prompts/registry. Географические особенности закреплены в [[geography-notes.json]]; точное совпадение с mesh не заявляется. [[generation-jobs.json]] / [[generated-registry.json]] / [[visual-review.json]].

20 настоящих RGB JPEG1500×1000 с описательными title/alt и явной AI-concept маркировкой. Один слайд desktop/mobile, две ручные стрелки вместе внутри доступной области блока, четыре точки, autoplay=no/wrap=no. Под слайдером только жирная центрованная **AI-generated application concepts.** Media caption не выводится в gallery. [[uploaded-media.json]].

Все пять listings указывают base=closed. Mesh/archive/readiness не проверялись; прежние claims сохранены, новых обещаний готовности/точности/совместимости/лицензии не добавлено. Подложки, рамы, упаковка, concrete fabrication и коммерческие permissions — отдельная проектная работа.

## Товары

| Товар | ID | Media IDs | URL |
|---|---:|---|---|
| Oman | 20046 | 22666, 22667, 22668, 22669 | https://shustrik-maps.com/product/oman-stl-model/ |
| Peru | 20070 | 22670, 22671, 22672, 22673 | https://shustrik-maps.com/product/peru-stl-model/ |
| Paraguay | 20078 | 22674, 22675, 22676, 22677 | https://shustrik-maps.com/product/paraguay-stl-model/ |
| Panama | 20086 | 22678, 22679, 22680, 22681 | https://shustrik-maps.com/product/panama-stl-model/ |
| Pakistan | 20095 | 22682, 22683, 22684, 22685 | https://shustrik-maps.com/product/pakistan-stl-model/ |

## Доставка и проверки

GitHub-first: starting HEAD7975ce8; SSH remote/main; fetch/prune, upstream0:0. Прежние dirty/untracked сохранены. Source 4236061d1b38d20d0c9c7ad27a94c360625045e3 committed/pushed и remote main подтверждён до apply. Exact archive SHA256 0b20ea47a2887e28f08d0b00659b3cd5ed3e6a9087bd07a8cdb65555ca981451 local/VPS совпал; source доставлен в /tmp/five-next-country-4236061 внешнего WordPress https://shustrik-maps.com. Lint/preview5/5 прошли. Apply выполнен ровно один раз с уникальными backup/journal, transactional guard и защитой от параллельных изменений. [[deployment.json]] / [[preview.json]] / [[apply.json]].

DB5/5: точные SEO/Description, protected data, backup before совпал с baseline, journal status=published. Media20/20: SHA256/image/jpeg/1500×1000/title/alt/caption. Public HTTP10/10: обычный и query URL200, точные SEO, H1/self-canonical/indexability/Product schema/CTA, четыре новых media, краткая подпись, отсутствие raw shortcode. Media20/20 HTTP200/image/jpeg. Query не доказывает cache bypass. [[verify.json]] / [[public-qa.json]].

Browser40/40: четыре слайда каждого товара на1440×1000 и390×844. Один активный/видимый слайд, изображение загружено, alt точный; две стрелки/четыре точки/center/font-weight≥600/безoverflow. На всех10 видах Next/Previous/first&last dots прошли. Сохранены10 screenshots, контрольные JSON и отдельный proof. Мобильные screenshots и published proof осмотрены. [[browser-qa.json]] / [[oman-published-proof.png]].

WireGuard SSH vpsadmin@10.66.66.1 и sudo Docker available, сервер/docker ps проверены до target WP/DB. Running/RestartCount0/StartedAt/ports before/after совпали: WP127.0.0.1:8083, DB безpublished ports. Build/restart/local runtime change нет; secrets/.env не читались. [[runtime-before.txt]] / [[runtime-after.txt]].

## Откат

Guarded rollback-preview5/5 passed, actual rollback не выполнялся. Backup _shustrik_five_next_country_stl_slider_backup_20261008_ID; journal _shustrik_five_next_country_stl_slider_media_20261008_ID. Перед откатом выполнить:

```sh
sudo -n docker exec shustrik-maps-wordpress-1 php /tmp/five-next-country-4236061/release.php --rollback-preview
```

Затем --rollback только при отсутствии published drift. Восстанавливаются прежние Description/SEO; old/new media сохраняются. Apply неидемпотентен: при неизвестном результате читать journals/backups, слепой повтор запрещён. [[rollback-preview.json]].

Партия5/5 завершена. P1 analytics/recovery/consent, индекс-контроль10.10, yellow/degraded сохранены. Рост позиций/продаж не заявляется. [[../STL Product Update Workflow]].
