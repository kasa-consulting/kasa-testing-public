# KASA public testing data

Reviewed hardware measurements and reproduction evidence for upstream investigations.

## MS-02 Ultra Thunderbolt 5 runtime PM, 2026-09-09

On Proxmox kernel `7.0.14-16-pve`, keeping only the discrete TB5 root port powered prevented the observed AER storm while downstream devices retained runtime power saving. Enabling autosuspend on the whole branch reproduced the fault within seconds. These are short tests with empty Thunderbolt ports, not peripheral compatibility validation.

- [Report and test conditions](hardware/ms-02-ultra/thunderbolt5/2026-09-09/report.md)
- [Browse the investigation](hardware/ms-02-ultra/thunderbolt5/2026-09-09/)
- [Draft upstream comment](hardware/ms-02-ultra/thunderbolt5/2026-09-09/upstream-comment.md)
- [Upstream issue](https://github.com/minisforum-docs/MS-02-Ultra/issues/10)
