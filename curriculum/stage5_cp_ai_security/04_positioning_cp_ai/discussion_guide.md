# Discussion Guide — Session 5.4: Positioning Check Point AI Security

> **For facilitators and self-study.** Use these exercises during the live session or work through them independently.

---

## Exercise 1: Elevator Pitch Practice (15 min)

### Task — Round 1: Deliver (6 min)

Each participant delivers the 2-minute unified Check Point AI Security pitch to a partner. The pitch should cover:
- The problem (shadow AI, unprotected LLM applications, ungoverned agents)
- The solution (Workforce AI Security + AI Guardrails + AI Agent Security)
- The differentiator (unified platform, prevention-first, integrated with existing Check Point infrastructure)
- The call to action

**Partner feedback form:**

| Criterion | Score (1-5) | Notes |
|-----------|------------|-------|
| Clear problem statement in the first 15 seconds | | |
| All three products mentioned with distinct value | | |
| Customer-centric language (not feature-listing) | | |
| Confident delivery, natural pacing | | |
| Compelling close / call to action | | |

### Task — Round 2: Switch (6 min)

Switch roles. The listener now delivers. The new listener scores.

### Task — Round 3: Best Pitch (3 min)

Each pair nominates their stronger pitch. The nominees deliver to the full group. Group votes on the most compelling.

**Discussion:**
- What made the winning pitch effective?
- Where did people struggle most — the opening, the middle, or the close?
- How would you adapt this pitch for a 30-second version? What would you cut?

---

## Exercise 2: Competitive Bake-Off Role-Play (20 min)

### Setup

Work in pairs. One person plays the **customer**, the other plays the **Check Point SE**.

### Customer Context

The customer is evaluating:
- **Microsoft Purview** for AI data governance (already in their E5 license)
- **Zscaler** for AI/ML traffic inspection (already deployed as their SWG)

The customer's perspective:
- "We already pay for Purview — why would we buy another tool?"
- "Zscaler sees all our web traffic, including AI tools. Isn't that enough?"
- "We want to consolidate vendors, not add more."

### Competitive positioning reference:

| Capability | Microsoft Purview | Zscaler | Check Point AI Security |
|-----------|------------------|---------|----------------------|
| Shadow AI discovery | Limited to Copilot ecosystem | URL-level visibility only | Full prompt-level visibility across all AI tools |
| Content inspection depth | DLP labels only | TLS inspection of traffic | Prompt and response content analysis with context |
| AI-specific policy actions | Allow / Block | Allow / Block / Isolate | Allow / Prevent / Redact / Detect / Block / Ask |
| Agent security | Not available | Not available | MCP-level control, least privilege, audit |
| LLM guardrails | Not available | Not available | Inbound and outbound prompt protection |
| Deployment for AI tools | Requires Microsoft ecosystem | Requires Zscaler proxy chain | Agentless, API-based, works with any AI tool |

### Round 1 (10 min)

The Check Point SE positions against the competitive landscape. The customer pushes back using the objections above.

### Round 2 (10 min)

Switch roles.

### Debrief
- What arguments worked best against the "we already have Purview" objection?
- What arguments worked best against the "Zscaler already sees AI traffic" objection?
- When the customer said "consolidate vendors, not add more," what was the most effective counter?
- Where did you feel weakest in your positioning? What do you need to learn more about?

---

## Exercise 3: Demo Selection (10 min)

### Customer Profiles

**Customer 1: CISO worried about data leakage**
- Industry: Financial services
- Pain: Board has asked for a report on AI risk exposure
- Current state: No AI policy, no visibility, employees using 10+ AI tools
- Technical maturity: Low (no SIEM, basic firewall, outsourced SOC)

**Customer 2: DevSecOps team building a chatbot**
- Industry: Technology / SaaS
- Pain: Shipping a customer-facing LLM application, concerned about prompt injection and data poisoning
- Current state: Application in staging, using GPT-4 via API, no guardrails
- Technical maturity: High (mature CI/CD, Kubernetes, existing security tooling)

**Customer 3: SOC team automating with agents**
- Industry: Large enterprise (10,000+ employees)
- Pain: 15,000 alerts/day, 60% false positives, struggling to hire analysts
- Current state: Evaluating AI agents for triage, enrichment, and response
- Technical maturity: High (Splunk, CrowdStrike, Palo Alto, mature SOC)

### Task

For each customer, choose the demo option that would have the most impact and explain your reasoning:

