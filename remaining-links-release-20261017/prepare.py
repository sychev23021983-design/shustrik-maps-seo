from pathlib import Path
import difflib
import hashlib
import json
import re

ROOT = Path(__file__).parent
baseline = json.loads((ROOT / 'baseline.json').read_text(encoding='utf-8'))
patches, diffs = [], []
for post in baseline['posts']:
    before = post['content']
    if post['id'] == 14596:
        marker = '<h3>3D Printing</h3>'
        index = before.index(marker, before.index('<h3>Computer Graphics</h3>'))
        text = '<p>For landscape visualization, the <a href="https://shustrik-maps.com/product-category/3d-models/">3D terrain model catalog</a> brings together geographic assets organized by region.</p>\n\n'
        edits = [{'operation': 'insert', 'at': index, 'text': text}]
        links_added = 1
    elif post['id'] == 15631:
        marker = 'In the world of 3D modeling and printing,'
        index = before.index(marker)
        text = '<p>The catalog includes <a href="https://shustrik-maps.com/product-category/3d-models/">3D terrain models</a> for visualization and a separate <a href="https://shustrik-maps.com/product-category/cnc-models/">terrain STL collection</a> for 3D printing and CNC projects.</p>\n\n'
        edits = [{'operation': 'insert', 'at': index, 'text': text}]
        links_added = 2
    elif post['id'] == 20707:
        old = '<a href="https://shustrik-maps.com/product/authagraph-world-map/">Map</a>'
        assert before.count(old) == 1
        text = '<a href="https://shustrik-maps.com/product/authagraph-world-map/">AuthaGraph world map image files (TIF/PSD)</a>'
        edits = [{'operation': 'replace', 'at': before.index(old), 'old': old, 'text': text}]
        links_added = 0
    elif post['id'] == 16110:
        old, text = 'title="Earth 3D model"', 'title="Earth terrain model without water"'
        assert before.count(old) == 1
        edits = [{'operation': 'replace', 'at': before.index(old), 'old': old, 'text': text}]
        links_added = 0
    else:
        raise AssertionError('Unexpected post')
    after = before
    for edit in edits:
        edit['at_bytes'] = len(before[:edit['at']].encode('utf-8'))
    for edit in sorted(edits, key=lambda item: item['at'], reverse=True):
        index, old = edit['at'], edit.get('old', '')
        assert after[index:index+len(old)] == old
        after = after[:index] + edit['text'] + after[index+len(old):]
    normalized = after.replace('title="Earth terrain model without water"', 'title="Earth 3D model"') if post['id'] == 16110 else after
    assert re.findall(r'\[[^\]]+\]', before) == re.findall(r'\[[^\]]+\]', normalized)
    assert after.count('<a ') - before.count('<a ') == links_added
    file = str(post['id']) + '-after.txt'
    (ROOT/file).write_bytes(after.encode('utf-8'))
    patches.append({**{key: post[key] for key in ['id','slug','post_type','url','before_sha256','protected_hash']}, 'file': file, 'after_sha256': hashlib.sha256(after.encode()).hexdigest(), 'edits': edits, 'links_added': links_added})
    diffs.extend(difflib.unified_diff(before.splitlines(True), after.splitlines(True), fromfile=post['slug']+'/before', tofile=post['slug']+'/after'))
manifest = {'site':'https://shustrik-maps.com','approved_date':'2026-10-17','backup_key':'_shustrik_remaining_links_backup_20261017','posts':patches,'scope':'L02/L06/L07: three contextual links; L08/L09: two anchor-only changes; other content/metadata/commerce/layout preserved'}
(ROOT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
(ROOT/'content.diff').write_text(''.join(diffs),encoding='utf-8',newline='\n')
print('Prepared four content changes: three new links and two anchors; prior layout preserved.')
