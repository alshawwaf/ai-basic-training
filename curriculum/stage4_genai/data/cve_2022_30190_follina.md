# CVE-2022-30190 — Follina

**CVSS:** 7.8 | **Severity:** High | **Disclosed:** 2022-05-27

## Summary
Follina is a remote code execution vulnerability in the Microsoft Windows Support Diagnostic Tool (MSDT). An attacker crafts a malicious Office document that uses the `ms-msdt:` protocol handler to invoke MSDT with arguments that execute arbitrary PowerShell code. Exploitation requires no macros and can be triggered simply by previewing the document in Windows Explorer or opening it in a supported Office application.

## Affected Products
- Microsoft Windows 7 through Windows 11
- Windows Server 2008 R2 through Windows Server 2022
- Microsoft Office 2013, 2016, 2019, 2021, and Microsoft 365
- Any application that processes OLE objects referencing the `ms-msdt:` URI handler

## Attack Vector
The attacker sends a Word document (`.docx`) containing an OLE object or HTML template reference that points to an external server. The external HTML triggers the `ms-msdt:/id PCWDiagnostic` protocol with a crafted `/param` argument embedding encoded PowerShell commands. When the victim opens or previews the document, MSDT launches and executes the attacker's commands under the current user's privileges. No macro execution or special user interaction beyond opening the file is required.

## Detection
- Monitor process trees for `msdt.exe` spawned by `WINWORD.EXE`, `EXCEL.EXE`, `OUTLOOK.EXE`, or `explorer.exe`
- Detect command-line arguments to `msdt.exe` containing `IT_BrowseForFile=` with embedded script content
- Network signatures: Office applications making HTTP requests to retrieve remote HTML templates
- Sysmon Event ID 1: look for `msdt.exe` with unusual `/param` flags

## Remediation
- **Patch:** Install the June 2022 cumulative update (KB5014699 for Windows 10 21H2, KB5014697 for Windows 11)
- **Workaround:** Disable the MSDT URL protocol by deleting the registry key `HKEY_CLASSES_ROOT\ms-msdt` (back up first: `reg export HKEY_CLASSES_ROOT\ms-msdt ms-msdt-backup.reg`)

## MITRE ATT&CK
- T1203 — Exploitation for Client Execution
- T1221 — Template Injection
- T1059.001 — Command and Scripting Interpreter: PowerShell
- T1566.001 — Phishing: Spearphishing Attachment

## References
- https://nvd.nist.gov/vuln/detail/CVE-2022-30190
- https://msrc.microsoft.com/update-guide/vulnerability/CVE-2022-30190
