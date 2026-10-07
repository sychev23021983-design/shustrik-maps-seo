---
type: work-log
project_id: shustrik-maps-seo
status: completed
date: 2026-10-07
market: USA
language: English
---

# Десять стран и островов STL: опубликовано и проверено

Afghanistan, Crete, Corsica, Algeria, Andorra, Angola, Armenia, Azerbaijan, Bangladesh, Dominica. По прямому поручению «Следующие десять» выполнен весь цикл до публикации и проверки. Завершено 2026-10-07 08:48 МСК.

Выбраны по свежему live inventory и журналам полных визуальных партий; собственных AI-слайдеров не было. Предыдущая десятка Indiana–South America и более ранние визуальные партии исключены. Выбор не является рейтингом спроса. Ранее опубликованные общие SEO/каталоговые поля учтены как baseline. [[baseline.json]].

## Изменения

Только SEO title/meta и иллюстрации в Description: у девяти заменена единственная вставка общего HTML-блока 9586; у Crete такой вставки не было, собственный слайдер добавлен после неизменного Applications текста в правой колонке. Все прежние основные тексты сохранены дословно, shortcode-структура проверена. H1/URL/excerpt/характеристики/цены/downloads/thumbnail/верхние галереи/protected productmeta сохранены. Общий HTML-блок 9586 и исходные media не удалялись; 71 прежних изображений верхних галерей сохранены по ID/title/URL. [[preservation-qa.json]] / [[after.json]].

Сверено сохранённое ядро Google/English/USA от 05.10: точных десяти STL-кластеров нет; новые группы редакционные, frequency/rank=null. Публичные поисковые наблюдения по digital-file intent сохранены отдельно, это не измеренные частотности/позиции и не контролируемый Google US SERP. Bangladesh независимый paid-STL intent остаётся гипотезой; DEM/DTM спрос не присваивался STL. Dominica отделена от Dominican Republic, Crete от without-water SKU, Armenia/Azerbaijan от multi-format terrain. Беларусь исключена. [[Intent Review]] / [[semantic-review.json]] / [[Page Briefs]].

40 отдельных native ImageGen вызовов по собственным SKU-рендерам. Все 40 результатов осмотрены: ivory PLA настольная модель на сплошной walnut-подложке, небольшая картина, подарок в коробке, большая grey concrete инсталляция. Настольные рельефы полностью поддержаны; Crete/Cabinda/Nakhchivan/дельта Bangladesh закреплены на общей подложке. Оригиналы PNG, 20 референсов и промпты сохранены. Рельефы иллюстрационные, не доказательство точного соответствия mesh. Pillow использован только для запрошенной JPEG-конверсии/ресайза. [[generation-jobs.json]] / [[generated-registry.json]] / [[visual-review.json]].

40 настоящих JPEG 1500×1000, title/alt с AI-концептом и верным материалом. Собственные Woodmart carousel: один слайд desktop/mobile, стрелки и четыре точки, autoplay=no. Под ними только жирная центрованная **AI-generated application concepts.** [[uploaded-media.json]].

Corsica listed base=open, остальные closed. Mesh/archive/готовность к печати и legacy accuracy/compatibility claims не проверены и не переписаны. Подложки/рамы/упаковка/изготовление из бетона — дополнительная работа; коммерческий концепт не расширяет лицензию.

## Опубликованные товары

