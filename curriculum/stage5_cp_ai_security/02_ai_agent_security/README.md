# AI Agent Security + MCP

> **Stage:** 5  |  **Week:** 14  |  **Time:** 90 min  |  **Format:** Lecture + hands-on lab

---

## Overview

AI is moving from chat interfaces to autonomous agents. Instead of a human typing prompts, an AI agent decides what tools to call, what data to access, and what actions to take — often without human approval for each step. This is powerful, but it creates a fundamentally new security challenge.

**AI Agent Security** monitors and secures these autonomous AI workflows — tracking every tool invocation, data access, and decision an agent makes.

---

## What Are AI Agents?

### From Chat to Agents

| Generation | How It Works | Human Involvement | Example |
|-----------|-------------|-------------------|---------|
| **Chat** | Human types a prompt, AI responds with text | Every interaction | "Summarise this log file" |
| **Copilot** | AI suggests, human approves | Every action | GitHub Copilot suggesting code |
| **Agent** | AI decides what to do, calls tools, acts autonomously | Minimal — oversight, not approval | "Investigate this alert and contain the threat" |

### The Agent Loop

An AI agent follows a reasoning loop:

| Step | What Happens | Security Implication |
|------|-------------|---------------------|
| 1. **Observe** | Receives a task or trigger | What data does the agent receive? Is it sensitive? |
| 2. **Reason** | Decides what action to take | Is the reasoning sound? Can it be manipulated? |
| 3. **Act** | Calls a tool (API, database, command) | What permissions does this tool have? What's the blast radius? |
| 4. **Evaluate** | Checks the result, decides next step | Does it know when to stop? Can it escalate to a human? |

Each cycle through this loop is an **invocation**. The Workforce AI Security dashboard tracks these — you saw "Top Used Agents By Invocations" in Session 5.1.

---

## What Is MCP (Model Context Protocol)?

MCP is an open standard (created by Anthropic) that gives AI agents a structured way to access external tools and data. Think of it as a universal adapter between LLMs and the systems they need to interact with.

### MCP Architecture

| Component | Role | Example |
|-----------|------|---------|
| **MCP Client** | The AI application that needs to access tools | Claude Desktop, Cursor, a custom agent |
| **MCP Server** | Exposes tools and data through a standard protocol | Check Point Management MCP, Jira MCP, GitHub MCP |
| **Tools** | Specific capabilities the server provides | `list_firewalls`, `get_policy`, `create_rule` |
| **Resources** | Data the server can provide to the AI | Firewall logs, policy configurations, threat intelligence |

### Why MCP Matters for Security

| Benefit | Risk |
|---------|------|
| Standardised tool access — one protocol instead of custom integrations | Every MCP connection is a potential data channel |
| AI agents can orchestrate complex multi-tool workflows | An agent with too many tools has too much blast radius |
| Tools are discoverable and documented | Tool descriptions can be manipulated (tool poisoning) |
| Enables automation of security operations | Autonomous actions without human approval in the loop |

---

## How AI Agent Security Works

### The Security Challenges

| Threat | Description | Example |
|--------|-------------|---------|
| **Excessive permissions** | Agent has access to more tools than it needs | An investigation agent that can also delete firewall rules |
| **Data exfiltration via tools** | Agent reads sensitive data and sends it to an external service | Agent reads credentials from a vault and posts them to Slack |
| **Prompt injection via tools** | Malicious data from a tool manipulates the agent's reasoning | A ticket contains hidden instructions that redirect the agent |
| **Agent confusion** | Agent misinterprets a tool response and takes wrong action | Agent quarantines a production server instead of a test instance |
| **Shadow agents** | Unauthorised agents connecting to corporate MCP servers | Developer spins up a personal agent that accesses production APIs |

### What AI Agent Security Monitors

| Dimension | What It Tracks | Why It Matters |
|-----------|---------------|----------------|
| **Agent inventory** | All active agents, their MCP connections, configured tools | You can't secure what you can't see |
| **Invocations** | Every tool call — what was called, with what parameters, what was returned | Audit trail for autonomous actions |
| **Data flows** | What data moves between agents and tools | Detect data exfiltration or sensitive data exposure |
| **Behavioural patterns** | Normal vs anomalous agent activity | A research agent suddenly calling administrative tools is a red flag |
| **Policy compliance** | Whether agent actions comply with organisational policies | Enforce least-privilege for agent tool access |

---

