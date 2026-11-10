"""Check shipped developed inputs and strictly local static assets."""
import json,re,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from auctionlab.controls import controls
root=Path(__file__).resolve().parents[1];cs=controls();assert json.loads((root/'docs/controls.json').read_text())==cs
assert sorted(p.stem for p in(root/'examples').glob('*.json'))==sorted(c['id']for c in cs)
for c in cs:assert json.loads((root/'examples'/f"{c['id']}.json").read_text())==c['input']
html=(root/'docs/index.html').read_text();ids=re.findall(r'id="([^"]+)"',html);assert len(ids)==len(set(ids))
for path in re.findall(r'(?:src|href)="([^"]+)"',html):
 if not path.startswith(('http','#')):assert(root/'docs'/path).is_file(),path
for name in['README.md','MODEL.md','EVIDENCE.md','SOURCES.md','LICENSE']:
 assert(root/name).is_file()
print('ASSET_CHECK',len(cs),'controls,',len(ids),'unique DOM IDs, local links and static inputs exact')
