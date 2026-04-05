# CVE-2023-23397 — Outlook NTLM Relay Elevation of Privilege

**CVSS:** 9.8 | **Severity:** Critical | **Disclosed:** 2023-03-14

## Summary
CVE-2023-23397 is a critical elevation of privilege vulnerability in Microsoft Outlook for Windows. A specially crafted email with a malicious `PidLidReminderFileParameter` property causes Outlook to initiate an NTLM authentication handshake to an attacker-controlled SMB server when the reminder fires. This requires zero user interaction beyond receiving the email. The captured Net-NTLMv2 hash can be relayed to other services for authentication or cracked offline.

## Affected Products
- Microsoft Outlook 2013 (all editions)
- Microsoft Outlook 2016 (all editions)
- Microsoft Outlook for Microsoft 365 (Windows desktop client)
- Microsoft Outlook 2019 (all editions)
- Outlook on the Web and Outlook for macOS/iOS/Android are NOT affected

## Attack Vector
The attacker sends a calendar meeting invite, task, or note containing a `PidLidReminderFileParameter` extended MAPI property set to a UNC path (e.g., `\\attacker-server\share`). When Outlook processes the reminder, it connects to the UNC path via SMB, automatically sending the victim's Net-NTLMv2 credential hash. No user action is needed beyond the email arriving in the inbox. The attacker can relay the hash to authenticate against Exchange, LDAP, or other NTLM-accepting services, or crack it offline using tools like Hashcat.

## Detection
- Run Microsoft's CVE-2023-23397 audit script to scan Exchange mailboxes for messages containing `PidLidReminderFileParameter` with UNC paths
- Monitor outbound SMB traffic (port 445) from workstations to external or unexpected IP addresses
- EDR: detect `OUTLOOK.EXE` initiating connections to non-internal SMB destinations
- Windows Event ID 4648 (logon with explicit credentials) from the Outlook process

## Remediation
- **Patch:** Install the March 2023 Patch Tuesday update for Outlook (KB5002265 for Outlook 2016, or the Microsoft 365 Apps update)
- **Workaround:** Block outbound SMB (TCP 445) at the perimeter firewall; add users to the Protected Users security group (prevents NTLM authentication)

## MITRE ATT&CK
- T1187 — Forced Authentication
- T1557.001 — Adversary-in-the-Middle: LLMNR/NBT-NS Poisoning and SMB Relay
- T1078 — Valid Accounts (via relayed credentials)

## References
- https://nvd.nist.gov/vuln/detail/CVE-2023-23397
- https://msrc.microsoft.com/update-guide/vulnerability/CVE-2023-23397
