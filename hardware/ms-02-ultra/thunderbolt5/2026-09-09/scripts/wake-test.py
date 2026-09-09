"""Bounded configuration-read exercise. No PCI config writes or device resets."""
import json
import subprocess
import time
from sample import DEVICES, sample

print(json.dumps(sample('config-read-before')), flush=True)
for cycle in range(1, 6):
    for device in DEVICES:
        result = subprocess.run(['lspci', '-s', '0000:' + device, '-vv'],
                                text=True, capture_output=True, timeout=10, check=True)
        controls = [line.strip() for line in result.stdout.splitlines()
                    if any(field in line for field in ('ACSCtl:', 'DevCtl:', 'LnkCtl:'))]
        print(json.dumps({'event': 'pci-config-read', 'cycle': cycle,
                          'device': device, 'returncode': result.returncode,
                          'controls': controls}), flush=True)
    print(json.dumps(sample('config-read-cycle-' + str(cycle))), flush=True)
    time.sleep(10)
    print(json.dumps(sample('config-read-idle-' + str(cycle))), flush=True)
