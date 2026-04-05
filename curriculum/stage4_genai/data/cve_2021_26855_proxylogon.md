# CVE-2021-26855 — ProxyLogon

**CVSS:** 9.8 | **Severity:** Critical | **Disclosed:** 2021-03-02

## Summary
ProxyLogon is a server-side request forgery (SSRF) vulnerability in Microsoft Exchange Server's Client Access Service (CAS). An unauthenticated attacker sends a specially crafted HTTP request to the Exchange server, which the CAS proxy forwards to an arbitrary internal URL. This SSRF is chained with CVE-2021-27065 (arbitrary file write) to drop a webshell, granting persistent remote code execution. The vulnerability was exploited in the wild by the HAFNIUM threat group before patches were available.

## Affected Products
- Microsoft Exchange Server 2013 (CU 23 and earlier)
- Microsoft Exchange Server 2016 (CU 19, CU 18 and earlier)
- Microsoft Exchange Server 2019 (CU 8, CU 7 and earlier)
- Exchange Online (Microsoft 365) was NOT affected

## Attack Vector
The attacker sends an HTTP POST request to `/ecp/DDI/DDIService.svc/SetObject` or similar Exchange Web Services endpoints with a crafted `X-BEResource` cookie. This cookie manipulates the CAS backend routing logic, causing the server to authenticate as SYSTEM to the Exchange backend and execute Exchange PowerShell cmdlets. The attacker leverages this to write a webshell (typically `aspx`) to an accessible directory such as `C:\inetpub\wwwroot\aspnet_client\`. From the webshell, the attacker executes arbitrary operating system commands.

## Detection
- Scan IIS logs for POST requests to `/ecp/DDI/DDIService.svc` and `/owa/auth/` with abnormal `X-BEResource` or `X-AnonResource-Backend` cookies containing internal server FQDNs
- Search for unexpected `.aspx` files in `C:\inetpub\wwwroot\aspnet_client\`, `C:\Program Files\Microsoft\Exchange Server\V15\FrontEnd\HttpProxy\owa\auth\`
- Use Microsoft's EOMT (Exchange On-premises Mitigation Tool) or the Test-ProxyLogon.ps1 script
- EDR: `w3wp.exe` spawning `cmd.exe` or `powershell.exe`

## Remediation
- **Patch:** Install Exchange Server March 2021 Security Update (KB5000871 for Exchange 2016 CU 19, KB5000871 for Exchange 2019 CU 8)
- **Workaround:** Apply IIS URL Rewrite rules to block requests containing `X-AnonResource-Backend` or `X-BEResource` cookies with autodiscover patterns; restrict external access to ECP/OWA if feasible

## MITRE ATT&CK
- T1190 — Exploit Public-Facing Application
- T1505.003 — Server Software Component: Web Shell
- T1078.003 — Valid Accounts: Local Accounts (post-exploitation)

## References
- https://nvd.nist.gov/vuln/detail/CVE-2021-26855
- https://msrc.microsoft.com/update-guide/vulnerability/CVE-2021-26855
