import pathlib, hashlib, subprocess, json, argparse
SOURCE=pathlib.Path(__file__).parent/'shustrik-php-profile.php'
TARGET=pathlib.Path('/opt/vps/shustrik-maps/wordpress/wp-content/mu-plugins/shustrik-php-profile.php')
BACKUP=pathlib.Path('/root/shustrik-php-profile-20261003')
CONTAINER='shustrik-maps-wordpress-1'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(*args):subprocess.run(args,check=True)
parser=argparse.ArgumentParser();parser.add_argument('--apply',action='store_true');parser.add_argument('--rollback',action='store_true');parser.add_argument('--update',action='store_true');args=parser.parse_args()
if args.rollback:
    saved=json.loads((BACKUP/'installed.json').read_text())
    if not TARGET.exists() or digest(TARGET)!=saved['sha256']:raise SystemExit('Rollback drift guard failed')
    # Archive instead of deleting source. Original target was absent.
    TARGET.rename(BACKUP/'removed-plugin.php')
    print('ROLLED_BACK; aggregate logs retained');raise SystemExit(0)
if args.update:
    saved=json.loads((BACKUP/'installed.json').read_text())
    if not TARGET.exists() or digest(TARGET)!=saved['sha256']:raise SystemExit('Update drift guard failed')
    run('docker','cp',str(SOURCE),CONTAINER+':/tmp/shustrik-profile-lint.php')
    run('docker','exec',CONTAINER,'php','-l','/tmp/shustrik-profile-lint.php')
    (BACKUP/('previous-'+digest(TARGET)+'.php')).write_bytes(TARGET.read_bytes())
    TARGET.write_bytes(SOURCE.read_bytes());TARGET.chmod(0o644)
    (BACKUP/'deploy.py').write_bytes(pathlib.Path(__file__).read_bytes())
    (BACKUP/'installed.json').write_text(json.dumps({'sha256':digest(TARGET),'target':str(TARGET)}))
    print('UPDATED guarded profiler; original absence rollback retained');raise SystemExit(0)
if TARGET.exists():raise SystemExit('Target already exists; refusing overwrite')
print(json.dumps({'source_sha256':digest(SOURCE),'target_absent':True,'expires_utc':'2026-10-04T00:00:00Z'}))
if not args.apply:raise SystemExit(0)
if BACKUP.exists():raise SystemExit('Backup directory already exists')
BACKUP.mkdir(mode=0o700);(BACKUP/'source.php').write_bytes(SOURCE.read_bytes());(BACKUP/'deploy.py').write_bytes(pathlib.Path(__file__).read_bytes())
run('docker','cp',str(SOURCE),CONTAINER+':/tmp/shustrik-profile-lint.php')
run('docker','exec',CONTAINER,'php','-l','/tmp/shustrik-profile-lint.php')
TARGET.write_bytes(SOURCE.read_bytes());TARGET.chmod(0o644)
(BACKUP/'installed.json').write_text(json.dumps({'sha256':digest(TARGET),'target':str(TARGET)}))
print('APPLIED; no restart or cache purge; rollback archives installed plugin')
