"""Read-only, passive PCI runtime-PM and AER sampling. Run on the target host."""
import datetime
import json
import pathlib
import platform
import sys
import time

DEVICES = ['80:1b.4', '82:00.0', '83:00.0', '83:01.0', '83:02.0', '83:03.0', '84:00.0', '97:00.0']

def read(path):
    try:
        return path.read_text().strip()
    except OSError as exc:
        return 'unavailable:' + str(exc.errno)

def sample(label):
    result = {'label': label, 'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'monotonic': time.monotonic(), 'kernel': platform.release(), 'devices': {}}
    for device in DEVICES:
        path = pathlib.Path('/sys/bus/pci/devices/0000:' + device)
        result['devices'][device] = {field: read(path / field) for field in ['vendor', 'device', 'power/control', 'power/runtime_status', 'power/runtime_active_time', 'power/runtime_suspended_time', 'd3cold_allowed', 'aer_dev_correctable', 'aer_dev_nonfatal', 'aer_dev_fatal']}
        result['devices'][device]['driver'] = (path / 'driver').resolve().name if (path / 'driver').exists() else None
    return result

if __name__ == '__main__':
    label, duration, interval = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
    end = time.monotonic() + duration
    while True:
        print(json.dumps(sample(label)), flush=True)
        remaining = end - time.monotonic()
        if remaining <= 0:
            break
        time.sleep(min(interval, remaining))
