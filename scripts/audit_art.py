"""Inventory all legacy and review SVGs without modifying their artwork."""
from pathlib import Path
import xml.etree.ElementTree as ET
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
rows = []
issues = []
for file in sorted((ROOT / 'public/illustrations').rglob('*.svg')):
    root = ET.parse(file).getroot()
    regions = [n for n in root.iter() if 'data-region' in n.attrib]
    ids = [n.attrib['data-region'] for n in regions]
    errors = []
    if len(ids) != len(set(ids)): errors.append('duplicate region IDs')
    if root.attrib.get('viewBox') != '0 0 400 400': errors.append('unexpected viewBox')
    if any(n.tag.split('}')[-1] in ('image', 'script', 'foreignObject') for n in root.iter()): errors.append('non-vector or executable content')
    for n in regions:
        if n.tag.endswith('path'):
            subpaths = re.split(r'(?=[Mm])', n.attrib['d'])
            if any(p.strip() and not p.strip().endswith(('Z', 'z')) for p in subpaths):
                errors.append('open region: ' + n.attrib['data-region'])
    row = dict(file=str(file.relative_to(ROOT)), regions=ids, count=len(ids),
               sha256=hashlib.sha256(file.read_bytes()).hexdigest(), errors=errors)
    rows.append(row)
    issues.extend(f'{file.name}: {e}' for e in errors)
result = {'legacy_count': sum('/v2/' not in r['file'] for r in rows),
          'review_count': sum('/v2/' in r['file'] for r in rows), 'issues': issues, 'files': rows}
path = ROOT / 'docs/art-review/inventory.json'
path.write_text(json.dumps(result, indent=2) + '\n')
print(f"{result['legacy_count']} legacy SVGs, {result['review_count']} review SVGs, {len(issues)} structural issues")
if issues: print('\n'.join(issues))
# Legacy defects are reported for the rollout; new artwork must pass strictly.
raise SystemExit(any(r['errors'] for r in rows if '/v2/' in r['file']))
