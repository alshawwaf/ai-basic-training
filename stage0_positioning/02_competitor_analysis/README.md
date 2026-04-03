# Session 0.2 — How Competitors Position AI

> **Format:** Lecture + group exercise  |  **Duration:** 60 min  |  **Prerequisites:** Session 0.1

---

## Learning Objectives

By the end of this session you will be able to:

1. Describe what the major security vendors are actually doing with AI under the hood
2. Map marketing language to specific ML techniques you'll learn in Stages 1-4
3. Identify each vendor's AI strengths and limitations in a customer conversation
4. Position your own capabilities against competitor AI claims with technical depth

---

## Why This Session Matters

Every competitor says "AI-powered." Customers hear it from 5 vendors in the same week. The architect who can say "their detection engine is a gradient-boosted tree retrained weekly on endpoint telemetry — here's how that compares to what we do" wins trust instantly. This session gives you that precision.

---

## Part 1 — The Competitive AI Landscape (10 min)

### The Five Vendors Customers Ask About Most

| Vendor | AI Brand | Positioning |
|--------|----------|-------------|
| **CrowdStrike** | Charlotte AI | ML-first endpoint detection |
| **Palo Alto Networks** | Cortex XSIAM | AI-driven SOC platform |
| **SentinelOne** | Purple AI | Autonomous endpoint response |
| **Darktrace** | Self-Learning AI | Unsupervised network anomaly detection |
| **Microsoft** | Security Copilot | LLM-based investigation and triage |

These are the vendors your customers will benchmark you against. For each, we'll cover:
- **What they claim** — the marketing message
- **What's under the hood** — the actual technology (mapped to ML concepts from this program)
- **Strengths** — where the AI genuinely adds value
- **Limitations** — where the AI falls short or is overstated
- **How to position against** — what to say in a customer conversation

---

## Part 2 — Vendor Deep Dives (35 min)

### CrowdStrike — Charlotte AI + ML-First Detection

#### What They Claim
"AI-native platform built from day one around ML." CrowdStrike positions heavily on their ML models replacing legacy antivirus signatures. Charlotte AI is their generative AI assistant for threat hunting and investigation.

#### What's Under the Hood

| Component | Actual Technology | Program Reference |
|-----------|------------------|-------------------|
| Pre-execution prevention | **Gradient-boosted trees** on static PE file features (import tables, section entropy, header metadata) | Stage 1: Decision Trees, Stage 2: Random Forests |
| Behavioural detection | **ML classifiers** on process behaviour telemetry (process trees, API call sequences, file system events) | Stage 2: Feature Engineering |
| Indicator of Attack (IOA) | **Rule-based + ML hybrid** — hand-crafted attack pattern rules enhanced with ML scoring | Stage 1: Model Evaluation (precision/recall) |
| Charlotte AI | **RAG architecture** — LLM with retrieval over CrowdStrike's threat intelligence database and customer telemetry | Stage 4: RAG |
| Threat Graph | **Graph database** with ML-based entity resolution and relationship scoring | Stage 2: Clustering |

#### Strengths
- Genuinely ML-first architecture — models are core to detection, not an add-on
- Massive training data advantage (processes telemetry from millions of endpoints)
- Charlotte AI is one of the more mature security LLM copilots

#### Limitations
- ML models are trained centrally — customer-specific threat patterns may be underrepresented
- Charlotte AI requires cloud connectivity — no air-gapped option
- Pre-execution ML can be evaded by adversarial techniques (packing, polymorphism)
- IOAs still rely heavily on hand-crafted rules for precision

#### How to Position Against
> "CrowdStrike's ML is strong for known threat families where they have training data. Ask them: how does the model perform on threats specific to YOUR industry that may not be well-represented in their global training set? And how often do their models retrain — because a model trained last quarter doesn't catch this quarter's TTPs."

---

### Palo Alto Networks — Cortex XSIAM + Cortex XDR

#### What They Claim
"AI-driven SOC" and "autonomous security operations." XSIAM is positioned as the replacement for traditional SIEM, using AI to correlate, triage, and respond to alerts automatically.

#### What's Under the Hood

| Component | Actual Technology | Program Reference |
|-----------|------------------|-------------------|
| Alert grouping | **Clustering algorithms** (likely k-means or DBSCAN) to group related alerts into incidents | Stage 2: Clustering |
| Analytics engine | **ML classifiers** for alert scoring and prioritisation, trained on analyst feedback loops | Stage 1: Logistic Regression, Stage 2: Random Forests |
| XSIAM Copilot | **LLM integration** for natural language queries over security data | Stage 4: LLM APIs |
| Behavioural analytics | **Statistical baselines + ML anomaly detection** on user and entity behaviour (UEBA) | Stage 2: Anomaly Detection |
| Cortex XDR ML | **Multi-layer ML** — local analysis (lightweight model on agent) + cloud analysis (heavier model) | Stage 3: Neural Networks (model architecture) |

