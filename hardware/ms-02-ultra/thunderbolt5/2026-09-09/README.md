# MS-02 Ultra Thunderbolt 5 investigation

**2026-09-09 · Proxmox 7.0.14-16-pve · Intel Core Ultra 9 285HX**

Keeping only the discrete TB5 root port powered prevented the observed AER storm while downstream devices retained runtime power saving. Allowing the whole branch to autosuspend reproduced errors within about one second. Tests used empty Thunderbolt ports and stopped guests.

Start with the **[report](report.md)** for results, hardware details, the workaround, and limitations. The **[upstream comment](upstream-comment.md)** is a shorter version for [issue #10](https://github.com/minisforum-docs/MS-02-Ultra/issues/10).

| Folder | Contents |
|---|---|
| [data/](data/) | Timestamped measurements, with a guide to the test sequence |
| [logs/](logs/) | Sanitized error signatures and successful boot excerpt |
| [scripts/](scripts/) | Capture, reproduction, and summary scripts with usage notes |
| [config/](config/) | Final root-port-only rule and broader comparison rule |

[SHA256SUMS](SHA256SUMS) covers the files in this investigation. Verify from this directory with `sha256sum -c SHA256SUMS`.
