# CVE-2021-34473 — ProxyShell

**CVSS:** 9.8 | **Severity:** Critical | **Disclosed:** 2021-08-05

## Summary
ProxyShell is a chain of three vulnerabilities in Microsoft Exchange Server that, when combined, allow an unauthenticated attacker to achieve remote code execution. CVE-2021-34473 is a path confusion / SSRF vulnerability in the Exchange Client Access Service (CAS) that bypasses access controls. It is chained with CVE-2021-34523 (privilege escalation to Exchange PowerShell backend) and CVE-2021-31207 (post-authentication arbitrary file write via Export-Mailbox). Together, these allow an unauthenticated attacker to drop a webshell and execute arbitrary commands as SYSTEM.

## Affected Products
- Microsoft Exchange Server 2013 (CU 23 and earlier)
- Microsoft Exchange Server 2016 (CU 20, CU 19 and earlier)
- Microsoft Exchange Server 2019 (CU 9, CU 8 and earlier)
- Exchange Online (Microsoft 365) was NOT affected

## Attack Vector
The attacker exploits CVE-2021-34473 by sending requests to the Exchange Autodiscover endpoint with a specially crafted URL path that confuses the CAS proxy normalization logic, granting unauthenticated access to backend services. Next, CVE-2021-34523 is used to impersonate an Exchange administrator by supplying a manipulated `X-Rps-CAT` token, gaining access to Exchange PowerShell. Finally, CVE-2021-31207 abuses the `New-MailboxExportRequest` cmdlet to write an encoded webshell payload to the Exchange web directory by exporting a specially crafted mailbox draft message as a `.aspx` file. The attacker then accesses the webshell for persistent command execution.

## Detection
- Scan IIS logs for Autodiscover requests with abnormal URL encoding or path traversal patterns (e.g., `/autodiscover/autodiscover.json?@evil.com/`)
- Search for unexpected `.aspx` files in Exchange web directories: `FrontEnd\HttpProxy\owa\auth\`, `aspnet_client\`
- Windows Event Log: look for `MSExchange Management` events related to `New-MailboxExportRequest` targeting web-accessible paths
- EDR: `w3wp.exe` spawning `cmd.exe`, `powershell.exe`, or writing files to web root directories

## Remediation
- **Patch:** Install the April 2021 or July 2021 Exchange Server cumulative updates (KB5001779 for Exchange 2019 CU 9, KB5001779 for Exchange 2016 CU 20)
- **Workaround:** Restrict external access to Exchange Autodiscover and PowerShell virtual directories via IIS URL Rewrite rules; monitor for and remove any unauthorized webshells

## MITRE ATT&CK
- T1190 — Exploit Public-Facing Application
- T1505.003 — Server Software Component: Web Shell
- T1114.002 — Email Collection: Remote Email Collection
- T1068 — Exploitation for Privilege Escalation

## References
- https://nvd.nist.gov/vuln/detail/CVE-2021-34473
- https://msrc.microsoft.com/update-guide/vulnerability/CVE-2021-34473
