"""CLI-only test against installed WP; all rows are temporary and orders synthetic."""
from pathlib import Path
import base64
import json
import subprocess

root = Path(__file__).resolve().parent
core = base64.b64encode((root / 'wp-adapter.php').read_bytes()).decode()
test = base64.b64encode((root / 'test-wp.php').read_bytes()).decode()
source = "<?php ob_start(); require '/var/www/html/wp-load.php'; ob_end_clean(); eval('?>'.base64_decode('" + core + "')); eval('?>'.base64_decode('" + test + "'));"
run = subprocess.run(['ssh', '-o', 'BatchMode=yes', 'vpsadmin@10.66.66.1',
                      'sudo -n docker exec -i shustrik-maps-wordpress-1 php'],
                     input=source, text=True, capture_output=True, timeout=60)
if run.returncode:
    raise SystemExit(run.stderr + run.stdout)
result = json.loads(run.stdout)
assert result['passed'] and result['actual_order_writes'] == 0
(root / 'wp-results-2026-10-10.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps(result, indent=2))
