# Новое меню shustrik-maps.com — до уровня категорий

На основе аудита (Шаг 1) и архитектуры (Шаг 2). Изменения по сравнению с текущим меню
отмечены **← NEW** / **← RENAMED** / **← SPLIT**.

---

## 1. 3D MODELS (OBJ/FBX/C4D) — визуализация
```
3D Models
├── Solar System
├── World
├── Continents
├── Peninsulas
├── Islands
├── Countries
├── States of America
├── Canadian Provinces
├── Mountains                    ← NEW (сейчас нет вообще)
├── Lakes                        ← NEW (сейчас нет вообще)
├── Volcanoes                    ← NEW (сейчас нет вообще)
├── Canyons & National Parks
├── Cities
├── Buildings & Landmarks
├── Minecraft
└── Art & Novelty
```

## 2. 3D PRINT / CNC (STL / STEP)
```
3D Print / CNC
├── Planets
├── Satellites (Moons)
├── Continents
├── Countries
├── Islands
├── States of America
├── Mountains                    ← NEW
├── Lakes                        ← NEW
├── Volcanoes                    ← NEW
└── Jewelry & Novelty            ← RENAMED (было "Other" — непонятное название,
                                    внутри и так в основном кулоны/новелти)
```

## 3. FANTASY MAPS — было ОДНА категория на две ветки, стало ДВЕ
```
Fantasy Maps
├── Fantasy — 3D Models (визуализация: Middle Earth, Westeros...)   ← SPLIT
└── Fantasy — STL/CNC (печать/фрезеровка тех же карт)               ← SPLIT
```
Причина: сейчас `/product-category/fantasy-maps/` — общий URL для обеих веток,
Google и пользователь не могут понять, к какому формату относится страница.

## 4. MAPS (TIF / PSD / SVG)
```
Maps
├── Satellite Maps
├── Night Satellite Maps
├── Heightmaps / Raster DEM
├── Relief Maps
├── Rendered Terrain Images      ← RENAMED (было "3D Maps" — конфликтует по названию
                                    с веткой "3D Models", хотя это просто готовый рендер,
                                    а не 3D-файл)
├── Historical Maps
├── Outline Maps
├── Elevation Maps
└── World Map Projections
```

## 5. EXPLORE BY LOCATION — новый слой (Geo Hub)      ← NEW ВЕТКА ЦЕЛИКОМ
Отдельный пункт в шапке или в футере — это НЕ замена веток 1-4, а страницы-хабы,
которые собирают все форматы одного гео-объекта на одной странице (см. Шаг 2).
```
Explore by Location
├── Countries              (A–Z index → /countries/)
├── US States               (A–Z index → /us-states/)
├── Canadian Provinces       (A–Z index → /canadian-provinces/)
├── Continents               (→ /continents/)
├── Islands                  (→ /islands/)
├── Mountains                (→ /mountains/)              ← NEW
├── Lakes                    (→ /lakes/)                   ← NEW
├── Volcanoes                (→ /volcanoes/)               ← NEW
└── National Parks & Canyons (→ /national-parks/)
```
Каждый пункт — это страница-индекс (список всех объектов этого уровня), с которой
пользователь попадает на гео-хаб конкретного объекта (`/countries/portugal/`),
а уже оттуда — на нужный формат.

---

## Итог: 5 top-level пунктов меню вместо 3
1. 3D Models
2. 3D Print / CNC
3. Fantasy Maps *(теперь с явным под-выбором формата)*
4. Maps
5. Explore by Location *(новое — вход по географии, а не по формату)*

## Что физически нужно сделать в WooCommerce
- Создать 3 новые категории-родителя: Mountains, Lakes, Volcanoes (в обеих ветках 3D Models и CNC — итого 6 новых категорий)
- Переименовать категорию "Other" (CNC) → "Jewelry & Novelty"
- Переименовать категорию "3D Maps" (Maps) → "Rendered Terrain Images"
- Разделить "Fantasy Maps" на два дочерних пункта под соответствующими родителями
- Geo Hub — это новые страницы (не категории WooCommerce, а обычные страницы/CPT), создаются отдельным этапом (Шаг 4 по roadmap)
