# Incident Response: Data Exfiltration

**Severity Classification:**
- **P1 (Critical):** Confirmed exfiltration of regulated data (PII, PHI, financial records) or classified/trade-secret material; large-volume transfer to external destination
- **P2 (High):** DLP alert triggered on sensitive data transfer with confirmed policy violation; investigation ongoing to determine if data left the network
- **P3 (Medium):** DLP alert triggered on data matching sensitive patterns but transfer was blocked; or anomalous data access patterns detected without confirmed exfiltration

## Phase 1: Detection and Triage (0-15 min)
1. Identify the detection source: DLP alert (endpoint, network, or cloud), CASB alert, UEBA anomaly, firewall/proxy alert for unusual outbound volume, or external notification (law enforcement, third party, dark web monitoring).
2. Determine the data involved: query the DLP platform for the specific files, data classification labels, and content inspection results (credit card numbers, SSNs, source code patterns, etc.).
3. Identify the source user and endpoint: correlate the DLP alert with the authenticated user, device hostname, IP address, and timestamp.
4. Assess the exfiltration channel: email attachment, cloud storage upload (personal OneDrive, Google Drive, Dropbox), USB device, web upload (paste sites, file-sharing services), DNS tunnelling, or encrypted channel to unknown destination.
5. Determine data volume: review proxy/firewall logs for total bytes transferred from the source endpoint to the destination over the alert timeframe and the preceding 30 days.
6. Classify the incident: is this a malicious insider, compromised account (external attacker), or accidental data exposure?

## Phase 2: Containment (15 min - 1 hr)
1. Block the exfiltration channel: add the destination IP/domain/URL to the block list at the proxy, firewall, and DNS resolver. If cloud storage, revoke sharing links and disable the external sharing capability.
2. If insider threat is suspected: coordinate with HR and Legal before taking visible containment actions to avoid tipping off the subject (see Insider Threat runbook for detailed guidance).
3. If compromised account: reset credentials, revoke sessions, and isolate the endpoint following standard account compromise procedures.
4. Preserve forensic evidence: capture a forensic disk image and memory dump of the source endpoint. Export DLP alert details, proxy logs, and cloud audit logs.
5. If USB exfiltration: identify the specific device by serial number from endpoint logs; if the device is company-issued, secure it as evidence.
6. Disable the user's access to sensitive data repositories while maintaining general account access (to avoid evidence destruction if they retain other access).

## Phase 3: Eradication (1-24 hr)
1. Conduct full forensic analysis of the source endpoint: browser history, file access timeline (MFT analysis), USB device connection history, installed applications (cloud sync clients, compression tools, encryption tools).
2. Review the user's data access history for the prior 90 days across all systems: file servers, SharePoint/OneDrive, databases, source code repositories, and SaaS applications.
3. Determine the full scope of exfiltrated data: build a comprehensive inventory of files and records transferred, their classification level, and the number of affected data subjects (for regulatory notification calculations).
4. If an external attacker was involved: conduct full threat-hunting engagement to identify additional compromised accounts, persistence mechanisms, and staging locations.
5. Check if the exfiltrated data has appeared on dark web markets, paste sites, or public file-sharing services using dark web monitoring tools.

## Phase 4: Recovery (1-7 days)
1. Implement additional DLP rules to detect and block the specific exfiltration technique observed (e.g., new cloud app restriction, USB device class block, enhanced content inspection for the specific data type).
2. Revoke or rotate any credentials, API keys, or certificates that were included in the exfiltrated data.
3. If source code was exfiltrated: assess the impact on product security and intellectual property; engage patent/IP counsel.
4. Notify affected third parties whose data was exposed (customers, partners, employees) as appropriate.
5. Begin regulatory notification process based on data type and jurisdiction.

## Phase 5: Post-Incident
- Complete regulatory notification requirements:
  - **GDPR:** Notify supervisory authority within 72 hours of becoming aware; notify affected data subjects "without undue delay" if high risk.
  - **CCPA/CPRA:** Notify affected California residents "in the most expedient time possible and without unreasonable delay."
  - **HIPAA:** Notify HHS within 60 days if PHI of 500+ individuals is breached; notify affected individuals within 60 days.
  - **SEC:** Publicly traded companies must disclose material cybersecurity incidents on Form 8-K within 4 business days of determining materiality.
- Engage external counsel for breach notification letters and regulatory filings.
- Conduct root cause analysis: why was this data accessible to this user? Were access controls appropriate? Was DLP coverage adequate?
- Review and update Data Loss Prevention policies, data classification programme, and access governance controls.

## Key Metrics
| Metric | Target |
|--------|--------|
| Time from DLP alert to analyst triage | < 15 minutes |
| Time to block active exfiltration channel | < 30 minutes |
| Time to determine data classification and scope | < 4 hours |
| Time to complete forensic evidence preservation | < 8 hours |
| Regulatory notification filing | Within jurisdictional deadlines |

## Escalation Matrix
- **P3 (blocked transfer):** SOC Tier 1 investigates; close if accidental or escalate to Tier 2 if pattern suggests intentional policy violation.
- **P2 (confirmed policy violation):** SOC Tier 2 leads; notify IR Manager and Data Protection Officer within 2 hours; begin regulatory clock assessment.
- **P1 (confirmed exfiltration of regulated data):** CISO activates full IR team; notify General Counsel and DPO immediately; engage external forensics and breach counsel within 4 hours; begin regulatory notification clock.
