# Facilitator Guide — Session 5.3: AI Guardrails

> **Stage:** 5  |  **Week:** 15  |  **Content:** `stage5_cp_ai_security/03_ai_guardrails/`  |  **Total time:** 90 min

---

## Pre-Session Checklist

- [ ] Reviewed the README.md and discussion_guide.md in the content folder
- [ ] Tested the Lakera-Demo lab environment end-to-end; confirmed all attack scenarios work
- [ ] Prepared competitive positioning notes (guardrails vs WAF, vs native LLM provider controls)

---

## Session Flow

| Time | Section | Activity |
|------|---------|----------|
| 0:00 – 0:05 | Recap | Recap 5.2. Ask: "What was the most dangerous agent threat you identified in the lab — and how would you explain it to a customer?" |
| 0:05 – 0:20 | LLM threat landscape | Walk through the attack categories: prompt injection (direct and indirect), jailbreaking, data extraction, hallucination exploitation, and model abuse. For each category, show a concrete example. Ask: "Which of these would a WAF catch? Which would it miss entirely?" |
| 0:20 – 0:30 | How guardrails work | Explain the technical architecture: input inspection, output validation, content classification, and policy enforcement. Connect to Stages 1-4: "The classifier that detects prompt injection uses the same NLP and ML techniques you've already built." |
| 0:30 – 1:10 | Hands-on lab | Run the Lakera-Demo lab. Participants design and execute attacks against a protected LLM, then observe how guardrails detect and block them. Encourage creativity — the goal is to understand both the attack and the defence. |
| 1:10 – 1:25 | Attack debrief + competitive positioning | Debrief: "Which attacks got through? Why?" Then cover competitive positioning: how guardrails differ from native LLM provider safety filters, WAFs, and DLP. |
| 1:25 – 1:30 | Wrap-up | Summarise the session. Preview Session 5.4: "Next session, you'll bring everything together — workforce security, agent security, and guardrails — into a unified positioning that you can deliver to any customer." |

---

## Key Points to Emphasise

1. **Traditional security doesn't work for LLM attacks** — WAFs look at HTTP structure, DLP looks at data patterns, and network security looks at traffic flows. None of them understand natural language semantics. A prompt injection is a valid HTTP request containing valid text — it's only malicious in the context of an LLM. Purpose-built guardrails are required because the attack surface is language itself.
2. **Guardrails use the same ML from Stages 1-4** — the classifiers that detect prompt injection, toxic content, and data leakage in LLM inputs/outputs are built on the NLP, classification, and deep learning techniques participants have already learned. This is the payoff of their technical training: they can explain HOW guardrails work, not just WHAT they do.
3. **The false positive trade-off is real** — aggressive guardrails block attacks but also block legitimate use. A guardrail that flags every question about "hacking" will block security professionals asking legitimate questions. Tuning this balance is the same precision-recall trade-off from Stage 1, Lecture 5 (Model Evaluation). Customers need to understand this trade-off upfront.

---

## Discussion Prompts

- "You're building a customer-facing AI chatbot for a bank. What types of inputs should the guardrails block? What should they allow that might look suspicious on the surface?"
- "A customer says their LLM provider (OpenAI, Anthropic) already has safety filters built in. Why would they need additional guardrails?"
- "Think about the false positive scenario: a security analyst asks your AI assistant 'How do attackers use SQL injection to exfiltrate data?' Should the guardrail block this? How do you design a policy that allows this but blocks actual attack instructions?"

---

## Common Questions and Answers

**Q: Can't the LLM provider handle this?**
A: LLM providers build general-purpose safety filters optimised for consumer use cases. They don't understand your customer's specific data policies, compliance requirements, or business context. A bank needs different guardrails than a hospital, which needs different guardrails than a software company. Provider-level safety is the baseline floor, not the ceiling. Enterprise guardrails add organisation-specific policies, audit logging, and integration with existing security workflows.

**Q: What's the latency impact?**
A: Modern guardrails add single-digit milliseconds for most checks — classification models are small and optimised for inference speed. The heavier checks (semantic analysis, multi-step validation) add more but are still measured in tens of milliseconds, not seconds. For context, a typical LLM response takes 1-5 seconds to generate. The guardrail overhead is a fraction of the overall response time. However, stacking many guardrail checks can accumulate latency, so policy design matters.

**Q: How do guardrails handle multi-language attacks?**
A: This is an active and evolving challenge. Attackers craft prompts in less-common languages, use transliteration, or mix languages to bypass classifiers trained primarily on English. Strong guardrails use multilingual models and character-level analysis, but coverage varies by language. This is an honest conversation to have with customers: guardrail effectiveness correlates with the linguistic diversity of the training data, and no solution has perfect coverage across all languages today.

---

## Facilitator Notes

- The attack design exercise generates the most energy in this session. Let participants compete to bypass the guardrails — it makes the product value tangible. When someone successfully bypasses a guardrail, use it as a teaching moment: "This is exactly why customers need configurable, updatable guardrails — the threat evolves."
- Expect participants to get creative with attacks. Some will try encoding tricks (base64, ROT13), multi-turn strategies (building up context across messages), or role-play prompts ("Pretend you're a security researcher..."). All of these are real-world attack patterns — encourage them.
- The competitive positioning segment is important for sales conversations. Make sure participants can articulate three clear differentiators vs native provider safety, vs WAFs, and vs open-source guardrail libraries.
- Connect back to Stage 1, Lecture 5 (Model Evaluation) when discussing the false positive trade-off. Ask: "Remember precision vs recall? Which matters more for guardrails — and does the answer change depending on the use case?"

---

## Connections to Sales Conversations

- **When a customer says:** "We're building an AI chatbot but our security team is blocking the project because of prompt injection risks."
- **You can now say:** "That's exactly the tension guardrails are designed to resolve. Let me show you how we inspect every input and output in real time — blocking prompt injection, data leakage, and abuse — so your security team can approve the project with confidence. And I can explain exactly how the detection works under the hood, because it uses the same ML classification your security tools already rely on."
