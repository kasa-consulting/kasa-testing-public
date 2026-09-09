# Measurements

Read the [report](../report.md) for interpretation. Each capture is newline-delimited JSON; sample rows contain UTC time, kernel version, PCI power states, and AER counters. Event rows record test actions or the error stop threshold. Counters are cumulative within a boot.

| Test sequence | Capture | Observation |
|---|---|---|
| 1. Older-kernel baseline | [baseline-6.17-auto.jsonl](baseline-6.17-auto.jsonl) | Entire branch suspended; zero errors |
| 2. New kernel, full branch powered | [full-path-on-boot.jsonl](full-path-on-boot.jsonl) | Zero errors |
| 3. Root port powered only | [root-only.jsonl](root-only.jsonl) | Downstream suspension; zero errors |
| 4. Deliberate reproduction | [all-auto-challenge.jsonl](all-auto-challenge.jsonl) | Rapid AER errors; stopped at threshold |
| 5. Restore full-branch power | [full-path-on-recovery.jsonl](full-path-on-recovery.jsonl) | Counter settled at 129, then stayed flat |
| 6. Repeat root-only setting | [root-only-after-recovery.jsonl](root-only-after-recovery.jsonl) | No additional errors |
| 7. Boot with root-only rule | [root-only-boot-confirmed.jsonl](root-only-boot-confirmed.jsonl) | Zero errors |
| 8. Five configuration-read cycles | [root-only-config-read-cycles.jsonl](root-only-config-read-cycles.jsonl) | Bridges woke and suspended; zero errors |

[summary.jsonl](summary.jsonl) contains derived counts, durations, and observed states for all eight captures. Regenerate it with [summarize.py](../scripts/summarize.py); the raw captures remain the source of truth.
