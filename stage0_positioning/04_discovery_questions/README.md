# Session 0.4 — Discovery Questions for AI Use Cases

> **Format:** Workshop  |  **Duration:** 60 min  |  **Prerequisites:** Sessions 0.1–0.3

---

## Learning Objectives

By the end of this session you will be able to:

1. Use the PDFC framework to systematically uncover AI opportunities in customer environments
2. Ask the right questions to qualify whether a problem is ML-solvable
3. Identify red flags that indicate AI is NOT the right solution
4. Map discovered pain points to specific ML approaches from Stages 1-4

---

## Why Discovery Matters More Than Demos

The biggest mistake in selling AI-powered solutions: leading with a demo of what AI can do instead of asking what the customer actually needs.

A demo says: "Look at this cool technology."
A discovery conversation says: "I understand your problem. Here's why AI is the right way to solve it."

**The customer doesn't care about AI. They care about:**
- Reducing alert fatigue
- Catching threats faster
- Doing more with fewer analysts
- Meeting compliance requirements
- Reducing dwell time

AI is the mechanism. Discovery uncovers the motivation.

---

## The PDFC Framework

```
+---------------------------------------------------------------+
|                   PDFC DISCOVERY FRAMEWORK                    |
|                                                               |
|   P — PAIN                                                    |
|       What problem are they trying to solve?                  |
|       What's the business impact of not solving it?           |
|                                                               |
|   D — DATA                                                    |
|       What data do they have? Where does it live?             |
|       Is it labelled? How much? How clean?                    |
|                                                               |
|   F — FIT                                                     |
|       Is this problem ML-solvable? Which approach fits?       |
|       What's the alternative (rules, manual, outsource)?      |
|                                                               |
|   C — COMMITMENT                                              |
|       Do they have the resources to operationalise AI?        |
|       Who owns the model after deployment?                    |
+---------------------------------------------------------------+
```

Each phase has a set of discovery questions. Work through them in order — each phase gates the next.

---

## Phase 1: PAIN — Uncovering the Problem (15 min)

### The Goal

Understand what hurts. Not what technology they want — what business problem keeps them up at night. AI is never the starting point of a conversation; pain is.

### Discovery Questions

#### Alert and Detection Pain

> "Walk me through what happens when an alert fires in your SOC today. How many alerts per day? How many get investigated? How many turn out to be real?"

**What you're listening for:** Alert volume, true positive rate, triage time. If they get 10,000 alerts/day and investigate 200, there's a massive scoring/prioritisation opportunity (Stage 1: classification, Stage 2: random forests).

> "What types of threats are you most worried about missing? Where do you feel blind?"

**What you're listening for:** Detection gaps — these map to ML-solvable problems. Insider threats → unsupervised anomaly detection. Novel malware → behavioural ML. Phishing → NLP classification.

> "How do you handle threats that don't match a known signature or rule?"

**What you're listening for:** If the answer is "we don't" or "manual hunt" — that's a direct use case for ML-based detection.

#### Operational Pain

> "If you could give every analyst on your team one superpower, what would it be?"

**What you're listening for:** Speed (→ LLM copilot), accuracy (→ ML scoring), coverage (→ automated detection), context (→ RAG over threat intel).

> "How much time does your team spend on repetitive tasks — triage, enrichment, report writing?"

**What you're listening for:** Automation opportunities. If analysts spend 2 hours per incident on enrichment and summary, that's a direct RAG/LLM use case (Stage 4).

> "What's your mean time to detect and mean time to respond? Are you measured on those metrics?"

**What you're listening for:** If MTTD/MTTR are KPIs, any improvement is quantifiable ROI.

#### Strategic Pain

> "Has your board or executive team asked about AI in security? What was the context?"

**What you're listening for:** Top-down AI mandates are increasingly common. If the board is asking, there's budget and urgency. Position yourself as the guide who helps them do it right.

> "Are you evaluating any competitors that position heavily on AI? What claims have they made?"

**What you're listening for:** Competitive context. Use your knowledge from Session 0.2 to provide a technically grounded comparison.

---

## Phase 2: DATA — Assessing ML Readiness (10 min)

### The Goal

Determine whether the customer has the data to make AI work. No data = no ML. Wrong data = wrong model.

### Discovery Questions

> "What telemetry sources are you collecting today? Endpoint, network, identity, cloud, email?"

**What you're listening for:** Data breadth. ML models are only as good as the features they're trained on. More diverse telemetry = richer features.

> "How far back does your log retention go? 30 days? 90 days? A year?"

**What you're listening for:** Training data volume. Most ML models need at least 3-6 months of historical data to learn stable patterns. If they retain 30 days, unsupervised baselines will be noisy.

> "Do you have any labelled data — incidents categorised as true positive or false positive? Analyst verdicts on alerts?"

