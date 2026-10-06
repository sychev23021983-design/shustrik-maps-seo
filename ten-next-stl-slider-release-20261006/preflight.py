import json,re
from pathlib import Path
root=Path(__file__).parent
baseline=json.loads((root/'baseline.json').read_text(encoding='utf-8'))
manifest=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
for before,after in zip(baseline['rows'],manifest['rows']):
 assert re.findall(r'Base: (.*?)</li>',before['excerpt'])[0].lower()==after['base_listed']
 target=after['illustration_target'];assert before['content'].count(target)==1
 # Compare by removing precisely the replacement island of markup.
 old_parts=before['content'].split(target)
 assert after['description'].startswith(old_parts[0]) and after['description'].endswith(old_parts[1])
 inserted=after['description'][len(old_parts[0]):-len(old_parts[1])]
 assert inserted.startswith('[woodmart_gallery ') and inserted.endswith('[/vc_column_text]')
 assert 'autoplay="no"' in inserted and 'text-align: center;' in inserted
 assert after['base_listed'] in ['closed','open','open / closed']
 assert 35<=len(after['seo_title'])<=60 and 130<=len(after['meta_description'])<=160
 print(after['id'],after['name'],'original prose and other shortcode blocks preserved; listed base preserved; metadata length passed')

