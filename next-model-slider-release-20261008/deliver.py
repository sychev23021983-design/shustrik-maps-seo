from pathlib import Path
import subprocess,json,hashlib,sys
root=Path(__file__).parent;repo=Path('J:/1. My Vault/90 Migration/shustrik-maps-seo');host='vpsadmin@10.66.66.1';folder='next-model-slider-release-20261008'
def run(args,cwd=None):
 r=subprocess.run(args,cwd=cwd,capture_output=True,text=True,encoding='utf-8',errors='replace');assert r.returncode==0,(r.returncode,r.stderr[:1200],r.stdout[:1200]);return r.stdout
def remote(command):return run(['ssh','-o','BatchMode=yes','-o','ConnectTimeout=15',host,command])
mode=sys.argv[1]
if mode=='prepare':
 commit=run(['git','rev-parse','HEAD'],repo).strip();assert run(['git','rev-list','--left-right','--count','HEAD...@{upstream}'],repo).strip()=='0\t0'
 assert run(['git','ls-remote','origin','refs/heads/main'],repo).split()[0]==commit
 archive=repo/'.codex-work'/('next-models-'+commit[:7]+'.tar');run(['git','archive','--format=tar','--output='+str(archive),commit+':'+folder],repo)
 sha=hashlib.sha256(archive.read_bytes()).hexdigest();target='/tmp/next-models-'+commit[:7];rtar=target+'.tar'
 run(['scp',str(archive),host+':'+rtar]);actual=remote('sha256sum '+rtar).split()[0];assert actual==sha
 remote('test ! -e '+target+' && mkdir '+target+' && tar -xf '+rtar+' -C '+target)
 remote('sudo -n docker cp '+target+' shustrik-maps-wordpress-1:'+target)
 lint=remote('sudo -n docker exec shustrik-maps-wordpress-1 php -l '+target+'/release.php');assert 'No syntax errors' in lint
 d={'commit':commit,'archive_sha256':sha,'remote_archive_sha256':actual,'target':'https://shustrik-maps.com','wp_source':target,'mode':'external','container':'shustrik-maps-wordpress-1','lint_pass':True}
 (root/'deployment.json').write_text(json.dumps(d,indent=2),encoding='utf-8');print(json.dumps(d))
else:
 assert mode in ['preview','apply','verify','rollback-preview']
 if mode=='apply':assert not (root/'apply.json').exists(),'Apply output exists: inspect before any retry'
 d=json.loads((root/'deployment.json').read_text());output=remote('sudo -n docker exec shustrik-maps-wordpress-1 php '+d['wp_source']+'/release.php --'+mode)
 (root/(mode+'.json')).write_text(output,encoding='utf-8');r=json.loads(next(x for x in output.splitlines() if x.startswith('{')));assert r['ok'];print(json.dumps({'mode':mode,'ok':r['ok'],'products':len(r['rows']),'media':sum(len(x['media']) for x in r['rows'])}))
