# Workforce AI Security

> **Stage:** 5  |  **Week:** 14  |  **Time:** 60 min  |  **Format:** Lecture + dashboard walkthrough

---

## Overview

Employees across every organisation are adopting AI tools — ChatGPT, Claude, Copilot, Cursor, and dozens more. This creates a new attack surface: sensitive data leaking to external AI services, shadow AI usage outside IT visibility, and compliance violations from unmonitored AI interactions.

**Workforce AI Security** solves this by providing visibility, governance, and data protection for all employee AI usage across the organisation.

---

## What Workforce AI Security Does

### The Core Problem

| Risk | Example | Impact |
|------|---------|--------|
| **Data leakage** | Engineer pastes proprietary source code into ChatGPT | Intellectual property exposure, potential training data contamination |
| **Shadow AI** | Sales team uses an unapproved AI tool for proposal generation | No visibility, no policy enforcement, no audit trail |
| **Compliance violation** | Analyst uploads customer PII to an AI assistant | GDPR/CCPA violation, regulatory penalties |
| **Prompt injection via AI tools** | Employee uses a compromised AI extension that exfiltrates data | Supply chain risk from third-party AI integrations |

### How It Works

Workforce AI Security operates as an inline security layer between employees and AI services:

| Stage | What Happens | Technical Detail |
|-------|-------------|-----------------|
| **Discovery** | Identifies all AI applications in use across the organisation | Traffic analysis, application fingerprinting, API endpoint detection |
| **Classification** | Categorises each interaction — what data is being shared, what AI service is receiving it | NLP-based content classification: PII, credentials, source code, financial data, medical data |
| **Policy enforcement** | Applies organisation-defined rules to each interaction in real time | Policy engine with 6 actions: Allow, Prevent, Redact, Detect, Block, Ask |
| **Monitoring** | Dashboards showing usage patterns, risk scores, top users, sensitive data exposure | Aggregation and analytics across all AI traffic |

### The Six Policy Actions

| Action | What It Does | When to Use |
|--------|-------------|-------------|
| **Allow** | Permit the interaction without modification | Low-risk AI usage within approved tools |
| **Prevent** | Block the interaction entirely | Prohibited AI services or high-risk data categories |
| **Redact** | Remove sensitive content before it reaches the AI service | Allow the workflow but strip PII, credentials, or code |
| **Detect** | Log the interaction and alert security team — don't block | Monitoring mode during initial rollout |
| **Block** | Block the AI application entirely | Unapproved or high-risk AI tools |
| **Ask** | Prompt the user with a justification dialog before proceeding | Moderate-risk interactions where user intent matters |

---

## Dashboard Walkthrough

The Workforce AI Security dashboard provides a single view of all AI activity:

### Key Metrics

| Metric | What It Shows | Why It Matters |
|--------|--------------|----------------|
| **Total Traffic** | Sessions, prompts, and file uploads across all AI services | Volume baseline — is AI usage growing, stable, or declining? |
| **Managed vs Unmanaged** | Which AI tools are under policy vs shadow AI | Unmanaged tools are blind spots — no policy enforcement |
| **Sensitive Data** | Count of interactions containing classified data types | Direct measure of data leakage risk |
| **Policy Enforcement** | Breakdown of Allow/Prevent/Redact/Detect/Block/Ask actions | Shows whether policies are too permissive or too restrictive |
| **Top-Risk Users** | Users with the highest volume or most sensitive interactions | Targeted coaching or policy adjustment |
| **Application Risk** | Risk-vs-usage matrix for each AI application | Prioritise which apps to manage first |
| **Agentic Activity** | AI agent invocations, MCP connections, tool usage | Visibility into autonomous AI workflows |

### Top Used Agents

The dashboard tracks AI agents by invocation count, showing which MCP servers and tool integrations are most active. This connects directly to Session 5.2 — Agent Security.

---

## Connecting to What You Know

### From Stage 1 (Classification)

Sensitive data detection is a **classification problem** — the same supervised learning approach you built in Stage 1. The model takes text input (a prompt or file upload) and classifies it into categories: PII, source code, credentials, financial data, or safe.

The key difference from your Stage 1 phishing classifier: this model must operate **inline at low latency** (milliseconds, not seconds) and handle **multi-label classification** (a single prompt can contain both PII and source code).

### From Stage 2 (Anomaly Detection)

Risk scoring uses **anomaly detection** — the same unsupervised approach from Stage 2. Normal usage patterns form a baseline; deviations (sudden spike in file uploads, unusual hours, new AI tools appearing) trigger alerts.

### From Stage 4 (LLM Understanding)

Understanding how LLMs process prompts — tokenisation, context windows, system prompts — is essential for understanding what data is at risk. When an employee pastes code into Claude, you now know that code becomes part of the conversation context and is sent to an external API. Workforce AI Security intercepts that before it leaves the organisation.

---

## Discussion Questions

1. "If you deployed Workforce AI Security in your customer's environment today, what do you think the dashboard would reveal? More shadow AI than expected?"
2. "A customer says 'We just block all AI tools at the firewall.' What's the problem with that approach, and how does Workforce AI Security offer a better alternative?"
3. "Which of the six policy actions (Allow/Prevent/Redact/Detect/Block/Ask) would you recommend for a customer's first deployment? Why?"
4. "How would you explain the difference between Redact and Block to a CISO who doesn't want any data leaving the organisation?"

---

## Key Takeaways

1. **Blocking AI is not a strategy** — employees will find workarounds. Governance with visibility is the sustainable approach.
2. **Sensitive data classification is ML in production** — the same classification concepts from Stage 1, applied inline at scale.
3. **The dashboard tells a story** — learn to read it like a SOC analyst reads a SIEM. The metrics surface the risks; the policies address them.
4. **Managed vs Unmanaged is the critical metric** — you can't enforce policy on tools you can't see. Discovery comes before governance.
