# Session 0.1 — The AI Landscape in Cybersecurity

> **Format:** Lecture + discussion  |  **Duration:** 60 min  |  **Prerequisites:** None

---

## Learning Objectives

By the end of this session you will be able to:

1. Explain what AI and ML mean in plain language — no jargon, no overselling
2. Trace the evolution from rule-based security to AI-powered detection
3. Identify where AI is deployed in production security tools today
4. Distinguish real AI capabilities from marketing hype ("AI washing")

---

## Part 1 — What AI Actually Means (10 min)

### The 30-Second Elevator Pitch

> "AI is software that learns patterns from data instead of following hand-written rules. In security, that means detection systems that adapt to new threats by studying examples of past attacks — not by waiting for a human to write a new signature."

That's it. Everything else is detail.

### Terminology — Precise, Not Impressive

These terms get thrown around interchangeably in sales conversations. Here's what they actually mean:

```
+-------------------------------------------------------------------+
|                    ARTIFICIAL INTELLIGENCE                         |
|   Any system that performs tasks normally requiring                |
|   human intelligence                                              |
|                                                                   |
|   +---------------------------------------------------------------+
|   |                  MACHINE LEARNING                             |
|   |   Systems that learn from data without being                  |
|   |   explicitly programmed for each case                        |
|   |                                                               |
|   |   +-----------------------------------------------------------+
|   |   |               DEEP LEARNING                              |
|   |   |   ML using neural networks with many                     |
|   |   |   layers — learns complex patterns                       |
|   |   |                                                           |
|   |   |   +-------------------------------------------------------+
|   |   |   |           GENERATIVE AI / LLMs                       |
|   |   |   |   Deep learning models that generate                 |
|   |   |   |   text, code, images, or structured                  |
|   |   |   |   output (ChatGPT, Claude, Gemini)                   |
|   |   |   +-------------------------------------------------------+
|   |   +-----------------------------------------------------------+
|   +---------------------------------------------------------------+
+-------------------------------------------------------------------+
```

**Key point for customer conversations:** Most AI in production security tools today is **machine learning** — not deep learning, not generative AI. When a vendor says "AI-powered," they usually mean a random forest or gradient-boosted tree trained on labelled telemetry. That's not a criticism — those models work well. But knowing this lets you ask the right follow-up questions.

### What ML Does That Rules Cannot

| Capability | Rule-Based | Machine Learning |
|-----------|-----------|-----------------|
| Detect known attack signatures | Yes | Yes |
| Detect variations of known attacks | Poorly — one character change breaks the rule | Yes — learned patterns generalise |
| Detect previously unseen attack types | No | Sometimes — if statistically similar to training data |
| Adapt to new data without human intervention | No — requires manual rule updates | Yes — retrain on new data |
| Explain why something was flagged | Yes — the rule is the explanation | Varies — some models are interpretable, some are not |
| Scale to millions of signals | Poorly — rule conflicts, ordering issues | Yes — models process feature vectors in milliseconds |

---

## Part 2 — The Evolution of AI in Security (15 min)

### Timeline: From Signatures to Self-Learning

```
1990s          2000s           2010s           2018+           2023+
  |              |               |               |               |
  v              v               v               v               v
SIGNATURES   HEURISTICS      MACHINE         DEEP            GENERATIVE
              & RULES        LEARNING        LEARNING        AI / LLMs

Exact-match   "If URL length   Trained on      Neural nets     LLMs for
virus sigs,   > 75 AND         labelled        for malware     analysis,
Snort rules,  domain age       datasets:       image class.,   triage,
regex on      < 7 days         random forests  NLP for         copilots,
log lines     THEN phish"      gradient boost  phishing text,  RAG over
                               SVM, k-means    sequence        threat
                                               models for      intel
                                               network data
```

### What Changed at Each Stage

**1990s — Signatures:** Effective against known threats. Completely blind to anything not in the signature database. Still the backbone of antivirus and IDS today — signatures are fast and precise.

**2000s — Heuristics and Rules:** Security teams wrote complex rule sets. Better coverage than pure signatures, but brittle. An attacker who knows the rules can engineer around them. Rule maintenance becomes a full-time job at scale.

**2010s — Machine Learning:** The shift. Instead of writing rules, you train models on labelled data (10,000 phishing URLs + 10,000 legitimate URLs). The model discovers the rules itself. CrowdStrike, Cylance, and Darktrace built their early products on this generation.

**2018+ — Deep Learning:** Neural networks that process raw data (packet bytes, binary executables, full email text) without manual feature engineering. More powerful but less interpretable. Requires more data and compute.

**2023+ — Generative AI:** LLMs that can read, summarise, and reason over security data. Used for analyst copilots, automated triage, report generation, and RAG over threat intelligence. This is where the industry is investing now — and what you'll build in Stage 4.

### The Key Insight for Customer Conversations

> Each generation did not replace the previous one. Production security stacks use **all of them simultaneously**. A modern endpoint agent might use signature matching (fast, precise), ML classifiers (broader detection), and an LLM copilot (analyst assistance) — all in the same product.