| Demo Option | Focus | Best For |
|------------|-------|----------|
| **Option A** | Workforce AI Security: shadow AI discovery, policy enforcement, dashboard | |
| **Option B** | AI Guardrails: prompt injection detection, content filtering, architecture | |
| **Option C** | AI Agent Security + MCP: agent governance, least privilege, audit trail | |

| Customer | Your Demo Choice | Why This Demo? | Opening Statement to Customer |
|----------|-----------------|---------------|------------------------------|
| 1: CISO / data leakage | | | |
| 2: DevSecOps / chatbot | | | |
| 3: SOC / agents | | | |

**Discussion:**
- Did everyone agree on the demo choice for each customer? Where did opinions differ?
- Would you ever show more than one demo in a single meeting? When is that appropriate vs. when does it dilute the message?
- How would you handle a customer who says "Show me everything"?

---

## Exercise 4: Objection Gauntlet (15 min)

### Setup

One volunteer sits in the "hot seat." The rest of the group fires AI security objections one at a time. The volunteer must handle each objection using the **ACE** (Acknowledge, Challenge, Explore) and **PDFC** (Pain, Data, Fit, Commitment) frameworks from Stage 0.

### Objection bank (facilitator selects 3-4 per round):

| # | Objection | Framework Hint |
|---|----------|----------------|
| 1 | "AI security is premature. The technology is too new." | ACE — Challenge with market data |
| 2 | "We already block ChatGPT. Problem solved." | ACE — Challenge with shadow AI reality |
| 3 | "Our DLP solution already covers this." | ACE — Challenge with AI-specific gaps |
| 4 | "We don't have budget for another security product." | PDFC — Quantify the Pain, then show Fit |
| 5 | "Microsoft Purview is included in our E5 license." | ACE — Acknowledge the value, Challenge the scope |
| 6 | "We're waiting to see how the market matures." | ACE — Explore what their competitors are doing |
| 7 | "Our developers say guardrails add latency." | ACE — Acknowledge the concern, Challenge with data |
| 8 | "We tried an AI security product before and it created too many false positives." | ACE — Acknowledge the experience, Explore what they tried |
| 9 | "Our legal team says we can't log employee AI usage." | ACE — Explore the actual regulation, Challenge the interpretation |
| 10 | "The board doesn't see AI security as a priority." | PDFC — Pain (what happens after a breach), Commitment (board engagement) |

### Rules
- Volunteer gets 60-90 seconds per objection
- Group scores each response: Strong / Adequate / Needs Work
- After 3-4 objections, rotate to a new volunteer

### Scoring criteria:

| Criterion | Strong | Adequate | Needs Work |
|-----------|--------|----------|------------|
| Acknowledged the objection without dismissing it | | | |
| Challenged with a specific fact or insight | | | |
| Asked an explore question that advanced the conversation | | | |
| Maintained confident, consultative tone | | | |

### Debrief
- Which objection was hardest to handle? Why?
- Which response got the best score? What made it work?
- Are there objections not on this list that you hear frequently? Add them for next time.

---

## Exercise 5: Final Preparation (10 min)

### Task

Each participant identifies their next real customer meeting where AI security could come up. Complete the preparation template:

| Preparation Item | Your Plan |
|-----------------|-----------|
| **Customer name** (or type if confidential) | |
| **Industry** | |
| **Meeting context** (new prospect, existing customer, renewal, QBR) | |
| **Product you will lead with** (Workforce AI Security / AI Guardrails / AI Agent Security) | |
| **Why this product first?** | |
| **Demo you will show** (Option A / B / C) | |
| **Opening question you will ask** | |
| **Objection you expect** | |
| **Your planned response to that objection** (using ACE) | |
| **Metric or proof point you will reference** | |
| **Desired outcome of the meeting** | |

### Group feedback (5 min)

Each participant shares their plan in 60 seconds. The group provides:
- One thing that's strong about the plan
- One suggestion to improve it

### Debrief
- How confident do you feel positioning AI security compared to when Stage 5 started?
- What's the one thing you still need to learn or practice before your customer meeting?
- What resource from the programme will you reference most in the field?

---

## Self-Study Reflection Questions

1. If you had to position Check Point AI Security in one sentence to a non-technical executive, what would you say?
2. What is the strongest competitive differentiator Check Point has in AI security today? Is it a product capability, an architectural advantage, or a strategic positioning?
3. Think about the last three customer conversations you had. In how many of them could AI security have been relevant? What would you have said differently with what you know now?
4. After completing Stage 5, what is the single most important thing you will do differently in your next customer meeting?
