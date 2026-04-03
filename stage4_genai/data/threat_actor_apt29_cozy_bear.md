# APT29 (Cozy Bear, Nobelium, Midnight Blizzard, The Dukes)

**Attribution:** Russia / SVR (Foreign Intelligence Service) | **Active Since:** 2008 | **Motivation:** Espionage

## Overview
APT29 is a sophisticated cyber-espionage group attributed to Russia's Foreign Intelligence Service (SVR). The group targets government networks, think tanks, and technology companies across NATO member states, prioritising long-term stealth over rapid exploitation. APT29 is distinguished by its operational discipline, minimal tooling reuse, and patience in maintaining persistent access for months or years before acting on objectives.

## Known Campaigns
- **SolarWinds supply chain compromise (2020):** Trojanised the Orion software update (SUNBURST backdoor), compromising approximately 18,000 organisations including US Treasury, DHS, and FireEye.
- **COVID-19 vaccine research targeting (2020):** Targeted pharmaceutical companies and research institutions in the US, UK, and Canada developing COVID-19 vaccines, using custom malware (WellMess, WellMail).
- **Microsoft 365 and Azure AD abuse (2021-2024):** Leveraged OAuth application permissions, tenant-to-tenant compromise, and stolen authentication tokens to access email and cloud resources of government agencies and Microsoft corporate systems.
- **European diplomatic institution targeting (2023):** Spear-phished diplomats using fake embassy event invitations delivering ROOTSAW/EnvyScout HTML smuggling payloads.

## TTPs (MITRE ATT&CK)
| Tactic | Technique | Description |
|--------|-----------|-------------|
| Initial Access | T1195.002 Supply Chain Compromise | Trojanised trusted vendor software updates |
| Persistence | T1098.003 Additional Cloud Roles | Granted OAuth app permissions for persistent mailbox access |
| Defence Evasion | T1027.006 HTML Smuggling | Delivered payloads via embedded encoded blobs in HTML attachments |
| Credential Access | T1528 Steal Application Access Token | Harvested OAuth tokens and SAML signing certificates (Golden SAML) |
| Lateral Movement | T1021.007 Cloud Service Authentication | Moved between Azure AD tenants using stolen credentials |
| Collection | T1114.002 Remote Email Collection | Exfiltrated targeted mailboxes via Microsoft Graph API |

## Tools and Malware
- **SUNBURST** — Backdoor implanted in SolarWinds Orion DLL, used DNS beaconing for C2
- **TEARDROP / Raindrop** — In-memory-only loaders deploying Cobalt Strike beacons
- **WellMess / WellMail** — Custom Go/Dotnet RATs used in vaccine research targeting
- **EnvyScout (ROOTSAW)** — HTML smuggling dropper delivered via spear-phishing
- **MagicWeb** — Malicious DLL replacing legitimate Azure AD FS component for persistent authentication manipulation
- **Brute Ratel C4** — Commercial adversary-simulation framework used as Cobalt Strike alternative

## Detection Opportunities
- Monitor Azure AD audit logs for anomalous OAuth application permission grants (Application.ReadWrite.All, Mail.Read)
- Alert on SAML token anomalies: token lifetimes exceeding policy, tokens issued by unexpected identity providers, or claims mismatch
- Inspect outbound DNS for high-entropy subdomain queries consistent with DNS-based C2 beaconing patterns
- Detect HTML smuggling by scanning inbound email attachments for JavaScript blob construction and Base64-encoded executables
- Monitor Microsoft Graph API calls for bulk mailbox access originating from unexpected service principals or IP ranges
- Baseline legitimate SolarWinds Orion network behaviour and alert on new external connections from Orion servers
