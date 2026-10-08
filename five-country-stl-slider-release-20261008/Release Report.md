---
type: work-log
project_id: shustrik-maps-seo
status: completed
date: 2026-10-08
market: USA
language: English
---

# Следующие пять country STL опубликованы и проверены

Venezuela, Uzbekistan, Uruguay, UAE, Taiwan. Завершено 2026-10-08 08:17 МСК по поручению «делай следующие 5».

## Выбор и семантика

Выбраны по возрастанию ID следующих country listings после Cambodia/Colombia/Costa Rica/Yemen/Vietnam. Журналы и fresh live inventory сверены: ни у одного из пяти не было собственного AI-слайдера, у каждого была одна ссылка на общий HTML-блок9586. Предыдущие партии исключены, Беларусь не рассматривается. [[selection.json]] / [[baseline.json]].

Сохранённое ядро Google/English/USA05.10 не содержит точных пяти STL-кластеров. Primary: place topographic map STL; support: terrain STL, relief map STL, map 3D print, CNC terrain model. Новые группы редакционные, frequency/rank=null. Фактически осмотрены пять Google выдач с hl=en/gl=us/pws=0. Footer Unknown / cannot determine location: US-local rank и фактическая локация не подтверждены. Частотности и позиции не измерялись. Paid whole-country STL intent отделён от free/physical/ordinary/GIS/vector/city/coin/outline intent. UAE и United Arab Emirates — один product intent, не Dubai city; у Venezuela/UAE/Taiwan сохранены острова, у Uzbekistan отдельный восточный фрагмент. Google AI Overview claims не переносились в карточки. [[Intent Review]] / [[intent-evidence.json]] / [[semantic-review.json]] / [[Page Briefs]]. Решение validate first относится к последующему измерению SEO-эффекта; порученная публикация существующих товаров выполнена.

## Публикация и сохранность

Изменены только SEO title/meta и выбранная иллюстрационная вставка Description: ссылка9586 заменена собственным native Woodmart carousel. Все прежние vc_column_text/main prose сохранены дословно. H1, URL, excerpt/specs, цены, downloads/files, thumbnail, верхняя галерея, прочие productmeta защищены. Общий блок9586 сохранён без изменений; 34 прежних media сохранены по ID/title/URL. [[preservation-qa.json]] / [[backup-export.json]] / [[after.json]].

20 отдельных native ImageGen вызовов, четыре разные сцены по собственному референсу каждого товара: ivory plastic desktop, небольшая картина, подарок в kraft-коробке, крупная инсталляция из серого бетона. Каждый результат визуально осмотрен. Все настольные рельефы полностью на цельной сплошной walnut-подложке, включая острова и выступы. Сохранены20 оригиналов PNG,10 собственных референсов, prompts/registry. Географические особенности закреплены в [[geography-notes.json]]; точное совпадение с mesh не заявляется. [[generation-jobs.json]] / [[generated-registry.json]] / [[visual-review.json]].

20 настоящих RGB JPEG1500×1000 с описательными title/alt и явной AI-concept маркировкой. Один слайд desktop/mobile, две ручные стрелки вместе внутри доступной области блока, четыре точки, autoplay=no/wrap=no. Под слайдером только жирная центрованная **AI-generated application concepts.** Media caption не выводится в gallery. [[uploaded-media.json]].

Все пять listings указывают base=closed. Mesh/archive/readiness не проверялись; прежние claims сохранены, новых обещаний готовности/точности/совместимости/лицензии не добавлено. Подложки, рамы, упаковка, concrete fabrication и коммерческие permissions — отдельная проектная работа.

## Товары

| Товар | ID | Media IDs | URL |
|---|---:|---|---|
| Venezuela | 19867 | 22626, 22627, 22628, 22629 | https://shustrik-maps.com/product/venezuela-stl-model/ |
| Uzbekistan | 19875 | 22630, 22631, 22632, 22633 | https://shustrik-maps.com/product/uzbekistan-stl-model/ |
| Uruguay | 19883 | 22634, 22635, 22636, 22637 | https://shustrik-maps.com/product/uruguay-stl-model/ |
| UAE | 19891 | 22638, 22639, 22640, 22641 | https://shustrik-maps.com/product/uae-stl-model/ |
| Taiwan | 19908 | 22642, 22643, 22644, 22645 | https://shustrik-maps.com/product/taiwan-stl-model/ |

## Доставка и проверки

GitHub-first: starting HEAD606e460; SSH remote/main; fetch/prune, upstream0:0. Прежние dirty/untracked сохранены. Source 37e0231545d5dbcb7304a696cb7678102f070552 committed/pushed и remote main подтверждён до apply. Exact archive SHA256 ef8ba261c1a0d864e4fdd14c72f724363111989dc996615b7408773063cb71db local/VPS совпал; source доставлен в /tmp/five-country-37e0231 внешнего WordPress https://shustrik-maps.com. Lint/preview5/5 прошли. Apply выполнен ровно один раз с уникальными backup/journal, transactional guard и защитой от параллельных изменений. [[deployment.json]] / [[preview.json]] / [[apply.json]].

DB5/5: точные SEO/Description, protected data, backup before совпал с baseline, journal status=published. Media20/20: SHA256/image/jpeg/1500×1000/title/alt/caption. Public HTTP10/10: обычный и query URL200, точные SEO, H1/self-canonical/indexability/Product schema/CTA, четыре новых media, краткая подпись, отсутствие raw shortcode. Media20/20 HTTP200/image/jpeg. Query не доказывает cache bypass. [[verify.json]] / [[public-qa.json]].

Browser40/40: четыре слайда каждого товара на1440×1000 и390×844. Один активный/видимый слайд, изображение загружено, alt точный; две стрелки/четыре точки/center/font-weight≥600/безoverflow. На всех10 видах Next/Previous/first&last dots прошли. Сохранены10 screenshots, контрольные JSON и отдельный proof. Мобильные screenshots и published proof осмотрены. [[browser-qa.json]] / [[venezuela-published-proof.png]].

WireGuard SSH vpsadmin@10.66.66.1 и sudo Docker available, сервер/docker ps проверены до target WP/DB. Running/RestartCount0/StartedAt/ports before/after совпали: WP127.0.0.1:8083, DB безpublished ports. Build/restart/local runtime change нет; secrets/.env не читались. [[runtime-before.txt]] / [[runtime-after.txt]].

## Откат

Guarded rollback-preview5/5 passed, actual rollback не выполнялся. Backup _shustrik_five_country_stl_slider_backup_20261008_ID; journal _shustrik_five_country_stl_slider_media_20261008_ID. Перед откатом выполнить:

```sh
sudo -n docker exec shustrik-maps-wordpress-1 php /tmp/five-country-37e0231/release.php --rollback-preview
```

Затем --rollback только при отсутствии published drift. Восстанавливаются прежние Description/SEO; old/new media сохраняются. Apply неидемпотентен: при неизвестном результате читать journals/backups, слепой повтор запрещён. [[rollback-preview.json]].

Партия5/5 завершена. P1 analytics/recovery/consent, индекс-контроль10.10, yellow/degraded сохранены. Рост позиций/продаж не заявляется. [[../STL Product Update Workflow]].

## Существующая ошибка Taiwan

В исходном Description Taiwan уже присутствует второй Sample Use Cases с упоминаниями UAE и Dubai. Это видно в baseline.json и desktop screenshot; блок сохранён дословно по поручению владельца. Исправление основного текста требует отдельного решения и не входит в этот SEO/media release.
