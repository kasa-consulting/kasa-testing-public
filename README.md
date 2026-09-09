# KASA public testing data

Reviewed hardware measurements and reproduction evidence for upstream investigations.

## MS-02 Ultra Thunderbolt 5 runtime PM, 2026-09-09

On Proxmox kernel `7.0.14-16-pve`, keeping only the discrete TB5 root port powered prevented the observed AER storm while downstream devices retained runtime power saving. Enabling autosuspend on the whole branch reproduced the fault within seconds. These are short tests with empty Thunderbolt ports, not peripheral compatibility validation.

- [Report and test conditions](hardware/ms-02-ultra/thunderbolt5/2026-09-09/report.md)
- [Measurements, scripts, and checksums](hardware/ms-02-ultra/thunderbolt5/2026-09-09/)
- [Draft upstream comment](hardware/ms-02-ultra/thunderbolt5/2026-09-09/upstream-comment.md)
- [Upstream issue](https://github.com/minisforum-docs/MS-02-Ultra/issues/10)

`sample.py` reads sysfs counters. `wake-test.py` exercises PCI configuration reads. `experiment.py` changes runtime-PM settings and deliberately reproduces the failure in its all-auto mode; it restores the full branch to powered-on afterward. The scripts use this machine’s measured PCI addresses.

`70-ms02-tb5-root-only.rules` is the final tested workaround. `70-ms02-tb5-runtime-pm.rules` records the broader full-branch rule used for comparison. They are separate experimental variants.
