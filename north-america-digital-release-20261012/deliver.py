from pathlib import Path
import subprocess,json,hashlib,sys
ROOT=Path(__file__).parent;REPO=ROOT.parent;HOST='vpsadmin@10.66.66.1';FOLDER=ROOT.name;CONTAINER='shustrik-maps-wordpress-1'
def run(args,cwd=None):
 result=subprocess.run(args,cwd=cwd,capture_output=True,text=True,encoding='utf-8',errors='replace')
 if result.returncode: raise RuntimeError(f'Command failed ({result.returncode}): {result.stderr[:1000]} {result.stdout[:1000]}')
 return result.stdout
def remote(command):return run(['ssh','-o','BatchMode=yes','-o','ConnectTimeout=15',HOST,command])
mode=sys.argv[1]
if mode=='prepare':
 commit=run(['git','rev-parse','HEAD'],REPO).strip()
 assert run(['git','rev-list','--left-right','--count','HEAD...@{upstream}'],REPO).strip()=='0\t0'
 assert run(['git','ls-remote','origin','refs/heads/main'],REPO).split()[0]==commit
 assert not run(['git','diff','HEAD','--',FOLDER],REPO).strip(),'Tracked release source must match the committed source'
 allowed_evidence={'deployment.json','preview.json','apply.json','verify.json','rollback-preview.json','public-qa.json'}
 untracked=run(['git','ls-files','--others','--exclude-standard','--',FOLDER],REPO).splitlines()
 assert all(Path(path).name in allowed_evidence for path in untracked),'Unexpected untracked release source'
 archive=REPO/'.codex-work'/('north-america-digital-'+commit[:12]+'.tar');archive.parent.mkdir(exist_ok=True)
 run(['git','-c','core.autocrlf=false','archive','--format=tar','--output='+str(archive),commit+':'+FOLDER],REPO)
 digest=hashlib.sha256(archive.read_bytes()).hexdigest();target='/tmp/north-america-digital-'+commit[:12];remote_archive=target+'.tar'
 run(['scp',str(archive),HOST+':'+remote_archive]);actual=remote('sha256sum '+remote_archive).split()[0];assert actual==digest
 remote('test ! -e '+target+' && mkdir '+target+' && tar -xf '+remote_archive+' -C '+target)
 remote('sudo -n docker cp '+target+' '+CONTAINER+':'+target)
 for file in ['release.php','snapshot.php']:
  assert 'No syntax errors' in remote('sudo -n docker exec '+CONTAINER+' php -l '+target+'/'+file)
 data=dict(commit=commit,archive_sha256=digest,remote_archive_sha256=actual,mode='external',target='https://shustrik-maps.com',wp_source=target,container=CONTAINER,php_lint=True)
 (ROOT/'deployment.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8');print(json.dumps(data))
else:
 assert mode in ['preview','apply','verify','rollback-preview','rollback']
 if mode=='apply':assert not (ROOT/'apply.json').exists(),'An apply record exists; inspect before retry'
 data=json.loads((ROOT/'deployment.json').read_text());output=remote('sudo -n docker exec '+CONTAINER+' php -d memory_limit=512M '+data['wp_source']+'/release.php --'+mode)
 result=json.loads(next(line for line in output.splitlines() if line.startswith('{')))
 (ROOT/(mode+'.json')).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');assert result['ok'];print(json.dumps(result))