| Товар | ID | Media IDs | URL |
|---|---:|---|---|
| Afghanistan | 9382 | 22346, 22347, 22348, 22349 | https://shustrik-maps.com/product/afghanistan-stl-model/ |
| Crete | 9384 | 22350, 22351, 22352, 22353 | https://shustrik-maps.com/product/crete-island-stl-model/ |
| Corsica | 9387 | 22354, 22355, 22356, 22357 | https://shustrik-maps.com/product/corsica-island-stl-model/ |
| Algeria | 9397 | 22358, 22359, 22360, 22361 | https://shustrik-maps.com/product/algeria-stl-model/ |
| Andorra | 9398 | 22362, 22363, 22364, 22365 | https://shustrik-maps.com/product/andorra-stl-model/ |
| Angola | 9399 | 22366, 22367, 22368, 22369 | https://shustrik-maps.com/product/angola-stl-model/ |
| Armenia | 9400 | 22370, 22371, 22372, 22373 | https://shustrik-maps.com/product/armenia-stl-model/ |
| Azerbaijan | 9401 | 22374, 22375, 22376, 22377 | https://shustrik-maps.com/product/azerbaijan-stl-model/ |
| Bangladesh | 9402 | 22378, 22379, 22380, 22381 | https://shustrik-maps.com/product/bangladesh-stl-model/ |
| Dominica | 9404 | 22382, 22383, 22384, 22385 | https://shustrik-maps.com/product/dominica-island-stl-model/ |

## Публикация и проверки

GitHub-first: SSH origin, main, исходный 7b2b7f4, fetch/prune/upstream 0:0; прежние dirty/untracked сохранены. Source `59d5e6119ca5d5765255babafb35078486841fd1` committed/pushed и main совпал; точный archive SHA256 `761d780abae7182f5b7f1a5809d36090ff43c3c729367d6502f15969108431e3` совпал local/VPS. Доставлен в `/tmp/ten-country-59d5e61` existing external WordPress https://shustrik-maps.com. [[deployment.json]].

PHP lint/preview passed; apply выполнен один раз. Новые backup/journal ключи уникальны для партии. DB 10/10 exact SEO/Description/protected поля; media 40/40 SHA256/JPEG/MIME 1500×1000/title/alt/caption. Экспорт before backups совпадает с baseline, journal 10/10 published. [[apply.json]] / [[verify.json]] / [[backup-export.json]].

Public HTTP 20/20: ordinary и query URL 200, точные SEO, один исходный H1/self canonical/indexability/Product schema/CTA/четыре новые картинки/краткая подпись/no raw shortcodes. Media 40/40 HTTP 200/image/jpeg. Для Algeria WordPress отображает исходный разделитель « - » как « – » через типографику; проверка H1 учитывает это преобразование, а значение post_title сохранено дословно. Query сам по себе не доказывает cache bypass. [[public-qa.json]].

Browser 80/80: четыре слайда каждой карточки desktop 1440×1000 и mobile 390×844; один видимый/активный слайд, соответствующий alt, JPEG загружен, стрелки/четыре точки, caption center/font-weight 600, overflow нет. На 20 видах Next три раза и возврат первой точкой проверены. Скриншоты 20 видов сохранены, checkout/оплата не выполнялись. [[browser-qa.json]] / [[afghanistan-published-proof.jpg]].

WireGuard SSH vpsadmin@10.66.66.1/sudo Docker доступны; сначала подтверждён сервер и docker ps, затем target WP/DB. Running/restarts 0/StartedAt/portbindings before/after совпали: WP 127.0.0.1:8083, DB без опубликованных ports. Build/restart не выполнялись, локальный runtime не менялся. Секреты/.env не читались. [[runtime-before.txt]] / [[runtime-after.txt]].

## Откат

Guarded rollback-preview 10/10 passed. Backup `_shustrik_ten_country_stl_slider_backup_20261007_ID`, journal `_shustrik_ten_country_stl_slider_media_20261007_ID`; локальный [[backup-export.json]]. Сначала `sudo -n docker exec shustrik-maps-wordpress-1 php /tmp/ten-country-59d5e61/release.php --rollback-preview`, затем `--rollback` только при отсутствии drift. Откат восстанавливает Description/title/meta и сохраняет новые/старые media. Фактический rollback не выполнялся. Apply не идемпотентен: отказ требует чтения journal/backup, слепой повтор запрещён. [[rollback-preview.json]].

Партия 10/10 завершена. Новую партию выбирать по следующему поручению и журналам/live inventory. Рост позиций/продаж не заявляется. P1 analytics/recovery/consent, контроль индекса 10.10, yellow/degraded сохранены. [[../STL Product Update Workflow]].
