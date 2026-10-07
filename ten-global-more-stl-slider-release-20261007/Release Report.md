---
type: work-log
project_id: shustrik-maps-seo
status: completed
date: 2026-10-07
market: USA
language: English
---

# Ещё десять Global STL опубликованы и проверены

Eritrea, Estonia, Bosnia and Herzegovina, Bulgaria, Djibouti, Dominican Republic, Egypt, Equatorial Guinea, Ethiopia, Papua New Guinea. Завершено 2026-10-07 17:30 МСК по прямому поручению «Следующие десять».

## Выбор и семантика

Свежий live inventory и журналы полных партий сверены. У выбранных товаров не было собственных AI-слайдеров; предыдущая десятка North Macedonia–El Salvador и более ранние партии исключены. Исторические SEO/каталоговые поля приняты как baseline. Denmark исключён как ранее обработанный; Earth sphere оставлен за рамками партии стран. Беларусь исключена. [[selection.json]] / [[baseline.json]].

В ядре Google / English / USA от 05.10 нет точных десяти STL-кластеров. Новые товарные группы редакционные; frequency/rank=null. Английские публичные поисковые наблюдения подтверждают существование ряда цифровых STL-предложений, но не являются измерением спроса, позиций или локализованным Google US SERP. Dominican Republic отделён от Dominica; Equatorial Guinea — от Guinea и Guinea-Bissau. Для Equatorial Guinea независимый STL всей страны по выполненным запросам не установлен. Бесплатные coins и физические локальные модели не приравниваются к платному STL всей страны. Предыдущие партии исключены по журналам. [[Intent Review]] / [[semantic-review.json]] / [[Page Briefs]].

## Что опубликовано

Изменены только SEO title/meta и выбранная иллюстрационная вставка Description: у всех десяти единственная ссылка на общий HTML-блок 9586 заменена собственным Woodmart carousel. Все прежние блоки основного текста сохранены дословно; shortcode-структура проверена. H1, URL, excerpt/specs, цены, downloads, thumbnail, верхние галереи и прочие productmeta защищены и сохранены. Общие HTML-блоки и исходные media не удалялись; 71 прежних media верхних галерей сохранены по ID/title/URL. [[preservation-qa.json]] / [[after.json]].

40 отдельных native ImageGen вызовов по собственным рендерам товаров. Все результаты осмотрены. Сцены: ivory PLA на сплошной walnut-подложке; небольшая картина в oak-раме; подарок в kraft-коробке; большая инсталляция из серого бетона. Настольные рельефы полностью поддержаны, острова и фрагменты Eritrea, Estonia, Dominican Republic, Egypt, Equatorial Guinea и Papua New Guinea закреплены на общей подложке. Сохранены 40 оригиналов PNG, 20 исходных референсов и полный набор prompts. Точное соответствие исходному mesh не заявляется. [[generation-jobs.json]] / [[generated-registry.json]] / [[visual-review.json]].

40 настоящих JPEG 1500×1000; title/alt отмечают AI-концепт и соответствующий материал. Один слайд desktop/mobile, ручные стрелки и четыре точки, autoplay=no; штатное carousel_arrows_position=together задано всем десяти. Под каждым слайдером только жирная центрованная **AI-generated application concepts.** [[uploaded-media.json]].

Все десять listings указывают base=closed. Исходные STL-архивы, mesh-готовность, точность и совместимость не проверялись; прежние claims сохранены, новые не добавлены. Подложки, рамы, упаковка и изготовление из бетона — дополнительная работа; коммерческая сцена не расширяет лицензию.

## Товары