**What you're listening for:** Supervised ML (Stages 1-2) needs labelled data. If they have analyst verdict history in their SIEM, that's gold. If not, point toward unsupervised approaches or pre-trained models.

> "Where does your data live? On-prem SIEM? Cloud data lake? Multiple locations?"

**What you're listening for:** Data architecture affects deployment. Cloud-native data lakes are easier to feed into ML pipelines. On-prem SIEMs with strict egress controls may need on-prem model deployment.

> "How clean is your data? Are there normalisation issues, missing fields, inconsistent formats across sources?"

**What you're listening for:** Data quality. Feature engineering (Lesson 2.1) can handle some messiness, but fundamentally broken data pipelines need to be fixed before ML adds value.

### The Data Readiness Matrix

| Data Situation | ML Approach That Fits | Program Stage |
|---------------|----------------------|---------------|
| Rich labelled data (analyst verdicts, categorised incidents) | Supervised classification — random forest, logistic regression | Stages 1-2 |
| Lots of unlabelled telemetry, no labels | Unsupervised clustering and anomaly detection | Stage 2 |
| Some labelled data, mostly unlabelled | Semi-supervised or transfer learning | Stages 2-3 |
| No internal data, but domain expertise | Pre-trained models, zero-shot classification, LLM APIs | Stage 4 |
| Historical data + unstructured documents (runbooks, reports) | RAG over documents + ML on structured data | Stage 4 |

---

## Phase 3: FIT — Qualifying the ML Use Case (10 min)

### The Goal

Not every problem needs AI. Some are better solved with rules, SOAR playbooks, or additional headcount. This phase qualifies whether ML is genuinely the right fit.

### The ML Fit Checklist

For a problem to be a good ML candidate, it should meet at least 4 of these 6 criteria:

```
+---------------------------------------------------------------+
|               ML FIT CHECKLIST                                |
|                                                               |
|   [ ] 1. PATTERN-BASED                                        |
|         The problem involves finding patterns in data          |
|         that are too complex or numerous for manual rules      |
|                                                               |
|   [ ] 2. DATA AVAILABLE                                       |
|         Relevant data exists (labelled or unlabelled)          |
|         in sufficient volume                                   |
|                                                               |
|   [ ] 3. TOLERANCE FOR IMPERFECTION                           |
|         The use case can handle some false positives           |
|         or false negatives — it's not all-or-nothing          |
|                                                               |
|   [ ] 4. SCALE PROBLEM                                        |
|         The volume of signals or decisions exceeds             |
|         what humans can handle manually                        |
|                                                               |
|   [ ] 5. DYNAMIC THREAT LANDSCAPE                             |
|         The patterns change over time — rules would            |
|         require constant manual updating                       |
|                                                               |
|   [ ] 6. MEASURABLE OUTCOME                                   |
|         You can define what "better" looks like                |
|         (fewer FPs, faster MTTD, higher recall)               |
+---------------------------------------------------------------+
```

### Discovery Questions for Fit

> "If I gave you a model that was 95% accurate at this task, would that be useful? What about 80%?"

**What you're listening for:** Tolerance for imperfection. If they need 100% accuracy, ML is not the right tool — rules or manual review are better. Most security use cases work well at 90-95%.

> "How many [alerts / decisions / classifications] per day are we talking about?"

**What you're listening for:** Scale. If it's 50 alerts a day, a human can handle it. If it's 5,000, they need ML scoring.

> "What does the current process look like without AI? Rules? Manual review? Nothing?"

**What you're listening for:** The baseline. ML needs to beat something. If there's no current process, the bar is low and impact is high. If there's a mature rule set, ML needs to demonstrably improve on it.

> "How would you measure success? What metric would prove this is working?"

**What you're listening for:** Measurability. If they can define success metrics (MTTD reduction, FP reduction, analyst hours saved), you can build a business case. If they can't, they're not ready.

### Red Flags: When AI Is NOT the Answer

| Red Flag | Why | Better Alternative |
|----------|-----|-------------------|
| "We need 100% accuracy" | No ML model achieves perfection; all have error rates | Rules for known patterns + ML for probabilistic scoring |
| "We have 50 events a day" | Too low volume for ML to add value over human review | SOAR playbook automation |
| "We can't tolerate any false positives" | ML inherently trades FPs for FNs; zero FPs means blind spots | Manual review with ML as a second opinion |
| "We don't know what success looks like" | Can't measure improvement → can't justify investment | Start with EDA (Stage 1) to understand the data first |
| "We want AI because the board asked for it" | AI without a problem to solve is an expensive experiment | Help them identify the problem first, then fit AI to it |
| "The problem changes every day" | If patterns are completely unpredictable, ML can't learn stable ones | Real-time rule updates or human-in-the-loop triage |

---

## Phase 4: COMMITMENT — Operationalisation (10 min)

### The Goal

Even the best ML model fails if no one owns it after deployment. This phase assesses whether the customer can operationalise AI long-term.

### Discovery Questions

