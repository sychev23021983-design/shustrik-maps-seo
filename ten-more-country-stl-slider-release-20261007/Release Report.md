---
type: work-log
project_id: shustrik-maps-seo
status: completed
date: 2026-10-07
market: USA
language: English
---

# Следующие десять стран STL опубликованы и проверены

Belgium, Jamaica, Jordan, Kazakhstan, Kosovo, Kuwait, Kyrgyzstan, Laos, Liberia, Libya. Завершено 2026-10-07 09:40 МСК по прямому поручению «Следующие десять».

## Выбор и семантика

Свежий live inventory и журналы полных партий сверены. У выбранных товаров не было собственных AI-слайдеров; предыдущая десятка Afghanistan–Dominica и более ранние партии исключены. Исторические SEO/каталоговые поля приняты как baseline. Illinois исключён как ранее обработанный SEO-кандидат. Беларусь исключена. [[selection.json]] / [[baseline.json]].

В ядре Google / English / USA от 05.10 нет точных десяти STL-кластеров. Новые товарные группы редакционные; frequency/rank=null. Английские публичные поисковые наблюдения подтверждают существование ряда цифровых STL-предложений, но не являются измерением спроса, позиций или локализованным Google US SERP. Liberia coin/token — смежный формат, а не доказательство спроса на эту карточку. Kazakhstan отделён от Astana, Jamaica от Kingston, Kuwait от Salmiya; Liberia и Libya различаются. [[Intent Review]] / [[semantic-review.json]] / [[Page Briefs]].

## Что опубликовано

Изменены только SEO title/meta и выбранная иллюстрационная вставка Description: у всех десяти единственная ссылка на общий HTML-блок 9586 заменена собственным Woodmart carousel. Все прежние блоки основного текста сохранены дословно; shortcode-структура проверена. H1, URL, excerpt/specs, цены, downloads, thumbnail, верхние галереи и прочие productmeta защищены и сохранены. Общие HTML-блоки и исходные media не удалялись; 65 прежних media верхних галерей сохранены по ID/title/URL. [[preservation-qa.json]] / [[after.json]].

40 отдельных native ImageGen вызовов по собственным рендерам товаров. Все результаты осмотрены. Сцены: ivory PLA на сплошной walnut-подложке; небольшая картина в oak-раме; подарок в kraft-коробке; большая инсталляция из серого бетона. Настольные рельефы полностью поддержаны, острова Kuwait закреплены на общей подложке. Сохранены 40 оригиналов PNG, 19 исходных референсов и полный набор prompts. Точное соответствие исходному mesh не заявляется. [[generation-jobs.json]] / [[generated-registry.json]] / [[visual-review.json]].

40 настоящих JPEG 1500×1000; title/alt отмечают AI-концепт и соответствующий материал. Один слайд desktop/mobile, ручные стрелки и четыре точки, autoplay=no. Под каждым слайдером только жирная центрованная **AI-generated application concepts.** [[uploaded-media.json]].

Все десять listings указывают base=closed. Исходные STL-архивы, mesh-готовность, точность и совместимость не проверялись; прежние claims сохранены, новые не добавлены. Подложки, рамы, упаковка и изготовление из бетона — дополнительная работа; коммерческая сцена не расширяет лицензию.

## Товары

| Товар | ID | Media IDs | URL |
|---|---:|---|---|
| Belgium | 9403 | 22386, 22387, 22388, 22389 | https://shustrik-maps.com/product/belgium-stl-model/ |
| Jamaica | 9406 | 22390, 22391, 22392, 22393 | https://shustrik-maps.com/product/jamaica-stl-model/ |
| Jordan | 9408 | 22394, 22395, 22396, 22397 | https://shustrik-maps.com/product/jordan-stl-model/ |
| Kazakhstan | 9409 | 22398, 22399, 22400, 22401 | https://shustrik-maps.com/product/kazakhstan-stl-model/ |
| Kosovo | 9410 | 22402, 22403, 22404, 22405 | https://shustrik-maps.com/product/kosovo-stl-model/ |
| Kuwait | 9411 | 22406, 22407, 22408, 22409 | https://shustrik-maps.com/product/kuwait-stl-model/ |
| Kyrgyzstan | 9412 | 22410, 22411, 22412, 22413 | https://shustrik-maps.com/product/kyrgyzstan-stl-model/ |
| Laos | 9420 | 22414, 22415, 22416, 22417 | https://shustrik-maps.com/product/laos-stl-model/ |
| Liberia | 9421 | 22418, 22419, 22420, 22421 | https://shustrik-maps.com/product/liberia-stl-model/ |
| Libya | 9422 | 22422, 22423, 22424, 22425 | https://shustrik-maps.com/product/libya-stl-model/ |

