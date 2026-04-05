# Check Point Workforce AI Security

## Overview

Workforce AI Security monitors and governs how employees interact with AI-powered tools such as ChatGPT, Claude, GitHub Copilot, Cursor, and other generative AI services. As AI adoption accelerates across organisations, employees routinely paste sensitive data — source code, customer PII, credentials, internal documents — into AI tools without considering data leakage implications. Workforce AI Security provides an inline scanning layer between employees and AI services to enforce organisational AI usage policies.

## Key Capabilities

| Capability | Description |
|-----------|-------------|
| AI Application Discovery | Identifies all AI tools in use across the organisation, including sanctioned, unsanctioned, and shadow AI applications |
| Sensitive Data Classification | Detects PII, credentials, API keys, source code, and proprietary content using NLP-based content classifiers |
| Policy Enforcement | Six configurable actions per policy rule: **Allow**, **Prevent**, **Redact**, **Detect**, **Block**, and **Ask** (user justification prompt) |
| Risk Scoring | Assigns risk scores to AI applications based on data handling practices, hosting location, and compliance posture |
| Managed vs Unmanaged Visibility | Distinguishes between IT-approved AI tools and unmanaged shadow AI services employees adopt independently |

## Architecture

Workforce AI Security operates as an inline scanning layer positioned between the employee's device and the AI service. All interactions — prompts, file uploads, code snippets — pass through the scanning engine before reaching the AI provider. The engine classifies content in real time, applies the relevant policy action, and logs the event for audit. This architecture ensures that sensitive data is intercepted before it leaves the organisation's control boundary, regardless of which AI tool the employee uses.

## Use Cases

- **Data leakage prevention:** Block or redact sensitive content before it reaches external AI services
- **Shadow AI discovery:** Identify unsanctioned AI tools employees are using without IT approval
- **Compliance enforcement:** Enforce regulatory requirements (GDPR, HIPAA, PCI-DSS) on AI tool interactions
- **Risk-based access control:** Allow low-risk AI usage while restricting high-risk interactions based on content sensitivity and application risk score
