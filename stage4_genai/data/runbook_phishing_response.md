# Incident Response: Phishing Email

**Severity Classification:**
- **P1 (Critical):** Confirmed credential compromise or malware execution from phishing; executive or privileged account targeted
- **P2 (High):** User clicked link or opened attachment but no confirmed compromise; multiple recipients of same campaign
- **P3 (Medium):** Phishing email reported by user with no interaction; single recipient

## Phase 1: Detection and Triage (0-15 min)
1. Record the reporter's name, timestamp, and how the email was identified (user report, email gateway alert, or SOC detection).
2. Obtain the original email as an EML/MSG file (not a screenshot or forward, which strips headers).
3. Analyse email headers: extract envelope sender, Reply-To address, originating IP, SPF/DKIM/DMARC authentication results, and X-Originating-IP.
4. Extract IOCs: sender address, subject line, URLs (defang before sharing), attachment hashes (SHA-256), and any embedded domain names.
5. Check IOCs against threat intelligence platforms (VirusTotal, URLhaus, OTX) and internal historical IOC databases.
6. Determine scope: query the email gateway for all recipients of emails matching the sender, subject, or attachment hash.

## Phase 2: Containment (15 min - 1 hr)
1. Quarantine the phishing email from all recipient mailboxes using the email security platform's retroactive purge (e.g., Microsoft Purge, Proofpoint TRAP).
2. Block the sender address, sending domain, and extracted URLs/IPs at the email gateway and web proxy.
3. If a user clicked a link: force a password reset for the user's account, revoke active sessions and OAuth tokens, and re-enrol MFA.
4. If an attachment was opened: isolate the endpoint from the network, capture a memory image, and initiate EDR investigation.
5. Notify all confirmed recipients that the email is malicious and instruct them not to interact with it.

## Phase 3: Eradication (1-24 hr)
1. Confirm complete quarantine by re-querying the email gateway for any remaining copies across all mailboxes.
2. For compromised accounts: review mailbox rules for attacker-created forwarding rules, review Azure AD/Okta sign-in logs for lateral access, and check for newly registered MFA devices.
3. For endpoints with malware execution: perform full forensic triage, identify persistence mechanisms, and re-image if necessary.
4. Update email gateway rules with new detection signatures based on campaign-specific patterns (subject line templates, sender infrastructure, URL patterns).

## Phase 4: Recovery (1-7 days)
1. Restore user access after confirming no residual compromise (clean credential state, no rogue mailbox rules, no attacker MFA devices).
2. Monitor previously compromised accounts for 30 days with enhanced logging and anomalous-login alerting.
3. Submit malicious URLs and domains to browser safe-browsing block lists and industry sharing groups (ISACs).
4. If the phishing campaign impersonated your organisation: initiate domain takedown requests and notify your brand protection service.

## Phase 5: Post-Incident
- Document the full timeline, IOCs, affected users, and response actions taken.
- Determine the root cause: did the email bypass existing filters? If so, identify the specific gap (new TLD, compromised legitimate sender, zero-day URL).
- Update detection rules and phishing simulation templates to reflect the observed campaign techniques.
- Provide targeted security awareness follow-up to affected users within 7 days.

## Key Metrics
| Metric | Target |
|--------|--------|
| Time from report to quarantine | < 30 minutes |
| Time to identify all recipients | < 15 minutes |
| Time to notify affected users | < 1 hour |
| Time to complete IOC extraction | < 30 minutes |
| Post-incident report delivery | < 5 business days |

## Escalation Matrix
- **P3:** SOC Tier 1 handles; escalate to Tier 2 if campaign targets more than 10 recipients.
- **P2:** SOC Tier 2 leads response; notify Security Manager if executive accounts are involved.
- **P1:** Incident Commander activates full IR team; notify CISO within 1 hour; engage legal if PII exposure is suspected.
