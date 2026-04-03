# Incident Response: Insider Threat

**Severity Classification:**
- **P1 (Critical):** Active data exfiltration or sabotage by a privileged user; confirmed collusion with external threat actor; imminent risk of significant financial or reputational damage
- **P2 (High):** Pattern of suspicious data access or policy violations by an identified employee; corroborating indicators from multiple detection sources (DLP, UEBA, HR report)
- **P3 (Medium):** Single behavioural indicator flagged (e.g., UEBA anomaly, after-hours access, resignation combined with increased data access) requiring investigation to confirm or dismiss

## Phase 1: Detection and Triage (0-15 min)
1. Identify the detection source: UEBA alert (anomalous access volume or timing), DLP alert, manager or HR referral, co-worker report, or exit-process data access review.
2. Review the subject's role, access level, and employment status: are they a current employee, contractor, or recently terminated? Are they in a notice period or on a performance improvement plan?
3. Assess the behavioural indicators present:
   - Accessing data outside normal job function or authorisation scope
   - Bulk downloading or copying files from repositories not typically accessed
   - Connecting personal USB storage devices or installing cloud sync clients
   - Accessing systems during unusual hours inconsistent with work pattern
   - Attempting to access resources after access has been restricted
   - Expressed grievances, financial hardship, or known external business interests
4. **Critical decision: covert monitoring vs. immediate lockout.** If there is no imminent risk of harm and legal/HR concur, maintain covert monitoring to understand the full scope before alerting the subject. If there is risk of data destruction, sabotage, or safety concern, proceed to immediate containment.
5. Engage HR and Legal from the outset. Insider threat investigations have significant legal, privacy, and employment law implications that vary by jurisdiction.

## Phase 2: Containment (15 min - 1 hr)
1. **If covert monitoring is approved:** Enable enhanced logging on the subject's accounts without changing access. Deploy additional endpoint telemetry. Monitor email, file access, web activity, and badge access through authorised channels.
2. **If immediate lockout is required:** Disable all accounts simultaneously (Active Directory, VPN, email, SaaS applications, badge access). Coordinate timing with HR so the subject is notified concurrently by their manager and HR.
3. Secure the subject's company-issued devices: laptop, mobile phone, and any removable media. Maintain chain of custody — document who collected each device, when, and its condition.
4. Revoke access to shared credentials, service accounts, or systems where the subject may have knowledge of credentials not tied to their personal account.
5. Preserve the subject's mailbox, cloud storage, and chat history under legal hold before any account deletion or offboarding process runs.
6. If the subject had access to production systems, infrastructure, or code repositories: review recent commits, configuration changes, and deployments for backdoors or logic bombs.

## Phase 3: Eradication (1-24 hr)
1. Conduct forensic analysis of the subject's endpoint(s): file access timeline, USB device history, browser history, installed applications, deleted file recovery, and cloud sync activity.
2. Review all data access for the preceding 90 days (or longer if indicators predate the detection): file server access logs, SharePoint/OneDrive activity, database query logs, source code repository clones, and SaaS application audit trails.
3. Determine if data was exfiltrated: identify all files accessed, downloaded, copied, or transferred externally. Classify the data involved and estimate the scope of potential exposure.
4. Check for dormant persistence: scheduled tasks, cron jobs, secondary accounts, SSH keys, API tokens, or shared credentials the subject may use to regain access after termination.
5. Interview relevant colleagues (with HR and Legal guidance) to understand if the subject shared credentials, discussed intentions, or involved others.

## Phase 4: Recovery (1-7 days)
1. Rotate all credentials the subject had access to: shared service accounts, API keys, database passwords, infrastructure secrets, and WiFi PSKs.
2. Review and tighten access controls for the role the subject held: apply least-privilege principles to prevent future over-provisioned access.
3. If data was exfiltrated: follow the Data Exfiltration runbook for regulatory notification requirements and external party notification.
4. If sabotage occurred: restore affected systems from verified clean backups, validate integrity of production data and code repositories, and review change management logs for unauthorised modifications.
5. Update offboarding procedures: ensure access revocation is complete and timely for all systems, including SaaS applications and third-party platforms.

## Phase 5: Post-Incident
- Compile a comprehensive investigation report for HR, Legal, and executive leadership. Clearly separate factual findings from analysis and conclusions.
- Determine disposition in coordination with Legal: internal disciplinary action, termination, civil litigation (trade secret theft, breach of contract), or criminal referral.
- If criminal referral is appropriate: engage with law enforcement (FBI for trade secret theft under the Economic Espionage Act or Defend Trade Secrets Act) and preserve all evidence under chain of custody.
- Review and update the Insider Threat Programme: detection rules, UEBA baselines, DLP policies, and access review processes.
- Conduct a lessons-learned session focused on detection timeliness, legal coordination effectiveness, and evidence preservation adequacy.

## Key Metrics
| Metric | Target |
|--------|--------|
| Time from indicator detection to HR/Legal notification | < 2 hours |
| Time to enable enhanced monitoring (covert path) | < 4 hours |
| Time to complete account lockout (immediate path) | < 30 minutes (all systems simultaneously) |
| Time to secure physical devices | < 2 hours from lockout decision |
| Forensic analysis completion | < 5 business days |

## Escalation Matrix
- **P3 (single indicator):** SOC Tier 2 investigates with HR awareness; escalate to IR Manager if additional corroborating indicators emerge.
- **P2 (corroborated pattern):** IR Manager leads with dedicated HR and Legal partners; notify CISO within 4 hours; begin formal investigation under attorney-client privilege if Legal advises.
- **P1 (active exfiltration or sabotage):** CISO activates crisis response team; notify General Counsel and CHRO immediately; engage external forensics firm; prepare for potential law enforcement referral and regulatory notifications.
