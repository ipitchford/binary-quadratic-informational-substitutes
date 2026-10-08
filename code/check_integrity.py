#!/usr/bin/env python3
"""Check all delivered files against MANIFEST.json; byte identity only."""
from pathlib import Path
import hashlib
import json

root=Path(__file__).resolve().parent.parent
manifest=json.loads((root/'MANIFEST.json').read_text())
bad=[]
for entry in manifest['files']:
    path=root/entry['path']
    if not path.is_file():bad.append({'path':entry['path'],'reason':'missing'});continue
    if path.stat().st_size!=entry['size_bytes'] or hashlib.sha256(path.read_bytes()).hexdigest()!=entry['sha256']:
        bad.append({'path':entry['path'],'reason':'byte mismatch'})
print(json.dumps({'status':'PASS' if not bad else 'FAIL','files_checked':len(manifest['files']),
                  'failures':bad,'scope':'Byte identity; not mathematical truth'},indent=2))
raise SystemExit(1 if bad else 0)
