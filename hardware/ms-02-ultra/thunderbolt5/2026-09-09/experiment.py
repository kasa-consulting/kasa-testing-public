"""Bounded PM experiments with an independent systemd restoration timer.

Requires sample.py alongside this script. Emits JSONL. Never resets/removes PCI
devices or starts guests. Restores the complete branch to power/control=on.
"""
import json
import pathlib
import platform
import subprocess
import sys
import time
from sample import DEVICES, sample

mode = sys.argv[1]
duration = int(sys.argv[2])
assert mode in ('root-only', 'all-auto') and 1 <= duration <= 120
assert platform.release() == '7.0.14-16-pve'
for command in (['qm', 'list'], ['pct', 'list']):
    assert 'running' not in subprocess.check_output(command, text=True), 'Guests must remain stopped'
paths = [pathlib.Path('/sys/bus/pci/devices/0000:' + d + '/power/control') for d in DEVICES]
assert all(p.exists() for p in paths)

def restore():
    for p in paths:
        p.write_text('on')

restore_code = 'import pathlib; ' + '; '.join('pathlib.Path(' + repr(str(p)) + ').write_text("on")' for p in paths)
unit = 'kasa-tb5-restore-' + str(int(time.time()))
subprocess.run(['systemd-run', '--quiet', '--unit=' + unit, '--on-active=' + str(duration + 15) + 's', '/usr/bin/python3', '-c', restore_code], check=True)

def count(snapshot):
    raw = snapshot['devices']['80:1b.4']['aer_dev_nonfatal']
    return int(next(x.split()[1] for x in raw.splitlines() if x.startswith('TOTAL_ERR_NONFATAL ')))

try:
    restore()
    start = sample(mode + '-before')
    initial = count(start)
    print(json.dumps(start), flush=True)
    for index, p in reversed(list(enumerate(paths))):
        p.write_text('on' if mode == 'root-only' and index == 0 else 'auto')
    end = time.monotonic() + duration
    while True:
        s = sample(mode)
        print(json.dumps(s), flush=True)
        if count(s) - initial >= 100:
            print(json.dumps({'event': 'error-limit-reached', 'delta': count(s) - initial}), flush=True)
            break
        remaining = end - time.monotonic()
        if remaining <= 0:
            break
        time.sleep(min(1, remaining))
finally:
    restore()
    print(json.dumps(sample(mode + '-restored')), flush=True)
    subprocess.run(['systemctl', 'stop', unit + '.timer'], check=True)
