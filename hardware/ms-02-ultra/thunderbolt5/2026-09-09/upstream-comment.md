I narrowed the runtime-PM workaround on an MS-02 Ultra / 285HX, BIOS 1.04, TB5 NVM 61.83, running Proxmox `7.0.14-16-pve` with no external TB devices and all VMs stopped.

Setting **only root port `0000:80:1b.4` to `power/control=on`** prevented errors while all downstream JHL9580 bridges, NHI and xHCI retained `auto` and reached `suspended`. Two 90-second trials passed, including one after deliberately reproducing the fault.

For comparison, switching the whole branch back to `auto` produced the first nonfatal AER error in about one second and 118 within four seconds. I stopped that trial and restored the branch to `on`; the counter settled at 129 and stayed flat without a reboot. The reproduced ACS violation had TLP header `34000000 00000052 00000000 00000000`. The same branch on `6.17.13-21-pve` remained suspended with zero errors during the baseline.

I also persisted the root-only rule in the initramfs and warm-rebooted: zero AER errors during a 120-second idle observation and five subsequent PCI configuration-read cycles. Downstream bridges woke and returned to suspension after each cycle.

Root-only rule used:

```udev
ACTION=="add|bind", SUBSYSTEM=="pci", KERNEL=="0000:80:1b.4", ATTR{vendor}=="0x8086", ATTR{device}=="0x7f44", ATTR{power/control}="on"
```

AER and ACS stayed enabled; no global PM overrides. This suggests the root port's runtime-PM transition is a useful place to investigate. These are short tests with empty ports, not validation of attached Thunderbolt devices. Timestamped sysfs counter/state samples and the test scripts are attached.
