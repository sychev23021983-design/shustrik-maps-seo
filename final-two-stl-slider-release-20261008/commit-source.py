from pathlib import Path
import subprocess,json
root=Path(__file__).parent;repo=Path('J:/1. My Vault/90 Migration/shustrik-maps-seo');folder='final-two-stl-slider-release-20261008'
def run(args):
 r=subprocess.run(args,cwd=repo,capture_output=True,text=True,encoding='utf-8',errors='replace');assert r.returncode==0,(r.stderr,r.stdout);return r.stdout
for d in [root,repo/folder]:
 for n in ['release.php','backup-export.php']:
  p=d/n;p.write_text(p.read_text(encoding='utf-8-sig').replace('final_two_stl_stl','final_two_stl'),encoding='utf-8',newline='\n')
before={'head':run(['git','rev-parse','HEAD']).strip(),'remote':run(['git','remote','get-url','origin']).strip(),'branch':run(['git','branch','--show-current']).strip(),'upstream':run(['git','rev-list','--left-right','--count','HEAD...@{upstream}']).strip(),'status':run(['git','status','--short'])}
assert before['head']=='2dfe29da75253c69a1aa026a1ec1fea37d883c90' and before['upstream']=='0\t0' and before['branch']=='main'
assert before['remote']=='git@github.com:sychev23021983-design/shustrik-maps-seo.git'
assert not run(['git','diff','--cached','--name-only']).strip()
(root/'github-first.json').write_text(json.dumps(before,indent=2)+'\n',encoding='utf-8');(repo/folder/'github-first.json').write_text(json.dumps(before,indent=2)+'\n',encoding='utf-8',newline='\n')
run(['git','add','--',folder])
staged=run(['git','diff','--cached','--name-only']).splitlines();assert staged and all(x.startswith(folder+'/') for x in staged)
run(['git','diff','--cached','--check'])
run(['git','commit','-m','Prepare remaining Moon Surface and Female Face STL product sliders'])
run(['git','push','origin','main'])
commit=run(['git','rev-parse','HEAD']).strip();assert run(['git','ls-remote','origin','refs/heads/main']).split()[0]==commit
assert run(['git','rev-list','--left-right','--count','HEAD...@{upstream}']).strip()=='0\t0'
(root/'source-commit.txt').write_text(commit+'\n',encoding='utf-8');print(commit)
