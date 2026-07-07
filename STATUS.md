# STATUS — shustrik-maps.com SEO Project

Последнее обновление: 2026-07-07 (Шаг 2 завершён)

## Что это за проект
Сайт shustrik-maps.com продаёт 3D-модели и карты (STL для 3D-печати/CNC, OBJ/FBX/C4D для
визуализации, GeoTIFF/PSD/SVG для GIS/дизайна). Идёт работа над семантическим ядром,
аудитом каталога и оптимизацией карточек товаров/категорий для Google SEO.

## Структура сайта (реальная, по факту меню)
- **3D Models (OBJ/FBX/C4D)** — Solar System, World, Continents, Peninsulas, Islands,
  Countries, States of America, Canadian Provinces, Canyons & Parks, Cities, Buildings,
  Minecraft, Other/Art
- **3D Print/CNC (STL/STEP)** — Planets, Satellites (Moons), Continents, Countries, Islands,
  States of America, Other (incl. Jewelry & Art)
- **Fantasy Maps** — общая категория для обоих форматов (это само по себе проблема
  структуры, см. Issues ниже)
- **Maps (TIF/PSD/SVG)** — Satellite Maps, Night Satellite Map, Heightmaps/Raster DEM,
  Relief Maps, 3D Maps, Historical Maps, Outline Maps, Elevation Maps, Various Map Projections

## Сделано ✅

### Шаг 1 — аудит и семантическое ядро
- [x] Собран список из 517 товарных карточек (site-map-html, стр. 1-2)
- [x] Собрана точная структура из 30 категорий с реальными URL
- [x] Классификация каждой карточки по типу (STL/CNC, визуализация, спутник, ночной спутник,
      relief-legacy, без воды, elevation, историческая, outline, planet, fantasy, здания,
      minecraft, art/novelty) — см. `semantic-core/products_seo.csv`
- [x] Найдено 39 служебных/мусорных страниц (Prepayment-*, тестовая "Map") —
      см. `semantic-core/junk_pages.csv` — рекомендация: noindex + убрать из sitemap.xml
- [x] Найдено ~22 группы дублей/каннибализации (одна и та же страна+тип встречается 2 раза
      под разными URL) — см. `semantic-core/duplicates_issues.csv`
- [x] Для каждой из 517 карточек и 30 категорий сгенерированы: SEO Title, H1, Meta Description,
      Primary keyword, Secondary keywords, LSI keywords — см. `semantic-core/*.csv`
- [x] LSI-банк ключевых слов по каждому типу карточки — `lsi-keyword-bank.csv`

### Шаг 2 — архитектура сайта и меню
- [x] Диагностированы структурные проблемы:
      - категория "Fantasy Maps" — общий URL для веток 3D Models и CNC Models (путает
        пользователя и Google)
      - "3D Maps" (в ветке Maps) vs "3D Models" — похожие термины для разных сущностей,
        риск путаницы в поиске и перелинковке
      - нет отдельных категорий для гор/озёр/вулканов (только единичные карточки —
        Grand Canyon, Zion, Rocky Mountain, Appalachian Trail)
- [x] Спроектирована двухслойная архитектура:
      - **Слой 1 (без изменений)** — навигация по формату: 3D Models / CNC Models / Maps
      - **Слой 2 (новый)** — Geo Hub Pages: одна страница на гео-объект
        (`/countries/{country}/`, `/us-states/{state}/`, `/national-parks/{park}/` и т.д.),
        объединяющая все доступные форматы (STL/CNC, 3D-модель, спутниковая карта) —
        закрывает самый сильный поисковый запрос вида "Portugal terrain model" одной
        сильной страницей вместо 2-3 конкурирующих карточек
- [x] Предложена URL-схема geo-хабов:
      ```
      /countries/{country}/                  ← hub
      /countries/{country}/stl/
      /countries/{country}/3d-model/
      /countries/{country}/satellite-map/
      ```
      аналогично для us-states, canadian-provinces, national-parks, continents, islands,
      cities, mountains (новое), lakes (новое), volcanoes (новое)
- [x] Согласован порядок внедрения (см. Roadmap)

## В работе / известные ограничения ⚠️
- Geo-объект и keywords сгенерированы алгоритмически по названию карточки. ~6 карточек
  с нестандартными названиями требуют ручной проверки (тип = "Unclassified"/"other" в CSV).
- **Нет данных по частотности и сложности запросов** (нужен внешний источник — Ahrefs/Semrush/
  Keyword Planner). Следующий шаг — прогнать колонки primary_keyword/secondary_keywords через
  один из этих сервисов.
- Meta description не проверены посимвольно на всех 517 строках, только выборочно.
- Geo Hub Pages пока только спроектированы (URL-схема, порядок внедрения) — ни одна
  реальная страница ещё не создана на сайте.

## Следующие шаги (roadmap)
1. [ ] Прогнать ключевые слова через Ahrefs/Semrush — добавить колонки volume/difficulty
2. [ ] Принять решение по 22 группам дублей/каннибализации (merge / redirect / развести)
       и по 39 junk-страницам (noindex)
3. [ ] Развести категорию "Fantasy Maps" на два формата или явно показать оба варианта
       на одной странице
4. [ ] Создать Geo Hub Pages для топ-30 стран (наибольший трафик) — пилот перед
       масштабированием на весь каталог
5. [ ] Массово обновить Title/H1/Meta в реальных карточках WooCommerce/CMS
       (по данным из products_seo.csv)
6. [ ] Добавить новые категории: Mountains, Lakes, Volcanoes (сейчас нет ни одной карточки)
7. [ ] Расширить geo-хабы на us-states, canadian-provinces, national-parks, continents,
       islands, cities
8. [ ] Написать первые статьи блога по уровню 5 (информационные запросы) — see
       `semantic-core/categories.csv` для тем по каждой категории

## Как работать с этим репозиторием (для Claude / будущих сессий)
Начинай каждую сессию с чтения этого файла. Данные лежат в `semantic-core/*.csv` —
читай их через pandas/csv, а не пытайся пересчитывать с нуля. Обновляй раздел
"Сделано"/"В работе" и дату наверху этого файла в конце каждой сессии, и добавляй
запись в `audit-log.md` с кратким описанием того, что изменилось и почему.

