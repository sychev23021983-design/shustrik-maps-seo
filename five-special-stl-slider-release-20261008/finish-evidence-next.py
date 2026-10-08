from pathlib import Path
import json,subprocess
root=Path(__file__).parent
out=Path('J:/1. My Vault/90 Migration/shustrik-maps-seo/five-special-stl-slider-release-20261008')
for n in ['apply.json','verify.json','preview.json','rollback-preview.json','backup-export.json']:
 s=(root/n).read_text(encoding='utf-8-sig')
 try:r=json.loads(s)
 except json.JSONDecodeError:r=json.loads(next(x for x in s.splitlines() if x.startswith('{')))
 (out/n).write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
runtime=out/'Runtime Status snapshot.md'
s=runtime.read_text(encoding='utf-8');s=s.split('\n## ',1)[0]
runtime.write_text(s.rstrip()+'\n',encoding='utf-8')
assert not any(k in (out/'release.php').read_text() for k in ['_shustrik_five_next_country_','20046,20070,20078,20086,20095'])
print('Evidence JSON normalized; addressed runtime snapshot contains this release only; publication code unchanged')
