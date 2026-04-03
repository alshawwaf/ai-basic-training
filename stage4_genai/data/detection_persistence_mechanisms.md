# Detection Guide: Persistence Mechanisms

## Overview

Persistence allows an attacker to maintain access to a compromised system across reboots, credential changes, and remediation attempts. Attackers install persistence early in the kill chain to ensure they can return even if their initial access vector is closed. Detecting persistence creation is high-value because it often occurs in a narrow window and leaves durable forensic artefacts.

## Indicators

| Source | Indicator | Description |
|--------|-----------|-------------|
| Sysmon Event 1 | `schtasks.exe /create` with suspicious arguments | Scheduled task creation used to run payloads at logon, startup, or on a timer |
| Sysmon Event 13 | Registry path contains `\CurrentVersion\Run` or `\CurrentVersion\RunOnce` | Registry Run key modification to auto-start a binary on user logon |
| WMI Event (Sysmon 19/20/21) | `WmiEventSubscription` created with `CommandLineTemplate` | WMI event subscription that executes a command when a system event fires |
| Sysmon Event 11 | File created in `shell:startup` folder | Executables or scripts dropped into the Startup folder for auto-execution |
| System Event 7045 | New service installed with unusual binary path | Service creation pointing to a non-standard path such as `%TEMP%` or `%APPDATA%` |

## Detection Rules

**Rule 1 — Suspicious scheduled task creation**
```
filter:
  EventID: 1
  Image|endswith: '\schtasks.exe'
  CommandLine|contains: '/create'
  CommandLine|contains:
    - '%APPDATA%'
    - '%TEMP%'
    - 'powershell'
    - 'cmd.exe /c'
    - 'mshta'
    - 'rundll32'
level: high
```

**Rule 2 — Registry Run key modification**
```
filter:
  EventID: 13
  TargetObject|contains:
    - '\CurrentVersion\Run\'
    - '\CurrentVersion\RunOnce\'
  Details|contains:
    - 'powershell'
    - 'cmd.exe'
    - 'mshta'
    - 'wscript'
    - '%APPDATA%'
    - '%TEMP%'
level: high
```

**Rule 3 — WMI event subscription creation**
```
filter:
  EventID:
    - 19  # WmiEventFilter
    - 20  # WmiEventConsumer
    - 21  # WmiEventConsumerToFilter
condition: any WMI subscription creation outside of known management tools
level: critical
```

## MITRE ATT&CK Mapping

| Technique ID | Name |
|-------------|------|
| T1053.005 | Scheduled Task/Job: Scheduled Task |
| T1547.001 | Boot or Logon Autostart Execution: Registry Run Keys |
| T1546.003 | Event Triggered Execution: WMI Event Subscription |
| T1547.001 | Boot or Logon Autostart Execution: Startup Folder |
| T1543.003 | Create or Modify System Process: Windows Service |

## False Positive Considerations

- Software installers and updaters (Chrome, Adobe, Java) routinely create scheduled tasks and Run keys. Whitelist by publisher signature and known installation paths.
- Enterprise management tools (SCCM, GPO, Intune) create WMI subscriptions and scheduled tasks for policy enforcement. Filter by the originating management server or known task names.
- Developers may add startup items during application testing. Baseline typical developer workstation behaviour and alert only on deviations.

## Response Actions

1. Identify the exact persistence artefact — capture the scheduled task XML, registry value, WMI subscription filter/consumer, or service binary path.
2. Determine when the persistence was installed and correlate with other host activity at that timestamp.
3. Remove the persistence mechanism and quarantine the referenced payload binary.
4. Scan the binary hash against threat intelligence feeds and submit to a sandbox.
5. Search all endpoints for the same persistence artefact (task name, registry value, service name) to identify additional compromised hosts.
