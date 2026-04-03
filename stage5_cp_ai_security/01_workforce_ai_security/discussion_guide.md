# Discussion Guide — Session 5.1: Workforce AI Security

> **For facilitators and self-study.** Use these exercises during the live session or work through them independently.

---

## Exercise 1: Shadow AI Audit (15 min)

Individually, list every AI tool you have seen customers using — both approved and unapproved. Include tools used by IT, developers, marketing, HR, legal, and executives.

| AI Tool | Department(s) Using It | Approved by IT? | Data Types Exposed | Risk Level (H/M/L) |
|---------|----------------------|-----------------|-------------------|-------------------|
| | | | | |
| | | | | |
| | | | | |
| | | | | |

Now combine your lists as a group into a single master inventory on a whiteboard or shared document.

**Discussion:**
- How many total tools did the group identify?
- What percentage are unmanaged (no IT approval, no policy, no visibility)?
- Which unapproved tools surprised you the most?
- If a customer's CISO saw this list for the first time, what would their reaction be?

---

## Exercise 2: Policy Design Workshop (20 min)

### Scenario

A financial services firm with 500 employees is using three AI tools:
- **ChatGPT** (browser-based, used by marketing, legal, and executives)
- **GitHub Copilot** (IDE plugin, used by 40 developers)
- **Claude** (browser-based, used by analysts and compliance team)

Design a policy matrix defining what action Workforce AI Security should take for each combination of tool and data type.

**Actions available:** Allow | Prevent | Redact | Detect | Block | Ask

| Data Type | ChatGPT | GitHub Copilot | Claude |
|-----------|---------|---------------|--------|
| **PII** (names, SSNs, account numbers) | | | |
| **Source code** (proprietary application code) | | | |
| **Financial data** (earnings, forecasts, M&A) | | | |
| **Customer communications** (emails, tickets) | | | |
| **General queries** (research, writing help) | | | |
| **Regulated data** (SOX, GDPR-relevant) | | | |

**Discussion:**
- Where did your group disagree? What drove the disagreement?
- Is "Block" ever the right default, or does it just push users to personal devices?
- How would this matrix change if the firm were in healthcare instead of financial services?
- Which action is hardest to implement without Workforce AI Security?

---

## Exercise 3: Dashboard Interpretation (10 min)

You have been given access to the Workforce AI Security dashboard for a mid-size enterprise. Here are the metrics from the last 30 days:

| Metric | Value |
|--------|-------|
| Total AI interactions monitored | 47,200 |
| Unique users | 812 of 2,000 employees (41%) |
| Top AI tool by volume | ChatGPT (61%) |
| Second tool | Copilot (24%) |
| Third tool | Gemini (9%) |
| Sensitive data exposure events | 1,340 |
| PII detected and redacted | 487 |
| Source code uploads blocked | 218 |
| Policy violations (user warned and continued) | 635 |
| Shadow AI tools discovered (previously unknown) | 7 |
| Departments with highest AI usage | Engineering (34%), Marketing (22%), Legal (18%) |
| After-hours AI usage (outside 8am-6pm) | 31% of all interactions |

**Task:** Write a 3-sentence executive summary for the CISO. It must convey the key risk, the scale of the issue, and a recommended action.

**Compare your summaries as a group:**
- Who led with risk? Who led with value?
- Which summary would make a CISO take action fastest?
- What metric did you choose to highlight, and why?

---

## Exercise 4: "Block Everything" Debate (15 min)

### Setup

Split the group into two teams.

**Team A — The Blockers:** Argue that the safest approach is to block all generative AI tools across the enterprise. No exceptions.

**Team B — The Governors:** Argue that governed access through Workforce AI Security is the better approach — visibility and policy instead of blanket prohibition.

### Rules
- Each team gets 3 minutes for an opening statement
- 5 minutes of rebuttals (alternating 1 minute each)
- Each team gets 1 minute for a closing statement

### Preparation prompts

**Team A (Block Everything):**
- Data leakage is irreversible — one incident can end a career
- Employees can use AI on personal devices anyway, so blocking at least removes corporate liability
- Regulatory compliance is simpler when the answer is "we don't allow it"

**Team B (Governed Access):**
- Blocking drives usage underground and eliminates all visibility
- Competitors who adopt AI will outpace those who block it
- Workforce AI Security gives the CISO control without killing productivity

### Debrief
- Which arguments were hardest to counter?
- In reality, which approach do most of your customers take today?
- How does this debate map to the early days of BYOD and cloud adoption?

---

## Exercise 5: Customer Scenario (15 min)

### The Situation

A healthcare company has 200 doctors using ChatGPT for patient note summarisation. The practice has grown organically over six months. The CISO had no idea this was happening. IT has no logs, no policy, and no controls.

You have just shown the CISO the Workforce AI Security dashboard for a 14-day proof-of-value. The dashboard reveals:

| Finding | Detail |
|---------|--------|
| Doctors using ChatGPT | 194 of 200 |
| Patient data (PHI) detected in prompts | 1,847 instances |
| Prompts containing full patient names | 612 |
| Prompts containing diagnosis information | 923 |
| Average prompts per doctor per day | 8.3 |
| Data sent to unapproved AI tools (not ChatGPT) | 14% of traffic — Gemini, Claude, Perplexity |
| HIPAA-relevant exposure events | 1,847 (all PHI instances) |

### Task

Role-play the conversation with the CISO. Work through these stages:

1. **Present the findings** — How do you frame the data without creating panic?
2. **Handle the reaction** — The CISO says: "We need to shut this down immediately." How do you respond?
3. **Propose the path forward** — What policy would you recommend? (Use your matrix from Exercise 2 as a starting point, adapted for healthcare.)
4. **Address the doctors** — The CISO asks: "How do I tell 200 doctors they can't use the tool that saves them an hour a day?" What do you suggest?
5. **Close** — What does the next step look like? POC? Full deployment? Policy workshop?

**Debrief:**
- What was the hardest part of this conversation?
- How did you balance urgency (PHI exposure) with empathy (doctors' productivity)?
- What would you have done differently in a real meeting?

---

## Self-Study Reflection Questions

1. Think about your own organisation. If a Workforce AI Security dashboard were deployed tomorrow, what would it reveal? What would surprise leadership?
2. What is the difference between "blocking AI" and "governing AI"? Why does this distinction matter in a sales conversation?
3. How does the shadow AI problem compare to the shadow IT problem from 10 years ago? What lessons from that era apply here?
4. If a customer asks "Why can't we just use DLP for this?", how would you explain what Workforce AI Security does differently?
