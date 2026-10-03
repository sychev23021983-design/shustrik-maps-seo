import pathlib, hashlib, json, subprocess, argparse
HERE=pathlib.Path(__file__).parent
TARGET=pathlib.Path('/opt/vps/shustrik-maps/wordpress/wp-content/mu-plugins/shustrik-pinterest-async.php')
BACKUP=pathlib.Path('/root/shustrik-pinterest-async-20261003')
CONTAINER='shustrik-maps-wordpress-1'
SERVICE=pathlib.Path('/etc/systemd/system/shustrik-pinterest-views.service')
TIMER=pathlib.Path('/etc/systemd/system/shustrik-pinterest-views.timer')
def run(*args):subprocess.run(args,check=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
parser=argparse.ArgumentParser();parser.add_argument('--apply',action='store_true');parser.add_argument('--rollback',action='store_true');parser.add_argument('--update',action='store_true');a=parser.parse_args()
if a.rollback:
    saved=json.loads((BACKUP/'installed.json').read_text())
    if not TARGET.exists() or sha(TARGET)!=saved['plugin_sha256']:raise SystemExit('Rollback drift guard failed')
    run('docker','cp',str(BACKUP/'admin.php'),CONTAINER+':/tmp/shustrik-pinterest-admin.php')
    # Restore synchronous admission, but keep consumers running until encrypted payloads drain.
    run('docker','exec',CONTAINER,'php','/tmp/shustrik-pinterest-admin.php','--disable')
    print('ENQUEUE_DISABLED: original synchronous trackers restored; existing encrypted queue still drains. Do not remove consumer while payloads remain.');raise SystemExit(0)
if a.update:
    saved=json.loads((BACKUP/'installed.json').read_text())
    if any(not p.exists() or sha(p)!=saved[k] for p,k in [(TARGET,'plugin_sha256'),(SERVICE,'service_sha256'),(TIMER,'timer_sha256')]):raise SystemExit('Update drift guard failed')
    run('docker','cp',str(BACKUP/'admin.php'),CONTAINER+':/tmp/shustrik-pinterest-admin.php')
    run('docker','exec',CONTAINER,'php','/tmp/shustrik-pinterest-admin.php','--disable')
    run('docker','cp',str(HERE)+'/.',CONTAINER+':/tmp/shustrik-pinterest-preflight')
    for name in ['shustrik-pinterest-async.php','worker.php','admin.php','test.php']:
        run('docker','exec',CONTAINER,'php','-l','/tmp/shustrik-pinterest-preflight/'+name)
    run('docker','exec',CONTAINER,'php','/tmp/shustrik-pinterest-preflight/test.php')
    run('docker','exec',CONTAINER,'php','/tmp/shustrik-pinterest-preflight/preflight.php')
    for name in ['shustrik-pinterest-async.php','worker.php','admin.php','deploy.py']:
        old=BACKUP/name
        (BACKUP/('previous-'+sha(old)+'-'+name)).write_bytes(old.read_bytes())
        old.write_bytes((HERE/name).read_bytes())
    TARGET.write_bytes((HERE/'shustrik-pinterest-async.php').read_bytes());TARGET.chmod(0o644)
    (BACKUP/('previous-'+sha(TIMER)+'-timer')).write_bytes(TIMER.read_bytes())
    TIMER.write_text(TIMER.read_text().replace('OnUnitInactiveSec=30s','OnUnitInactiveSec=5s'))
    saved['plugin_sha256']=sha(TARGET);saved['timer_sha256']=sha(TIMER);(BACKUP/'installed.json').write_text(json.dumps(saved))
    run('systemd-analyze','verify',str(SERVICE),str(TIMER));run('systemctl','daemon-reload');run('systemctl','restart',TIMER.name)
    run('systemctl','start',SERVICE.name);run('systemctl','is-active',TIMER.name)
    run('docker','exec',CONTAINER,'php','/tmp/shustrik-pinterest-admin.php','--enable')
    print('UPDATED guarded package; consumer verified before admission');raise SystemExit(0)
if TARGET.exists() or SERVICE.exists() or TIMER.exists() or BACKUP.exists():raise SystemExit('Target/units/backup already exist; refusing overwrite')
run('docker','cp',str(HERE)+'/.',CONTAINER+':/tmp/shustrik-pinterest-preflight')
for name in ['shustrik-pinterest-async.php','worker.php','admin.php','test.php']:
    run('docker','exec',CONTAINER,'php','-l','/tmp/shustrik-pinterest-preflight/'+name)
run('docker','exec',CONTAINER,'php','/tmp/shustrik-pinterest-preflight/test.php')
run('docker','exec',CONTAINER,'php','/tmp/shustrik-pinterest-preflight/preflight.php')
print(json.dumps({'preview':True,'plugin_sha256':sha(HERE/'shustrik-pinterest-async.php')}))
if not a.apply:raise SystemExit(0)
BACKUP.mkdir(mode=0o700)
for name in ['shustrik-pinterest-async.php','worker.php','admin.php','deploy.py']:(BACKUP/name).write_bytes((HERE/name).read_bytes())
run('docker','cp',str(BACKUP/'admin.php'),CONTAINER+':/tmp/shustrik-pinterest-admin.php')
service='''[Unit]
Description=Shustrik isolated Pinterest view-event consumer
After=docker.service
Requires=docker.service
[Service]
Type=oneshot
Nice=10
TimeoutStartSec=60
ExecStartPre=/usr/bin/docker cp /root/shustrik-pinterest-async-20261003/worker.php shustrik-maps-wordpress-1:/tmp/shustrik-pinterest-worker.php
ExecStart=/usr/bin/docker exec shustrik-maps-wordpress-1 php -d memory_limit=256M /tmp/shustrik-pinterest-worker.php
'''
timer='''[Unit]
Description=Shustrik Pinterest view-event consumer timer
[Timer]
OnBootSec=30s
OnUnitInactiveSec=5s
Unit=shustrik-pinterest-views.service
[Install]
WantedBy=timers.target
'''
# Start a consumer before enabling admission; new MU plugin is initially disabled.
run('docker','exec',CONTAINER,'php','/tmp/shustrik-pinterest-admin.php','--disable')
TARGET.write_bytes((HERE/'shustrik-pinterest-async.php').read_bytes());TARGET.chmod(0o644)
SERVICE.write_text(service);TIMER.write_text(timer)
(BACKUP/'installed.json').write_text(json.dumps({'plugin_sha256':sha(TARGET),'service_sha256':sha(SERVICE),'timer_sha256':sha(TIMER)}))
try:
    run('systemd-analyze','verify',str(SERVICE),str(TIMER))
    run('systemctl','daemon-reload');run('systemctl','enable','--now',TIMER.name)
    run('systemctl','start',SERVICE.name)
    run('systemctl','is-active',TIMER.name)
    run('docker','exec',CONTAINER,'php','/tmp/shustrik-pinterest-admin.php','--enable')
except BaseException:
    run('docker','exec',CONTAINER,'php','/tmp/shustrik-pinterest-admin.php','--disable')
    raise
print('APPLIED: consumer active, asynchronous admission enabled; no vendor edits/restart/cache purge')