> "Who would own the AI/ML capability after deployment — your security team, IT, a data team, or a vendor?"

**What you're listening for:** Ownership. Models need monitoring, retraining, and threshold tuning. If no one owns it, it will decay.

> "Do you have anyone on staff with data science or ML experience? Or would this be fully vendor-managed?"

**What you're listening for:** Internal capability vs. dependence. This is exactly what your Ninja program builds — architects who can evaluate, tune, and manage AI systems.

> "How would this integrate with your existing workflow? What would change for your analysts day-to-day?"

**What you're listening for:** Change management. An ML model that adds a new dashboard no one checks is wasted. The output needs to integrate into existing SIEM/SOAR workflows.

> "What's your timeline? Are you looking at a POC, a phased rollout, or a full deployment?"

**What you're listening for:** Urgency and commitment. A POC is a great starting point — it lets you prove value with low risk.

> "What budget have you allocated for AI/ML initiatives this year?"

**What you're listening for:** Reality check. If there's no budget, this is a future opportunity. If there's allocated AI budget (increasingly common), you're in a qualified deal.

---

## Mapping Discovery to Solutions

After PDFC discovery, map what you learned to a specific solution approach:

| Pain Discovered | Data Available | Best ML Approach | Program Stage |
|----------------|---------------|-----------------|---------------|
| Alert fatigue — too many false positives | Analyst verdicts in SIEM (labelled) | Alert scoring with supervised ML (random forest) | Stage 2 |
| Missing novel threats | Raw endpoint telemetry (unlabelled) | Behavioural anomaly detection (unsupervised) | Stage 2 |
| Slow investigation / triage | Incident data + threat reports (documents) | LLM copilot with RAG over internal docs | Stage 4 |
| Phishing getting past email filters | URL logs + user reports (labelled) | Phishing URL classifier (logistic regression) | Stage 1 |
| Insider threat detection | User activity logs (unlabelled) | Clustering + anomaly scoring (k-means) | Stage 2 |
| Manual threat intel processing | CVE feeds + reports (unstructured text) | RAG pipeline over threat intel corpus | Stage 4 |
| Vulnerability prioritisation | CVSS data + exploit history (structured) | Risk scoring model (gradient boosting) | Stage 2 |
| SOC analyst onboarding | Runbooks + past incident reports | RAG-based knowledge assistant | Stage 4 |

---

## Workshop Exercise: Practice Discovery (20 min)

### Scenario-Based Role-Play

Work in pairs. One person is the architect, one is the customer. The architect must use PDFC to uncover AI opportunities. The customer should answer honestly based on the scenario — don't make it easy.

#### Scenario 1: Regional Bank (10 min)

**Customer profile:**
- Regional bank, 500 employees, 5-person security team
- Splunk SIEM with 90-day retention
- 3,000 alerts per day, team investigates ~100
- Recently failed a phishing simulation (40% click rate)
- CISO wants "an AI strategy" for the board presentation next quarter
- No ML experience on the team
- Budget: exploring, not allocated

**Architect goal:** Use PDFC to find at least two qualified AI use cases and one red flag.

#### Scenario 2: Large Enterprise (10 min)

**Customer profile:**
- Fortune 500 manufacturing company, global operations
- Microsoft Sentinel + Defender XDR stack
- 50-person SOC across 3 regions
- Investigating Security Copilot but uncertain about ROI
- OT/IT convergence creating new threat surface
- Have 2 years of labelled incident data
- Data science team exists but has never worked on security
- Budget: $500K allocated for "AI/ML security initiatives"

**Architect goal:** Use PDFC to identify the highest-value AI use case and build a POC proposal.

### Debrief Questions
- What was the first AI use case you identified? Was it the highest-value one?
- Did the DATA phase change your recommendation?
- Where did you find red flags? How did you handle them?
- What would your POC proposal look like?

---

## Key Takeaways

1. **Discovery before demo** — understand the problem before showing the technology
2. **PDFC structures the conversation** — Pain, Data, Fit, Commitment. Each phase gates the next.
3. **Not every problem needs AI** — qualifying out is as valuable as qualifying in. It builds trust.
4. **Data readiness determines approach** — labelled data → supervised ML; unlabelled → unsupervised; unstructured → RAG
5. **Operationalisation is the hidden risk** — the best model fails if no one owns, monitors, and retrains it
6. **Map pain to Stages 1-4** — every customer pain point connects to a specific ML technique you'll learn in this program

---

## Stage 0 Complete

You've finished all four positioning sessions. You can now:
- Explain AI in security with technical precision (Session 0.1)
- Evaluate competitor AI claims (Session 0.2)
- Handle AI objections with the ACE framework (Session 0.3)
- Discover AI opportunities using PDFC (Session 0.4)

**Next:** [Stage 1 — Classic Machine Learning](../../stage1_classic_ml/README.md) — time to build the technical depth behind the conversations.
