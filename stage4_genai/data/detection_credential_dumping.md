# Detection Guide: Credential Dumping

## Overview

Credential dumping is the extraction of authentication material — passwords, hashes, or Kerberos tickets — from operating system memory or storage. Attackers use dumped credentials to escalate privileges and move laterally. Because a single compromised domain admin hash can give an attacker full control of an Active Directory environment, detecting credential dumping early is one of the highest-value activities in a SOC.

## Indicators

| Source | Indicator | Description |
|--------|-----------|-------------|
| Sysmon Event 10 | `TargetImage` ends with `lsass.exe` | Any process opening a handle to LSASS with `PROCESS_VM_READ` access |
| Windows Security 4656/4663 | Object access to `SAM`, `SECURITY`, or `SYSTEM` hives | Registry export of credential stores via `reg save` or `reg export` |
| Windows Security 4662 | `DS-Replication-Get-Changes-All` property access | DCSync — a non-DC machine requesting AD replication |
| Sysmon Event 1 | Process command line contains `sekurlsa`, `lsadump`, or `kerberos::` | Mimikatz module invocation patterns |
| Sysmon Event 7 | Unsigned DLL loaded into LSASS | Credential-stealing SSP injection |

## Detection Rules

**Rule 1 — LSASS handle access from non-system process**
```
filter:
  EventID: 10
  TargetImage|endswith: '\lsass.exe'
  GrantedAccess|contains:
    - '0x1010'
    - '0x1410'
    - '0x1438'
  SourceImage|not_endswith:
    - '\csrss.exe'
    - '\svchost.exe'
    - '\MsMpEng.exe'
level: high
```

**Rule 2 — DCSync replication request from non-DC**
```
filter:
  EventID: 4662
  Properties|contains: 'DS-Replication-Get-Changes-All'
  SubjectUserName|not_endswith: '$'
condition: source host is not a domain controller
level: critical
```

**Rule 3 — SAM registry hive export**
```
filter:
  EventID: 1
  CommandLine|contains|all:
    - 'reg'
    - 'save'
    - '\sam'
level: high
```

## MITRE ATT&CK Mapping

| Technique ID | Name |
|-------------|------|
| T1003.001 | OS Credential Dumping: LSASS Memory |
| T1003.002 | OS Credential Dumping: Security Account Manager |
| T1003.006 | OS Credential Dumping: DCSync |

## False Positive Considerations

- Endpoint protection products (EDR, AV) legitimately open handles to LSASS for scanning. Whitelist known security tooling by `SourceImage` path and code-signing certificate.
- Backup utilities such as `ntdsutil` may trigger replication-related events during authorised AD maintenance windows.
- IT administrators running `reg save` during legitimate forensic or migration tasks.

## Response Actions

1. Immediately isolate the source host from the network.
2. Identify the account context — determine which user or service account initiated the dumping.
3. Force a password reset for any accounts whose credentials may have been exposed.
4. If DCSync is confirmed, audit all domain admin and service accounts for unauthorised changes.
5. Preserve memory and disk images for forensic analysis before reimaging.