#### Strengths
- Enormous data pipeline — ingests from firewall, endpoint, cloud, identity, and network in one platform
- Alert grouping and auto-triage are genuine AI applications that reduce analyst workload
- XSIAM's data lake approach means models train on correlated, multi-source data

#### Limitations
- "Autonomous SOC" is aspirational — complex incidents still require human investigation
- Model quality depends on the volume and quality of customer data ingested
- Risk of over-automation — auto-closing alerts that should have been investigated
- XSIAM is a massive platform commitment — hard to validate AI claims without full deployment

#### How to Position Against
> "Palo Alto's AI strength is in data correlation — they see across firewall, endpoint, and cloud. But 'autonomous SOC' is marketing. Ask them: what percentage of incidents does XSIAM fully resolve without human intervention? What's the false negative rate on auto-closed incidents? And what happens when the model is wrong and auto-closes a real breach?"

---

### SentinelOne — Purple AI + Singularity Platform

#### What They Claim
"Autonomous AI-powered security." SentinelOne was one of the first to brand around AI heavily. Purple AI is their generative AI analyst for threat hunting.

#### What's Under the Hood

| Component | Actual Technology | Program Reference |
|-----------|------------------|-------------------|
| Static AI engine | **ML classifier** on file attributes — similar approach to CrowdStrike's pre-execution model | Stage 2: Random Forests |
| Behavioural AI engine | **ML models** on endpoint telemetry — system call sequences, file operations, network behaviour | Stage 2: Feature Engineering |
| ActiveEDR | **Storyline technology** — tracks process relationships and applies ML scoring to the full attack chain | Stage 1: Decision Trees (interpretability) |
| Purple AI | **LLM-based** natural language interface for threat hunting queries across telemetry | Stage 4: LLM APIs, RAG |
| Ranger (network discovery) | **Fingerprinting + classification** — ML models identify device types on the network | Stage 1: Logistic Regression |

#### Strengths
- Storyline concept is genuinely useful — traces full attack chain for analyst review
- Strong autonomous response capabilities (auto-remediate, rollback)
- Purple AI translates natural language into structured hunt queries

#### Limitations
- "Autonomous" response is effective for known patterns but risky for novel attacks
- Rollback capability requires adequate disk space and can fail on encrypted ransomware
- ML models face the same adversarial evasion challenges as all endpoint ML
- Purple AI generates queries but doesn't validate their correctness — analyst judgment still needed

#### How to Position Against
> "SentinelOne's Storyline is strong for investigation. But 'autonomous' means 'automated playbook' — it follows predefined response patterns. Ask them: what happens when the threat doesn't match a known pattern? How does Purple AI handle queries about threats it hasn't seen? And what's the rollback success rate on ransomware that encrypts before the model catches it?"

---

### Darktrace — Self-Learning AI

#### What They Claim
"Self-learning AI that understands the unique digital fingerprint of every organisation." Darktrace pioneered the "immune system" metaphor — the AI learns what's normal and flags deviations.

#### What's Under the Hood

| Component | Actual Technology | Program Reference |
|-----------|------------------|-------------------|
| Enterprise Immune System | **Unsupervised ML** — primarily Bayesian models and clustering on network metadata (NetFlow, DNS, HTTP) | Stage 2: Clustering, Anomaly Detection |
| Antigena (autonomous response) | **Threshold-based response** triggered by anomaly scores — slows or blocks connections exceeding risk thresholds | Stage 1: Model Evaluation (thresholds) |
| Cyber AI Analyst | **ML + rules** that groups related anomalies and generates natural language investigation reports | Stage 4: LLM concepts |
| Network sensors | **Deep packet inspection + metadata extraction** feeds into the unsupervised models | Stage 2: Feature Engineering |

#### Strengths
- Genuinely unsupervised — learns from your network without labelled data, making it useful in environments where you don't know what "bad" looks like
- Effective at detecting insider threats and lateral movement — anomalies in user behaviour
- Deploys relatively quickly — learns baseline in 1-2 weeks

#### Limitations
- **High false positive rate** — unsupervised anomaly detection flags anything unusual, not just threats. A new application deployment or a legitimate business change will trigger alerts.
- "Self-learning" means the model adapts — but if an attacker is slow and persistent, the model learns the attack as "normal" (baseline poisoning)
- Limited effectiveness against threats that look statistically similar to normal traffic
- The "immune system" metaphor oversimplifies — real immune systems have memory of past pathogens; Darktrace's models don't have this kind of memory in the same way

