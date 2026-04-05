# CVE-2021-34527 — PrintNightmare

**CVSS:** 8.8 | **Severity:** High | **Disclosed:** 2021-07-01

## Summary
PrintNightmare is a remote code execution vulnerability in the Windows Print Spooler service. The flaw exists in the `RpcAddPrinterDriverEx` function, which fails to properly restrict access to authenticated users who call it with the `APD_INSTALL_WARNED_DRIVER` flag. Any authenticated domain user can install a malicious printer driver on a remote system, achieving SYSTEM-level code execution. A related local privilege escalation variant allows the same exploitation path on the local machine.

## Affected Products
- Windows 7 SP1 through Windows 10 21H1
- Windows Server 2008 R2 through Windows Server 2019
- Windows Server Core installations
- Any Windows system with the Print Spooler service running (enabled by default on all Windows systems, including domain controllers)

## Attack Vector
An authenticated low-privilege domain user calls `RpcAddPrinterDriverEx` against a target machine's Print Spooler service over SMB (port 445) or named pipes. The attacker specifies a UNC path (`\\attacker\share\malicious.dll`) as the driver path. The Spooler service loads the DLL as SYSTEM, granting full control of the target host. Public tools such as Impacket's `rpcdump.py` and custom PoC scripts automate the full attack chain. On domain controllers, this yields domain-wide compromise.

## Detection
- Monitor for new printer driver installations: Windows Event ID 316 (PrintService-Admin) and Event ID 808 (PrintService-Operational)
- Sysmon: watch for `spoolsv.exe` loading DLLs from non-standard paths or UNC shares
- EDR indicators: `spoolsv.exe` spawning child processes such as `cmd.exe`, `powershell.exe`, or `rundll32.exe`
- Network: SMB traffic to unusual or external file shares originating from the Spooler service

## Remediation
- **Patch:** Install the July 2021 out-of-band update KB5004945 (Windows 10) / KB5004953 (Server 2019) and subsequent cumulative updates
- **Workaround:** Disable the Print Spooler service on systems that do not need printing, especially domain controllers: `Stop-Service Spooler; Set-Service Spooler -StartupType Disabled`

## MITRE ATT&CK
- T1547.012 — Boot or Logon Autostart Execution: Print Processors
- T1068 — Exploitation for Privilege Escalation
- T1021.002 — Remote Services: SMB/Windows Admin Shares

## References
- https://nvd.nist.gov/vuln/detail/CVE-2021-34527
- https://msrc.microsoft.com/update-guide/vulnerability/CVE-2021-34527
