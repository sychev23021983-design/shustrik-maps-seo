---
type: seo-live-qa
site_profile: shustrik-maps
url: https://shustrik-maps.com/product-category/3d-models/continents-3d-models/asia/
status: draft
publication_state: published-http-qa-passed
created_at: 2026-10-12
sources:
  - public-qa.json
  - verify.json
  - runtime-after.json
next_action: "Visual desktop/mobile review when browser inspection is available"
source_commit: 55bb859a445613d4fc63514e90e7d26e4cb69d3f
published_at_utc: 2026-10-12T16:15:30+00:00
---

# Asia — оптимизация текста одной модели

Владелец запросил следующую категорию и ранее указал: для одной модели только оптимизация текста, без новых рендеров. Подтверждён один товар Asia Terrain 3D Model, карточка HTTP200. Изменены только существующий H1, subtitle и тело одного woodmart_text_block в dedicated block15264/term162. Новый H1: Asia 3D Model for Renders and Animation. Три абзаца объясняют цифровое применение, C4D/OBJ-FBX по запросу, Equidistant Conic/open base, шесть типов карт и CTA на продукт/Continents/root. Нет обещаний универсальной совместимости, included architecture, лицензии, точности или готовых сцен.

Сохранена исходная структура shortcodes; PHP guard сравнивает весь source после маскирования разрешённых title/subtitle/text slots. Исходное изображение15418 и пять region blocks15244/15238/15221/15218/15200 сохранены. Новых изображений, media imports, блоков и placement изменений нет. Все 55 main images URL/alt/dimensions, 57 h4 headings и 97 существующих main link entries совпали с baseline. Новые три inline links проверены HTTP200.

GitHub-first fetch/SSH remote/main/upstream0:0. Шесть посторонних modified files и прочие untracked сохранены. Source **55bb859a445613d4fc63514e90e7d26e4cb69d3f** pushed до CMS изменения; exact archive SHA256 **4d33ad23d678a93d8eff428c00de7ac2b10284dbf22108c573e35951e532a88e** подтверждён на VPS. External target https://shustrik-maps.com через WireGuard vpsadmin@10.66.66.1/sudoDocker; источник `/tmp/asia-text-55bb859a4456`. PHP lint/preview прошли; apply один раз **2026-10-12T16:15:30+00:00**. Backup и пустой journal перед conditionalSQL content transaction. Installed contentSHA256 **e541c78c61f90735275608d5f7e2876519d27184578735b75f867aaaf065ac27**. Verify/rollback-preview прошли; actual rollback не выполнялся.

Protected: term fields/meta/description, block identity/meta, один product state кроме generated CSS cache,42 prior posts (38CMS,три menu items, retained image attachment) и terms63/67/68/159/160/161. Dedicated15264 referenced только term162.description, иных term/post/meta usage нет. Europe и все прежние категории защищены.

| Проверка | Результат | Evidence |
|---|---|---|
| Category/home/cart/empty checkout | HTTP200, checkout→cart | public-qa.json |
| H1/copy | Один H1, точные три параграфа | public-qa.json |
| Catalogue/prices | Один прежний товар без изменений | public-qa.json / verify.json |
| Title/meta/canonical/robots/schema types | Сохранены | public-qa.json |
| Existing images/region headings/links | Полное совпадение baseline | public-qa.json |
| Inline links | Три endpoint HTTP200 | public-qa.json |
| CMS/protected state/rollback preview | Passed | verify.json / rollback-preview.json |
| Runtime | SSH/sudoDocker available, WP/DB running, restarts0, StartedAt unchanged | runtime-after.json |
| Native desktop/mobile visual QA | Не выполнялась, browser inspection была недоступна в предыдущем проходе; никаких неподтверждённых визуальных результатов | Scope limitation |

Нативная визуальная проверка и полная schema validation не завершены, поэтому полный SEO QA status остаётся draft; publication_state фиксирует отдельный фактический HTTP/CMS слой. Layout/CSS не менялись; эта узкая текстовая публикация проверена структурно и через публичный HTML. Europe visual QA остаётся отдельным незавершённым действием. SEO uplift/index changes не измерялись. Orders/payments не выполнялись. P1consent/recovery/analytics/yellow/degraded/high/paidguard03fc676 сохранены. External CMS без build/restart/config changes.

Rollback backup `_shustrik_asia_text_backup_20261012`: в WP container `php -d memory_limit=512M /tmp/asia-text-55bb859a4456/release.php --rollback` условно восстанавливает исходный contentSHA256 **bcf1b63fef2c6d4619b3137f36fad6af9f8645cce59686dda5119177a7233ba3**, сохраняя block/reference/media. Затем public QA.
