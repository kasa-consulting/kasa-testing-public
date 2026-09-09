"""Summarize captured JSONL without changing target-host state."""
import json
import pathlib

here = pathlib.Path(__file__).resolve().parent

def total(row, field):
    text = row['devices']['80:1b.4'][field]
    return int(next(line.split()[1] for line in text.splitlines() if line.startswith('TOTAL_')))

for path in sorted(here.glob('*.jsonl')):
    rows = [json.loads(line) for line in path.read_text().splitlines()]
    samples = [row for row in rows if 'devices' in row]
    if not samples:
        continue
    first, last = samples[0], samples[-1]
    result = {'file': path.name, 'kernel': first['kernel'], 'samples': len(samples), 'start_utc': first['utc'], 'end_utc': last['utc'], 'duration_s': round(last['monotonic'] - first['monotonic'], 2)}
    for field in ['aer_dev_nonfatal', 'aer_dev_correctable', 'aer_dev_fatal']:
        result[field] = {'start': total(first, field), 'end': total(last, field), 'delta': total(last, field) - total(first, field)}
    result['states'] = {device: sorted(set(row['devices'][device]['power/control'] + '/' + row['devices'][device]['power/runtime_status'] for row in samples)) for device in first['devices']}
    result['events'] = [row for row in rows if 'event' in row]
    print(json.dumps(result))
