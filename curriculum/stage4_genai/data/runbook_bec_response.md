# Incident Response: Business Email Compromise (BEC)

**Severity Classification:**
- **P1 (Critical):** Fraudulent wire transfer executed or in progress; executive account actively compromised and sending fraudulent instructions
- **P2 (High):** Account takeover confirmed but no financial transaction initiated; attacker has established mailbox rules or is conducting reconnaissance
- **P3 (Medium):** Suspicious email requesting wire transfer or payment change flagged by user or detection rule; no confirmed account compromise

## Phase 1: Detection and Triage (0-15 min)
1. Determine the BEC variant: account takeover (attacker controls legitimate mailbox), domain spoofing (look-alike domain), or direct impersonation (display name spoofing of executive).
2. If a financial transaction was requested: immediately contact the finance/treasury team to determine if the transfer has been initiated, is pending, or has been completed.
3. For account takeover: review Azure AD/Okta sign-in logs for the compromised account — identify the attacker's IP addresses, login timestamps, and geographic locations.
4. Check for attacker-created mailbox rules: search for forwarding rules, redirect rules, or rules moving emails to RSS Feeds/Deleted Items folders to hide attacker activity from the legitimate user.
5. Review the mailbox's Sent Items and Deleted Items for fraudulent emails the attacker may have sent to other employees, customers, or business partners.
6. Determine scope: have other accounts in the organisation been compromised? Search for logins from the same attacker IP addresses across all accounts.

## Phase 2: Containment (15 min - 1 hr)
1. **Financial containment (IMMEDIATE if funds transferred):** Contact the originating bank's fraud department and request a wire recall. For international transfers, request the bank initiate the Financial Fraud Kill Chain through the FBI's IC3 Recovery Asset Team (RAT). Time is critical — recall success drops significantly after 24 hours.
2. Reset the compromised account password, revoke all active sessions and refresh tokens, and remove any attacker-registered MFA devices.
3. Delete all attacker-created mailbox rules (forwarding rules, inbox rules hiding messages, and delegated access grants).
4. Block attacker IP addresses and any look-alike domains identified at the email gateway, DNS resolver, and web proxy.
5. If the attacker sent fraudulent emails to external parties (customers, vendors): notify those parties immediately via a verified out-of-band channel (phone call to known number) that the communication was fraudulent.
6. Place a legal hold on the compromised mailbox and all related mailboxes to preserve evidence for potential law enforcement or civil proceedings.

## Phase 3: Eradication (1-24 hr)
1. Perform a comprehensive review of the compromised mailbox: catalogue all emails read, sent, and deleted by the attacker, and identify any sensitive data accessed (financial records, PII, contracts).
2. Review OAuth application consent grants on the compromised account and revoke any suspicious or unfamiliar applications.
3. Check for secondary persistence: attacker-configured SMTP forwarding at the transport level, Power Automate flows, or connected accounts.
4. Scan for additional compromised accounts by correlating attacker infrastructure (IPs, user agents) across the full Azure AD / identity provider sign-in log set.
5. If a look-alike domain was used: initiate a domain takedown request through the domain registrar's abuse process and your brand protection service.

## Phase 4: Recovery (1-7 days)
1. Restore the user's access with hardened configuration: enforce phishing-resistant MFA (FIDO2 or certificate-based), enable Conditional Access policies restricting login to compliant devices and expected locations.
2. Implement or strengthen payment verification controls: require out-of-band verbal confirmation (callback to a known number) for all wire transfers, payment method changes, and new vendor setups.
3. Review and update email authentication records: ensure DMARC policy is set to `p=reject`, SPF records are current, and DKIM is enabled for all sending domains.
4. Monitor the recovered account with enhanced logging for 30 days, alerting on new mailbox rules, sign-ins from new locations, and OAuth grants.

## Phase 5: Post-Incident
- Document total financial exposure: amount transferred, amount recovered, and unrecovered losses.
- File an FBI IC3 complaint (ic3.gov) regardless of financial loss amount; file a SAR (Suspicious Activity Report) if applicable.
- Conduct a lessons-learned session focused on how the initial compromise occurred (credential phishing, token theft, password reuse) and what controls failed.
- Deliver targeted finance-team training on BEC red flags: urgency, secrecy, changes to payment instructions, and unusual sender behaviour.

## Key Metrics
| Metric | Target |
|--------|--------|
| Time from fraud detection to bank notification | < 30 minutes |
| Time to contain compromised account | < 1 hour |
| Time to notify affected external parties | < 4 hours |
| Wire recall initiation | < 24 hours (critical for recovery) |
| Post-incident report delivery | < 5 business days |

## Escalation Matrix
- **P3:** SOC Tier 1 validates; escalate to Tier 2 if account compromise is confirmed.
- **P2:** IR Manager leads; notify CISO and Legal within 2 hours; begin evidence preservation under legal hold.
- **P1:** CISO activates crisis response; notify CFO/General Counsel immediately; contact FBI IC3 and originating bank fraud department within 30 minutes; engage external forensics if losses exceed insurance threshold.
