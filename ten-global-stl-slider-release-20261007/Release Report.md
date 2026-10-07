---
type: work-log
project_id: shustrik-maps-seo
status: completed
date: 2026-10-07
market: USA
language: English
---

# Десять стран Global STL опубликованы и проверены

North Macedonia, Croatia, Liechtenstein, Greece, Cyprus, Argentina, Austria, DR Congo, Ecuador, El Salvador. Завершено 2026-10-07 14:07 МСК по прямому поручению «Следующие десять».

## Выбор и семантика

Свежий live inventory и журналы полных партий сверены. У выбранных товаров не было собственных AI-слайдеров; предыдущая десятка Latvia–Montenegro и более ранние партии исключены. Исторические SEO/каталоговые поля приняты как baseline. Illinois исключён как ранее обработанный SEO-кандидат. Беларусь исключена. [[selection.json]] / [[baseline.json]].

В ядре Google / English / USA от 05.10 нет точных десяти STL-кластеров. Новые товарные группы редакционные; frequency/rank=null. Английские публичные поисковые наблюдения подтверждают существование ряда цифровых STL-предложений, но не являются измерением спроса, позиций или локализованным Google US SERP. North Macedonia отделён от Greek Macedonia и спутниковых визуализаций; независимый print-only intent установлен ограниченно. DR Congo отделён от Republic of Congo и нерелевантного акронима Sharing the Land; независимое предложение цифрового рельефа всей страны по выполненным запросам не установлено. Cyprus отражает остров собственного SKU, Ecuador сохраняет только исходное материковое покрытие. Austria URL ausrtia-stl-model сохранён. Предыдущие партии исключены по журналам. [[Intent Review]] / [[semantic-review.json]] / [[Page Briefs]].

## Что опубликовано

Изменены только SEO title/meta и выбранная иллюстрационная вставка Description: у всех десяти единственная ссылка на общий HTML-блок 9586 заменена собственным Woodmart carousel. Все прежние блоки основного текста сохранены дословно; shortcode-структура проверена. H1, URL, excerpt/specs, цены, downloads, thumbnail, верхние галереи и прочие productmeta защищены и сохранены. Общие HTML-блоки и исходные media не удалялись; 71 прежних media верхних галерей сохранены по ID/title/URL. [[preservation-qa.json]] / [[after.json]].

40 отдельных native ImageGen вызовов по собственным рендерам товаров. Все результаты осмотрены. Сцены: ivory PLA на сплошной walnut-подложке; небольшая картина в oak-раме; подарок в kraft-коробке; большая инсталляция из серого бетона. Настольные рельефы полностью поддержаны, острова Croatia/Greece и фрагменты Argentina/Ecuador/El Salvador закреплены на общей подложке. Сохранены 40 оригиналов PNG, 20 исходных референсов и полный набор prompts. Точное соответствие исходному mesh не заявляется. [[generation-jobs.json]] / [[generated-registry.json]] / [[visual-review.json]].

40 настоящих JPEG 1500×1000; title/alt отмечают AI-концепт и соответствующий материал. Один слайд desktop/mobile, ручные стрелки и четыре точки, autoplay=no. Под каждым слайдером только жирная центрованная **AI-generated application concepts.** [[uploaded-media.json]].

Все десять listings указывают base=closed; Liechtenstein подтверждён вручную по исходной строке «Base: Closed». Исходные STL-архивы, mesh-готовность, точность и совместимость не проверялись; прежние claims сохранены, новые не добавлены. Подложки, рамы, упаковка и изготовление из бетона — дополнительная работа; коммерческая сцена не расширяет лицензию.

## Товары

| Товар | ID | Media IDs | URL |
|---|---:|---|---|
| North Macedonia | 9493 | 22506, 22507, 22508, 22509 | https://shustrik-maps.com/product/north-macedonia-stl-model/ |
| Croatia | 9494 | 22510, 22511, 22512, 22513 | https://shustrik-maps.com/product/croatia-stl-model/ |
| Liechtenstein | 9495 | 22514, 22515, 22516, 22517 | https://shustrik-maps.com/product/liechtenstein-stl-model/ |
| Greece | 9496 | 22518, 22519, 22520, 22521 | https://shustrik-maps.com/product/greece-stl-model/ |
| Cyprus | 9499 | 22522, 22523, 22524, 22525 | https://shustrik-maps.com/product/cyprus-island-stl-model/ |
| Argentina | 9500 | 22526, 22527, 22528, 22529 | https://shustrik-maps.com/product/argentina-stl-model/ |
| Austria | 9501 | 22530, 22531, 22532, 22533 | https://shustrik-maps.com/product/ausrtia-stl-model/ |
| DR Congo | 9502 | 22534, 22535, 22536, 22537 | https://shustrik-maps.com/product/democratic-republic-of-congo-stl-model/ |
| Ecuador | 9506 | 22538, 22539, 22540, 22541 | https://shustrik-maps.com/product/ecuador-stl-model/ |
| El Salvador | 9507 | 22542, 22543, 22544, 22545 | https://shustrik-maps.com/product/el-salvador-stl-model/ |

