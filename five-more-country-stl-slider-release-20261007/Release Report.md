---
type: work-log
project_id: shustrik-maps-seo
status: completed
date: 2026-10-07
market: USA
language: English
---

# Пять следующих STL опубликованы и проверены

Haiti, Belize, Bolivia, Bhutan, Bermuda. Завершено 2026-10-07 20:25 МСК по прямому поручению «делай».

## Выбор и семантика

Журналы и свежий live inventory сверены; у пяти выбранных товаров не было собственных AI-слайдеров, у каждого стояла единственная ссылка на общий HTML-блок9586. Предыдущая партия Eritrea–Papua New Guinea и более ранние завершённые партии исключены. Беларусь не рассматривается. [[selection.json]] / [[baseline.json]].

Google / English / USA: сохранённое ядро05.10 не содержит точных пяти STL-кластеров. Новые группы редакционные, frequency/rank=null. Публичный английский поиск проверяет intent, а не частотности или Google-US позиции. Haiti отделён от Dominican Republic; Bermuda — островная территория с морским рельефом вокруг архипелага. Бесплатный Bhutan STL, локальные рельефы, обычные карты и laser SVG не приравниваются к платному whole-place STL. Для Bermuda независимое точное платное STL-предложение не установлено по выполненным запросам. [[Intent Review]] / [[semantic-review.json]] / [[Page Briefs]].

## Публикация

Изменены только SEO title/meta и выбранная иллюстрационная вставка Description: ссылка на общий блок9586 заменена собственным native Woodmart carousel. Все прежние vc_column_text/main prose сохранены дословно. H1, URL, excerpt/specs, цены, files/downloads, thumbnail, верхняя галерея и прочие productmeta защищены. Общий блок9586 не изменён, старые media не удалялись: 34 прежних изображений сохранены по ID/title/URL. [[preservation-qa.json]] / [[after.json]].

20 отдельных native ImageGen вызовов по собственным географическим референсам; каждый результат осмотрен. Сцены: ivory plastic desktop на сплошной walnut-подложке; небольшая картина; подарок в kraft-коробке; большая инсталляция из серого бетона. Настольные рельефы целиком опираются на цельную подложку, включая острова Haiti/Belize. Bermuda сохраняет квадратный bathymetric tile, мелководную платформу, островную цепь и подводные склоны; вся плитка на сплошной подложке. Сохранены20 оригиналов PNG,10 собственных референсов и prompts. Точное совпадение с mesh не заявляется. [[generation-jobs.json]] / [[generated-registry.json]] / [[visual-review.json]].

20 настоящих JPEG1500×1000 с описательными title/alt и явной AI-концепт маркировкой. Один слайд desktop/mobile, две ручные стрелки внутри доступной области блока (carousel_arrows_position=together), четыре точки, autoplay=no. Под слайдером только жирная центрованная **AI-generated application concepts.** [[uploaded-media.json]].

Все пять listings указывают base=closed. Mesh/STL archives/readiness не проверялись; прежние claims сохранены, новые не добавлены. Подложки, рамы, упаковка и concrete fabrication — отдельная проектная работа; коммерческий концепт не расширяет лицензию.

## Товары

| Товар | ID | Media IDs | URL |
|---|---:|---|---|
| Haiti | 16849 | 22586, 22587, 22588, 22589 | https://shustrik-maps.com/product/haiti-terrain-stl-model/ |
| Belize | 19729 | 22590, 22591, 22592, 22593 | https://shustrik-maps.com/product/belize-stl-model/ |
| Bolivia | 19737 | 22594, 22595, 22596, 22597 | https://shustrik-maps.com/product/bolivia-stl-model/ |
| Bhutan | 19746 | 22598, 22599, 22600, 22601 | https://shustrik-maps.com/product/bhutan-stl-model/ |
| Bermuda | 19753 | 22602, 22603, 22604, 22605 | https://shustrik-maps.com/product/bermuda-stl-model/ |

## Доставка, QA и runtime

GitHub-first: SSH origin/main; starting HEAD9ec16eb; fetch/prune, upstream0:0, прежние dirty/untracked сохранены. Source 16774f00dd945bc2acdaa92a8e8ae530848904d5 committed/pushed, remote main совпал. Точный архив SHA256 594fe5b151ca673dfd4c9334ac194417524c9af641e02d351fcee1d801df10dc local/VPS совпал; source доставлен в /tmp/five-more-country-16774f0 внешнего WordPress https://shustrik-maps.com. PHP lint/preview5/5 прошли. Apply выполнен ровно один раз с уникальными backup/journal и проверкой параллельных изменений. [[deployment.json]] / [[apply.json]].

DB5/5: точные SEO/Description, защищённые данные, before-backup совпал с baseline, journal status=published. Media20/20: SHA256, image/jpeg,1500×1000,title/alt/caption. Public HTTP10/10: обычный и query URL200, точные SEO, H1/self-canonical/indexability/Product schema/CTA, четыре новых media, краткая подпись, отсутствие raw shortcode. Media20/20 HTTP200/image/jpeg. Query не доказывает bypass cache. [[verify.json]] / [[backup-export.json]] / [[public-qa.json]].

Browser40/40: четыре слайда каждого товара на1440×1000 и390×844. Один активный/видимый слайд с загруженным изображением и верным alt; две стрелки, четыре точки, caption center/font-weight≥600; overflow нет. На всех10 видах Next/Previous/first&last dots прошли. Сохранены10 screenshots и proof. [[browser-qa.json]] / [[haiti-published-proof.png]].

WireGuard SSH vpsadmin@10.66.66.1 и sudo Docker доступны; сначала проверены сервер/docker ps, затем target WP/DB. Running,RestartCount0,StartedAt и ports before/after совпали: WP127.0.0.1:8083,DB без published ports. Контейнеры не перестраивались и не перезапускались; local runtime не менялся; secrets/.env не читались. [[runtime-before.txt]] / [[runtime-after.txt]].

## Откат

Guarded rollback-preview5/5 прошёл. Backup _shustrik_five_more_country_stl_slider_backup_20261007_ID; journal _shustrik_five_more_country_stl_slider_media_20261007_ID. Перед откатом: sudo -n docker exec shustrik-maps-wordpress-1 php /tmp/five-more-country-16774f0/release.php --rollback-preview; затем --rollback только при отсутствии drift. Восстанавливаются прежние Description/SEO; old/new media сохраняются. Rollback не выполнялся. Apply неидемпотентен; при неопределённом результате читать journals/backups, слепой повтор запрещён. [[rollback-preview.json]].

Партия5/5 завершена. P1 analytics/recovery/consent, индекс10.10, yellow/degraded сохранены. Рост позиций/продаж не заявляется. [[../STL Product Update Workflow]].

Source push дважды получил GitHub Internal Server Error; после сверки origin тот же commit16774f0 успешно отправлен через git push --no-thin. Публикация началась только после подтверждения GitHub0:0.
