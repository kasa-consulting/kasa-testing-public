# Test scripts

These scripts record the procedure used for this investigation. They assume the PCI addresses listed in the [report](../report.md).

| Script | Purpose | Changes host state? |
|---|---|---|
| [sample.py](sample.py) | Passively sample sysfs power states and AER counters | No |
| [summarize.py](summarize.py) | Summarize the captures in `../data/` | No |
| [wake-test.py](wake-test.py) | Five PCI configuration-read cycles, with idle observations | Reads can wake devices; no PCI configuration writes |
| [experiment.py](experiment.py) | Bounded root-only or all-auto runtime-PM trial | Yes; changes power control and restores the entire branch to `on` |

From the investigation directory, regenerate the summary locally:

```sh
python3 scripts/summarize.py > /tmp/ms02-tb5-summary.jsonl
diff -u data/summary.jsonl /tmp/ms02-tb5-summary.jsonl
```

For passive capture on the target host, use `python3 sample.py LABEL DURATION_SECONDS INTERVAL_SECONDS`, for example `python3 sample.py idle 120 5`.

`wake-test.py` requires `sample.py` beside it and `lspci` on the host. `experiment.py` likewise imports `sample.py`; its arguments are `root-only` or `all-auto`, followed by a duration of 1–120 seconds. It checks for kernel `7.0.14-16-pve` and stopped Proxmox guests, installs a timed restoration watchdog, and stops at 100 additional nonfatal errors. **All-auto deliberately reproduces the failure.** Neither experiment mode leaves the final root-only policy in place: both restore the full branch to `on`.
