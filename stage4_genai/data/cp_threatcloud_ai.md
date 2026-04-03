# Check Point ThreatCloud AI

## Overview

ThreatCloud AI is the AI-powered threat intelligence engine that serves as the backbone of all Check Point security products. It processes billions of indicators of compromise (IOCs) daily, aggregating threat data from network, endpoint, cloud, mobile, and email sensors deployed across Check Point's global customer base. Every Check Point enforcement point — from Quantum gateways to Harmony endpoints — receives real-time threat verdicts from ThreatCloud AI, creating a collective defence model where a threat identified anywhere is blocked everywhere.

## Data Sources

| Source | Telemetry |
|--------|-----------|
| Network sensors | Firewall logs, IPS events, DNS queries, URL requests, file hashes from Quantum gateways |
| Endpoint agents | Process behaviour, file events, registry changes, network connections from Harmony Endpoint |
| Cloud workloads | Cloud firewall logs, workload behaviour, API activity from CloudGuard |
| Mobile devices | App behaviour, network traffic, device posture from Harmony Mobile |
| Email gateways | Attachment analysis, URL scanning, sender reputation from Harmony Email |
| External feeds | OSINT, CERT advisories, dark web monitoring, vulnerability databases |

## Machine Learning Models

ThreatCloud AI employs multiple ML model families, each optimised for a specific threat detection task:

- **Gradient-boosted trees** for malware classification — trained on static file features (PE headers, section entropy, import tables) to classify files as malicious or benign before execution
- **Deep learning models** for zero-day detection — neural networks that analyse behavioural patterns in sandbox execution traces to identify previously unseen threats
- **NLP models** for phishing analysis — natural language processing classifiers that evaluate email subject lines, body text, sender patterns, and URL context to detect phishing campaigns

## Key Outputs

| Output | Description |
|--------|-------------|
| Threat verdicts | Real-time malicious/benign/suspicious classification for files, URLs, domains, and IP addresses |
| Behavioural signatures | Dynamically generated detection rules based on observed threat behaviour in sandbox environments |
| Campaign attribution | Correlation of individual IOCs into broader threat campaigns with actor attribution where possible |

## Real-Time Global Updates

When ThreatCloud AI identifies a new threat — whether through ML model detection, sandbox analysis, or external intelligence — it pushes updated protections to all connected enforcement points globally within seconds. This closed-loop architecture means that a zero-day detected in one customer's environment immediately protects every other Check Point customer worldwide.