When a customer asks "Do you use AI?", the real question is "Which generation of AI, for which problem, and how do they work together?"

---

## Part 3 — Where AI Is Deployed in Security Today (20 min)

### The AI Map Across the Security Stack

```
+------------------------------------------------------------------+
|                        SECURITY STACK                             |
|                                                                   |
|  ENDPOINT          NETWORK          EMAIL           IDENTITY      |
|  +-----------+    +-----------+    +-----------+   +-----------+  |
|  | Behavioural|   | Traffic   |    | Phishing  |   | Anomalous |  |
|  | analysis   |   | anomaly   |    | detection |   | login     |  |
|  | Process    |   | DPI +     |    | URL       |   | detection |  |
|  | lineage    |   | flow      |    | analysis  |   | Risk      |  |
|  | ML models  |   | analysis  |    | NLP on    |   | scoring   |  |
|  +-----------+    +-----------+    | body text |   +-----------+  |
|                                    +-----------+                  |
|                                                                   |
|  SIEM/SOAR         CLOUD           THREAT INTEL    VULNERABILITY  |
|  +-----------+    +-----------+    +-----------+   +-----------+  |
|  | Alert     |    | Config    |    | IOC        |   | Priority  |  |
|  | scoring   |    | drift     |    | clustering |   | scoring   |  |
|  | Anomaly   |    | detection |    | Campaign   |   | Exploit   |  |
|  | detection |    | Workload  |    | attribution|   | prediction|  |
|  | Auto-     |    | profiling |    | Report     |   | CVSS      |  |
|  | triage    |    +-----------+    | generation |   | enrichment|  |
|  +-----------+                     +-----------+   +-----------+  |
+------------------------------------------------------------------+
```

### Breakdown by Domain

#### Endpoint Detection & Response (EDR)

| What AI Does | How It Works | Example |
|-------------|-------------|---------|
| Behavioural analysis | ML model trained on process behaviour — file access patterns, network calls, registry modifications | Detects fileless malware by flagging unusual PowerShell execution chains |
| Process lineage scoring | Decision tree or random forest scores parent-child process relationships | Flags `outlook.exe → powershell.exe → cmd.exe` as suspicious |
| Pre-execution classification | ML classifier on static file features (PE headers, import tables, entropy) before the file runs | Blocks a novel binary that resembles known malware families |

#### Email Security

| What AI Does | How It Works | Example |
|-------------|-------------|---------|
| Phishing URL analysis | Logistic regression or gradient boost on URL features (length, domain age, path depth, TLD) | Catches URLs that pass SPF/DKIM but have phishing structural patterns |
| Body text analysis | NLP models (now increasingly LLMs) analyse writing style, urgency cues, impersonation signals | Detects BEC attempts where a "CEO" requests an urgent wire transfer |
| Attachment sandboxing + ML | Combine sandbox detonation with ML classification of observed behaviours | Classifies attachments that evade signature scanners |

#### SIEM and SOAR

| What AI Does | How It Works | Example |
|-------------|-------------|---------|
| Alert scoring / prioritisation | ML model trained on analyst feedback — which alerts were true positives vs noise | Reduces alert volume by 60-80% by surfacing only high-confidence incidents |
| Anomaly detection | Unsupervised learning (k-means, isolation forest) on log baselines | Flags a service account authenticating at 3 AM from a new geography |
| Automated triage | LLM reads alert context, enriches with threat intel, suggests playbook | Copilot summarises an incident and recommends containment steps |

#### Network Detection & Response (NDR)

| What AI Does | How It Works | Example |
|-------------|-------------|---------|
| Traffic classification | Deep learning on packet metadata (flow duration, byte distribution, protocol behaviour) | Identifies C2 beaconing hidden in HTTPS traffic |
| Lateral movement detection | Graph-based ML on authentication and connection patterns | Detects credential hopping across hosts after initial compromise |
| DNS anomaly detection | Statistical model on query patterns, domain generation algorithm (DGA) detection | Catches DGA domains used by botnets for C2 resolution |

#### Identity and Access

| What AI Does | How It Works | Example |
|-------------|-------------|---------|
| Impossible travel detection | Geolocation + timing analysis (often rule-based, increasingly ML) | Flags login from London 10 minutes after login from Tokyo |
| Risk-based authentication | ML model scores login risk based on device, location, time, behaviour | Steps up to MFA only when risk score exceeds threshold |
| Privilege anomaly detection | Baseline normal access patterns, flag deviations | Alerts when a developer suddenly accesses production databases |

### What to Notice

1. **ML is already everywhere** — this is not future technology. Every major security vendor ships ML models today.
2. **Most production models are "classic ML"** — random forests, gradient boosting, logistic regression. Not deep learning, not LLMs.
3. **LLMs are the newest layer** — primarily used for copilots and triage assistance, not core detection (yet).
4. **The biggest impact is often the simplest model** — alert scoring with a random forest can cut analyst workload by 60-80%. That's not glamorous, but it's transformative.

---

## Part 4 — AI Washing: Spotting Hype (10 min)

### What Is AI Washing?

