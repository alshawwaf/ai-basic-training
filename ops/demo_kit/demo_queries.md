# Demo Queries: Reference Card

Pre-built queries for demonstrating the Security Analyst Assistant. Run these in order during live demos or use them for testing after corpus changes.

| # | Category | Query | What It Demonstrates |
|---|----------|-------|---------------------|
| 1 | Detection | "How do I detect credential dumping via LSASS access?" | Retrieves specific Sysmon Event 10 indicators and Sigma-style rule logic from a single document |
| 2 | Detection | "What are the signs of DNS tunnelling in my network?" | Pulls C2 detection content — entropy thresholds, TXT record abuse, and beaconing analysis |
| 3 | Threat Techniques | "What techniques can attackers use to maintain persistence on Windows?" | Multi-indicator retrieval across scheduled tasks, registry Run keys, WMI subscriptions, services, and startup folder |
| 4 | Threat Techniques | "How does pass-the-hash work and what logs should I monitor?" | Retrieves lateral movement indicators — NTLM logon events, admin share access patterns |
| 5 | Incident Response | "We detected PsExec lateral movement. What should we do?" | Returns structured response actions — isolate, correlate, disable accounts, audit access |
| 6 | Incident Response | "An analyst found an AMSI bypass in PowerShell logs. Walk me through the response." | Retrieves PowerShell abuse response steps and links to ScriptBlock logging and host isolation |
| 7 | MITRE Mapping | "Which MITRE ATT&CK techniques relate to command and control?" | Returns technique IDs (T1071, T1572, T1090.004, T1573) with descriptions from the C2 guide |
| 8 | Cross-Topic | "An attacker dumped credentials and is now moving laterally. What should I look for?" | Tests multi-document retrieval — the system should pull from both the credential dumping and lateral movement guides |
| 9 | Synthesis | "Compare the detection approaches for scheduled task persistence versus WMI event subscriptions." | Tests the LLM's ability to synthesise and contrast information from within the same document |
| 10 | Out-of-Scope | "How do I detect SQL injection attacks in my web application?" | No SQLi document in the corpus — the assistant should indicate insufficient context rather than hallucinate |