#### How to Position Against
> "Darktrace is genuinely unsupervised — that's their real strength for unknown threats. But unsupervised means high false positives. Ask them: what's their false positive rate in the first month? What happens when a legitimate business change triggers the model? And how do they handle baseline poisoning — an attacker who moves slowly enough to become 'normal'?"

---

### Microsoft — Security Copilot

#### What They Claim
"AI-powered security analysis." Microsoft Security Copilot uses GPT-4 to help analysts investigate incidents, summarise alerts, generate KQL queries, and reason across Microsoft's security data.

#### What's Under the Hood

| Component | Actual Technology | Program Reference |
|-----------|------------------|-------------------|
| Core engine | **GPT-4** (large language model) with RAG over Microsoft threat intelligence and customer tenant data | Stage 4: RAG |
| Query generation | **LLM prompt engineering** — translates natural language to KQL, Sentinel queries | Stage 4: LLM APIs |
| Incident summarisation | **LLM + retrieval** — reads alert details, enriches from threat intel, generates summary | Stage 4: RAG pipeline |
| Plugin ecosystem | **Tool-use / function calling** — Copilot calls APIs for VirusTotal, Sentinel, Defender, Intune | Stage 4: Structured output |
| Embedded copilots | **LLM integrated into** Defender XDR, Sentinel, Intune, Entra, Purview | Stage 4: System prompts |

#### Strengths
- Deepest integration with the Microsoft security stack — Copilot can reason across Defender, Sentinel, Entra, and Intune in a single query
- Backed by Microsoft's threat intelligence (trillions of signals per day)
- Plugin architecture allows extensibility to third-party tools
- Natural language interface lowers the barrier for junior analysts

#### Limitations
- **LLM, not ML-based detection** — Copilot assists human analysis but does not detect threats itself. Detection is still done by Defender's existing ML models and rules.
- Quality of answers depends heavily on prompt quality — garbage in, garbage out
- Hallucination risk — Copilot can generate plausible-sounding but incorrect analysis
- Requires Microsoft security stack for full value — limited utility in heterogeneous environments
- Compute units pricing model can become expensive at scale

#### How to Position Against
> "Microsoft Copilot is an LLM assistant, not a detection engine. It helps analysts investigate faster, but it doesn't find threats that Defender's existing models miss. Ask them: what net-new threats does Copilot detect that weren't already caught? How do they handle hallucinated analysis — a confident-sounding but wrong investigation summary? And what's the cost per analyst per month when you factor in compute units?"

---

## Part 3 — The Competitive Positioning Matrix (5 min)

### Summary: What Each Vendor Actually Does

| Vendor | Supervised ML (classifiers) | Unsupervised ML (anomaly) | LLM / GenAI (copilots) |
|--------|---------------------------|--------------------------|----------------------|
| CrowdStrike | Strong | Low | Medium |
| Palo Alto | Strong | Medium | Medium |
| SentinelOne | Strong | Low | Medium |
| Darktrace | Low | **Very Strong** | Low |
| Microsoft | Medium | Low | **Very Strong** |