## Публикация и QA

GitHub-first: SSH origin/main, starting HEAD d7b8e3f, fetch/prune, upstream 0:0; прежние dirty/untracked сохранены. Source `20ce527a22ec5e34a971b73a635bae68a2eaebd3` committed/pushed и сверён с remote main. Точный archive SHA256 `8bfe16bcedc7fdb62b9cea590c36016326ba598dc5a583aa97a9d024dccb59da` совпал local/VPS. Пакет доставлен в `/tmp/ten-global-20ce527`, existing external WordPress https://shustrik-maps.com. [[deployment.json]].

PHP lint и preview прошли. Apply выполнен один раз с уникальными backup/journal ключами партии и проверкой параллельных изменений. DB 10/10: точные SEO/Description и защищённые поля. Media 40/40: SHA256, JPEG/MIME, размер 1500×1000, title/alt/caption. Before backups совпадают с baseline; journals 10/10 published. [[apply.json]] / [[verify.json]] / [[backup-export.json]].

Public HTTP 20/20: обычные и query URL 200; точные SEO, один исходный H1, self canonical, indexability, Product schema, commerce CTA, четыре новых изображения, краткая подпись, отсутствие raw shortcodes. Media 40/40 HTTP 200/image/jpeg. Для H1 учтена типографика WordPress « - » → « – », значение post_title отдельно сохранено точно. Query не доказывает cache bypass. [[public-qa.json]].

Browser 80/80: четыре слайда каждой карточки desktop 1440×1000 и mobile 390×844. Один активный и видимый слайд, верный alt, изображение загружено, две стрелки, четыре точки, caption center/font-weight≥600, горизонтального overflow нет. На всех 20 видах проверены Next через четыре слайда, Previous и возврат первой/четвёртой точкой. Скриншоты 20 видов и proof сохранены. [[browser-qa.json]] / [[north-macedonia-published-proof.png]].

WireGuard SSH vpsadmin@10.66.66.1 и sudo Docker доступны. Сначала проверены сервер и docker ps, затем target WP/DB. Status running, RestartCount 0, StartedAt и portbindings before/after совпали: WP 127.0.0.1:8083, DB без published ports. Контейнеры не перестраивались и не перезапускались; локальный runtime не менялся; секреты/.env не читались. [[runtime-before.txt]] / [[runtime-after.txt]].

## Исправление стрелок El Salvador

Первичная публикация SEO и 40 media выполнена один раз из source `50ce4d978fb8d6ef5cc353e2c600472c7d032545`, exact archive `173dda4adf417df669c17f3813e2164bb78f1b5b0e841403bbe5b4cee069a58e`, `/tmp/ten-global-50ce4d9`. На desktop у El Salvador правая отдельная стрелка выходила за доступную область и клик не переключал слайд. Проверены фактические исходники Woodmart: штатная настройка `carousel_arrows_position="together"` поддерживается. Source `20ce527a22ec5e34a971b73a635bae68a2eaebd3` добавил её только в собственный слайдер ID9507. Guarded arrow-preview/apply/verify прошли; новые media не импортировались. Первоначальный before-backup партии сохранён дословно, after-backup обновлён до проверенного конечного состояния; дополнительная option backup `_shustrik_ten_global_slider_arrow_fix_backup_20261007_9507` сохраняет состояние до исправления. El Salvador повторно прошёл четыре слайда desktop и mobile. После исправления повторены DB/media/protected/public QA и rollback-preview. [[deployment-original.json]] / [[arrow-preview.json]] / [[arrow-apply.json]] / [[arrow-verify.json]] / [[arrow-diagnostic-before.json]] / [[arrow-diagnostic-after.json]].

## Откат

Guarded rollback-preview 10/10 прошёл. Backup `_shustrik_ten_global_stl_slider_backup_20261007_ID`, journal `_shustrik_ten_global_stl_slider_media_20261007_ID`, локальный [[backup-export.json]]. Сначала `sudo -n docker exec shustrik-maps-wordpress-1 php /tmp/ten-global-20ce527/release.php --rollback-preview`; затем `--rollback` только при отсутствии drift. Откат восстанавливает Description/SEO и сохраняет старые/новые media. Фактический rollback не выполнялся. Apply не идемпотентен: при неопределённом результате сначала читать journal/backup; слепой повтор запрещён. [[rollback-preview.json]].

Партия 10/10 завершена. Следующую выбирать по новому поручению и свежей сверке журналов/live inventory. Рост позиций и продаж не заявляется. P1 analytics/recovery/consent, контроль индекса 10.10 и yellow/degraded сохранены. [[../STL Product Update Workflow]].
