import pathlib,hashlib,json,subprocess,sys
ROOT=pathlib.Path(__file__).parent
TARGET=pathlib.Path('/opt/vps/shustrik-maps/wordpress/wp-content/mu-plugins/shustrik-pinterest-async.php')
EXPECTED='185bdec33fee3c46691d44a766e47f80f90453de4b8b1c586dbb76f70053bb44'
CONTAINER='shustrik-maps-wordpress-1'
STATE=ROOT/'backup.json'
SERVICE='shustrik-pinterest-views.service'
TIMER='shustrik-pinterest-views.timer'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(*a):subprocess.run(a,check=True)
def output(*a):return subprocess.check_output(a,text=True)
def admin(*args):return output('docker','exec',CONTAINER,'php','/tmp/shustrik-pinterest-cart-release/admin.php',*args)
def install_helpers():
 run('docker','cp',str(ROOT)+'/.',CONTAINER+':/tmp/shustrik-pinterest-cart-release')
def healthy():
 if output('systemctl','is-active',TIMER).strip()!='active':raise RuntimeError('Consumer timer unavailable')
 if output('systemctl','show',SERVICE,'-p','Result','--value').strip()!='success':raise RuntimeError('Consumer result not success')
def pending(a):return sum(int(r['count']) for r in a['queue_status'] if r['status'] in ['pending','in-progress'])
def write_atomic(data):
 temp=TARGET.with_suffix('.php.cart-tmp')
 if temp.exists():raise RuntimeError('Temporary target exists')
 temp.write_bytes(data);temp.chmod(0o644);temp.replace(TARGET)
mode=sys.argv[1] if len(sys.argv)>1 else '--preview'
if mode not in ['--preview','--apply','--enable','--rollback','--restore-old']:raise RuntimeError('Unknown mode')
install_helpers()
if mode in ['--enable','--rollback','--restore-old']:
 saved=json.loads(STATE.read_text())
 if sha(TARGET)!=saved['installed_sha256']:raise RuntimeError('Installed source drift')
 if mode=='--enable':
  healthy();a=json.loads(admin())
  if a['enqueue_disabled']:raise RuntimeError('View admission disabled')
  print(admin('--cart-enable'))
 elif mode=='--rollback':
  print(admin('--cart-disable'));print('New cart events synchronous; keep current consumer until queue drains')
 else:
  a=json.loads(admin())
  if a['cart_enabled'] or a['payloads'] or pending(a):raise RuntimeError('Disable cart and drain all payloads/actions before old consumer')
  old=ROOT/'previous-plugin.php'
  if sha(old)!=saved['prior_sha256']:raise RuntimeError('Backup drift')
  write_atomic(old.read_bytes())
  if not saved['prior_flag_exists']:print(admin('--cart-restore-absent'))
  print('Prior own plugin restored after verified drainage')
 print(admin());sys.exit(0)
if STATE.exists() or sha(TARGET)!=EXPECTED:raise RuntimeError('Prior source/backup guard')
healthy()
for name in ['shustrik-pinterest-async.php','test.php','preflight.php','admin.php']:
 run('docker','exec',CONTAINER,'php','-l','/tmp/shustrik-pinterest-cart-release/'+name)
run('docker','exec',CONTAINER,'php','/tmp/shustrik-pinterest-cart-release/test.php')
run('docker','exec',CONTAINER,'php','/tmp/shustrik-pinterest-cart-release/preflight.php')
a=json.loads(admin())
if a['cart_enabled'] or a['enqueue_disabled']:raise RuntimeError('Unexpected prior admission state')
print(json.dumps({'mode':mode,'prior_sha256':EXPECTED,'installed_sha256':sha(ROOT/'shustrik-pinterest-async.php'),'prior_flag_exists':a['cart_flag_exists']}))
if mode=='--preview':sys.exit(0)
(ROOT/'previous-plugin.php').write_bytes(TARGET.read_bytes())
STATE.write_text(json.dumps({'prior_sha256':EXPECTED,'installed_sha256':sha(ROOT/'shustrik-pinterest-async.php'),'prior_flag_exists':a['cart_flag_exists'],'prior_cart_enabled':False}))
STATE.chmod(0o600)
write_atomic((ROOT/'shustrik-pinterest-async.php').read_bytes())
if sha(TARGET)!=sha(ROOT/'shustrik-pinterest-async.php'):raise RuntimeError('Installation hash mismatch')
print('Own plugin installed with cart flag OFF; consumer and existing view queue unchanged')
print(admin())
