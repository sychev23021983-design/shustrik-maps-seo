"""Read-only installed MU QA, with synthetic lookup/inline sinks in one CLI request."""
import base64
import json
from pathlib import Path
import subprocess

root=Path(__file__).resolve().parent
repo=root.parent
source=(repo/'purchase-paid-guard/test-installed.php').read_text(encoding='utf-8-sig')
source=source.replace("$guard_file=getenv('SHUSTRIK_GUARD_TEST_FILE')?:__DIR__.'/shustrik-purchase-paid-guard.php';",
                      "$guard_file=WPMU_PLUGIN_DIR.'/shustrik-purchase-paid-guard.php';")
fixture=base64.b64encode((repo/'purchase-lab/installed-fixture-2026-10-03.json').read_bytes()).decode()
source=source.replace("$fixture=json_decode(file_get_contents($fixture_path),true);",
                      "$fixture=json_decode(base64_decode('"+fixture+"'),true);")
probe=r'''
    $wp_filter['woocommerce_thankyou']=clone $base;
    $slots=array_keys($wp_filter['woocommerce_thankyou']->callbacks[10]);
    verify('installed environment accepts supported guest receipt',\Shustrik\PurchasePaidGuard\environment_ready());
    \Shustrik\PurchasePaidGuard\install();
    verify('fresh request installs wrapper',($GLOBALS['shustrik_purchase_paid_guard_state']??'')==='wrapped');
    verify('fresh installation preserves callback slots',$slots===array_keys($wp_filter['woocommerce_thankyou']->callbacks[10]));
    $wrapped=$wp_filter['woocommerce_thankyou']->callbacks;
    \Shustrik\PurchasePaidGuard\install();
    verify('second install idempotent',$wrapped===$wp_filter['woocommerce_thankyou']->callbacks);
'''
source=source.replace('    $fixture_path=',probe+'    $fixture_path=',1)
source=source.replace("'utc'=>gmdate('c'),'checks_passed'", "'fresh_install_state'=>($GLOBALS['shustrik_purchase_paid_guard_state']??null),'utc'=>gmdate('c'),'checks_passed'",1)
run=subprocess.run(['ssh','-o','BatchMode=yes','vpsadmin@10.66.66.1',
                    'sudo -n docker exec -i shustrik-maps-wordpress-1 php'],
                   input=source,capture_output=True,text=True,timeout=60)
if run.returncode:raise SystemExit(run.stderr+run.stdout)
result=json.loads(run.stdout)
assert result['guard_sha256']=='6a9cfc06e1a93060777df0f8baef7aa54c13908486695a4b6ed5cf8d817b978d'
assert result['assertion_failures']==0 and result['fresh_install_state']=='wrapped'
(root/'installed-qa.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({k:result[k] for k in ['utc','checks_passed','assertion_failures','fresh_install_state','guard_sha256','actual_orders_saved','real_ga4_requests']}))
