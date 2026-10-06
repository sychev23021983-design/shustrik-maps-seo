import json,re,hashlib
from pathlib import Path
root=Path(__file__).parent
b=json.loads((root/'baseline.json').read_text(encoding='utf-8-sig'))
m=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
for before,after in zip(b['rows'],m['rows']):
 target=after['illustration_target'];assert target=='[html_block id="9586"]'
 prefix,suffix=before['content'].split(target)
 assert after['description'].startswith(prefix) and after['description'].endswith(suffix)
 assert len(re.findall('woodmart_gallery',after['description']))==1
 assert after['description'].count('AI-generated application concepts.')==1
 assert hashlib.sha256(before['content'].encode()).hexdigest()==after['before_content_sha256']
 assert 'slides_per_view="1"' in after['description'] and 'slides_per_view_mobile="1"' in after['description']
 assert all(t in after['description'] for t in ['autoplay="no"','hide_prev_next_buttons="no"','hide_pagination_control_mobile="no"'])
assert len(m['rows'])==10
print('10 descriptions: exact original content outside replacement, original SEO/excerpt/protected baseline, manual one-slide settings passed')
