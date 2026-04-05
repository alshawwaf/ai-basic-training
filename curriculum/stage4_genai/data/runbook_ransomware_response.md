# Incident Response: Ransomware

**Severity Classification:**
- **P1 (Critical):** Active encryption observed on multiple systems or domain controller compromise confirmed; business operations disrupted
- **P2 (High):** Ransomware detected on a single endpoint with no evidence of lateral spread; encryption halted by EDR
- **P3 (Medium):** Ransomware precursor activity detected (Cobalt Strike beacon, credential dumping) but no encryption initiated

## Phase 1: Detection and Triage (0-15 min)
1. Identify the detection source: EDR alert, user report, or ransom note discovery. Record the exact timestamp and affected hostname(s).
2. Determine the ransomware variant from the ransom note, encrypted file extension, or EDR detection signature. Check No More Ransom (nomoreransom.org) for available decryptors.
3. Assess blast radius: query EDR console for additional endpoints showing the same binary hash, similar file modification patterns, or related C2 connections.
4. Identify Patient Zero: trace the infection chain backwards using EDR telemetry, email gateway logs, and VPN/RDP authentication logs to determine initial access vector.
5. Determine if data exfiltration occurred before encryption by reviewing DLP alerts, firewall logs for large outbound transfers, and any attacker communication referencing stolen data.

## Phase 2: Containment (15 min - 1 hr)
1. Immediately isolate confirmed infected systems at the network level: disable switch ports, apply host-based firewall deny-all rules via EDR, or remove from VLAN.
2. Disable compromised accounts and service accounts identified in the attack chain. Reset the KRBTGT account twice (with a 12-hour interval) if domain compromise is suspected.
3. Block all identified C2 infrastructure (IPs, domains) at the perimeter firewall and DNS resolver.
4. If encryption is actively spreading, consider temporarily isolating network segments or shutting down file-sharing services (SMB) at the network level.
5. Preserve evidence: do NOT reboot affected systems. Capture memory images from key systems before any remediation.
6. Verify backup integrity: confirm that backup systems are isolated and not connected to the compromised domain. Check that recent backups exist and have not been encrypted or deleted.

## Phase 3: Eradication (1-24 hr)
1. Perform comprehensive threat hunting across the entire environment using IOCs from Patient Zero analysis (binary hashes, C2 IPs, lateral movement tools, created accounts).
2. Identify and remove all persistence mechanisms: scheduled tasks, services, registry run keys, WMI subscriptions, and Group Policy Objects modified by the attacker.
3. Rebuild compromised systems from known-good images. Do not attempt to "clean" encrypted systems.
4. Reset all potentially compromised credentials: domain admin accounts, service accounts, local admin passwords (LAPS rotation), and VPN/remote access credentials.
5. Patch the initial access vulnerability (exposed RDP, unpatched VPN appliance, etc.) before reconnecting any systems.

## Phase 4: Recovery (1-7 days)
1. Restore data from verified clean backups, prioritising business-critical systems as defined in the Business Continuity Plan.
2. Rebuild and harden domain controllers if domain compromise occurred; consider standing up a new forest if Golden Ticket or KRBTGT compromise is confirmed.
3. Reconnect restored systems to the network incrementally, monitoring each for re-infection indicators.
4. Validate that business applications, databases, and file shares are functional and data-consistent after restoration.
5. Ransom payment decision framework: engage legal counsel, cyber insurer, and law enforcement before any payment decision. Document that payment does not guarantee decryption and may violate OFAC sanctions if the actor is on the SDN list.

## Phase 5: Post-Incident
- Notify law enforcement (FBI IC3, CISA, or national CERT) regardless of payment decision.
- File regulatory notifications if PII or protected data was exfiltrated (timelines vary by jurisdiction).
- Conduct a full lessons-learned review within 14 days covering detection gaps, response bottlenecks, and backup effectiveness.
- Implement identified hardening measures: network segmentation, EDR coverage gaps, backup isolation improvements, and privileged access management.

## Key Metrics
| Metric | Target |
|--------|--------|
| Time from detection to network isolation | < 15 minutes |
| Time to identify Patient Zero | < 4 hours |
| Time to verify backup integrity | < 2 hours |
| Time to begin restoration from backups | < 24 hours |
| Full business operations recovery | < 72 hours (based on BCP tier) |

## Escalation Matrix
- **P3 (precursor activity):** SOC Tier 2 leads threat hunt; notify IR Manager within 1 hour.
- **P2 (single endpoint):** IR Manager coordinates response; notify CISO within 2 hours; place external IR retainer on standby.
- **P1 (active spread):** CISO activates crisis management team; engage external IR firm and legal counsel immediately; notify CEO/Board within 4 hours; contact law enforcement and cyber insurer within 24 hours.