| Vendor | Primary AI Approach | Best At | Weakest At |
|--------|-------------------|---------|------------|
| CrowdStrike | Supervised ML on endpoint telemetry | Known threat family detection | Novel threats outside training distribution |
| Palo Alto | Multi-source data correlation + ML | Alert reduction and prioritisation | Over-automation risk |
| SentinelOne | Supervised ML + autonomous response | Investigation (Storyline) | Novel attack response |
| Darktrace | Unsupervised anomaly detection | Unknown threat / insider threat | False positives, baseline poisoning |
| Microsoft | LLM-based analyst assistance | Investigation speed, KQL generation | Net-new detection (LLM doesn't detect) |

### The Key Positioning Insight

> No vendor has solved security AI. Each has optimised for a different part of the problem. The architect who understands this can position any product — including their own — by identifying which part of the AI problem space it addresses and where the gaps remain.

---

## Part 4 — How to Read a Competitor Datasheet (5 min)

### The Translation Table

When you see this in a datasheet, here's what it usually means technically:

| Marketing Language | Probable Technology | Questions to Ask |
|-------------------|-------------------|------------------|
| "AI-native architecture" | ML models are core to detection pipeline, not bolted on | "Which models? Retrained how often?" |
| "Self-learning" | Unsupervised ML (clustering or statistical baselines) | "What's the false positive rate during the learning period?" |
| "Autonomous response" | Automated playbooks triggered by ML confidence scores | "What percentage of incidents are fully auto-resolved?" |
| "Next-gen AI" | Typically means they've added an LLM copilot | "What does the LLM do that wasn't possible before?" |
| "Trained on [large number] events" | Training data scale for supervised models | "How representative is that data for THIS customer's industry?" |
| "Zero-day detection" | ML model generalises beyond known signatures | "Show me a detection of a genuine zero-day with timeline" |
| "AI-driven SOC" | Alert scoring + LLM triage assistance | "What's the analyst workload reduction in actual deployments?" |
| "Proprietary ML" | Custom-trained models (not off-the-shelf) | "Proprietary is not a feature. What architecture? What performance?" |

---

## Discussion Exercise (remaining time)

### Group Exercise: Competitor Battlecard

In groups of 2-3, pick one vendor from this session. Using the information provided and your own field experience, create a one-page battlecard:

**Battlecard Template:**

```
VENDOR: _______________

THEIR AI CLAIM (1 sentence):


WHAT'S ACTUALLY UNDER THE HOOD (2-3 sentences):


THEIR GENUINE STRENGTHS (2-3 bullets):
-
-
-

THEIR AI LIMITATIONS (2-3 bullets):
-
-
-

QUESTIONS TO ASK IN A COMPETITIVE DEAL (3 questions):
1.
2.
3.

OUR POSITIONING STATEMENT (2-3 sentences):

```

**Share with the full group and refine based on feedback.**

---

## Key Takeaways

1. **Every vendor's AI has a real core** — dismissing competitors as "just hype" loses credibility. Acknowledge what's real, then expose the gaps.
2. **Supervised ML dominates endpoint and email** — CrowdStrike, SentinelOne, and Palo Alto all use tree-based classifiers trained on labelled data.
3. **Darktrace is the unsupervised outlier** — genuinely different approach, with genuinely different trade-offs (high FP rate, baseline poisoning risk).
4. **LLM copilots are the new battleground** — every vendor is shipping one. The differentiator is data access and integration depth, not the LLM itself.
5. **The winning move is precision** — "Their model is a gradient-boosted tree retrained weekly" is 10x more credible than "Our AI is better."

---

---

## Check Point AI Security — Our Position

While this session focuses on how competitors position their AI, it's equally important to understand our own AI capabilities and how to articulate them.

### Check Point's AI Stack

| Layer | Product | What It Does | AI Under the Hood |
|-------|---------|-------------|-------------------|
| Threat Intelligence | ThreatCloud AI | Real-time threat verdicts across all enforcement points | Gradient-boosted trees for malware classification, deep learning for zero-day detection, NLP for phishing |
| AI Governance | Workforce AI Security | Monitors and governs employee AI tool usage | NLP content classification, sensitive data detection, application fingerprinting |
| AI Application Security | AI Guardrails | Protects LLM applications against prompt injection, jailbreaks | NLP classifiers, semantic embedding analysis, pattern matching |
| AI Agent Security | AI Agent Security | Secures autonomous AI agents and MCP tool access | Behavioural analysis, anomaly detection on agent invocations |

### How to Position Against Each Competitor

| Competitor Claim | Our Response |
|-----------------|-------------|
| "CrowdStrike Charlotte AI is the most advanced security copilot" | "Charlotte is an investigation assistant — it helps analysts ask questions faster. It doesn't govern employee AI usage, protect LLM applications, or secure AI agents. Our AI Security suite covers all three." |
| "Microsoft Copilot for Security uses GPT-4 for threat analysis" | "Copilot for Security is Microsoft-only — it doesn't cover ChatGPT, Claude, or open-source models. Workforce AI Security governs ALL AI tools, not just Microsoft's." |
| "Palo Alto XSIAM uses AI for autonomous SOC operations" | "XSIAM automates SOC workflows — but who secures the AI agents doing the automating? AI Agent Security provides the governance layer for autonomous AI operations." |
| "Darktrace uses unsupervised AI to detect unknown threats" | "Darktrace detects network anomalies — a different problem. We're talking about securing the AI tools and applications themselves. Workforce AI Security + AI Guardrails is a new category they don't play in." |

### The Key Differentiator

After completing this program, you can do something no competitor's SE can: explain how AI actually works — classification, embeddings, retrieval, neural networks — and connect it directly to how our products use those techniques. That technical depth is the ultimate competitive advantage.

---

## Next Session

**[Session 0.3 — AI Objection Handling](../03_objection_handling/README.md)**
The 8 most common AI objections customers raise — and technically grounded responses for each.
