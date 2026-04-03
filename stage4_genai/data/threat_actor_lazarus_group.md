# Lazarus Group (Hidden Cobra, ZINC, Diamond Sleet, APT38, BlueNoroff)

**Attribution:** North Korea / RGB (Reconnaissance General Bureau) | **Active Since:** 2009 | **Motivation:** Financial Theft, Espionage, Destruction

## Overview
Lazarus Group is a North Korean state-sponsored threat actor operating under the Reconnaissance General Bureau. The group is unique among nation-state actors for its primary focus on revenue generation to fund the DPRK regime, combining state espionage tradecraft with large-scale financial crime. Sub-clusters include APT38 (banking-focused) and BlueNoroff (cryptocurrency-focused). Lazarus has been responsible for some of the most consequential and financially damaging cyber operations in history.

## Known Campaigns
- **Sony Pictures Entertainment hack (2014):** Destructive wiper attack and data theft in retaliation for the film "The Interview," causing an estimated $35 million in damage and leaking unreleased films and internal emails.
- **Bangladesh Bank SWIFT heist (2016):** Attempted to steal $951 million from Bangladesh Bank's account at the Federal Reserve Bank of New York via fraudulent SWIFT messages; $81 million was successfully transferred.
- **WannaCry ransomware (2017):** Global ransomware outbreak leveraging EternalBlue (MS17-010), infecting over 200,000 systems across 150 countries including UK NHS hospitals.
- **Cryptocurrency exchange and DeFi exploits (2021-2024):** Stole over $2 billion in cryptocurrency including the Ronin Network bridge ($620M, 2022), Harmony Horizon bridge ($100M, 2022), and multiple DeFi protocol exploits using social-engineered developer access.

## TTPs (MITRE ATT&CK)
| Tactic | Technique | Description |
|--------|-----------|-------------|
| Initial Access | T1566.001 Spearphishing Attachment | Weaponised documents with fake job offers targeting developers and financial sector employees |
| Execution | T1059.007 JavaScript | Malicious npm packages and trojanised open-source development tools |
| Persistence | T1543.003 Windows Service | Installed backdoors as system services for persistent access |
| Defence Evasion | T1140 Deobfuscate/Decode Files | Multi-stage payloads with XOR and AES encryption requiring victim-specific decryption keys |
| Impact | T1486 Data Encrypted for Impact | WannaCry ransomware encrypted files using RSA-2048 and AES-128 |
| Impact | T1657 Financial Theft | Fraudulent SWIFT transfers, cryptocurrency bridge exploitation, and DeFi smart contract manipulation |

## Tools and Malware
- **BLINDINGCAN / DTrack** — Full-featured RAT with keylogging, screen capture, file manipulation, and process management
- **AppleJeus** — Trojanised cryptocurrency trading applications targeting macOS and Windows for wallet theft
- **HOPLIGHT** — Proxy tool establishing encrypted tunnels through multiple compromised hosts
- **TraderTraitor** — Malicious blockchain applications used to target cryptocurrency developers via fake job recruitment
- **ELECTRICFISH** — Custom tunnelling tool for exfiltrating data through proxy chains
- **Custom SWIFT manipulation tools** — Purpose-built malware for intercepting and modifying SWIFT financial transaction messages

## Detection Opportunities
- Monitor developer endpoints for unexpected npm package installations from unknown publishers or packages with obfuscated post-install scripts
- Alert on SWIFT messaging anomalies: transactions outside business hours, unusual destination banks, or message format inconsistencies
- Detect fake job recruitment campaigns by scanning email for lure documents referencing cryptocurrency firms, blockchain positions, or containing embedded macros
- Monitor cryptocurrency wallet infrastructure for unauthorised smart contract interactions or bridge transactions exceeding normal thresholds
- Hunt for multi-stage payload loaders that read decryption keys from victim-specific environment variables or hardware identifiers
- Baseline outbound connections from developer workstations and flag new connections to infrastructure in atypical geographic regions
