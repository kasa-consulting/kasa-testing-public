# Runtime-PM rules

- **[70-ms02-tb5-root-only.rules](70-ms02-tb5-root-only.rules): final tested workaround.** Keeps only `0000:80:1b.4` powered; descendants retain their normal runtime-PM policy.
- [70-ms02-tb5-runtime-pm.rules](70-ms02-tb5-runtime-pm.rules): broader comparison variant. Keeps the entire discrete TB5 branch powered.

These are alternative experimental configurations. The final root-only contents were deployed under `/etc/udev/rules.d/70-ms02-tb5-runtime-pm.rules` and included in the affected kernel’s initramfs. Verify PCI addresses before reuse. See the [report](../report.md) for test conditions and limits.
