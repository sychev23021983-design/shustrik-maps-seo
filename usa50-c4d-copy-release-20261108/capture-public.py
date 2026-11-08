from pathlib import Path
import runpy,json,concurrent.futures
root=Path(__file__).resolve().parent
fetch=runpy.run_path(str(root/'public-dom.py'))['fetch']
urls=['https://shustrik-maps.com/product/50-united-states-of-america-3d-model/','https://shustrik-maps.com/product/complete-usa-50-states-topographic-map-3d-model-for-3d-printing-cnc-carving/','https://shustrik-maps.com/product/usa-map-3d-model/']
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool: rows=list(pool.map(fetch,urls))
(root/'public-baseline.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:rows[0][k] for k in ['title','meta_description','h1','summary_text','description_text','description_links']},ensure_ascii=True))