## Публикация и QA

GitHub-first: SSH origin/main, starting HEAD c93c0b0, fetch/prune, upstream 0:0; прежние dirty/untracked сохранены. Source `2eef228c5834442c0a2b3083b09ddd9452d423ae` committed/pushed и сверён с remote main. Точный archive SHA256 `034fbd6b4a56e5d921f21ece70a0088edc0d38f389d689a07c71378f307e5c54` совпал local/VPS. Пакет доставлен в `/tmp/ten-more-country-2eef228`, existing external WordPress https://shustrik-maps.com. [[deployment.json]].

PHP lint и preview прошли. Apply выполнен один раз с уникальными backup/journal ключами партии и проверкой параллельных изменений. DB 10/10: точные SEO/Description и защищённые поля. Media 40/40: SHA256, JPEG/MIME, размер 1500×1000, title/alt/caption. Before backups совпадают с baseline; journals 10/10 published. [[apply.json]] / [[verify.json]] / [[backup-export.json]].

Public HTTP 20/20: обычные и query URL 200; точные SEO, один исходный H1, self canonical, indexability, Product schema, commerce CTA, четыре новых изображения, краткая подпись, отсутствие raw shortcodes. Media 40/40 HTTP 200/image/jpeg. Для H1 учтена типографика WordPress « - » → « – », значение post_title отдельно сохранено точно. Query не доказывает cache bypass. [[public-qa.json]].

Browser 80/80: четыре слайда каждой карточки desktop 1440×1000 и mobile 390×844. Один активный и видимый слайд, верный alt, изображение загружено, две стрелки, четыре точки, caption center/font-weight≥600, горизонтального overflow нет. На всех 20 видах проверены Next через четыре слайда, Previous и возврат первой/четвёртой точкой. Скриншоты 20 видов и proof сохранены. [[browser-qa.json]] / [[belgium-published-proof.png]].

WireGuard SSH vpsadmin@10.66.66.1 и sudo Docker доступны. Сначала проверены сервер и docker ps, затем target WP/DB. Status running, RestartCount 0, StartedAt и portbindings before/after совпали: WP 127.0.0.1:8083, DB без published ports. Контейнеры не перестраивались и не перезапускались; локальный runtime не менялся; секреты/.env не читались. [[runtime-before.txt]] / [[runtime-after.txt]].

## Откат

Guarded rollback-preview 10/10 прошёл. Backup `_shustrik_ten_more_country_stl_slider_backup_20261007_ID`, journal `_shustrik_ten_more_country_stl_slider_media_20261007_ID`, локальный [[backup-export.json]]. Сначала `sudo -n docker exec shustrik-maps-wordpress-1 php /tmp/ten-more-country-2eef228/release.php --rollback-preview`; затем `--rollback` только при отсутствии drift. Откат восстанавливает Description/SEO и сохраняет старые/новые media. Фактический rollback не выполнялся. Apply не идемпотентен: при неопределённом результате сначала читать journal/backup; слепой повтор запрещён. [[rollback-preview.json]].

Партия 10/10 завершена. Следующую выбирать по новому поручению и свежей сверке журналов/live inventory. Рост позиций и продаж не заявляется. P1 analytics/recovery/consent, контроль индекса 10.10 и yellow/degraded сохранены. [[../STL Product Update Workflow]].
