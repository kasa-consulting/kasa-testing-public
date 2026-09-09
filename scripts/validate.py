"""Validate public evidence without executing host-side experiments."""
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

root = Path(__file__).resolve().parent.parent
tracked = subprocess.check_output(['git', 'ls-files'], cwd=root, text=True).splitlines()
for name in tracked:
    path = root / name
    if path.suffix == '.py':
        ast.parse(path.read_text(), filename=name)
    elif path.suffix == '.jsonl':
        for line in path.read_text().splitlines():
            json.loads(line)
    elif path.suffix == '.md':
        for link in re.findall(r'\]\(([^)]+)\)', path.read_text()):
            if '://' not in link and not link.startswith('#'):
                target = link.split('#', 1)[0]
                if not (path.parent / target).exists():
                    raise ValueError(f'{name}: broken link {link}')

for manifest in root.glob('hardware/**/SHA256SUMS'):
    folder = manifest.parent
    listed = set()
    for line in manifest.read_text().splitlines():
        digest, name = line.split('  ', 1)
        if name in listed:
            raise ValueError(f'{manifest}: duplicate entry {name}')
        listed.add(name)
        path = (folder / name).resolve()
        if not path.is_relative_to(folder.resolve()):
            raise ValueError(f'{manifest}: path escapes evidence folder')
        if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError(f'{manifest}: checksum mismatch for {name}')
    actual = {str(p.relative_to(folder)) for p in folder.rglob('*')
              if p.is_file() and p != manifest}
    if actual != listed:
        raise ValueError(f'{manifest}: incomplete manifest')
    summarizer = folder / 'scripts/summarize.py'
    if summarizer.exists():
        generated = subprocess.check_output([sys.executable, str(summarizer)], text=True)
        expected = (folder / 'data/summary.jsonl').read_text()
        if generated != expected:
            raise ValueError(f'{folder}: derived summary differs from captures')

subprocess.run(['git', 'diff', '--check', 'HEAD'], cwd=root, check=True)
print('Evidence checksums, JSONL, summaries, Python syntax, and local links passed.')
