# Facilitator Guide — Session 5.2: AI Agent Security + MCP

> **Stage:** 5  |  **Week:** 14  |  **Content:** `stage5_cp_ai_security/02_ai_agent_security/`  |  **Total time:** 90 min

---

## Pre-Session Checklist

- [ ] Reviewed the README.md and discussion_guide.md in the content folder
- [ ] Verified Docker is installed and running on your machine; tested the cp-agentic-mcp-playground lab end-to-end
- [ ] Confirmed participants received the Docker setup instructions at least 1 week before this session
- [ ] Prepared the pre-recorded lab walkthrough video as backup for participants who cannot run Docker

---

## Session Flow

| Time | Section | Activity |
|------|---------|----------|
| 0:00 – 0:05 | Recap | Recap 5.1. Ask: "What was the most surprising thing your group found in the Workforce AI Security discussion?" |
| 0:05 – 0:15 | Chat → Copilot → Agent | Walk through the evolution: Chat (human drives, AI responds) → Copilot (AI suggests, human approves) → Agent (AI acts autonomously). Ask: "Where on this spectrum are your customers today? Where will they be in 12 months?" |
| 0:15 – 0:30 | MCP deep dive | Explain the Model Context Protocol: what it is, how it connects agents to tools and data sources, and why it creates a new attack surface. Draw the parallel: "MCP is to AI agents what APIs are to web applications — and we know how that attack surface played out." |
| 0:30 – 0:40 | Agent security threats | Cover the threat categories: prompt injection through tool results, excessive permissions, data exfiltration via agent actions, and lateral movement between connected tools. For each threat, ask: "What's the blast radius if this agent is compromised?" |
| 0:40 – 1:20 | Hands-on lab | Run the cp-agentic-mcp-playground lab. Participants deploy an agent environment, connect MCP tools, and observe security events. Circulate and help with Docker issues in the first 5 minutes. |
| 1:20 – 1:30 | Lab debrief + wrap-up | Debrief the lab: "What surprised you? What would you show a customer?" Preview Session 5.3: "Next session, we'll go inside the guardrails that protect AI models themselves." |

---

## Key Points to Emphasise

1. **Agents are not chatbots — they take autonomous action** — the fundamental shift is from AI that generates text to AI that executes tasks. An agent with access to your ticketing system, cloud console, and email can take actions with real-world consequences. Security must match the level of autonomy.
2. **MCP is the new attack surface** — the Model Context Protocol standardises how agents connect to external tools and data. Every MCP connection is a potential path for prompt injection, data leakage, or privilege escalation. Securing MCP connections is the agent-era equivalent of securing API endpoints.
3. **Ask the blast radius question for every agent** — before deploying or approving any AI agent, the security question is: "If this agent is fully compromised, what can it access and what can it do?" The answer determines the security controls required. Least privilege applies to agents just as it applies to users.

---

## Discussion Prompts

- "Think about a SOC workflow you'd want to automate with an agent. Now list every system that agent would need access to. What's the blast radius if that agent is compromised?"
- "A customer says 'We're using MCP to connect our AI assistant to Slack, Jira, and our cloud console.' What are the first three security questions you'd ask?"
- "How do you explain the difference between a copilot and an agent to a non-technical CISO in under 60 seconds?"

---

## Common Questions and Answers

**Q: What if the customer isn't using MCP?**
A: MCP is one protocol, but the pattern it represents — agents connecting to external tools — is universal. Whether the customer uses MCP, custom API integrations, or LangChain tool bindings, the security challenges are identical: controlling what the agent can access, monitoring what it does, and limiting blast radius. Position the solution around the pattern, not the protocol.

**Q: How does this relate to API security?**
A: API security protects the interface between applications. Agent security protects the interface between an autonomous AI and the tools it controls — which often includes APIs. The new dimension is that the "caller" is an AI making dynamic decisions, not a predictable application following coded logic. Traditional API security (rate limiting, authentication, schema validation) is necessary but not sufficient when the caller can be manipulated via prompt injection.

**Q: Is this only for Check Point agents?**
A: No. The security layer is agent-agnostic. It works with any AI agent framework — LangChain, CrewAI, AutoGen, custom-built agents, or any system using MCP. The value proposition is securing the customer's entire agent ecosystem, regardless of which frameworks or vendors they use to build their agents.

---

## Facilitator Notes

- The lab requires Docker pre-installed. Send setup instructions 1 week before the session. Have the pre-recorded lab walkthrough ready for participants who can't run Docker — they should watch and follow along even if they can't execute hands-on.
- The Chat → Copilot → Agent evolution slide is critical for framing. Spend time here. Many participants (and their customers) conflate chatbots with agents. If participants don't internalise this distinction, the rest of the session won't land.
- During the lab, the most common issues are Docker networking and port conflicts. Have participants run `docker ps` at the start to confirm Docker is healthy. If someone is stuck for more than 3 minutes, pair them with a neighbour who has it working.
- The MCP deep dive can get abstract quickly. Anchor every concept to a concrete example: "Imagine an agent connected to your SIEM via MCP. A malicious log entry contains a prompt injection. The agent reads the log, follows the injected instruction, and opens a firewall rule via another MCP tool."

---

## Connections to Sales Conversations

- **When a customer says:** "We're automating SOC tasks with AI agents and need to make sure they're secure."
- **You can now say:** "The first question is: what's the blast radius of each agent? Let me show you how we map every tool connection, monitor agent actions in real time, and enforce least-privilege policies — so your agents can automate effectively without becoming a new attack vector."
