#!/usr/bin/env python3
"""Guarded Shustrik-only cache coalescing pilot. No shared policy or secrets."""
import hashlib,json,os,pathlib,shutil,subprocess,sys
VHOST=pathlib.Path('/etc/nginx/sites-enabled/shustrik-maps.com')
BACKUP=pathlib.Path('/root/shustrik-cache-pilot-20261003')
EXPECTED='798cfea5695ae7ec0b93b02a4a5582f38f3fa037fed34a4a6e05a6b59d8cfc63'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(*args):subprocess.run(args,check=True)
def restore():
    shutil.copyfile(BACKUP/'vhost',VHOST)
    run('nginx','-t');run('systemctl','reload','nginx')
if os.geteuid()!=0:raise SystemExit('Use existing sudo role.')
mode=sys.argv[1] if len(sys.argv)>1 else '--preview'
if mode=='--rollback':
    if sha(VHOST)!=json.loads((BACKUP/'installed.json').read_text())['vhost']:raise SystemExit('Drift; rollback aborted.')
    restore();print('Cache pilot rolled back; observability retained.');raise SystemExit(0)
if mode not in ['--preview','--apply']:raise SystemExit('Use --preview/--apply/--rollback.')
if sha(VHOST)!=EXPECTED or BACKUP.exists():raise SystemExit('Baseline drift or existing rollout; no changes.')
t=VHOST.read_text();anchor='        include /etc/nginx/snippets/wordpress-page-cache.conf;'
if t.count(anchor)!=1 or 'proxy_cache_lock' in t or 'proxy_cache_background_update' in t:raise SystemExit('Unexpected vhost shape.')
patch=anchor+'\n        # Coalesce anonymous cache misses; serve stale during background refresh.\n        proxy_cache_lock on;\n        proxy_cache_lock_timeout 5s;\n        proxy_cache_lock_age 5s;\n        proxy_cache_background_update on;'
print(json.dumps({'mode':mode,'scope':'Shustrik location / only','baseline':EXPECTED,'cache_ttl_seconds':60,'private_query_routes_bypass_unchanged':True}))
if mode=='--preview':raise SystemExit(0)
BACKUP.mkdir(mode=0o700);shutil.copy2(VHOST,BACKUP/'vhost');shutil.copy2(__file__,BACKUP/'deploy.py')
try:
    VHOST.write_text(t.replace(anchor,patch));run('nginx','-t');run('systemctl','reload','nginx')
    (BACKUP/'installed.json').write_text(json.dumps({'vhost':sha(VHOST)},indent=2))
except Exception:restore();raise
print('Cache pilot deployed; original vhost saved.')
