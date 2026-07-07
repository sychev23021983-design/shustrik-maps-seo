# shustrik-maps-seo

SEO-аудит, семантическое ядро и рабочая база для продвижения shustrik-maps.com в Google.

- **STATUS.md** — текущее состояние проекта: что сделано, что дальше (читать первым)
- **CLAUDE.md** — инструкции для Claude Code, если вы подключите его к этому репозиторию
- **audit-log.md** — история решений и изменений
- **semantic-core/shustrik-maps_SEO_audit_and_core.xlsx** — РАБОЧИЙ ФАЙЛ. Всё в одном месте:
  категории, товарные карточки, SEO-поля, дубли/junk-страницы, LSI-банк, и отслеживание
  прогресса (колонка Applied?/Date Applied на листах Categories и Products_SEO).
- **site-menu-structure.md** — предложенная структура меню (Шаг 2)

## Как обновлять
1. Внесли изменения на сайте → отметьте `Applied? = Yes` + дату в xlsx (листы Categories /
   Products_SEO)
2. Перезапишите `semantic-core/shustrik-maps_SEO_audit_and_core.xlsx` этой же обновлённой
   версией
3. Обновите `STATUS.md` (дату и статус)
4. Добавьте запись в `audit-log.md`
5. `git add . && git commit -m "..." && git push`

## Важно про xlsx в git
Это бинарный формат — GitHub не покажет построчный diff, как для CSV. Версии всё равно
сохраняются, и файл открывается нормально в любой новой сессии — для отслеживания прогресса
через колонку Applied? этого достаточно.
