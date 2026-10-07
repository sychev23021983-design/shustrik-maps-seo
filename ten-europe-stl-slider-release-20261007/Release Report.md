---
type: work-log
project_id: shustrik-maps-seo
status: completed
date: 2026-10-07
market: USA
language: English
---

# Десять европейских STL опубликованы и проверены

Latvia, Lithuania, Poland, Hungary, Serbia, Slovakia, Slovenia, Moldova, Netherlands, Montenegro. Завершено 2026-10-07 11:23 МСК по прямому поручению «Следующие десять».

## Выбор и семантика

Свежий live inventory и журналы полных партий сверены. У выбранных товаров не было собственных AI-слайдеров; предыдущая десятка Myanmar–Luxembourg и более ранние партии исключены. Исторические SEO/каталоговые поля приняты как baseline. Illinois исключён как ранее обработанный SEO-кандидат. Беларусь исключена. [[selection.json]] / [[baseline.json]].

В ядре Google / English / USA от 05.10 нет точных десяти STL-кластеров. Новые товарные группы редакционные; frequency/rank=null. Английские публичные поисковые наблюдения подтверждают существование ряда цифровых STL-предложений, но не являются измерением спроса, позиций или локализованным Google US SERP. Slovakia и Slovenia разделены по собственным странам и SKU. Netherlands отделён от Holland, городских миниатюр и физического декора. Для Moldova независимое предложение цифрового рельефа всей страны по выполненным запросам не установлено; регион Moldavia и векторные карты исключены. Предыдущие партии исключены по журналам. [[Intent Review]] / [[semantic-review.json]] / [[Page Briefs]].

## Что опубликовано

Изменены только SEO title/meta и выбранная иллюстрационная вставка Description: у всех десяти единственная ссылка на общий HTML-блок 9586 заменена собственным Woodmart carousel. Все прежние блоки основного текста сохранены дословно; shortcode-структура проверена. H1, URL, excerpt/specs, цены, downloads, thumbnail, верхние галереи и прочие productmeta защищены и сохранены. Общие HTML-блоки и исходные media не удалялись; 67 прежних media верхних галерей сохранены по ID/title/URL. [[preservation-qa.json]] / [[after.json]].

40 отдельных native ImageGen вызовов по собственным рендерам товаров. Все результаты осмотрены. Сцены: ivory PLA на сплошной walnut-подложке; небольшая картина в oak-раме; подарок в kraft-коробке; большая инсталляция из серого бетона. Настольные рельефы полностью поддержаны, острова Netherlands и фрагменты Lithuania/Montenegro закреплены на общей подложке. Сохранены 40 оригиналов PNG, 20 исходных референсов и полный набор prompts. Точное соответствие исходному mesh не заявляется. [[generation-jobs.json]] / [[generated-registry.json]] / [[visual-review.json]].

40 настоящих JPEG 1500×1000; title/alt отмечают AI-концепт и соответствующий материал. Один слайд desktop/mobile, ручные стрелки и четыре точки, autoplay=no. Под каждым слайдером только жирная центрованная **AI-generated application concepts.** [[uploaded-media.json]].

Все десять listings указывают base=closed; Netherlands подтверждён вручную по исходной строке «Base: Closed». Исходные STL-архивы, mesh-готовность, точность и совместимость не проверялись; прежние claims сохранены, новые не добавлены. Подложки, рамы, упаковка и изготовление из бетона — дополнительная работа; коммерческая сцена не расширяет лицензию.

## Товары

