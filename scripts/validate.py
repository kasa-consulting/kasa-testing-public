"""Validate public evidence without executing host-side experiments."""
import ast
from datetime import date
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

root = Path(__file__).resolve().parent.parent
tracked = sorted(set(subprocess.check_output(
    ['git', 'ls-files', '-z', '--cached', '--others', '--exclude-standard'],
    cwd=root, text=True).split('\0')) - {''})

# These checks catch common mistakes; release review must still inspect the contents.
secret_patterns = [
    rb'-----BEGIN (?:[A-Z ]*PRIVATE KEY|CERTIFICATE)-----',
    rb'\bgh[pousr]_[A-Za-z0-9]{30,}\b',
    rb'\bgithub_pat_[A-Za-z0-9_]{40,}\b',
    rb'\bAKIA[A-Z0-9]{16}\b',
    rb'(?i)\bAuthorization\s*[\"\']?\s*[:=]\s*[\"\']?Bearer\s+[A-Za-z0-9._~-]{20,}',
    rb'(?i)\b(?:api_key|api_token|access_token|client_secret|password)\b'
    rb'\s*[\"\']?\s*[:=]\s*[\"\']?[A-Za-z0-9_./+~=-]{20,}',
]
private_source_link = ('https://github.com/kasa-consulting/' + 'kasa-testing/').encode()
for name in tracked:
    path = root / name
    if path.is_symlink():
        raise ValueError(f'{name}: symlinks are not public evidence files')
    if path.name.startswith('.env') or path.suffix.lower() in {'.pem', '.p12', '.pfx', '.key'} \
            or path.name in {'id_rsa', 'id_ed25519', 'credentials.json'} \
            or path.name.startswith('service-account'):
        raise ValueError(f'{name}: credential-shaped filename')
    if path.stat().st_size > 95_000_000:
        raise ValueError(f'{name}: exceeds the 95 MB Git file limit')
    contents = path.read_bytes()
    if any(re.search(pattern, contents) for pattern in secret_patterns):
        raise ValueError(f'{name}: possible credential; inspect locally before publishing')
    if private_source_link in contents:
        raise ValueError(f'{name}: evidence link points at the private source repository')
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

for folder in (root / 'reports').iterdir():
    if not folder.is_dir():
        if folder.name != 'README.md':
            raise ValueError(f'{folder}: put reports inside a dated bundle directory')
        continue
    match = re.fullmatch(r'(\d{4}-\d{2}-\d{2})-[a-z0-9]+(?:-[a-z0-9]+)*', folder.name)
    if not match:
        raise ValueError(f'{folder}: expected YYYY-MM-DD-subject bundle name')
    date.fromisoformat(match.group(1))
    report = folder / 'report.md'
    if not report.is_file() or not (folder / 'SHA256SUMS').is_file():
        raise ValueError(f'{folder}: report.md and SHA256SUMS are required')
    text = report.read_text()
    measured = re.search(r'^Date:\s*(\d{4}-\d{2}-\d{2})', text, re.MULTILINE)
    if not measured:
        raise ValueError(f'{report}: Date must begin with an ISO measurement date')
    date.fromisoformat(measured.group(1))
    if not re.search(r'^Verdict:[ \t]*\S[^\n]*', text, re.MULTILINE):
        raise ValueError(f'{report}: one-line Verdict is required')
    for heading in ['Environment', 'Measurements', 'Reproduction', 'Limitations', 'Evidence']:
        if not re.search(rf'^## {heading}\s*$', text, re.MULTILINE):
            raise ValueError(f'{report}: missing {heading} section')
    if f'reports/{folder.name}/report.md' not in (root / 'README.md').read_text():
        raise ValueError(f'{report}: missing from the published-results index')

manifests = list(root.glob('hardware/**/SHA256SUMS')) + list(root.glob('reports/**/SHA256SUMS'))
for manifest in manifests:
    folder = manifest.parent
    listed = set()
    for line in manifest.read_text().splitlines():
        digest, name = line.split('  ', 1)
        path = (folder / name).resolve()
        if Path(name).is_absolute() or not path.is_relative_to(folder.resolve()):
            raise ValueError(f'{manifest}: path escapes evidence folder')
        normalized = str(path.relative_to(folder.resolve()))
        if normalized in listed:
            raise ValueError(f'{manifest}: duplicate entry {name}')
        listed.add(normalized)
        if not re.fullmatch(r'[0-9a-f]{64}', digest):
            raise ValueError(f'{manifest}: invalid SHA256 digest for {name}')
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
print('Public-file checks, report structure, evidence checksums, JSONL, summaries, '
      'Python syntax, and local links passed.')
