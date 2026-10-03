import argparse, hashlib, json, pathlib, subprocess
HERE = pathlib.Path(__file__).resolve().parent
TARGET = pathlib.Path('/opt/vps/shustrik-maps/wordpress/wp-content/mu-plugins')
BACKUP = pathlib.Path('/root/shustrik-ecommerce-funnel-20261003')
CONTAINER = 'shustrik-maps-wordpress-1'
FILES = ['shustrik-ecommerce-funnel.php', 'shustrik-ecommerce-funnel.js']
def run(*args):
    return subprocess.run(args, check=True, capture_output=True, text=True).stdout
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def admin(mode):
    run('docker', 'cp', str(BACKUP / 'admin.php'), CONTAINER + ':/tmp/shustrik-ecommerce-admin.php')
    return run('docker', 'exec', CONTAINER, 'php', '/tmp/shustrik-ecommerce-admin.php', mode)
parser = argparse.ArgumentParser()
parser.add_argument('--apply', action='store_true')
parser.add_argument('--rollback', action='store_true')
args = parser.parse_args()
if args.apply == args.rollback:
    raise SystemExit('Select apply or rollback')
if TARGET.resolve() != TARGET or not TARGET.is_dir():
    raise SystemExit('Target path guard failed')
if args.rollback:
    saved = json.loads((BACKUP / 'installed.json').read_text())
    if any(not (TARGET / name).is_file() or sha(TARGET / name) != saved[name] for name in FILES):
        raise SystemExit('Runtime drift: do not overwrite')
    run('docker', 'cp', str(BACKUP / 'option-backup.json'), CONTAINER + ':/tmp/shustrik-ecommerce-option-backup-20261003.json')
    print(admin('--rollback').strip())
    # Keep the exact files available for stale cached HTML until its 60-second TTL expires.
    # They are inert in newly generated pages. Do not purge shared cache or unrelated plugins.
    print('Own option restored; wait beyond cache TTL and verify product HTML before removing own files.')
    raise SystemExit(0)
if BACKUP.exists() or any((TARGET / name).exists() for name in FILES):
    raise SystemExit('Existing release/files: refusing replacement')
BACKUP.mkdir(mode=0o700)
for name in FILES + ['admin.php', 'deploy.py']:
    (BACKUP / name).write_bytes((HERE / name).read_bytes())
run('docker', 'cp', str(HERE) + '/.', CONTAINER + ':/tmp/shustrik-ecommerce-preflight')
for name in ['shustrik-ecommerce-funnel.php', 'admin.php', 'preview.php', 'test-gates.php']:
    run('docker', 'exec', CONTAINER, 'php', '-l', '/tmp/shustrik-ecommerce-preflight/' + name)
run('docker', 'exec', CONTAINER, 'php', '/tmp/shustrik-ecommerce-preflight/test-gates.php')
print(run('docker', 'exec', CONTAINER, 'php', '/tmp/shustrik-ecommerce-preflight/preview.php').strip())
before = json.loads(admin('--inspect'))
if before['enabled'] or before['wc_version'] != '11.1.2' or before['sitekit_version'] != '1.184.0':
    raise SystemExit('Preflight mismatch; no runtime files installed')
(BACKUP / 'before.json').write_text(json.dumps(before))
manifest = {name: sha(HERE / name) for name in FILES}
for name in FILES:
    with (TARGET / name).open('xb') as file:
        file.write((HERE / name).read_bytes())
    (TARGET / name).chmod(0o644)
    if sha(TARGET / name) != manifest[name]:
        raise SystemExit('Copied hash mismatch; option still disabled')
(BACKUP / 'installed.json').write_text(json.dumps(manifest))
print(admin('--apply').strip())
run('docker', 'cp', CONTAINER + ':/tmp/shustrik-ecommerce-option-backup-20261003.json', str(BACKUP / 'option-backup.json'))
(BACKUP / 'option-backup.json').chmod(0o600)
print('APPLIED exact files; no restart. Verify cached HTML after 60-second TTL and GA4 browser delivery.')
