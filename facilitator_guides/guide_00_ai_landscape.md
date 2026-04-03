# Facilitator Guide — Session 0.1: The AI Landscape in Cybersecurity

> **Stage:** 0  |  **Week:** 1  |  **Content:** `stage0_positioning/01_ai_landscape/`  |  **Total time:** 60 min

---

## Pre-Session Checklist

- [ ] Reviewed the README.md and discussion_guide.md
- [ ] Prepared 1-2 personal examples of AI claims you've encountered in the field
- [ ] Opened the cohort channel — checked for questions posted during the week

---

## Session Flow

| Time | Section | Activity |
|------|---------|----------|
| 0:00 – 0:05 | Welcome | Introductions (first session), set expectations for Stage 0 |
| 0:05 – 0:15 | AI terminology | Walk through the 4-layer hierarchy (AI → ML → DL → GenAI). Ask: "When vendors say AI, which layer do they usually mean?" |
| 0:15 – 0:30 | Security stack map | Cover where AI is deployed today. Ask each participant: "Which domain is most relevant to your current role?" |
| 0:30 – 0:40 | AI washing | Present the 5-question evaluation framework. Show 1-2 real vendor claims and evaluate them live. |
| 0:40 – 0:55 | Round-table exercise | Each participant shares one AI claim from the field. Group evaluates using the 5-question framework. |
| 0:55 – 1:00 | Wrap-up | Preview Session 0.2 (competitor analysis). Assign: "Find one competitor datasheet with an AI claim before next session." |

---

## Key Points to Emphasise

1. **Most AI in production security is classic ML** (random forests, gradient boosting) — not deep learning, not LLMs. This single fact gives participants instant credibility.
2. **Each AI generation layers on top** — signatures, heuristics, ML, deep learning, and LLMs all coexist in production. No generation replaced the previous one.
3. **The 5-question framework is the takeaway** — participants should memorise: What model? What data? What metric? What baseline? What fails?

---

## Discussion Prompts

- "Think about a security product you use daily. Can you answer all 5 evaluation questions about its AI? What's missing?"
- "A customer says 'We want AI in our security stack.' What's the first question you'd ask them?"
- "If you had to explain AI in security in 30 seconds to your CEO, what would you say?"

---

## Common Questions and Answers

**Q: Isn't deep learning always better than classic ML?**
A: No. Deep learning needs more data, more compute, and is harder to explain. For tabular security data (logs, alerts, network flows), classic ML often performs equally well and is far more interpretable. Deep learning shines on unstructured data — images, raw text, packet bytes.

**Q: Where does ChatGPT / Claude fit in the security stack?**
A: LLMs are primarily used for analyst assistance today — copilots for investigation, triage, and report generation. They don't replace detection engines. They augment human analysts. Participants will build exactly this in Stage 4.

**Q: Is "AI washing" really that common?**
A: Yes. A significant portion of products marketed as "AI-powered" are rule-based systems or simple statistical thresholds. The 5-question framework quickly separates real ML from marketing.

---

## Connections to Sales Conversations

- **When a customer asks:** "What's the difference between your AI and [competitor]'s?"
- **You can now say:** "Let me walk you through what's actually under the hood. Most security AI is [specific ML technique]. The real question is: what data is it trained on, and what's the false positive rate?"
