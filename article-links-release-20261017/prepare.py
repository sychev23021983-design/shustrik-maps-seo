from pathlib import Path
import difflib
import hashlib
import json
import re

ROOT = Path(__file__).parent
baseline = json.loads((ROOT / 'baseline.json').read_text(encoding='utf-8'))
copy = {
    14594: 'Terrain relief is one application of STL geometry. The <a href="https://shustrik-maps.com/product-category/cnc-models/">terrain STL collection</a> includes regional maps, globes and planetary surfaces for 3D printing and CNC projects.',
    14581: 'For a geographic example, the <a href="https://shustrik-maps.com/product/usa-map-3d-model/">USA terrain model</a> is supplied with C4D geometry, OBJ versions at three levels of detail and TIF textures. The illustrated <a href="https://shustrik-maps.com/how-to-convert-a-model-from-c4d-to-obj/">C4D-to-OBJ terrain workflow</a> covers mesh export and texture handling.',
    15849: 'A downloadable example is the <a href="https://shustrik-maps.com/product/usa-map-3d-model/">USA terrain model with OBJ LOD variants</a>, supplied with C4D, three OBJ detail levels and TIF textures.',
}
correction = 'Wavefront OBJ is a text-based geometry format. Material definitions are commonly stored in an associated MTL file, with texture images supplied separately.'
patches = []
diffs = []
for post in baseline['posts']:
    before = post['content']
    if post['id'] == 14594:
        start = before.index('title="3D PRINTING AN STL FILE"')
    elif post['id'] == 14581:
        start = before.index('title="OBJ FILE FORMAT: USAGE IN 3D GRAPHICS APPLICATIONS"')
    else:
        start = 0
    pos = before.index('[/woodmart_text_block]', start)
    edits = [{'operation': 'insert', 'at': pos, 'text': '\n\n<p>' + copy[post['id']] + '</p>'}]
    if post['id'] == 14581:
        start = before.index('In addition to compatibility, OBJ files are much lighter')
        end = before.index('OBJ is a fitting file format.', start) + len('OBJ is a fitting file format.')
        # The following FBX sentence is outside the approved replacement range.
        # Retain it and its existing quotation styling; do not leave an empty quote.
        assert before[end:].startswith(' In practically all other cases, FBX remains')
        old = before[start:end]
        assert old.count('<blockquote>') == 1 and 'own binary encoding' in old
        edits.append({'operation': 'replace', 'at': start, 'old': old, 'text': correction + '\n<blockquote>'})
    after = before
    for edit in edits:
        edit['at_bytes'] = len(before[:edit['at']].encode('utf-8'))
    for edit in sorted(edits, key=lambda item: item['at'], reverse=True):
        index = edit['at']
        old = edit.get('old', '')
        assert after[index:index + len(old)] == old
        after = after[:index] + edit['text'] + after[index + len(old):]
    assert re.findall(r'\[[^\]]+\]', before) == re.findall(r'\[[^\]]+\]', after)
    count = 2 if post['id'] == 14581 else 1
    assert after.count('<a ') - before.count('<a ') == count
    assert after.count('<blockquote>') == after.count('</blockquote>')
    file = str(post['id']) + '-after.txt'
    (ROOT / file).write_bytes(after.encode('utf-8'))
    patches.append({**{key: post[key] for key in ['id', 'slug', 'url', 'before_sha256', 'protected_hash']}, 'file': file, 'after_sha256': hashlib.sha256(after.encode()).hexdigest(), 'edits': edits, 'links_added': count})
    diffs.extend(difflib.unified_diff(before.splitlines(True), after.splitlines(True), fromfile=post['slug'] + '/before', tofile=post['slug'] + '/after'))
manifest = {'site': 'https://shustrik-maps.com', 'approved_date': '2026-10-17', 'backup_key': '_shustrik_article_links_backup_20261017', 'posts': patches, 'scope': 'Four approved links and exact OBJ correction; other copy, shortcodes, metadata and media retained'}
(ROOT / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8', newline='\n')
(ROOT / 'content.diff').write_text(''.join(diffs), encoding='utf-8', newline='\n')
print('Prepared three posts, four links and one exact correction; shortcode tokens and other copy preserved.')
