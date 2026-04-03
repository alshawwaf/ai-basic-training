# Detection Guide: PowerShell Abuse

## Overview

PowerShell is one of the most commonly abused living-off-the-land tools in modern attacks. It provides direct access to the .NET framework, Windows APIs, and remote management capabilities — all without dropping a traditional executable to disk. Detecting malicious PowerShell usage while filtering out the enormous volume of legitimate administrative use is a core SOC challenge.

## Indicators

| Source | Indicator | Description |
|--------|-----------|-------------|
| Sysmon Event 1 | Command line contains `-enc`, `-EncodedCommand`, or Base64 strings | Attackers encode commands to evade static string matching |
| PowerShell 4104 (ScriptBlock) | Script text contains `AmsiUtils`, `amsiInitFailed`, or reflection to patch AMSI | AMSI bypass disables anti-malware scanning of in-memory scripts |
| PowerShell 4104 | Script text contains `IEX`, `Invoke-Expression`, `Invoke-WebRequest`, or `Net.WebClient` | Download cradle pattern — fetches and executes remote payloads in memory |
| Sysmon Event 1 | `powershell.exe` launched with `-nop -sta -w 1` flags | Common Cobalt Strike and Empire launcher flags |
| PowerShell 4104 | Script text references `LanguageMode` or `FullLanguage` | Attempt to escape Constrained Language Mode, a security boundary |

## Detection Rules

**Rule 1 — Encoded PowerShell command execution**
```
filter:
  EventID: 1
  Image|endswith: '\powershell.exe'
  CommandLine|contains:
    - '-enc'
    - '-EncodedCommand'
    - '-ec '
condition: decoded Base64 content is not in whitelist of known admin scripts
level: high
```

**Rule 2 — AMSI bypass attempt**
```
filter:
  EventID: 4104
  ScriptBlockText|contains:
    - 'AmsiUtils'
    - 'amsiInitFailed'
    - 'SetValue($null,$true)'
    - 'Amsi.dll'
level: critical
```

**Rule 3 — Download cradle execution**
```
filter:
  EventID: 4104
  ScriptBlockText|contains|all:
    - 'Net.WebClient'
    - 'DownloadString'
  OR ScriptBlockText|re: 'IEX\s*\(.*Invoke-WebRequest'
level: high
```

## MITRE ATT&CK Mapping

| Technique ID | Name |
|-------------|------|
| T1059.001 | Command and Scripting Interpreter: PowerShell |
| T1562.001 | Impair Defenses: Disable or Modify Tools (AMSI bypass) |
| T1027 | Obfuscated Files or Information (Base64 encoding) |
| T1105 | Ingress Tool Transfer (download cradles) |

## False Positive Considerations

- Many legitimate admin scripts use `-EncodedCommand` to handle special characters in scheduled tasks. Maintain a hash-based whitelist of approved encoded scripts.
- SCCM, Intune, and DSC configurations frequently use `Invoke-WebRequest` to pull packages from internal repositories. Filter by destination URL to internal domains.
- Security tools such as Microsoft Defender for Endpoint may reference AMSI internals during self-diagnostics.

## Response Actions

1. Enable ScriptBlock logging (Event 4104) and Module logging across all endpoints if not already active.
2. Decode any Base64 content and analyse the full script for IOCs (URLs, IPs, file hashes).
3. Check whether AMSI is still functional on the affected host — run a test detection.
4. Isolate the host and identify the parent process that launched PowerShell.
5. Search for the same encoded command or script hash across all endpoints to determine blast radius.
