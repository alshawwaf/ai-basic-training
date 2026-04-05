# APT28 (Fancy Bear, Sofacy, Strontium, Forest Blizzard, Sednit)

**Attribution:** Russia / GRU Unit 26165 (85th Main Special Service Centre) | **Active Since:** 2004 | **Motivation:** Espionage, Information Operations, Destructive Attacks

## Overview
APT28 is a cyber-espionage and information operations group attributed to Russia's GRU military intelligence Unit 26165. Unlike the more stealthy SVR-linked APT29, APT28 conducts higher-tempo operations combining espionage with hack-and-leak campaigns designed to influence geopolitical outcomes. The group is prolific in credential harvesting at scale and has repeatedly targeted military, government, media, and sporting organisations worldwide.

## Known Campaigns
- **Democratic National Committee (DNC) hack (2016):** Compromised DNC networks and exfiltrated emails subsequently leaked via DCLeaks and WikiLeaks to influence the US presidential election.
- **Olympic Destroyer (2018):** Deployed destructive wiper malware against the Pyeongchang Winter Olympics opening ceremony IT infrastructure, using false flags mimicking North Korean and Chinese code artefacts.
- **Credential phishing campaigns (2015-ongoing):** Operated large-scale OAuth phishing and credential-harvesting infrastructure targeting government and military personnel across NATO and Ukraine.
- **Exploitation of edge devices (2023-2024):** Exploited vulnerabilities in Cisco routers (Jaguar Tooth malware), Outlook (CVE-2023-23397 NTLM relay), and other network perimeter devices for initial access.

## TTPs (MITRE ATT&CK)
| Tactic | Technique | Description |
|--------|-----------|-------------|
| Initial Access | T1566.002 Spearphishing Link | Credential-harvesting pages mimicking OAuth consent or webmail login portals |
| Initial Access | T1190 Exploit Public-Facing Application | Exploited Outlook NTLM relay (CVE-2023-23397) and edge device vulnerabilities |
| Persistence | T1137.002 Office Application Startup | Planted malicious Outlook Home Page rules for persistent mailbox backdoor access |
| Defence Evasion | T1036.005 Masquerading | Olympic Destroyer used code artefacts and metadata to impersonate other threat actors |
| Credential Access | T1556.007 Hybrid Identity | Abused on-prem to cloud sync to escalate from Active Directory to Azure AD |
| Exfiltration | T1048.002 Exfiltration Over Asymmetric Encrypted Non-C2 Protocol | Used legitimate cloud services for data staging and exfiltration |

## Tools and Malware
- **X-Agent (Sofacy)** — Cross-platform modular implant (Windows, Linux, iOS, Android) with keylogging, file collection, and remote shell capabilities
- **X-Tunnel** — Network tunnelling tool used to relay traffic from isolated networks through compromised hosts
- **Responder** — NTLM hash capture tool used alongside CVE-2023-23397 exploitation
- **Jaguar Tooth** — Custom malware targeting Cisco IOS routers for credential harvesting and persistent access
- **GooseEgg** — Post-exploitation tool exploiting Windows Print Spooler (CVE-2022-38028) for privilege escalation
- **Headlace** — Backdoor deployed via phishing using legitimate services as C2 infrastructure

## Detection Opportunities
- Monitor for Outlook NTLM authentication to external attacker-controlled SMB/WebDAV servers triggered by calendar invitations (CVE-2023-23397 indicator)
- Detect suspicious Outlook Home Page registry modifications under `HKCU\Software\Microsoft\Office\<version>\Outlook\WebView`
- Alert on OAuth consent grants to unfamiliar applications requesting Mail.Read or Files.ReadWrite permissions
- Inspect edge device configurations (Cisco, Ubiquiti) for unexpected SNMP community strings, GRE tunnels, or modified firmware images
- Baseline authentication patterns and flag impossible-travel logins to webmail or VPN portals
- Hunt for Print Spooler exploitation artefacts: unexpected driver installations or `spool\drivers` directory modifications
