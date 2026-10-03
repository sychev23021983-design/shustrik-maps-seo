#!/usr/bin/env python3
"""Root-only guarded deploy/rollback; never reads compose/.env/credentials."""
import hashlib, json, os, pathlib, shutil, subprocess, sys
SRC = pathlib.Path(__file__).resolve().parent
VHOST = pathlib.Path('/etc/nginx/sites-enabled/shustrik-maps.com')
MPM = pathlib.Path('/opt/vps/shustrik-maps/apache-mpm.conf')
BACKUP = pathlib.Path('/root/shustrik-observability-20261003-lf')
HASHES = {'vhost': '45cd027257e18ed31d6686a726695ac0c564074cdd23e551ef7a2428713745fe',
          'mpm': '8136c078dbc17fb044036bd8b9b36110db9c1a7083326bc53c25aefe75bf8faf'}
INSTALL = {'nginx.conf': '/etc/nginx/conf.d/30-shustrik-observability.conf',
 'sample.py': '/opt/vps/shustrik-observability/sample.py',
 'shustrik-worker-sample.service': '/etc/systemd/system/shustrik-worker-sample.service',
 'shustrik-worker-sample.timer': '/etc/systemd/system/shustrik-worker-sample.timer',
 'logrotate.conf': '/etc/logrotate.d/shustrik-observability'}
def run(*args): subprocess.run(args, check=True)
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def restore():
    subprocess.run(['systemctl','disable','--now','shustrik-worker-sample.timer'],check=False)
    subprocess.run(['systemctl','stop','shustrik-worker-sample.service'],check=False)
    shutil.copyfile(BACKUP / 'vhost', VHOST)
    # Preserve inode of the bind-mounted MPM file.
    MPM.write_bytes((BACKUP / 'mpm').read_bytes())
    for path in INSTALL.values(): pathlib.Path(path).unlink(missing_ok=True)
    run('docker','exec','shustrik-maps-wordpress-1','apache2ctl','-t')
    run('nginx','-t'); run('docker','exec','shustrik-maps-wordpress-1','apache2ctl','-k','graceful')
    run('systemctl','reload','nginx'); run('systemctl','daemon-reload')
    print('Rollback complete; aggregate logs and original backups retained.')
if os.geteuid() != 0: raise SystemExit('Run via existing sudo role.')
mode = sys.argv[1] if len(sys.argv)>1 else '--preview'
if mode == '--rollback':
    manifest=json.loads((BACKUP/'installed.json').read_text())
    if digest(VHOST)!=manifest['vhost'] or digest(MPM)!=manifest['mpm'] or any(not pathlib.Path(p).exists() or digest(pathlib.Path(p))!=h for p,h in manifest['files'].items()): raise SystemExit('Configuration drift; rollback aborted.')
    restore(); raise SystemExit(0)
if mode not in ['--preview','--apply']: raise SystemExit('Use --preview/--apply/--rollback.')
if digest(VHOST)!=HASHES['vhost'] or digest(MPM)!=HASHES['mpm']: raise SystemExit('Baseline drift; no changes.')
if BACKUP.exists() or any(pathlib.Path(p).exists() for p in INSTALL.values()): raise SystemExit('Existing rollout; no changes.')
text = VHOST.read_text()
anchor = '    server_name shustrik-maps.com www.shustrik-maps.com;'
if text.count(anchor)!=2: raise SystemExit('Unexpected vhost shape.')
newtext=text.replace(anchor,anchor+'\n    # Dedicated aggregate log; retain inherited legacy access log.\n    access_log /var/log/nginx/access.log combined;\n    access_log /var/log/nginx/shustrik-timing.jsonl shustrik_timing buffer=32k flush=5s;',1)
print(json.dumps({'mode':mode,'baseline_hashes':HASHES,'install_targets':INSTALL,'sampler_seconds':15,'status_bind':'inside-container 127.0.0.1:8099'}))
if mode=='--preview': raise SystemExit(0)
BACKUP.mkdir(mode=0o700)
shutil.copy2(VHOST,BACKUP/'vhost'); shutil.copy2(MPM,BACKUP/'mpm')
shutil.copytree(SRC,BACKUP/'release')
try:
    pathlib.Path('/opt/vps/shustrik-observability').mkdir(exist_ok=True,mode=0o755)
    logdir=pathlib.Path('/var/log/shustrik-observability'); logdir.mkdir(exist_ok=True,mode=0o750)
    shutil.chown(logdir,user='vpsadmin',group='vpsadmin')
    for name,dest in INSTALL.items(): shutil.copyfile(SRC/name,dest); os.chmod(dest,0o644)
    VHOST.write_text(newtext)
    MPM.write_bytes((BACKUP/'mpm').read_bytes()+(SRC/'apache-status.conf').read_bytes())
    run('docker','exec','shustrik-maps-wordpress-1','apache2ctl','-t'); run('nginx','-t')
    run('systemd-analyze','verify',INSTALL['shustrik-worker-sample.service'],INSTALL['shustrik-worker-sample.timer'])
    run('logrotate','-d',INSTALL['logrotate.conf'])
    run('docker','exec','shustrik-maps-wordpress-1','apache2ctl','-k','graceful')
    run('systemctl','reload','nginx'); run('systemctl','daemon-reload')
    run('systemctl','enable','--now','shustrik-worker-sample.timer')
    run('systemctl','start','shustrik-worker-sample.service')
    (BACKUP/'installed.json').write_text(json.dumps({'vhost':digest(VHOST),'mpm':digest(MPM),'files':{p:digest(pathlib.Path(p)) for p in INSTALL.values()}},indent=2))
    print('Deployed; original configs backed up; no worker/cache limits changed.')
except Exception:
    restore(); raise
