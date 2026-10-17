---
type: verification-report
project_id: shustrik-maps-seo
site_profile: shustrik-maps
status: published-checked
last_reviewed: 2026-10-17
published_at: 2026-10-17 18:00:01 Europe/Moscow
source_commit: b4547ac01329e6cdf54ff9c91f96e707ba66cb90
next_action: "Накопить сопоставимые данные GSC после двух выпусков; план перелинковки 9 из 9 закрыт"
---

# Оставшиеся пять предложений по перелинковке

По прямому поручению владельца опубликованы L02/L06/L07/L08/L09: три новые контекстные ссылки и две замены анкоров на четырёх существующих страницах. Apply выполнен один раз 17.10.2026 в 18:00:01 МСК. **План из девяти предложений выполнен полностью:** семь новых ссылок и два уточнённых анкора, включая предыдущий выпуск.

| Пункт | Страница | Изменение |
|---|---|---|
| L02 | [FBX](https://shustrik-maps.com/understanding-the-fbx-file-format-a-simple-explanation/) — post14596 | В конце Computer Graphics добавлен абзац со ссылкой 3D terrain model catalog → 3D Models |
| L06 и L07 | [C4D и STL](https://shustrik-maps.com/the-difference-between-c4d-and-stl-models/) — post15631 | После первого абзаца один общий абзац: 3D terrain models → 3D Models и terrain STL collection → CNC Models |
| L08 | [Проекции](https://shustrik-maps.com/3d-models-and-maps-in-various-map-projections/) — page20707 | У существующего href на цифровую AuthaGraph заменён Map на AuthaGraph world map image files (TIF/PSD); соседний 3D model сохранён |
| L09 | [Moon](https://shustrik-maps.com/product/moon-3d-model/) — product16110 | Только title существующей кнопки: Earth 3D model → Earth terrain model without water. href, link attributes, стиль, BG и соседняя Moon STL сохранены |

Точные вставки и замены: [manifest](manifest.json), [diff](content.diff). Прочие тексты и исходные технические/маркетинговые утверждения этих страниц не переписывались и не объявляются полностью фактчекингованными.

## Проверки

- CMS: четыре точных content hashes совпали; post types/URLs/status/title/excerpt/meta/taxonomy сохранены. Product metadata, цены, download-настройки и media refs защищены hash-проверкой. Обновлены только content и штатные modification timestamps.
- Ранее опубликованные post14594/14581/15849 защищены отдельными fingerprints: четыре ссылки и исправление OBJ не изменились.
- Публичные обычные URL: HTTP11/11=200, self-canonical, index/follow, один H1. Проверены пять точных анкоров и href. Title/meta/H1/robots/canonical и авторские media сохранены; наборы schema types совпали, полной schema validation не заявляем.
- У WooCommerce блок Related products динамически меняет подборку. Публичное сравнение product media относится к gallery/Description, а не случайным related cards. Изменения подборки не выдаются за изменение медиа товара. Локальный QA helper уточнён в evidence; CMS повторно не применялся.
- Первые HTTP-ответы на части URL вернули X-Page-Cache: STALE. Ответ с диагностическим query показывал новый контент; затем обычные URL после фонового обновления прошли проверки. Global purge, изменение конфигурации cache, повторный apply и restart не выполнялись.
- Chrome: все пять переходов завершились на ожидаемых URL. Визуально проверены четыре источника на текущем desktop viewport. Для длинных анкоров Moon и AuthaGraph дополнительно проверен экран 390×844; текст помещается, viewport затем сброшен. Для L09 окончательная проверка дождалась фактического завершения навигации, ранний незавершённый snapshot не засчитывался как результат.
- SSH WireGuard/sudoDocker доступны. WP/DB running, restarts0, StartedAt28.08 и port bindings unchanged. Build/restart не требовались для CMS-пакета.

[CMS verify](verify.json), [public QA](public-qa.json), [browser QA](browser-qa.json), [runtime after](runtime-after.json).

## GitHub и откат

Source **b4547ac01329e6cdf54ff9c91f96e707ba66cb90** committed/pushed/main и доставлен точным git archive в external target https://shustrik-maps.com. Archive SHA256 локально и на VPS: `2387054d63c53da5eff4705dc3bbaf804cff0a487dc9b1b746557ecfecd9740b`. Серверный source `/tmp/remaining-links-b4547ac01329` внутри shustrik-maps-wordpress-1; PHP lint и preview прошли до apply. GitHub-first fetch выполнен; прежние шесть modified files и untracked не затронуты.

Backup option `_shustrik_remaining_links_backup_20261017` содержит четыре исходных content. Guarded rollback-preview прошёл. Команда из repo_path:

```powershell
python remaining-links-release-20261017/deliver.py rollback
```

Откат откажется перезаписывать новые изменения контента, метаданных или предыдущего выпуска. Он откатывает только эту пятёрку предложений; первый пакет четырёх ссылок/OBJ correction сохраняется. Modification timestamps отражают время отката. Откат не запускался. Evidence commit добавляется отдельно без повторного apply.

## Следующий шаг

Дать накопиться данным после 17 октября. Сравнивать согласованные query/page/US/device срезы и клики; связать с продажами только после подтверждённой полноты purchase/consent. Результат выпуска не объявляется ростом трафика или продаж. Новая автоматизация не создавалась; индекс-контроль13 URL 24.10 в10:00 МСК сохранён. Active/high/yellow/degraded и P1analytics/consent/recovery не менялись. Заказы, платежи и запросы индексирования/удаления не создавались.

## Скриншоты

![FBX ссылка в конце Computer Graphics](fbx-desktop.jpg)

![Ссылки из C4D STL](difference-desktop.jpg)

![AuthaGraph desktop](projections-desktop.jpg)

![AuthaGraph mobile](projections-mobile.jpg)

![Moon desktop](moon-desktop.jpg)

![Moon mobile](moon-mobile.jpg)
