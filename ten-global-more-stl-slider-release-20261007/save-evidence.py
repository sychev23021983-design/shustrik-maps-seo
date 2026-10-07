from pathlib import Path
import json,shutil
root=Path(__file__).parent
repo=Path('J:/1. My Vault/90 Migration/shustrik-maps-seo/ten-global-more-stl-slider-release-20261007')
for n in ['public-qa.json','preservation-qa.json','browser-qa.json','deployment.json','uploaded-media.json','Release Report.md','eritrea-published-proof.png','browser-check-functions.js','runtime-before.txt','runtime-after.txt']:
    shutil.copy2(root/n,repo/n)
for n in ['apply.json','verify.json','rollback-preview.json','backup-export.json','after.json']:
    raw=(root/n).read_text(encoding='utf-8-sig')
    try:d=json.loads(raw)
    except json.JSONDecodeError:d=json.loads(next(x for x in raw.splitlines() if x.startswith('{')))
    (repo/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for p in root.glob('*-controls.json'):
    shutil.copy2(p,repo/p.name)
assert len(list(root.glob('*-controls.json')))==20
manifest=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
assert all((root/(r['slug']+'-'+mode+'-qa.json')).exists() for r in manifest['rows'] for mode in ['desktop','mobile'])
print('Verification evidence copied; original CLI stdout retained in vault')
