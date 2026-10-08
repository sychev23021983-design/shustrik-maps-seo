from pathlib import Path
import json,subprocess
from datetime import datetime,timezone,timedelta
root=Path(__file__).parent;repo=Path('J:/1. My Vault/90 Migration/shustrik-maps-seo')
def git(*args):
 r=subprocess.run(['git',*args],cwd=repo,capture_output=True,text=True,encoding='utf-8',errors='replace');assert r.returncode==0,r.stderr;return r.stdout.strip()
head=git('rev-parse','HEAD');origin=git('ls-remote','origin','refs/heads/main').split()[0]
assert head==origin and git('rev-list','--left-right','--count','HEAD...@{upstream}')=='0\t0'
assert not git('status','--short','--','five-special-stl-slider-release-20261008')
d=json.loads((root/'deployment.json').read_text());stamp=datetime.now(timezone(timedelta(hours=3))).isoformat()
receipt={'utc_moscow':stamp,'source_commit':d['commit'],'evidence_commit':head,'origin_main':origin,'upstream':'0:0','release_folder_clean':True,'prior_unrelated_dirty_untracked_preserved':True,'apply_count':1}
(root/'git-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
line=f'GitHub evidence commit {head} pushed; origin/main=HEAD, upstream0:0, release-folder clean. Published content source remains {d["commit"]}; evidence push does not repeat apply. Previous unrelated dirty/untracked preserved.'
p=root/'Release Report.md';p.write_text(p.read_text(encoding='utf-8')+'\n'+line+'\n',encoding='utf-8')
for n in ['Shustrik Maps SEO - Overview.md','Shustrik Maps SEO - Next Actions.md']:
 p=root.parent/n;s=p.read_text(encoding='utf-8');front,body=s.rsplit('---',1) if False else ('','')
 parts=s.split('---',2);assert '## Пять специальных STL завершены 08.10' in parts[2]
 body=parts[2]
 heading=next(x for x in body.splitlines() if x.startswith('## Пять специальных STL завершены 08.10'))
 parts[2]=body.replace(heading+'\n',heading+'\n\n'+line+'\n',1)
 p.write_text('---'+parts[1]+'---'+parts[2],encoding='utf-8')
p=root.parents[3]/'04 Operations/Runtime Status.md';s=p.read_text(encoding='utf-8');first,rest=s.split('\n## ',1)
assert 'Five Special STL' in first
p.write_text(first.rstrip()+'\n\n'+line+'\n\n## '+rest,encoding='utf-8')
print(json.dumps(receipt))
