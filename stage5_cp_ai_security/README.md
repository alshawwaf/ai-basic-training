# Stage 5 — Check Point AI Security

> Apply everything you've learned to Check Point's AI Security product line — and become the expert your customers need.

Stages 1–4 taught you how AI works from the ground up. This stage connects that knowledge to the products you sell and the problems your customers face. By the end, you will understand how Check Point's AI Security suite works under the hood, be able to demo it with technical depth, and position it against competitors with confidence.

---

## The Check Point AI Security Suite

Check Point's Infinity Platform includes three AI Security products:

| Product | What It Does | Under the Hood |
|---------|-------------|----------------|
| **Workforce AI Security** | Monitors and governs employee AI tool usage (ChatGPT, Claude, Copilot, Cursor). Enforces policy: allow, prevent, redact, detect, block. Protects sensitive data from leaking to AI services. | Classification models for sensitive data detection, NLP for content analysis, policy engine with real-time inline scanning |
| **AI Agent Security** | Secures autonomous AI agents — monitors tool access, MCP connections, and agentic workflows. Tracks agent invocations and data flows. | Agent behaviour analysis, MCP protocol inspection, tool-use monitoring, anomaly detection on agent actions |
| **AI Guardrails** | Defends LLM applications against prompt injection, jailbreaks, data extraction, and toxic content generation. | Input/output scanning with NLP classifiers, pattern matching for known attack signatures, semantic analysis for novel attacks, content filtering |

---

## Why This Stage Matters

Every concept from the program maps to something in these products:

| Program Concept | Where It Appears in Check Point AI Security |
|----------------|---------------------------------------------|
| Classification (Stage 1) | Sensitive data detection in Workforce AI Security — classifying content as PII, credentials, source code, etc. |
| Feature engineering (Stage 2) | Extracting signals from AI traffic — session patterns, prompt characteristics, data volume anomalies |
| Anomaly detection (Stage 2) | Risk scoring in Workforce AI Security — identifying unusual AI usage patterns |
| Neural networks (Stage 3) | NLP models powering content analysis, prompt classification, and semantic understanding |
| Embeddings (Stage 4) | Semantic similarity for detecting rephrased prompt injection attempts |
| RAG (Stage 4) | Understanding what customers are building — and what AI Guardrails protects |
| LLM security (Stage 4) | The entire AI Guardrails product — defending the systems you learned to build |

---

## Sessions

| # | Session | Format | Time | Hands-On |
|---|---------|--------|------|----------|
| 5.1 | [Workforce AI Security](01_workforce_ai_security/README.md) | Lecture + walkthrough | 60 min | Dashboard exploration, policy creation exercise |
| 5.2 | [AI Agent Security + MCP](02_ai_agent_security/README.md) | Lecture + lab | 90 min | cp-agentic-mcp-playground — build a Check Point workflow |
| 5.3 | [AI Guardrails](03_ai_guardrails/README.md) | Lecture + lab | 90 min | Lakera-Demo — test attack vectors, benchmark defenses |
| 5.4 | [Positioning Check Point AI Security](04_positioning_cp_ai/README.md) | Workshop | 60 min | Build and rehearse a customer-facing demo |

---

## Prerequisites

- Stages 0–4 completed (or concurrent with Stage 4)
- Docker Desktop installed (for Sessions 5.2 and 5.3)
- Access to a Check Point Infinity Portal demo tenant (provided by program lead)
- GitHub access to clone the lab repos

### Lab Repositories

| Repo | Used In | Purpose |
|------|---------|---------|
| [cp-agentic-mcp-playground](https://github.com/alshawwaf/cp-agentic-mcp-playground) | Session 5.2 | Docker-based AI sandbox with 13 Check Point MCP servers, n8n, Ollama, Qdrant |
| [Lakera-Demo](https://github.com/alshawwaf/Lakera-Demo) | Session 5.3 | LLM security testing platform with 24+ attack vectors |

---

## What You Will Be Able to Do After Stage 5

- Explain how Workforce AI Security monitors and governs AI tool usage — and why organisations need it
- Demonstrate how AI Agent Security secures MCP-based agentic workflows
- Test LLM applications against prompt injection and jailbreak attacks using AI Guardrails
- Position the full Check Point AI Security suite against competitors with technical specificity
- Deliver a customer-facing demo that connects AI fundamentals to Check Point's implementation