| Товар | ID | Media IDs | URL |
|---|---:|---|---|
| Eritrea | 9508 | 22546, 22547, 22548, 22549 | https://shustrik-maps.com/product/eritrea-stl-model/ |
| Estonia | 9509 | 22550, 22551, 22552, 22553 | https://shustrik-maps.com/product/estonia-stl-model/ |
| Bosnia and Herzegovina | 9513 | 22554, 22555, 22556, 22557 | https://shustrik-maps.com/product/bosnia-and-herzegovina-stl-model/ |
| Bulgaria | 9515 | 22558, 22559, 22560, 22561 | https://shustrik-maps.com/product/bulgaria-stl-model/ |
| Djibouti | 9517 | 22562, 22563, 22564, 22565 | https://shustrik-maps.com/product/djibouti-stl-model/ |
| Dominican Republic | 9518 | 22566, 22567, 22568, 22569 | https://shustrik-maps.com/product/dominican-republic-stl-model/ |
| Egypt | 9525 | 22570, 22571, 22572, 22573 | https://shustrik-maps.com/product/egypt-stl-model/ |
| Equatorial Guinea | 9526 | 22574, 22575, 22576, 22577 | https://shustrik-maps.com/product/equatorial-guinea-stl-model/ |
| Ethiopia | 9528 | 22578, 22579, 22580, 22581 | https://shustrik-maps.com/product/ethiopia-stl-model/ |
| Papua New Guinea | 15811 | 22582, 22583, 22584, 22585 | https://shustrik-maps.com/product/papua-new-guinea-stl-model/ |

## Публикация и QA

GitHub-first: SSH origin/main, starting HEAD 94ee322, fetch/prune, upstream 0:0; прежние dirty/untracked сохранены. Source `1e52c0ada960da4a08cd3499614f02c2eaf30e07` committed/pushed и сверён с remote main. Точный archive SHA256 `3b030c1fa4e9ecbe3b091c8fa88d6988d1efa5edf7e97950ffe64cee905aba44` совпал local/VPS. Пакет доставлен в `/tmp/ten-global-more-1e52c0a`, existing external WordPress https://shustrik-maps.com. [[deployment.json]].

PHP lint и preview прошли. Apply выполнен один раз с уникальными backup/journal ключами партии и проверкой параллельных изменений. DB 10/10: точные SEO/Description и защищённые поля. Media 40/40: SHA256, JPEG/MIME, размер 1500×1000, title/alt/caption. Before backups совпадают с baseline; journals 10/10 published. [[apply.json]] / [[verify.json]] / [[backup-export.json]].

Public HTTP 20/20: обычные и query URL 200; точные SEO, один исходный H1, self canonical, indexability, Product schema, commerce CTA, четыре новых изображения, краткая подпись, отсутствие raw shortcodes. Media 40/40 HTTP 200/image/jpeg. Для H1 учтена типографика WordPress « - » → « – », значение post_title отдельно сохранено точно. Query не доказывает cache bypass. [[public-qa.json]].

Browser 80/80: четыре слайда каждой карточки desktop 1440×1000 и mobile 390×844. Один активный и видимый слайд, верный alt, изображение загружено, две стрелки, четыре точки, caption center/font-weight≥600, горизонтального overflow нет. На всех 20 видах проверены Next через четыре слайда, Previous и возврат первой/четвёртой точкой. Скриншоты 20 видов и proof сохранены. [[browser-qa.json]] / [[eritrea-published-proof.png]].

WireGuard SSH vpsadmin@10.66.66.1 и sudo Docker доступны. Сначала проверены сервер и docker ps, затем target WP/DB. Status running, RestartCount 0, StartedAt и portbindings before/after совпали: WP 127.0.0.1:8083, DB без published ports. Контейнеры не перестраивались и не перезапускались; локальный runtime не менялся; секреты/.env не читались. [[runtime-before.txt]] / [[runtime-after.txt]].

## Откат

Guarded rollback-preview 10/10 прошёл. Backup `_shustrik_ten_global_more_stl_slider_backup_20261007_ID`, journal `_shustrik_ten_global_more_stl_slider_media_20261007_ID`, локальный [[backup-export.json]]. Сначала `sudo -n docker exec shustrik-maps-wordpress-1 php /tmp/ten-global-more-1e52c0a/release.php --rollback-preview`; затем `--rollback` только при отсутствии drift. Откат восстанавливает Description/SEO и сохраняет старые/новые media. Фактический rollback не выполнялся. Apply не идемпотентен: при неопределённом результате сначала читать journal/backup; слепой повтор запрещён. [[rollback-preview.json]].

Партия 10/10 завершена. Следующую выбирать по новому поручению и свежей сверке журналов/live inventory. Рост позиций и продаж не заявляется. P1 analytics/recovery/consent, контроль индекса 10.10 и yellow/degraded сохранены. [[../STL Product Update Workflow]].
