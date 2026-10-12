---
type: seo-live-qa
status: draft
publication_state: published-http-qa-passed
site_profile: shustrik-maps
url: https://shustrik-maps.com/product-category/3d-models/continents-3d-models/africa/
source_commit: 75f60bcafd6fb25bc4cdfeb1ed861b556f7e6ad2
reviewed: 2026-10-12
published_at_utc: 2026-10-12T16:33:44+00:00
visual_qa: not-completed-tool-stopped
---

# Africa Digital — описание и цифровые примеры

По запросу владельца обновлён существующий dedicated block15343 для term163. Добавлены H1, три абзаца по фактам двух карточек, четыре связанных примера и видимое указание AI. Все исходные подборки стран сохранены точной строкой shortcode для блоков15306/15321/15314/15296/15276. Категория содержит две модели; правило single-model text-only действует для следующих категорий.

- Africa — website banner — https://shustrik-maps.com/product/3d-model-of-africa-relief/
- Africa — relief illustration — https://shustrik-maps.com/product/africa-3d-model-terrain/
- Africa — animation frame — https://shustrik-maps.com/product/africa-3d-model-terrain/
- Africa — presentation graphic — https://shustrik-maps.com/product/3d-model-of-africa-relief/

Две карточки HTTP200: обе C4D, Mercator, открытое основание, OBJ/FBX export по запросу. Первая содержит шесть типов текстур, вторая multi-layer TIF. Mainland-only и Madagascar-containing варианты сверены каждый с собственным product reference. Исходные product images просмотрены перед built-in imagegen. Четыре новых изображения визуально сверены с исходниками; точные prompts и пути в image-prompts.json. Это иллюстративные цифровые концепции, кадр анимации — статичное изображение. Готовые сцены/анимации не обещаны. PNG и исходники сохранены, PIL использован только для RGB/WebP88 конвертации 1536×1024.

| Example | Attachment | Published media |
|---|---|---|
| website-banner | 22884 | https://shustrik-maps.com/wp-content/uploads/2023/09/africa-digital-website-banner-20261012.webp |
| relief-illustration | 22885 | https://shustrik-maps.com/wp-content/uploads/2023/09/africa-digital-relief-illustration-20261012.webp |
| animation-frame | 22886 | https://shustrik-maps.com/wp-content/uploads/2023/09/africa-digital-animation-frame-20261012.webp |
| presentation-graphic | 22887 | https://shustrik-maps.com/wp-content/uploads/2023/09/africa-digital-presentation-graphic-20261012.webp |

GitHub-first: fetch, SSH remote, main, upstream0:0. Шесть посторонних modified files и untracked сохранены. Source **75f60bcafd6fb25bc4cdfeb1ed861b556f7e6ad2** отправлен до CMS изменения. Archive SHA256 **333f0ca90b5b0f515533edff0dee6ac6e82354619ba9e357326159acba0f0f38** совпадает на VPS. External target https://shustrik-maps.com через WireGuard/vpsadmin@10.66.66.1/sudoDocker; источник `/tmp/africa-digital-75f60bcafd6f`. PHP lint/preview прошли; apply один раз **2026-10-12T16:33:44+00:00**. Backup/journal созданы до импорта; conditionalSQL content transaction с before/protected guards. Новый блок и placement не создавались. Installed contentSHA256 **69120b2ed9302836ef8712185706b072608b8173a0eae72a818ef2bbcf7b4e54**.

Защищены term fields/meta/description, identity/meta блока15343, два товара кроме generated CSS cache, 48 prior posts (44CMS/три menu items/один Asia image attachment), terms63/67/68/159/160/161/162. Exact html_block parser подтверждает только term163.description reference, остальные term/post/meta usage отсутствуют. Предыдущие категории, пять retained country collection blocks и исходные media сохранены.

Public HTTP QA: категория, home/cart и emptycheckout→cart200; четыре endpoint200, четыре изображения200 с alt; metadata/canonical/robots/schema types/cards/prices/pagination и все 62 прежние h4 headings сохранены. Один H1, четыре изображения, восемь article anchors и AI disclosure подтверждены. Verify и rollback-preview прошли; реальный rollback не выполнялся. Static CSS подтверждает две desktop колонки и одну до600px. **Native visual desktop/mobile QA не завершена:** Нативная browser QA для этой публикации не выполнялась; предыдущий инструмент проверки остановился из-за невозможности надёжно определить URL. HTTP/CMS проверки не являются доказательством визуальной mobile QA. Скриншот страницы не создан.

SSH/sudoDocker доступны; WP/DB running, restarts0 и StartedAt2026-08-28 unchanged. External CMS без build/restart/config изменений. Orders/payments не выполнялись. P1consent/recovery/analytics, yellow/degraded/high и paidguard03fc676 сохранены. SEO uplift/index changes не оценивались.

Rollback backup `_shustrik_africa_digital_backup_20261012`: в WP container `php -d memory_limit=512M /tmp/africa-digital-75f60bcafd6f/release.php --rollback` условно восстанавливает исходный contentSHA256 **875cf159fead28da78a4303a293143fbf9291a55d5100ad2a11b55b038af73a5**, сохраняя block/reference/media. Затем выполнить publicQA.

Незавершённая проверка: визуально открыть Africa на desktop и телефоне, проверить четыре изображения и отсутствие horizontal overflow.
