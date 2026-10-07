---
type: work-log
project_id: shustrik-maps-seo
status: completed
date: 2026-10-07
market: USA
language: English
---

# Десять Eurasia и Lambert STL опубликованы и проверены

Myanmar, Turkey, Ukraine, Finland, Ireland, Sweden, North America Lambert, Romania, Czech Republic, Luxembourg. Завершено 2026-10-07 10:33 МСК по прямому поручению «Следующие десять».

## Выбор и семантика

Свежий live inventory и журналы полных партий сверены. У выбранных товаров не было собственных AI-слайдеров; предыдущая десятка Belgium–Libya и более ранние партии исключены. Исторические SEO/каталоговые поля приняты как baseline. Illinois исключён как ранее обработанный SEO-кандидат. Беларусь исключена. [[selection.json]] / [[baseline.json]].

В ядре Google / English / USA от 05.10 нет точных десяти STL-кластеров. Новые товарные группы редакционные; frequency/rank=null. Английские публичные поисковые наблюдения подтверждают существование ряда цифровых STL-предложений, но не являются измерением спроса, позиций или локализованным Google US SERP. North America Lambert 9475 — отдельная SKU и проекция; показатели широкого North America relief не перенесены. Luxembourg city miniatures — смежный формат, а не доказательство спроса на рельеф страны. Предыдущие партии исключены по журналам. [[Intent Review]] / [[semantic-review.json]] / [[Page Briefs]].

## Что опубликовано

Изменены только SEO title/meta и выбранная иллюстрационная вставка Description: у всех десяти единственная ссылка на общий HTML-блок 9586 заменена собственным Woodmart carousel. Все прежние блоки основного текста сохранены дословно; shortcode-структура проверена. H1, URL, excerpt/specs, цены, downloads, thumbnail, верхние галереи и прочие productmeta защищены и сохранены. Общие HTML-блоки и исходные media не удалялись; 62 прежних media верхних галерей сохранены по ID/title/URL. [[preservation-qa.json]] / [[after.json]].

40 отдельных native ImageGen вызовов по собственным рендерам товаров. Все результаты осмотрены. Сцены: ivory PLA на сплошной walnut-подложке; небольшая картина в oak-раме; подарок в kraft-коробке; большая инсталляция из серого бетона. Настольные рельефы полностью поддержаны, острова Sweden и фрагменты North America Lambert закреплены на общей подложке. Сохранены 40 оригиналов PNG, 19 исходных референсов и полный набор prompts. Точное соответствие исходному mesh не заявляется. [[generation-jobs.json]] / [[generated-registry.json]] / [[visual-review.json]].

40 настоящих JPEG 1500×1000; title/alt отмечают AI-концепт и соответствующий материал. Один слайд desktop/mobile, ручные стрелки и четыре точки, autoplay=no. Под каждым слайдером только жирная центрованная **AI-generated application concepts.** [[uploaded-media.json]].

Все десять listings указывают base=closed; Luxembourg подтверждён вручную по исходной строке «Base: Closed». Исходные STL-архивы, mesh-готовность, точность и совместимость не проверялись; прежние claims сохранены, новые не добавлены. Подложки, рамы, упаковка и изготовление из бетона — дополнительная работа; коммерческая сцена не расширяет лицензию.

## Товары

| Товар | ID | Media IDs | URL |
|---|---:|---|---|
| Myanmar | 9423 | 22426, 22427, 22428, 22429 | https://shustrik-maps.com/product/myanmar-stl-model/ |
| Turkey | 9424 | 22430, 22431, 22432, 22433 | https://shustrik-maps.com/product/turkey-stl-model/ |
| Ukraine | 9465 | 22434, 22435, 22436, 22437 | https://shustrik-maps.com/product/ukraine-stl-model/ |
| Finland | 9466 | 22438, 22439, 22440, 22441 | https://shustrik-maps.com/product/finland-stl-model/ |
| Ireland | 9472 | 22442, 22443, 22444, 22445 | https://shustrik-maps.com/product/ireland-stl-model/ |
| Sweden | 9474 | 22446, 22447, 22448, 22449 | https://shustrik-maps.com/product/sweden-stl-model/ |
| North America Lambert | 9475 | 22450, 22451, 22452, 22453 | https://shustrik-maps.com/product/north-america-lambert-conformal-conic-stl-model/ |
| Romania | 9477 | 22454, 22455, 22456, 22457 | https://shustrik-maps.com/product/romania-stl-model/ |
| Czech Republic | 9479 | 22458, 22459, 22460, 22461 | https://shustrik-maps.com/product/czech-republic-stl-model/ |
| Luxembourg | 9481 | 22462, 22463, 22464, 22465 | https://shustrik-maps.com/product/luxembourg-stl-model/ |

