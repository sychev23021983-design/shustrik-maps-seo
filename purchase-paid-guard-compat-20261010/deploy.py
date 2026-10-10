"""Replace exactly the existing own MU file; never modify options or orders."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent
TARGET = Path('/opt/vps/shustrik-maps/wordpress/wp-content/mu-plugins/shustrik-purchase-paid-guard.php')
BACKUP = Path('/root/shustrik-paid-guard-compat-20261010-backup')
OLD = '666940e505df36627c2c556f680f0a0e3e71a7515c68e994b3f8c6a460b2fbe6'
NEW = '6a9cfc06e1a93060777df0f8baef7aa54c13908486695a4b6ed5cf8d817b978d'
PROVIDER = '82da28caecda75acca747963336c170ddf6399999a91f7ecb7588db0b6182c85'
CONTAINER = 'shustrik-maps-wordpress-1'

def sha(data): return hashlib.sha256(data).hexdigest()
def inspect():
    run = subprocess.run(['docker','exec','-i',CONTAINER,'php'], input=(HERE/'inspect.php').read_bytes(), capture_output=True,check=True)
    return json.loads(run.stdout)
def atomic(data, stat):
    staging = TARGET.with_name('.shustrik-purchase-paid-guard-compat.tmp')
    with staging.open('xb') as output:
        output.write(data); output.flush(); os.fsync(output.fileno())
    os.chmod(staging, stat.st_mode & 0o777); os.chown(staging,stat.st_uid,stat.st_gid)
    os.replace(staging,TARGET)
    directory=os.open(TARGET.parent,os.O_RDONLY)
    try: os.fsync(directory)
    finally: os.close(directory)

parser=argparse.ArgumentParser()
group=parser.add_mutually_exclusive_group(required=True)
group.add_argument('--apply',action='store_true');group.add_argument('--rollback',action='store_true')
parser.add_argument('--source-commit')
args=parser.parse_args()
if TARGET.resolve()!=TARGET or not TARGET.is_file() or TARGET.is_symlink(): raise SystemExit('Unexpected target')
before=inspect()
if before['home']!='https://shustrik-maps.com' or before['sitekit']!='1.184.0' or before['woo']!='11.2.1' or before['block_theme'] or before['provider_hash']!=PROVIDER or before['option'] not in [True,'1']:
    raise SystemExit('Runtime drift; no change')
stat=TARGET.stat()
if args.rollback:
    previous=(BACKUP/'before.php').read_bytes()
    if before['guard_hash']!=NEW or sha(previous)!=OLD:raise SystemExit('Rollback drift')
    atomic(previous,stat)
    after=inspect(); (BACKUP/'rollback.json').write_text(json.dumps(after,indent=2))
    if after['guard_hash']!=OLD or after['option']!=before['option']:raise SystemExit('Rollback verification failed')
    print(json.dumps({'rolled_back':True,'after':after,'warning':'Original Woo11.1.2 gate is incompatible with current Woo11.2.1'}));raise SystemExit(0)
if not args.source_commit or not re.fullmatch('[0-9a-f]{40}',args.source_commit):raise SystemExit('Exact source commit required')
data=(HERE/'shustrik-purchase-paid-guard.php').read_bytes()
if sha(data)!=NEW or before['guard_hash']!=OLD or sha(TARGET.read_bytes())!=OLD or BACKUP.exists():raise SystemExit('Source/target/backup drift; no change')
subprocess.run(['docker','exec','-i',CONTAINER,'php','-l'],input=data,capture_output=True,check=True)
BACKUP.mkdir(mode=0o700)
(BACKUP/'before.php').write_bytes(TARGET.read_bytes()); (BACKUP/'before.php').chmod(0o600)
manifest={'source_commit':args.source_commit,'old_hash':OLD,'new_hash':NEW,'before':before,'uid':stat.st_uid,'gid':stat.st_gid,'mode':stat.st_mode & 0o777}
(BACKUP/'manifest.json').write_text(json.dumps(manifest,indent=2));(BACKUP/'manifest.json').chmod(0o600)
atomic(data,stat)
after=inspect();(BACKUP/'after.json').write_text(json.dumps(after,indent=2))
if after['guard_hash']!=NEW or after['option']!=before['option'] or after['provider_hash']!=PROVIDER:raise SystemExit('Postflight mismatch; use guarded rollback')
print(json.dumps({'applied':True,'source_commit':args.source_commit,'after':after,'backup':str(BACKUP)}))
