# LockBit (LockBit 2.0, LockBit 3.0 / LockBit Black, LockBit Green)

**Attribution:** Ransomware-as-a-Service (RaaS), Russian-speaking administrators, global affiliate network | **Active Since:** 2019 | **Motivation:** Financial (Extortion)

## Overview
LockBit is a Ransomware-as-a-Service operation that became the most deployed ransomware variant globally between 2022 and 2024. The operation runs an affiliate model where the core developers provide the ransomware payload, leak site infrastructure, and negotiation services in exchange for a percentage of ransom payments (typically 20%). LockBit distinguished itself through fast encryption speeds, a public-facing administrator ("LockBitSupp"), and a bug bounty programme for its malware. In February 2024, Operation Cronos disrupted LockBit infrastructure, though the group attempted to reconstitute operations.

## Known Campaigns
- **LockBit 2.0 expansion (2021-2022):** Introduced StealBit automated data exfiltration and aggressive affiliate recruitment, becoming the most prolific ransomware operation by victim count.
- **LockBit 3.0 / LockBit Black (2022):** Released rebuilt ransomware incorporating anti-analysis techniques borrowed from BlackMatter/DarkSide, along with the first ransomware bug bounty programme.
- **Royal Mail attack (January 2023):** Disrupted UK Royal Mail international shipping operations for weeks, demanding $80 million ransom.
- **Operation Cronos takedown (February 2024):** Law enforcement coalition led by the UK NCA and FBI seized LockBit infrastructure, obtained 2,500 decryption keys, unmasked affiliates, and revealed the identity of administrator Dmitry Khoroshev (LockBitSupp), who was subsequently sanctioned and indicted.

## TTPs (MITRE ATT&CK)
| Tactic | Technique | Description |
|--------|-----------|-------------|
| Initial Access | T1133 External Remote Services | Affiliates commonly exploit exposed RDP, VPN (Citrix, Fortinet), and other remote access services |
| Execution | T1059.001 PowerShell | PowerShell scripts for disabling security tools, deleting shadow copies, and deploying payloads |
| Persistence | T1136.001 Local Account | Creation of local admin accounts for backup access if primary credentials are reset |
| Defence Evasion | T1562.001 Disable or Modify Tools | Terminates EDR processes, disables Windows Defender, and uses BYOVD (Bring Your Own Vulnerable Driver) to kill security software |
| Exfiltration | T1567.002 Exfiltration to Cloud Storage | StealBit tool and cloud upload utilities stage stolen data before encryption begins |
| Impact | T1486 Data Encrypted for Impact | Fast multi-threaded encryption using AES-256 and RSA-2048; partial file encryption for speed |

## Tools and Malware
- **LockBit 3.0 (LockBit Black)** — Primary ransomware payload with anti-debugging, code obfuscation, and self-spreading via SMB and Group Policy
- **StealBit** — Custom data exfiltration tool that automatically identifies and uploads valuable files before encryption
- **Cobalt Strike** — Heavily used by affiliates for post-exploitation, lateral movement, and C2
- **Mimikatz** — Credential dumping for privilege escalation and lateral movement
- **PsExec / WMIC** — Lateral deployment of ransomware across domain-joined systems
- **Process Hacker / Defender Control** — Security tool disablement utilities

## Detection Opportunities
- Monitor for Group Policy Object (GPO) modifications that deploy scripts or scheduled tasks to domain-joined endpoints (common LockBit propagation method)
- Alert on volume shadow copy deletion commands: `vssadmin delete shadows /all /quiet` and `wmic shadowcopy delete`
- Detect BYOVD attacks by monitoring driver loads for known vulnerable drivers (e.g., Process Explorer driver, RentDrv2)
- Flag high-volume file rename operations with common LockBit extensions (.lockbit, .lock3) or ransom note file creation across multiple directories simultaneously
- Monitor for StealBit indicators: rapid sequential file reads followed by large outbound data transfers to uncommon destinations
- Implement canary files in network shares; alert when these files are accessed or modified, indicating ransomware traversal
