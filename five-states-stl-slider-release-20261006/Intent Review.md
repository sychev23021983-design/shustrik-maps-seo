# Проверка товарного intent — Google / English / USA

06.10.2026 проверены существующее ядро, текущие CMS-карточки и публичные поисковые результаты. Это редакционная проверка соответствия формата и географии, не US-local rank check и не измерение спроса. У Florida существующий кластер keep=0: число retained строк не является нулевой частотностью. Для Colorado/Utah/Montana/Nevada STL-кластеры в текущем ядре отсутствуют. Новые группы запросов записаны в semantic-review.json с frequency/rank=null; исходное ядро и его измеренные показатели сохраняются.

- Colorado: [собственная STL-карточка](https://shustrik-maps.com/product/state-of-colorado-stl-model/) и [листинг автора модели на Cults](https://cults3d.com/en/3d-model/architecture/colorado-topographic-map-3d-model-for-3d-printing-cnc-carving) используют topographic map / STL / 3D printing / CNC.
- Florida: [листинг STL на Cults](https://cults3d.com/en/3d-model/architecture/topographic-map-of-florida-3d-terrain) подтверждает digital STL intent; free results и vector/elevation-map queries отделены.
- Utah: [товар Printed Canyon](https://www.printedcanyon.com/places/utah) предлагает 3D terrain file formats рядом с постером, поэтому meta нашей STL-карточки явно указывает digital file. Это не доказательство совместимости чужих форматов с нашим товаром.
- Montana: [листинг автора на Cults](https://cults3d.com/en/3d-model/architecture/montana-topographic-map-3d-model-for-3d-printing-cnc-carving) использует state terrain / STL / printing / CNC.
- Nevada: [листинг автора на Cults](https://cults3d.com/es/modelo-3d/arquitectura/nevada-topographic-map-3d-model-for-3d-printing-cnc-carving) описывает state terrain STL. Обычные топографические PDF/DRG относятся к другому формату и исключены.

Основная гипотеза для каждого SKU: Place topographic map STL. Supporting: Place terrain STL; Place relief map STL; Place map 3D print; Place CNC terrain model. Не считать пять фраз независимым спросом и не суммировать частотности. Публикация поручена владельцем; она не подтверждает рост продаж.

Utah excerpt заявляет Base: Open. Meta отражает возможную подготовку; подложки и опоры на AI-концептах — отдельные работы. Остальные четыре excerpt заявляют Closed. Геометрия выдаваемых архивов этим выпуском не проверяется.
