# Discussion Guide — Session 5.2: AI Agent Security + MCP

> **For facilitators and self-study.** Use these exercises during the live session or work through them independently.

---

## Exercise 1: Agent Risk Assessment (15 min)

For each of the three agent scenarios below, analyse the tools it needs, its blast radius if compromised, and the least-privilege controls you would apply.

### Agent A: SOC Triage Agent
- **Purpose:** Receives alerts from SIEM, enriches with threat intelligence, assigns severity, creates tickets, and escalates critical incidents to on-call analysts.
- **Integrations:** SIEM (read), threat intel feeds (read), ticketing system (read/write), messaging platform (write), firewall (read).

### Agent B: Vulnerability Scanner Agent
- **Purpose:** Runs scheduled scans against internal infrastructure, correlates findings with CVE databases, prioritises by asset criticality, and generates remediation tickets.
- **Integrations:** Scanner tool (execute), asset inventory (read), CVE database (read), ticketing system (read/write), configuration management (read).

### Agent C: Compliance Reporting Agent
- **Purpose:** Pulls audit data from multiple sources, checks against regulatory frameworks (PCI-DSS, HIPAA, SOX), generates compliance reports, and flags gaps.
- **Integrations:** Log management (read), identity provider (read), configuration management (read), document storage (read/write), email (write).

Fill in the table for each agent:

| Dimension | Agent A: SOC Triage | Agent B: Vuln Scanner | Agent C: Compliance |
|-----------|--------------------|-----------------------|--------------------|
| **Tools needed** (list all) | | | |
| **Blast radius if compromised** | | | |
| **Most dangerous permission** | | | |
| **Least-privilege controls** | | | |
| **What should it NEVER have access to?** | | | |
| **Human-in-the-loop checkpoints** | | | |

**Discussion:**
- Which agent has the largest blast radius? Why?
- Where did you place human-in-the-loop checkpoints? What was your reasoning?
- How does the principle of least privilege apply differently to AI agents versus human users?

---

## Exercise 2: MCP Mapping Exercise (15 min)

Check Point provides 13 MCP servers that enable AI agents to interact with security infrastructure:

| # | MCP Server | Capability |
|---|-----------|------------|
| 1 | Threat Intelligence | Query indicators, get reputation scores, search threat campaigns |
| 2 | Quantum Gateway | Read/manage firewall policies, NAT rules, objects |
| 3 | Quantum SD-WAN | Read SD-WAN topology, site health, policies |
| 4 | CloudGuard CNAPP | Cloud posture findings, workload protection, asset inventory |
| 5 | CloudGuard WAF | WAF rules, security events, application profiles |
| 6 | Harmony Email | Email security events, quarantine actions, sender policies |
| 7 | Harmony Endpoint | Endpoint status, threat events, policy management |
| 8 | Infinity Events | Cross-product security event queries and log access |
| 9 | Infinity Policies | Unified policy management across products |
| 10 | Infinity Users | Identity and access information, user context |
| 11 | Infinity External Risk Management | Attack surface discovery, brand protection, dark web monitoring |
| 12 | Infinity Copilot | AI assistant interaction, workflow automation |
| 13 | Infinity Playblocks | Automated response playbooks, remediation actions |

### Task

For each of the three agents from Exercise 1, select the **minimum** set of MCP servers required. Fill in the table and justify every inclusion and exclusion.

| MCP Server | Agent A: SOC Triage | Agent B: Vuln Scanner | Agent C: Compliance | Justification |
|-----------|--------------------|-----------------------|--------------------|---------------|
| 1. Threat Intelligence | | | | |
| 2. Quantum Gateway | | | | |
| 3. Quantum SD-WAN | | | | |
| 4. CloudGuard CNAPP | | | | |
| 5. CloudGuard WAF | | | | |
| 6. Harmony Email | | | | |
| 7. Harmony Endpoint | | | | |
| 8. Infinity Events | | | | |
| 9. Infinity Policies | | | | |
| 10. Infinity Users | | | | |
| 11. Infinity External Risk Mgmt | | | | |
| 12. Infinity Copilot | | | | |
| 13. Infinity Playblocks | | | | |
| **Total servers** | | | | |

Mark each cell: **R** (Read only), **RW** (Read/Write), **X** (Execute), or **--** (No access).