## Публикация и QA

GitHub-first: SSH origin/main, starting HEAD 265c3d3, fetch/prune, upstream 0:0; прежние dirty/untracked сохранены. Source `2265489ea02f2ad8043fa2a887ca5ccca136f397` committed/pushed и сверён с remote main. Точный archive SHA256 `28ff6cc346f003b5fefcb3a679d1f339c8d2973570c537b4b1166f1b5ebd3565` совпал local/VPS. Пакет доставлен в `/tmp/ten-eurasia-2265489`, existing external WordPress https://shustrik-maps.com. [[deployment.json]].

PHP lint и preview прошли. Apply выполнен один раз с уникальными backup/journal ключами партии и проверкой параллельных изменений. DB 10/10: точные SEO/Description и защищённые поля. Media 40/40: SHA256, JPEG/MIME, размер 1500×1000, title/alt/caption. Before backups совпадают с baseline; journals 10/10 published. [[apply.json]] / [[verify.json]] / [[backup-export.json]].

Public HTTP 20/20: обычные и query URL 200; точные SEO, один исходный H1, self canonical, indexability, Product schema, commerce CTA, четыре новых изображения, краткая подпись, отсутствие raw shortcodes. Media 40/40 HTTP 200/image/jpeg. Для H1 учтена типографика WordPress « - » → « – », значение post_title отдельно сохранено точно. Query не доказывает cache bypass. [[public-qa.json]].

Browser 80/80: четыре слайда каждой карточки desktop 1440×1000 и mobile 390×844. Один активный и видимый слайд, верный alt, изображение загружено, две стрелки, четыре точки, caption center/font-weight≥600, горизонтального overflow нет. На всех 20 видах проверены Next через четыре слайда, Previous и возврат первой/четвёртой точкой. Скриншоты 20 видов и proof сохранены. [[browser-qa.json]] / [[myanmar-published-proof.png]].

WireGuard SSH vpsadmin@10.66.66.1 и sudo Docker доступны. Сначала проверены сервер и docker ps, затем target WP/DB. Status running, RestartCount 0, StartedAt и portbindings before/after совпали: WP 127.0.0.1:8083, DB без published ports. Контейнеры не перестраивались и не перезапускались; локальный runtime не менялся; секреты/.env не читались. [[runtime-before.txt]] / [[runtime-after.txt]].

## Откат

Guarded rollback-preview 10/10 прошёл. Backup `_shustrik_ten_eurasia_stl_slider_backup_20261007_ID`, journal `_shustrik_ten_eurasia_stl_slider_media_20261007_ID`, локальный [[backup-export.json]]. Сначала `sudo -n docker exec shustrik-maps-wordpress-1 php /tmp/ten-eurasia-2265489/release.php --rollback-preview`; затем `--rollback` только при отсутствии drift. Откат восстанавливает Description/SEO и сохраняет старые/новые media. Фактический rollback не выполнялся. Apply не идемпотентен: при неопределённом результате сначала читать journal/backup; слепой повтор запрещён. [[rollback-preview.json]].

Партия 10/10 завершена. Следующую выбирать по новому поручению и свежей сверке журналов/live inventory. Рост позиций и продаж не заявляется. P1 analytics/recovery/consent, контроль индекса 10.10 и yellow/degraded сохранены. [[../STL Product Update Workflow]].
