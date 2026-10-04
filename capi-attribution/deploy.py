import hashlib,json,pathlib,subprocess,sys
root=pathlib.Path(__file__).parent
source=root/'shustrik-capi-attribution.php'
target=pathlib.Path('/opt/vps/shustrik-maps/wordpress/wp-content/mu-plugins/shustrik-capi-attribution.php')
backup=root/'backup.json'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
mode=sys.argv[1] if len(sys.argv)>1 else '--preview'
if mode=='--rollback':
 saved=json.loads(backup.read_text())
 if saved['prior_absent'] is not True or not target.exists() or digest(target)!=saved['installed_sha256']:raise RuntimeError('Rollback drift')
 target.rename(root/'removed-plugin.php');print('Own profiler archived; logs retained');sys.exit(0)
if mode not in ['--preview','--apply'] or target.exists() or backup.exists():raise RuntimeError('Mode/target/backup guard')
subprocess.run(['docker','cp',str(source),'shustrik-maps-wordpress-1:/tmp/shustrik-capi-attribution-lint.php'],check=True)
subprocess.run(['docker','exec','shustrik-maps-wordpress-1','php','-l','/tmp/shustrik-capi-attribution-lint.php'],check=True)
if mode=='--apply':
 backup.write_text(json.dumps({'prior_absent':True,'installed_sha256':digest(source)}),encoding='utf-8')
 temp=target.with_suffix('.php.tmp')
 if temp.exists():raise RuntimeError('Unexpected temporary file')
 temp.write_bytes(source.read_bytes());temp.chmod(0o644);temp.replace(target)
 if digest(target)!=digest(source):raise RuntimeError('Installed hash mismatch')
print(json.dumps({'mode':mode,'ok':True,'sha256':digest(source),'expires_utc':'2026-10-04T12:00:00Z'}))
