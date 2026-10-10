"""Check candidate in a renamed CLI namespace; do not replace the installed MU file."""
from pathlib import Path
import base64
import hashlib
import json
import subprocess

root = Path(__file__).resolve().parent
candidate = (root / 'paid-guard-compatibility-preview.php').read_text(encoding='utf-8')
transformed = candidate.replace('Shustrik\\PurchasePaidGuard', 'Shustrik\\PurchasePaidGuardCompatPreview')
source = (root.parent / 'purchase-paid-guard/test-installed.php').read_text(encoding='utf-8-sig').replace('Shustrik\\PurchasePaidGuard', 'Shustrik\\PurchasePaidGuardCompatPreview')
fixture = (root.parent / 'purchase-lab/installed-fixture-2026-10-03.json').read_bytes()
source = source.replace("$fixture=json_decode(file_get_contents($fixture_path),true);", "$fixture=json_decode(base64_decode('" + base64.b64encode(fixture).decode() + "'),true);")
source = source.replace('    require_once $guard_file;', "    eval('?>'.base64_decode('" + base64.b64encode(transformed.encode()).decode() + "'));")
source = source.replace("hash_file('sha256',$guard_file)", "'" + hashlib.sha256(candidate.encode()).hexdigest() + "'")
run = subprocess.run(['ssh', '-o', 'BatchMode=yes', 'vpsadmin@10.66.66.1',
                      'sudo -n docker exec -i shustrik-maps-wordpress-1 php'],
                     input=source, text=True, capture_output=True, timeout=60)
if run.returncode:
    raise SystemExit(run.stderr + run.stdout)
result = json.loads(run.stdout)
assert result['assertion_failures'] == 0 and result['actual_orders_saved'] == 0
(root / 'guard-compatibility-results-2026-10-10.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps({k: result[k] for k in ['checks_passed', 'assertion_failures', 'actual_orders_saved', 'real_ga4_requests', 'guard_sha256']}))
