# Security Document Corpus

> **Purpose:** RAG training corpus for Stage 4 exercises and the Capstone Demo

This folder contains 25 curated security documents that participants load into their RAG pipelines. The documents are intentionally varied in format and length to give the retrieval engine a realistic challenge.

---

## Document Inventory

### CVE Advisories (10)

| File | CVE | Vulnerability | CVSS |
|------|-----|---------------|------|
| `cve_2020_1472_zerologon.md` | CVE-2020-1472 | Netlogon privilege escalation | 10.0 |
| `cve_2021_26855_proxylogon.md` | CVE-2021-26855 | Exchange Server SSRF to RCE | 9.8 |
| `cve_2021_34473_proxyshell.md` | CVE-2021-34473 | Exchange ProxyShell chain | 9.8 |
| `cve_2021_34527_printnightmare.md` | CVE-2021-34527 | Print Spooler RCE | 8.8 |
| `cve_2021_44228_log4shell.md` | CVE-2021-44228 | Log4j JNDI injection | 10.0 |
| `cve_2022_30190_follina.md` | CVE-2022-30190 | MSDT RCE via Word documents | 7.8 |
| `cve_2023_23397_outlook_elevation.md` | CVE-2023-23397 | Outlook NTLM relay | 9.8 |
| `cve_2023_34362_moveit.md` | CVE-2023-34362 | MOVEit Transfer SQL injection | 9.8 |
| `cve_2023_44487_http2_rapid_reset.md` | CVE-2023-44487 | HTTP/2 stream reset DDoS | 7.5 |
| `cve_2024_3094_xz_backdoor.md` | CVE-2024-3094 | XZ Utils supply chain backdoor | 10.0 |

### Threat Actor Profiles (5)

| File | Group | Attribution | Motivation |
|------|-------|-------------|------------|
| `threat_actor_apt28_fancy_bear.md` | APT28 / Fancy Bear | Russia (GRU) | Espionage |
| `threat_actor_apt29_cozy_bear.md` | APT29 / Cozy Bear | Russia (SVR) | Espionage |
| `threat_actor_lazarus_group.md` | Lazarus Group | North Korea | Financial / Espionage |
| `threat_actor_lockbit.md` | LockBit | Criminal (RaaS) | Financial |
| `threat_actor_scattered_spider.md` | Scattered Spider | Criminal | Financial |

### Incident Response Runbooks (5)

| File | Incident Type |
|------|---------------|
| `runbook_bec_response.md` | Business Email Compromise |
| `runbook_data_exfiltration.md` | Data Exfiltration |
| `runbook_insider_threat.md` | Insider Threat |
| `runbook_phishing_response.md` | Phishing |
| `runbook_ransomware_response.md` | Ransomware |

### Detection Engineering Guides (5)

| File | Detection Domain |
|------|-----------------|
| `detection_c2_communication.md` | Command and Control channels |
| `detection_credential_dumping.md` | Credential theft (LSASS, DCSync) |
| `detection_lateral_movement.md` | Lateral movement (PsExec, WMI, RDP) |
| `detection_persistence_mechanisms.md` | Persistence (tasks, registry, WMI subs) |
| `detection_powershell_abuse.md` | PowerShell-based attacks |

---

## How to Use

### In Stage 4 Exercises

The RAG exercises (`04_rag/`) reference this corpus. Each exercise loads documents from this folder automatically.

### In the Capstone

Participants are encouraged to **add their own documents** to this folder for their capstone demo. The best demos use content from real customer engagements (sanitised) or the participant's own team runbooks.

### In the Demo Kit

The `demo_kit/demo_assistant.py` loads all `.md` files from this folder at startup.

---

## Adding Your Own Documents

Drop any `.md` file into this folder. The RAG pipeline picks up all markdown files automatically. Recommended document types:

- Your team's incident response playbooks
- Threat intelligence reports relevant to your customers
- Internal security advisories or post-mortems
- Vendor-specific detection guides