AI washing is when a product claims to use "AI" or "ML" but the actual technology is:
- Hard-coded rules labelled as "AI-driven"
- Simple statistical thresholds marketed as "machine learning"
- A product that uses an LLM API call with no meaningful integration
- A feature that was already there, rebranded with "AI" in the name

### The Detection Framework

When evaluating an AI claim — from a competitor, a vendor, or your own product — ask these five questions:

```
+-------------------------------------------------------+
|           AI CLAIM EVALUATION FRAMEWORK               |
|                                                       |
|  1. WHAT MODEL?                                       |
|     "What algorithm or model architecture?"            |
|     Vague: "proprietary AI"                           |
|     Real: "gradient-boosted tree on 50M samples"      |
|                                                       |
|  2. WHAT DATA?                                        |
|     "What training data? How much? How often updated?"|
|     Vague: "trained on global threat intelligence"    |
|     Real: "retrained weekly on 2M labelled events"    |
|                                                       |
|  3. WHAT METRIC?                                      |
|     "What's the false positive rate? Recall?"         |
|     Vague: "industry-leading detection rates"         |
|     Real: "97% recall at 0.1% FPR on CICIDS2017"     |
|                                                       |
|  4. WHAT BASELINE?                                    |
|     "Compared to what? Rules alone? Previous version?"|
|     Vague: "significantly reduces alert fatigue"      |
|     Real: "58% fewer false positives vs rule-only"    |
|                                                       |
|  5. WHAT FAILS?                                       |
|     "Where does the model struggle? What are the      |
|      known failure modes?"                            |
|     Vague: (silence)                                  |
|     Real: "struggles with encrypted C2 over port 443" |
+-------------------------------------------------------+
```

### Red Flags in Vendor Claims

| Red Flag | What It Usually Means |
|----------|----------------------|
| "AI-powered" with no technical detail | Marketing label on existing rules |
| "Self-learning" with no retraining pipeline described | Static model shipped once, never updated |
| Claims 99.9%+ accuracy | Either cherry-picked metric, or the problem is too easy to need ML |
| "No false positives" | Not measuring properly, or heavily filtering before evaluation |
| "Replaces your SOC analysts" | Overpromising — current AI assists analysts, it doesn't replace them |
| Only mentions LLMs / ChatGPT when the product is a classifier | Riding the hype wave; the actual product is classic ML (which is fine) |

### The Right Response Is Not Cynicism

AI washing is real, but so is genuine AI in security. The goal is not to dismiss AI claims — it's to **evaluate them with precision**. After completing this program, you will have the technical depth to do exactly that.

---

## Part 5 — Where the Market Is Heading (5 min)

### Three Trends to Watch

**1. LLM Copilots Everywhere**
Every major vendor is shipping an LLM-based assistant: Microsoft Copilot for Security, CrowdStrike Charlotte AI, SentinelOne Purple AI, Palo Alto Cortex XSIAM Copilot. These are RAG-based systems — the same architecture you'll build in Stage 4.

**2. AI for Offensive Security**
Attackers are using LLMs for phishing email generation, code obfuscation, vulnerability discovery, and social engineering at scale. This is not theoretical — it's happening now. Defenders need AI literacy to understand what they're facing.

**3. Autonomous Response**
The frontier is moving from "AI detects, human responds" to "AI detects and takes containment action." Automated quarantine, network isolation, credential revocation. High stakes — the model must be right, or it causes outages.

### What This Means for You

As a security architect or engineer in a customer-facing role, you are at the intersection of these trends. Customers will ask you:
- "Should we trust AI-based detection?"
- "How is your AI different from [competitor]?"
- "Can AI replace our Tier 1 analysts?"
- "What's the risk of adversarial attacks against your ML models?"

By the end of this program, you will answer every one of these with technical depth — not marketing talking points.

---

## Discussion Exercise (remaining time)

### Round-Table: AI Claims You've Encountered

Each participant shares one AI claim they've seen in the field — from a competitor, a vendor, a customer RFP, or their own product. The group evaluates it using the 5-question framework.

**Format:**
1. One participant states the claim (30 seconds)
2. The group asks the 5 evaluation questions (2 minutes)
3. Group rates: Real AI / Partial / AI Washing (30 seconds)
4. Rotate to the next participant

**Goal:** Practice the evaluation framework on real examples so it becomes instinctive.

---

## Key Takeaways

1. **AI in security is mostly classic ML** — random forests, gradient boosting, logistic regression. Knowing this gives you credibility.
2. **Each generation of AI adds a layer** — signatures, heuristics, ML, deep learning, LLMs all coexist in production.
3. **AI is deployed across the entire security stack** — endpoint, network, email, identity, SIEM, cloud, threat intel.
4. **Use the 5-question framework** to evaluate any AI claim: What model? What data? What metric? Compared to what? Where does it fail?
5. **The market is moving toward LLM copilots and autonomous response** — you'll build the former in Stage 4.

---

## Next Session

**[Session 0.2 — How Competitors Position AI](../02_competitor_analysis/README.md)**
Deep dive into what CrowdStrike, Palo Alto, SentinelOne, Darktrace, and Microsoft are actually doing under the hood.
