# Detection Guide: Lateral Movement

## Overview

Lateral movement is how attackers expand their foothold from an initial compromised host to other systems across the network. Detecting lateral movement is critical because it typically occurs between the initial compromise and the attacker reaching their objective — making it one of the last opportunities to contain an incident before major damage.

## Indicators

| Source | Indicator | Description |
|--------|-----------|-------------|
| Sysmon Event 1 / System 7045 | Service name `PSEXESVC` created | PsExec remote execution creates a temporary service on the target |
| Sysmon Event 1 | `wmiprvse.exe` spawning `cmd.exe` or `powershell.exe` | WMI-based remote process creation |
| Windows Security 4625 | Multiple Type 10 (RemoteInteractive) logon failures | RDP brute-force attempts against a single host |
| Windows Security 4624 | Type 3 logon to `ADMIN$` or `C$` share | Administrative share access from a workstation (not a server) |
| Windows Security 4624 | Type 3 logon where `LogonProcessName` is `NtLmSsp` and source is unexpected | Pass-the-hash — NTLM authentication from hosts that normally use Kerberos |

## Detection Rules

**Rule 1 — PsExec service installation**
```
filter:
  source: System
  EventID: 7045
  ServiceName|contains: 'PSEXE'
  ServiceFileName|contains: 'PSEXESVC'
level: high
```

**Rule 2 — WMI remote process creation**
```
filter:
  EventID: 1
  ParentImage|endswith: '\wmiprvse.exe'
  Image|endswith:
    - '\cmd.exe'
    - '\powershell.exe'
condition: parent WMI provider host spawning a shell
level: medium
```

**Rule 3 — Admin share access from workstation**
```
filter:
  EventID: 5140
  ShareName|contains:
    - 'ADMIN$'
    - 'C$'
  SubjectUserName|not_endswith: '$'
condition: source IP belongs to workstation subnet, not server/admin subnet
level: high
```

## MITRE ATT&CK Mapping

| Technique ID | Name |
|-------------|------|
| T1021.002 | Remote Services: SMB/Windows Admin Shares |
| T1021.001 | Remote Services: Remote Desktop Protocol |
| T1047 | Windows Management Instrumentation |
| T1569.002 | System Services: Service Execution |
| T1550.002 | Use Alternate Authentication Material: Pass the Hash |

## False Positive Considerations

- System administrators legitimately use PsExec and WMI for remote management. Baseline normal admin tooling and restrict alerts to non-admin source accounts or unexpected source hosts.
- RDP brute-force alerts can fire during legitimate password resets or account lockout troubleshooting.
- Automated deployment tools (SCCM, Ansible, GPO scripts) access admin shares during software distribution.

## Response Actions

1. Correlate the source host — check whether it has existing alerts for credential dumping or initial access.
2. Validate the user account against authorised administrators for the target system.
3. If unauthorised, disable the account and isolate both source and destination hosts.
4. Audit all systems the compromised account has accessed in the last 24-48 hours.
5. Check for persistence mechanisms installed on newly accessed hosts.
