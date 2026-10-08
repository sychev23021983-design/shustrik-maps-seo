from pathlib import Path
import subprocess,json,re
root=Path(__file__).parent;host='vpsadmin@10.66.66.1';repo=Path('J:/1. My Vault/90 Migration/shustrik-maps-seo')
def run(args):
 r=subprocess.run(args,capture_output=True,text=True,encoding='utf-8',errors='replace');assert r.returncode==0,r.stderr;return r.stdout
raw=run(['ssh',host,'sudo -n docker exec shustrik-maps-wordpress-1 php /tmp/final-catalog.php']);catalog=json.loads(raw)
audit=[{'id':r['id'],'title':r['title'],'slug':r['slug'],'has_stl_format_icon':bool(re.search(r'/STL(?:-min)?\.png',r['excerpt'],re.I)),'ai_concepts_present':'AI-generated' in r['content']} for r in catalog]
remaining=[r for r in audit if r['has_stl_format_icon'] and not r['ai_concepts_present']]
(root/'catalog-audit.json').write_text(json.dumps({'published_products':len(audit),'remaining_by_stl_icon':remaining,'all_products':audit,'historical_exclusions':{'Denmark':'Completed earlier per Ten More Global STL report; original carousel remains, do not repeat','Belarus':'Owner excluded','Prepayment':'Not a product STL release'},'scope_pending':'Burj Al Arab and Burj Khalifa have C4D/FBX formats; STL on request only, not included without owner choice'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
slides=[];controls=[]
for id,slug,name in json.loads((root/'defs.json').read_text()):
 for mode in ['desktop','mobile']:
  samples=json.loads((root/(slug+'-'+mode+'-qa.json')).read_text());assert len(samples)==4;slides+=samples
  c=json.loads((root/(slug+'-'+mode+'-controls.json')).read_text());assert c['pass'];controls.append({'id':id,'mode':mode,'pass':True})
assert len(slides)==24 and len(controls)==6
(root/'browser-qa.json').write_text(json.dumps({'pass':True,'slide_checks':24,'control_sets':controls,'samples':slides},indent=2)+'\n',encoding='utf-8')
print('Browser24/24; catalog',len(audit),'remaining STL-icon candidates',[(r['id'],r['title']) for r in remaining])
