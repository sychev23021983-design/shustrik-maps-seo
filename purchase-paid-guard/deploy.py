import argparse,hashlib,json,pathlib,subprocess
HERE=pathlib.Path(__file__).resolve().parent
TARGET=pathlib.Path('/opt/vps/shustrik-maps/wordpress/wp-content/mu-plugins')
BACKUP=pathlib.Path('/root/shustrik-paid-guard-20261003')
NAME='shustrik-purchase-paid-guard.php'
HASH='666940e505df36627c2c556f680f0a0e3e71a7515c68e994b3f8c6a460b2fbe6'
CONTAINER='shustrik-maps-wordpress-1'
def run(*args):return subprocess.run(args,check=True,capture_output=True,text=True).stdout
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def admin(mode):
    run('docker','cp',str(BACKUP/'admin.php'),CONTAINER+':/tmp/shustrik-paid-guard-admin.php')
    return json.loads(run('docker','exec',CONTAINER,'php','/tmp/shustrik-paid-guard-admin.php',mode))
parser=argparse.ArgumentParser();parser.add_argument('--apply',action='store_true');parser.add_argument('--rollback',action='store_true');args=parser.parse_args()
if args.apply==args.rollback:raise SystemExit('Select apply or rollback')
if TARGET.resolve()!=TARGET or not TARGET.is_dir():raise SystemExit('Target path mismatch')
dest=TARGET/NAME
if args.rollback:
    saved=json.loads((BACKUP/'before.json').read_text())
    if saved['option_present'] or saved['file_exists'] or not dest.is_file() or sha(dest)!=HASH:raise SystemExit('Rollback drift guard')
    print(json.dumps(admin('--rollback')))
    dest.unlink() # One exact own file, after disabling option; never order metadata.
    print('Restored absent own file/option');raise SystemExit(0)
if BACKUP.exists() or dest.exists() or sha(HERE/NAME)!=HASH:raise SystemExit('Existing release or source drift')
BACKUP.mkdir(mode=0o700)
for name in [NAME,'admin.php','deploy.py']:(BACKUP/name).write_bytes((HERE/name).read_bytes())
before=admin('--inspect')
if before['option_present'] or before['file_exists'] or before['sitekit_version']!='1.184.0' or before['woocommerce_version']!='11.1.2' or before['block_theme']:raise SystemExit('Preflight mismatch; not installed')
(BACKUP/'before.json').write_text(json.dumps(before));(BACKUP/'before.json').chmod(0o600)
with dest.open('xb')as f:f.write((HERE/NAME).read_bytes())
dest.chmod(0o644)
if sha(dest)!=HASH:raise SystemExit('Installed source mismatch; option not enabled')
after=admin('--activate');(BACKUP/'after.json').write_text(json.dumps(after))
print(json.dumps(after));print('Applied own file/option; verify fresh request and isolated deployed-file test')
