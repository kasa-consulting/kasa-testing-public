# MS-02 Ultra TB5 runtime-PM investigation

Date: 2026-09-09. Related upstream discussion: https://github.com/minisforum-docs/MS-02-Ultra/issues/10

Verdict: Keeping only PCIe root port `0000:80:1b.4` at `power/control=on` prevented the observed AER storm on `7.0.14-16-pve`, while downstream TB5 devices retained `auto` and reached `suspended`. Allowing the root port to autosuspend reproduced the storm within about one second. Restoring the whole branch to `on` stopped additional errors without rebooting.

## Environment and test conditions

- Minisforum MS-02 Ultra, Intel Core Ultra 9 285HX.
- BIOS 1.04 (2026-04-21), firmware revision 0.19; discrete JHL9580 TB5 NVM 61.83.
- Root port `80:1b.4` (`8086:7f44`); bridges `82:00.0`, `83:00.0`–`83:03.0` (`8086:5780`); NHI `84:00.0` (`8086:5781`, thunderbolt); USB controller `97:00.0` (`8086:5782`, xhci_hcd).
- No external Thunderbolt devices enumerated. Guests stopped throughout these tests; guest autostart disabled.
- AER and ACS remained enabled. No `pci=noaer`, ACS override, global PM disable, or Thunderbolt driver blacklist. Root-port ASPM was already disabled before this experiment.
- Counters sampled passively from PCI sysfs, including runtime status and accumulated runtime active/suspended time. PCI configuration-space reads were excluded from idle sampling.

## Controlled comparisons

| Kernel | Runtime-PM setting | Observation | Root-port AER result |
|---|---|---|---|
| 6.17.13-21-pve | Entire branch `auto` | 60 s; all devices suspended | Zero correctable, nonfatal and fatal errors |
| 7.0.14-16-pve | Entire branch `on`, set during boot | 120 s | Zero errors |
| 7.0.14-16-pve | Root port `on`, descendants `auto` | 90 s; descendants suspended | Zero errors |
| 7.0.14-16-pve | Entire branch switched to `auto` | Aborted after 4.1 s at the error threshold | 118 nonfatal errors at abort; 126 immediately after restoration, settling at 129; one correctable, zero fatal |
| 7.0.14-16-pve | Entire branch restored to `on` | 60 s, same boot | Nonfatal counter stayed at 129; no additional errors |
| 7.0.14-16-pve | Root port `on`, descendants `auto`, repeated after recovery | 90 s; descendants suspended | No additional errors |
| 7.0.14-16-pve | Root-only rule persisted in initramfs, warm reboot | 120 s passive observation; all descendants suspended | Zero errors since boot |
| 7.0.14-16-pve | Root-only rule; five configuration-read cycles across all eight devices | 53.2 s; downstream bridges woke and returned to suspension after each cycle | Zero errors |

The all-auto test used one-second sampling, a 100-nonfatal-error stop threshold, and an independent timed restoration watchdog. Restoring `on` allowed a few already-in-flight errors before counters stabilized. Initial all-auto nonfatal counts were 0, 1, 36, 76 and 118 at roughly one-second intervals.

The reproduced logs include `ACSViol`, `UnsupReq`, missing `error_detected` callbacks for thunderbolt/xHCI, and failed PCI recovery. The ACS violation TLP header was `34000000 00000052 00000000 00000000`.

## Narrow workaround

The [final persistent rule](config/70-ms02-tb5-root-only.rules) targets the discrete TB5 root port only:

```udev
ACTION=="add|bind", SUBSYSTEM=="pci", KERNEL=="0000:80:1b.4", ATTR{vendor}=="0x8086", ATTR{device}=="0x7f44", ATTR{power/control}="on"
```

Install in `/etc/udev/rules.d/70-ms02-tb5-runtime-pm.rules` and regenerate the affected kernel's initramfs so it also applies during early boot. The PCI address must be verified on another machine before reusing this rule. This rule prevents runtime suspension of one root port; it does not disable the Thunderbolt controller or suppress error reporting.

## Interpretation and limits

The reversible comparison implicates runtime PM of the root port or its interaction with the TB5 branch. It does not identify the faulty source-code change, prove which device sends the offending transaction, or distinguish a firmware defect from a kernel regression.

These are short host-side idle and PM-transition tests. They do not validate Thunderbolt hotplug, external peripherals, sustained transfer, system sleep, cold AC-power boot, or guest workloads. No upstream fix is claimed.

The final boot also logged a separate i915 `assert_dmc_loaded` warning (`DMC 1 program storage start incorrect`) and Intel ICE LLDP-filter fallback messages. These were outside the TB5 experiment; a clean TB5 result does not mean the entire kernel log was warning-free.

[Raw JSONL files](data/) contain the complete sampled counters and states. Private host inventory and unredacted administrative logs are excluded from the shareable bundle.

## Final host disposition

Running and default-pinned kernel: `7.0.14-16-pve`. The root-port-only rule is installed and included in this kernel’s initramfs. `6.17.13-21-pve` remains installed as a fallback. The guest remains stopped with autostart disabled. Final checks showed zero root-port AER counters, healthy ZFS pools and cluster quorum.
