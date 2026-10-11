# KASA public test results

Reviewed hardware measurements, software benchmarks, and model evaluations from KASA.
Each result states its test conditions, supporting evidence, and limits. A measurement
applies to the configuration tested; a newer software release needs its own test.

## Published results

| Measured | Investigation | Result |
| --- | --- | --- |
| 2026-09-09 | [MS-02 Ultra Thunderbolt 5 runtime PM](hardware/ms-02-ultra/thunderbolt5/2026-09-09/report.md) | Keeping the discrete TB5 root port powered prevented the observed AER storm on kernel `7.0.14-16-pve` during short tests with empty ports. Peripheral compatibility was not tested. |
| 2026-09-16 | [Intel Arc Pro B65 local LLM inference, 1-4 cards: raw data](reports/2026-09-16-b65-local-llm-inference/report.md) · [file index](reports/2026-09-16-b65-local-llm-inference/README.md) | Every measured value and GPU/host telemetry trace behind https://b65.thekaiser.us. Qwen3.8-27B INT4 up to 105.9 tok/s for one user on four cards. |

New report bundles belong in [reports/](reports/README.md). The B65 inference bundle above is a
raw-data archive; the current results and their corrections are on https://b65.thekaiser.us.

## Thunderbolt investigation

On Proxmox kernel `7.0.14-16-pve`, keeping only the discrete TB5 root port powered prevented the observed AER storm while downstream devices retained runtime power saving. Enabling autosuspend on the whole branch reproduced the fault within seconds. These are short tests with empty Thunderbolt ports, not peripheral compatibility validation.

- [Report and test conditions](hardware/ms-02-ultra/thunderbolt5/2026-09-09/report.md)
- [Browse the investigation](hardware/ms-02-ultra/thunderbolt5/2026-09-09/)
- [Draft upstream comment](hardware/ms-02-ultra/thunderbolt5/2026-09-09/upstream-comment.md)
- [Upstream issue](https://github.com/minisforum-docs/MS-02-Ultra/issues/10)

## Reproduce and contribute

Start with a report's environment and reproduction instructions. Some experiments change
host configuration; read their instructions before running them. Repository validation
checks the published evidence and does not run the hardware experiments:

```sh
python3 scripts/validate.py
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for report preparation and public release review,
and [the report template](templates/report.md) for the required structure. Open an issue
for a result you cannot reproduce, with the report link and your software and hardware
versions. Use synthetic inputs and omit credentials and private logs.
