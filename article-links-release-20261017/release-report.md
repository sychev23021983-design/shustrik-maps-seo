---
type: verification-report
project_id: shustrik-maps-seo
site_profile: shustrik-maps
status: published-checked
last_reviewed: 2026-10-17
published_at: 2026-10-17 17:46:50 Europe/Moscow
source_commit: a0f0c6fa80cb77be0bd6a4d142aba4cdd57ec158
next_action: "Сохранить baseline; оценить GSC после накопления данных, остальные предложения не публиковать без решения владельца"
---

# Четыре ссылки в статьях и исправление OBJ

По прямому разрешению владельца опубликованы ровно L01/L03/L04/L05 и согласованная замена OBJ. Публикация выполнена один раз 17.10.2026 в 17:46:50 МСК. Остальные пять предложений из плана не входили в выпуск.

| Статья | Что опубликовано |
|---|---|
| [STL](https://shustrik-maps.com/what-is-an-stl-file-explaining-the-stl-format/) — post14594 | После 3D PRINTING AN STL FILE добавлен абзац с terrain STL collection → CNC Models |
| [OBJ](https://shustrik-maps.com/understanding-the-obj-file-format-a-simple-explanation/) — post14581 | В конце USAGE IN 3D GRAPHICS APPLICATIONS добавлен один абзац с USA terrain model и C4D-to-OBJ terrain workflow |
| [C4D→OBJ](https://shustrik-maps.com/how-to-convert-a-model-from-c4d-to-obj/) — post15849 | После введения добавлен пример USA terrain model with OBJ LOD variants |

В ADVANTAGES OF THE OBJ FILE FORMAT заменён согласованный диапазон, начинающийся In addition to compatibility и заканчивающийся OBJ is a fitting file format. Новая редакция:

> Wavefront OBJ is a text-based geometry format. Material definitions are commonly stored in an associated MTL file, with texture images supplied separately.

Последующее существующее предложение о FBX, которое не входило в согласованную замену, сохранено вместе с оформлением цитаты. Остальная статья не редактировалась и не объявляется полностью проверенной на техническую корректность. [Фактический diff](content.diff), [точный manifest](manifest.json).

## Проверка результата

- CMS verify: 3/3 точных content hashes; остальные поля постов, post metadata и taxonomy совпадают с baseline. Из служебных дат обновлены только post_modified/post_modified_gmt. Существующие shortcode tokens и медиассылки сохранены.
- Публичный HTML: 3 статьи и 2 дополнительных назначения — HTTP200, self-canonical, index/follow, по одному H1. Все 4 href и анкоры найдены. Исходные title/meta/H1/robots/canonical и media URLs совпадают с сегодняшним baseline; old binary claim отсутствует, новая редакция присутствует.
- Chrome: выполнены все 4 перехода, целевые URL совпали. Визуально проверены вставки в трёх статьях на текущем desktop viewport; сохранены скриншоты. Отдельная mobile viewport проверка не выполнялась. Ссылки находятся в согласованных местах.
- SSH WireGuard и sudo Docker доступны. WP/DB running, restarts0, StartedAt и port bindings не изменились. Старт WP 28.08.2026 05:54:09 UTC, DB 05:54:08 UTC. Build/restart не требовались для изменения CMS.
- Заказы/платежи и requests indexing/removal не создавались. Browser-переходы на товарные страницы не объявляются проверкой purchase.

[CMS verify](verify.json), [публичная проверка](public-qa.json), [браузерная проверка](browser-qa.json), [runtime after](runtime-after.json).

## Источник и откат

GitHub-first: до изменений fetch/main/upstream0:0; шесть прежних modified files и untracked сохранены. Source **a0f0c6fa80cb77be0bd6a4d142aba4cdd57ec158** committed/pushed, в external target https://shustrik-maps.com доставлен точным git archive. Локальный и серверный archive SHA256 совпали: 84e4ed3db14c1551302f73c039bc5fd21063be76dc24362737c55dd8f9fe1a69. PHP lint и preview прошли до apply. Серверный source: `/tmp/article-links-a0f0c6fa80cb` внутри shustrik-maps-wordpress-1.

Резервная копия трёх исходных текстов в WP option `_shustrik_article_links_backup_20261017`; source baseline также хранится в репозитории. Rollback-preview прошёл после публикации. Guarded rollback из repo_path:

```powershell
python article-links-release-20261017/deliver.py rollback
```

Откат откажется затирать новые изменения content или защищённых полей. Он восстанавливает исходные тексты, а modification timestamps отражают время отката. Откат не запускался. Evidence commit публикуется отдельно от source, без повторного apply.

## Измерение и состояние проекта

Срез 17.09–14.10 — baseline до этого выпуска. Он не является чистой оценкой изменений категорий 05–12 октября. Данные после 17.10 пока не накоплены; рост трафика/продаж не заявлен. Новое измерительное напоминание не создавалось. Плановый индекс-контроль 13 служебных URL 24.10 в 10:00 МСК сохранён.

Статус active/high/yellow/degraded и P1 consent/recovery/analytics сохранены; HTTP200 не снимает эти риски.

## Скриншоты

![OBJ ссылки и техническая корректировка](obj-browser.jpg)

![Пример USA в C4D OBJ](c4d-browser.jpg)

![STL ссылка на каталог](stl-browser.jpg)