## Hands-On Lab: cp-agentic-mcp-playground

### Lab Overview

You will use the [cp-agentic-mcp-playground](https://github.com/alshawwaf/cp-agentic-mcp-playground) — a Docker-based sandbox with 13 Check Point MCP servers, n8n workflow automation, Ollama (local LLM), and Qdrant (vector database).

### Setup

```bash
git clone https://github.com/alshawwaf/cp-agentic-mcp-playground.git
cd cp-agentic-mcp-playground
./setup.sh
docker compose --profile cpu up -d
```

### Available MCP Servers

| MCP Server | Check Point Product | Tools Provided |
|-----------|-------------------|----------------|
| Documentation MCP | Check Point docs | Search documentation, get guides |
| Quantum Management MCP | Security Management | List gateways, get policies, manage rules |
| Quantum Gateway CLI MCP | Quantum Gateways | Execute CLI commands on gateways |
| Quantum Gaia MCP | Gaia OS | OS-level operations on appliances |
| Connection Analysis MCP | Gateway diagnostics | Analyse network connections |
| Threat Emulation MCP | SandBlast | Submit files for sandboxing, get verdicts |
| Threat Prevention MCP | Threat Prevention | Check threat prevention status, policies |
| HTTPS Inspection MCP | SSL Inspection | Manage HTTPS inspection policies |
| Reputation Service MCP | ThreatCloud | Look up IP/domain/URL reputation |
| Management Logs MCP | SmartLog | Query audit and security logs |
| Harmony SASE MCP | Harmony SASE | Manage SASE policies and users |
| Spark Management MCP | Spark appliances | Manage Spark devices |
| CPInfo Analysis MCP | CPInfo tool | Analyse system diagnostic bundles |

### Lab Exercises

**Exercise 1: Explore the MCP landscape (15 min)**
- Open n8n at `http://localhost:5678`
- Browse the pre-loaded workflows
- Identify which MCP servers are connected and what tools they expose
- Question: "If an agent had access to all 13 MCP servers, what's the maximum damage it could do?"

**Exercise 2: Build a threat investigation workflow (25 min)**
- Using n8n, create a workflow that:
  1. Takes an IP address as input
  2. Checks its reputation via the Reputation Service MCP
  3. Queries Management Logs for any connections to/from that IP
  4. Generates a summary using the local Ollama LLM
- This simulates what an AI security agent does — orchestrating multiple tools to investigate a threat

**Exercise 3: Observe agent security concerns (10 min)**
- Review the workflow you built: what data did the agent access? What tools did it use?
- If this agent were compromised (prompt injection from a malicious log entry), what could it do?
- How would AI Agent Security detect and prevent misuse?

---

## Connecting to What You Know

### From Stage 4 (LLM APIs + RAG)

In Stage 4, you called an LLM API with a system prompt, user messages, and a context window. An AI agent does the same thing — but instead of you typing the messages, the agent generates them based on tool results. The RAG pipeline you built is a simple form of tool use: retrieve documents, inject into context, generate an answer.

MCP formalises this: instead of hardcoded document loading, the agent can discover and call any available tool through a standard protocol.

### From Stage 2 (Anomaly Detection)

Agent behaviour monitoring is anomaly detection applied to tool invocation patterns. Normal agent activity forms a baseline (10 reputation lookups/hour, 2 log queries/hour). An agent suddenly making 500 management API calls is anomalous — the same statistical approach from Stage 2, applied to a new data source.

---

## Discussion Questions

1. "What's the difference between a vulnerability scanner and an AI agent? Both automate security tasks — why does the agent need different security controls?"
2. "A customer's SOC wants to deploy an AI agent that can automatically quarantine endpoints. What guardrails would you recommend?"
3. "An agent has access to both the Reputation Service and Quantum Management MCP servers. Why is this a risk, and how would you apply least-privilege?"
4. "How would you explain MCP to a customer who's never heard of it, in under 60 seconds?"

---

## Key Takeaways

1. **Agents are not chatbots** — they act autonomously, which means security must be automated too. You can't review every agent decision manually.
2. **MCP is the new attack surface** — every MCP connection is a data channel and a capability grant. Least-privilege applies to agents just like it applies to human users.
3. **Visibility is the first step** — you can't secure agents you can't see. AI Agent Security discovers and inventories all agent activity.
4. **The blast radius question** — for every agent, ask: "If this agent were compromised, what's the worst it could do?" The answer should be small.