**Discussion:**
- Which agent needed the fewest servers? Which needed the most? Does that correlate with risk?
- Did any server appear in all three agents? Is that a concern?
- How would you enforce the distinction between Read and Read/Write at the MCP level?
- What happens if an agent needs a capability you didn't include? What's the approval process?

---

## Exercise 3: Attack the Agent (15 min)

Switch to the attacker's mindset. For each agent from Exercise 1, brainstorm at least two realistic attack vectors. Consider these categories:

| Attack Category | Description |
|----------------|-------------|
| **Prompt injection via tool response** | Malicious content embedded in data returned by a tool (e.g., a SIEM alert containing crafted text that redirects the agent) |
| **Excessive permissions** | The agent has more access than needed, and an attacker exploits the extra surface area |
| **Data exfiltration channel** | The agent's write permissions are used to send data to an attacker-controlled destination |
| **Confused deputy** | The agent is tricked into using its legitimate permissions for illegitimate purposes |
| **Supply chain compromise** | A tool or MCP server the agent depends on is compromised |
| **Context window poisoning** | Accumulated data in the agent's context leads to degraded decision-making |

Fill in the table:

| Agent | Attack Vector | Category | Impact | Detection Difficulty (H/M/L) |
|-------|--------------|----------|--------|------------------------------|
| SOC Triage | | | | |
| SOC Triage | | | | |
| Vuln Scanner | | | | |
| Vuln Scanner | | | | |
| Compliance | | | | |
| Compliance | | | | |

**Discussion:**
- Which attack vector did the group consider most realistic in today's threat landscape?
- Which would be hardest to detect?
- How does AI Agent Security address each of these attack categories?
- Are there attack vectors unique to AI agents that don't apply to traditional automation (scripts, SOAR playbooks)?

---

## Exercise 4: Lab Debrief (10 min)

After completing the cp-agentic-mcp-playground lab, discuss the following as a group:

### Individual reflection (3 min)

Write brief answers to these questions:
1. What surprised you most during the lab?
2. What was the most powerful workflow you built or observed?
3. What was the biggest security concern you noticed?
4. If you were a SOC analyst using this daily, what would you want added?

### Group discussion (7 min)

| Topic | Key Takeaways |
|-------|--------------|
| Most powerful use case demonstrated | |
| Biggest security concern identified | |
| How this compares to traditional SOAR | |
| What customers would be most impressed by | |
| What customers would be most worried about | |

**Discussion:**
- How would you demo this to a customer without overwhelming them?
- What guardrails would a customer want before deploying this in production?
- How does the lab experience change how you would position AI Agent Security?

---

## Exercise 5: Customer Pitch (15 min)

### The Scenario

A customer's CISO says:

> "We're not using AI agents yet, so AI Agent Security isn't relevant to us. Maybe in a year or two."

### Task — Part 1: Discovery (5 min)

Before responding, develop discovery questions that would reveal whether AI agents are already in use without the CISO's knowledge. Fill in the table:

| Discovery Question | What It Reveals | Likely Answer |
|-------------------|----------------|---------------|
| "Are any of your teams using GitHub Copilot or similar code assistants?" | Code-generating agents already in the environment | |
| "Does your SOC use any automation that makes decisions without human approval?" | SOAR playbooks that function as primitive agents | |
| | | |
| | | |
| | | |

### Task — Part 2: Response (5 min)

Role-play the conversation. One person plays the CISO, the other responds. The responder should:

1. Validate the CISO's perspective — don't dismiss it
2. Ask 2-3 discovery questions from your table
3. Reframe: even if the CISO hasn't deployed agents, their vendors, partners, and employees may already be using them
4. Connect to a concrete risk the CISO cares about
5. Position AI Agent Security as preparation, not reaction

### Debrief (5 min)
- What discovery question was most effective at shifting the CISO's thinking?
- How is this objection similar to "we don't need cloud security because we're not in the cloud" from five years ago?
- What's the difference between "we're not using agents" and "we don't know if agents are being used"?

---

## Self-Study Reflection Questions

1. How do AI agents differ from traditional automation (scripts, SOAR playbooks) in terms of security risk? What's genuinely new?
2. Why is the Model Context Protocol (MCP) significant for security? How does standardised tool access change the control surface?
3. Think about your own organisation's automation. Which existing workflows could become AI agents in the next 12 months? What controls would they need?
4. If an AI agent causes a security incident (e.g., it miscategorises a critical alert as low-severity and a breach follows), who is responsible? How should accountability work?