| Товар | ID | Media IDs | URL |
|---|---:|---|---|
| Latvia | 9482 | 22466, 22467, 22468, 22469 | https://shustrik-maps.com/product/latvia-stl-model/ |
| Lithuania | 9483 | 22470, 22471, 22472, 22473 | https://shustrik-maps.com/product/lithuania-stl-model/ |
| Poland | 9484 | 22474, 22475, 22476, 22477 | https://shustrik-maps.com/product/poland-stl-model/ |
| Hungary | 9485 | 22478, 22479, 22480, 22481 | https://shustrik-maps.com/product/hungary-stl-model/ |
| Serbia | 9486 | 22482, 22483, 22484, 22485 | https://shustrik-maps.com/product/serbia-stl-model/ |
| Slovakia | 9487 | 22486, 22487, 22488, 22489 | https://shustrik-maps.com/product/slovakia-stl-model/ |
| Slovenia | 9488 | 22490, 22491, 22492, 22493 | https://shustrik-maps.com/product/slovenia-stl-model/ |
| Moldova | 9490 | 22494, 22495, 22496, 22497 | https://shustrik-maps.com/product/moldova-stl-model/ |
| Netherlands | 9491 | 22498, 22499, 22500, 22501 | https://shustrik-maps.com/product/netherlands-stl-model/ |
| Montenegro | 9492 | 22502, 22503, 22504, 22505 | https://shustrik-maps.com/product/montenegro-stl-model/ |

## Публикация и QA

GitHub-first: SSH origin/main, starting HEAD fab6af7, fetch/prune, upstream 0:0; прежние dirty/untracked сохранены. Source `a30719e3a7beeaf2d29cdb35b08162d8238e85cd` committed/pushed и сверён с remote main. Точный archive SHA256 `14674507aa244d06d7dade6973a4c8f19cb41f56959c574215f7f733f040bcd5` совпал local/VPS. Пакет доставлен в `/tmp/ten-europe-a30719e`, existing external WordPress https://shustrik-maps.com. [[deployment.json]].

PHP lint и preview прошли. Apply выполнен один раз с уникальными backup/journal ключами партии и проверкой параллельных изменений. DB 10/10: точные SEO/Description и защищённые поля. Media 40/40: SHA256, JPEG/MIME, размер 1500×1000, title/alt/caption. Before backups совпадают с baseline; journals 10/10 published. [[apply.json]] / [[verify.json]] / [[backup-export.json]].

Public HTTP 20/20: обычные и query URL 200; точные SEO, один исходный H1, self canonical, indexability, Product schema, commerce CTA, четыре новых изображения, краткая подпись, отсутствие raw shortcodes. Media 40/40 HTTP 200/image/jpeg. Для H1 учтена типографика WordPress « - » → « – », значение post_title отдельно сохранено точно. Query не доказывает cache bypass. [[public-qa.json]].

Browser 80/80: четыре слайда каждой карточки desktop 1440×1000 и mobile 390×844. Один активный и видимый слайд, верный alt, изображение загружено, две стрелки, четыре точки, caption center/font-weight≥600, горизонтального overflow нет. На всех 20 видах проверены Next через четыре слайда, Previous и возврат первой/четвёртой точкой. Скриншоты 20 видов и proof сохранены. Первая browser-попытка началась до готовности карусели; добавлено ожидание `.wd-initialized`, после чего полный цикл пройден заново. [[browser-qa.json]] / [[latvia-published-proof.png]].

WireGuard SSH vpsadmin@10.66.66.1 и sudo Docker доступны. Сначала проверены сервер и docker ps, затем target WP/DB. Status running, RestartCount 0, StartedAt и portbindings before/after совпали: WP 127.0.0.1:8083, DB без published ports. Контейнеры не перестраивались и не перезапускались; локальный runtime не менялся; секреты/.env не читались. [[runtime-before.txt]] / [[runtime-after.txt]].

## Откат

Guarded rollback-preview 10/10 прошёл. Backup `_shustrik_ten_europe_stl_slider_backup_20261007_ID`, journal `_shustrik_ten_europe_stl_slider_media_20261007_ID`, локальный [[backup-export.json]]. Сначала `sudo -n docker exec shustrik-maps-wordpress-1 php /tmp/ten-europe-a30719e/release.php --rollback-preview`; затем `--rollback` только при отсутствии drift. Откат восстанавливает Description/SEO и сохраняет старые/новые media. Фактический rollback не выполнялся. Apply не идемпотентен: при неопределённом результате сначала читать journal/backup; слепой повтор запрещён. [[rollback-preview.json]].

Партия 10/10 завершена. Следующую выбирать по новому поручению и свежей сверке журналов/live inventory. Рост позиций и продаж не заявляется. P1 analytics/recovery/consent, контроль индекса 10.10 и yellow/degraded сохранены. [[../STL Product Update Workflow]].
