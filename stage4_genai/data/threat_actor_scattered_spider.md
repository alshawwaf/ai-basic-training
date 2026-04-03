# Scattered Spider (UNC3944, Roasted 0ktapus, Octo Tempest, Star Fraud)

**Attribution:** Loosely organised English-speaking threat actors, primarily US/UK-based young adults | **Active Since:** 2022 | **Motivation:** Financial (Extortion, Fraud, Cryptocurrency Theft)

## Overview
Scattered Spider is a loosely affiliated group of young, predominantly English-speaking threat actors known for exceptionally effective social engineering. Unlike traditional cybercriminal groups, their native English fluency and deep familiarity with enterprise IT helpdesk procedures allow them to bypass identity verification processes that would typically stop non-native speakers. The group escalated from SIM swapping and cryptocurrency theft to major enterprise ransomware operations through affiliation with ALPHV/BlackCat. Microsoft has called them "one of the most dangerous financial criminal groups."

## Known Campaigns
- **0ktapus campaign (2022):** Mass phishing campaign impersonating Okta login pages, compromising over 130 organisations including Twilio, Cloudflare, and Mailchimp through SMS-based credential phishing and real-time OTP relay.
- **MGM Resorts attack (September 2023):** Social-engineered the MGM IT helpdesk via a phone call to reset an employee's MFA, then deployed ALPHV/BlackCat ransomware, causing an estimated $100 million in losses and 10 days of operational disruption across casinos and hotels.
- **Caesars Entertainment breach (September 2023):** Compromised Caesars using similar social engineering techniques; Caesars reportedly paid approximately $15 million ransom to prevent data publication.
- **Ongoing identity provider targeting (2023-2024):** Persistent campaigns against Okta customer support portals, Azure AD, and other identity platforms to steal session tokens and HAR files for downstream access.

## TTPs (MITRE ATT&CK)
| Tactic | Technique | Description |
|--------|-----------|-------------|
| Initial Access | T1566.004 Spearphishing Voice (Vishing) | Called IT helpdesks impersonating employees to trigger MFA resets and credential recovery |
| Initial Access | T1078.004 Cloud Accounts | Used stolen credentials and session cookies to access cloud identity providers directly |
| Persistence | T1098.001 Additional Cloud Credentials | Registered new MFA devices and federated identity providers on compromised accounts |
| Credential Access | T1111 Multi-Factor Authentication Interception | Real-time OTP phishing relay using custom phishing kits (e.g., EvilProxy) and MFA fatigue/push bombing |
| Lateral Movement | T1021.004 SSH | Leveraged existing SSH keys and cloud management consoles to move through infrastructure |
| Impact | T1486 Data Encrypted for Impact | Deployed ALPHV/BlackCat ransomware for double extortion after data exfiltration |

## Tools and Malware
- **Custom Okta/Azure phishing kits** — Real-time credential and OTP relay pages with convincing replicas of corporate SSO login portals
- **ALPHV/BlackCat ransomware** — Rust-based ransomware deployed as an affiliate for double extortion operations
- **SIM swapping infrastructure** — Social engineering of mobile carrier employees to port victim phone numbers for SMS-based MFA bypass
- **AnyDesk / Splashtop / RustDesk** — Legitimate remote access tools installed for persistent access that blends with normal IT operations
- **Mimikatz / Impacket** — Standard credential extraction and lateral movement tooling in Windows/Active Directory environments
- **Tailscale / Cloudflare Tunnel** — Mesh VPN and tunnel tools used to maintain covert access channels from attacker infrastructure

## Detection Opportunities
- Implement out-of-band verification for all helpdesk password and MFA reset requests (callback to registered number, manager approval, or in-person verification)
- Monitor identity provider audit logs for anomalous MFA device registrations, especially new device enrolments shortly after helpdesk interactions
- Alert on federated identity provider configuration changes in Azure AD/Entra ID or Okta (new SAML/OIDC providers added)
- Detect installation of unauthorised remote access tools (AnyDesk, RustDesk, Splashtop) on endpoints that do not normally use them
- Flag impossible-travel scenarios: logins from geographic locations inconsistent with the employee's known location within short time windows
- Monitor for bulk data access or download patterns from SharePoint, OneDrive, or internal documentation systems following account compromise
