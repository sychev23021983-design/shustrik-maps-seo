import hashlib, json, pathlib, subprocess, sys
SOURCE=pathlib.Path(__file__).parent
TARGET=pathlib.Path('/opt/vps/shustrik-maps/wordpress/wp-content/mu-plugins/shustrik-catalog-navigation.php')
BACKUP=SOURCE/'backup.json'
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def verify():
    subprocess.run(['docker','cp',str(SOURCE)+'/.','shustrik-maps-wordpress-1:/tmp/shustrik-catalog-navigation/'],check=True)
    subprocess.run(['docker','exec','shustrik-maps-wordpress-1','php','/tmp/shustrik-catalog-navigation/admin.php','--verify'],check=True)
mode=sys.argv[1] if len(sys.argv)>1 else '--preview'
source=SOURCE/'shustrik-catalog-navigation.php'
if mode in ['--preview','--apply']:
    if TARGET.exists() or BACKUP.exists(): raise RuntimeError('Own target/backup already exists; refuse overwrite')
    verify()
    subprocess.run(['docker','exec','shustrik-maps-wordpress-1','php','-l','/tmp/shustrik-catalog-navigation/shustrik-catalog-navigation.php'],check=True)
    if mode=='--apply':
        BACKUP.write_text(json.dumps({'prior_file_absent':True,'installed_sha256':digest(source)}),encoding='utf-8')
        temp=TARGET.with_suffix('.php.tmp')
        if temp.exists(): raise RuntimeError('Temporary target exists; refuse overwrite')
        temp.write_bytes(source.read_bytes()); temp.chmod(0o644); temp.replace(TARGET)
        if digest(TARGET)!=digest(source): raise RuntimeError('Installed hash mismatch')
        verify()
    print(json.dumps({'mode':mode,'ok':True,'sha256':digest(source),'target':str(TARGET)}))
elif mode=='--rollback':
    data=json.loads(BACKUP.read_text())
    if data.get('prior_file_absent') is not True or not TARGET.exists() or digest(TARGET)!=data['installed_sha256']: raise RuntimeError('Rollback drift; refuse deletion')
    verify(); TARGET.unlink()
    print(json.dumps({'mode':mode,'ok':True,'only_own_file_removed':True,'backup_retained':True}))
else: raise RuntimeError('Unsupported mode')
