import hashlib, pathlib, subprocess, sys, json, datetime
HERE=pathlib.Path(__file__).resolve().parent
CONF=pathlib.Path('/etc/nginx/sites-enabled/shustrik-maps.com')
MU=pathlib.Path('/opt/vps/shustrik-maps/wordpress/wp-content/mu-plugins/shustrik-responsive-thumbnails.php')
EXPECTED='a073fb4d0d4dae07087415b6d4cc3980de0331d89e178a4271d46162eaabb8cd'
def run(*args): subprocess.run(args,check=True)
if '--rollback' in sys.argv:
    assert (HERE/'nginx-before.conf').exists()
    CONF.write_bytes((HERE/'nginx-before.conf').read_bytes())
    if MU.exists(): MU.unlink()
    run('nginx','-t'); run('systemctl','reload','nginx')
    print('Rolled back own MU file and exact Nginx backup'); sys.exit(0)
old=CONF.read_bytes()
assert hashlib.sha256(old).hexdigest()==EXPECTED, 'Nginx config drift'
assert not MU.exists(), 'Own MU already exists'
source=(HERE/'shustrik-responsive-thumbnails.php').read_bytes()
run('docker','exec','-i','shustrik-maps-wordpress-1','php','-l') if False else None
lint=subprocess.run(['docker','exec','-i','shustrik-maps-wordpress-1','php','-l'],input=source,capture_output=True)
assert lint.returncode==0, lint.stdout.decode()+lint.stderr.decode()
text=old.decode()
marker='    # Static media bypasses Apache/PHP to keep WordPress workers free.\n'
assert text.count(marker)==1
block='''    # Versioned public assets only; never match PHP, account or payment endpoints.
    location ~* ^/(?:wp-includes|wp-content/(?:themes|plugins))/.+\\.(?:css|js|woff2?|ttf|eot)$ {
        root /opt/vps/shustrik-maps/wordpress;
        try_files $uri =404;
        access_log off;
        expires 30d;
    }
    # Public images: keep the existing PDF rule and lifetime below unchanged.
    location ~* ^/wp-content/uploads/(.+\\.(?:jpe?g|png|gif|webp|avif|svg|ico|css|js|woff2?|ttf|eot))$ {
        alias /opt/vps/shustrik-maps/wordpress/wp-content/uploads/$1;
        access_log off;
        expires 30d;
    }

'''
(HERE/'nginx-before.conf').write_bytes(old)
try:
    CONF.write_text(text.replace(marker,block+marker))
    run('nginx','-t')
    MU.write_bytes(source); MU.chmod(0o644)
    run('systemctl','reload','nginx')
except Exception:
    CONF.write_bytes(old)
    if MU.exists(): MU.unlink()
    run('nginx','-t'); run('systemctl','reload','nginx')
    raise
print(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'mu_sha256':hashlib.sha256(source).hexdigest(),'nginx_sha256':hashlib.sha256(CONF.read_bytes()).hexdigest(),'backup':str(HERE/'nginx-before.conf')}))
