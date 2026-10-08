---
type: seo-live-qa
site_profile: shustrik-maps
project_id: shustrik-maps-seo
status: published-check-passed
created_at: 2026-10-08
sources: [manifest.json, preservation-qa.json, public-qa.json, browser-qa.json, deployment.json]
---

# Kiwi: исправление руки в первом слайде

Проверено 08.10.2026, 13:50 МСК. По замечанию владельца исправлены неестественные форма и положение указательного пальца. Использован native ImageGen в режиме редактирования исходной фотографии. Осмотрены полный PNG, экспорт JPEG и опубликованная карточка: пять пальцев, естественный хват, без вытянутого поперечного пальца. Сохранены круглый обод, ivory plastic, рельеф головы Kiwi, клюв влево, Union Jack, четыре звезды и тёплый фон. Визуальная сохранность формы не означает пиксельную идентичность.

Исходный файл сохранён как [[kiwi-hand-before-original.png]], новый — [[kiwi-hand-corrected-original.png]]. Полный prompt — [[prompt.txt]], осмотр — [[visual-review.json]]. Финальный RGB JPEG1500×1000: [[kiwi-medallion-hand-corrected-1500x1000.jpg]]. Опубликовано [Kiwi Medallion](https://shustrik-maps.com/product/new-zealand-medallion-kiwi-stl/).

Изменена только первая ссылка в images native Woodmart carousel: 22766→22774. Текущие четыре media: 22774,22767,22768,22769. Title/alt обозначают AI-generated concept и соответствуют сцене. Прежний media22766 и остальные три файла сохранены вместе с их title/alt/URL/SHA256. Все SEO-поля, H1, URL, основной текст, excerpt, характеристики, цены, downloads, верхняя галерея и полная metadata товара совпали с baseline. Content отличается только одним ID, все текстовые shortcode блоки дословно совпали. Hashes четырёх остальных товаров и общего HTML-блока9586 совпали. [[manifest.json]] / [[after.json]] / [[preservation-qa.json]].

GitHub-first: SSH origin/main, fetch, HEAD/upstream0:0, прежние dirty/untracked сохранены. Source c65c85a91b9f9c1cd9153c25b92026cfec2903cc committed/pushed и доставлен точным архивом SHA256 e7548911d04d285f6b233acab197a70248ac21ddb90dc7a9acba04c6bed954da (local/VPS совпал) в /tmp/kiwi-hand-fix-c65c85a. PHP lint и preview прошли. Новый guarded apply выполнен один раз; предыдущие release.php не запускались. Отдельные backup/journal защищают от повторной публикации и параллельного изменения.

Проверки: DB/media4/4 и guarded rollback-preview прошли. HTTP2/2 (обычный и query URL) проверил прежние SEO, H1, self-canonical, robots, Product schema, CTA, отсутствие raw shortcodes и корректную подпись. Все четыре media HTTP200/image/jpeg; WP подтвердил JPEG1500×1000/SHA/title/alt. Query сам по себе не доказывает bypass. Browser8/8: четыре слайда desktop1440×1000 и mobile390×844, Next/Previous/первая и последняя точки, одна видимая загруженная картинка, две стрелки, четыре точки, без переполнения. Autoplay=no/wrap=no сохранены в неизменном shortcode. Под слайдером только жирная центрованная AI-generated application concepts. [[verify.json]] / [[public-qa.json]] / [[browser-qa.json]] / [[kiwi-hand-published-proof.png]].

SSH WireGuard vpsadmin@10.66.66.1 / sudo Docker доступны. WP и DB running/restart0, StartedAt/ports before/after совпали: WP127.0.0.1:8083, DB без published ports. Контейнеры не перестраивались и не перезапускались; secrets/.env не читались. [[runtime-before.txt]] / [[runtime-after.txt]].

## Откат

Backup _shustrik_kiwi_hand_fix_backup_20261008_21381, journal _shustrik_kiwi_hand_fix_media_20261008_21381. Перед откатом повторить guard:

```sh
sudo -n docker exec shustrik-maps-wordpress-1 php /tmp/kiwi-hand-fix-c65c85a/release.php --rollback-preview
```

При отсутствии drift выполнить тот же source с --rollback: вернётся прежний первый слайд22766; новые и старые media сохраняются. Actual rollback не выполнялся. Для более раннего состояния сначала откатить эту правку, затем заново guarded preview/rollback Kiwi/Nautilus revision79f6673, и при необходимости initial466394c. Старые apply не повторять. [[backup-export.json]] / [[rollback-preview.json]].

P1 analytics/recovery/consent, индекс-контроль10.10, yellow/degraded сохранены. Семантика и SEO не менялись; новый замер спроса/позиций не заявляется. Основной отчёт партии: [[../Five Special STL Sliders 2026-10-08/Release Report]].
