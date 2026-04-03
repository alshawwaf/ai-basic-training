# Facilitator Guide — Session 0.4: Discovery Questions for AI Use Cases

> **Stage:** 0  |  **Week:** 2  |  **Content:** `stage0_positioning/04_discovery_questions/`  |  **Total time:** 60 min

---

## Pre-Session Checklist

- [ ] Reviewed the README.md and discussion_guide.md
- [ ] Prepared a personal example of a discovery conversation where PDFC would have helped
- [ ] Printed the PDFC framework and ML Fit Checklist for quick reference

---

## Session Flow

| Time | Section | Activity |
|------|---------|----------|
| 0:00 – 0:05 | Recap | "Name one ACE response from last session that you've already used — or plan to use." |
| 0:05 – 0:15 | PDFC framework | Walk through Pain → Data → Fit → Commitment. Emphasise that each phase gates the next. |
| 0:15 – 0:25 | Pain + Data questions | Cover the discovery questions for Pain and Data. Demonstrate with a real example: "Here's how I'd run PDFC on a customer I worked with last quarter." |
| 0:25 – 0:35 | Fit + Commitment | Cover the ML Fit Checklist (6 criteria) and the red flags table. Ask: "Which red flag do you see most often?" |
| 0:35 – 0:55 | Role-play scenarios | Run both scenarios from the discussion guide (regional bank + enterprise). 10 min each. Debrief after each. |
| 0:55 – 1:00 | Stage 0 wrap-up | Celebrate completing Stage 0. Preview Stage 1: "Next week you start building the technical depth behind everything we've discussed. First up: What is Machine Learning?" |

---

## Key Points to Emphasise

1. **Discovery before demo** — the biggest mistake is leading with what AI can do instead of asking what the customer needs. Pain first, always.
2. **Not every problem needs AI** — qualifying out is as valuable as qualifying in. Red flags (zero FP tolerance, 50 events/day, no success metrics) save everyone time.
3. **Data readiness determines approach** — labelled data → supervised ML; unlabelled → unsupervised; documents → RAG. This mapping is the practical output of PDFC.

---

## Discussion Prompts

- "Think about your last 3 customer engagements. For each one, which PDFC phase would have been most revealing?"
- "A customer says 'Our board wants an AI strategy.' How do you redirect from a solution-first conversation to a pain-first one?"
- "When is the right time to walk away from an AI opportunity?"

---

## Common Questions and Answers

**Q: What if the customer doesn't know what data they have?**
A: That's a finding, not a blocker. "If you're not sure what telemetry you're collecting, that's actually the first step — let's map your data sources before we talk about what AI can do with them." This positions you as a consultant, not a vendor.

**Q: How detailed should the FIT assessment be in a first meeting?**
A: Light touch. The 6-criteria checklist is for your internal qualification — you don't walk the customer through it explicitly. Instead, ask natural questions that surface the answers: "How many alerts per day?" covers Scale. "What would success look like?" covers Measurable Outcome.

**Q: What if the customer has a genuine AI use case but no budget?**
A: Document the opportunity and the PDFC findings. Suggest a low-cost POC using open-source tools (scikit-learn, HuggingFace, Ollama). This builds the business case for future budget. Stage 4 of this program gives you exactly the tools to build that POC.

---

## Facilitator Notes

- This is the most interactive session in Stage 0. The role-plays should take at least 20 minutes — don't shortchange them.
- The regional bank scenario is intentionally resource-constrained. Watch whether participants identify the red flags (small team, no ML experience, no allocated budget) or try to sell AI anyway.
- The enterprise scenario is the opposite — plenty of resources, the challenge is identifying the highest-value use case among many options. Watch whether participants default to the most technical solution vs the most impactful one.
- End the session with energy — Stage 0 completion is a milestone. Acknowledge the group's progress and set expectations for the technical depth coming in Stage 1.

---

## Connections to Sales Conversations

- **When a customer says:** "We want to use AI for security but don't know where to start."
- **You can now say:** "Let me ask a few questions to find where AI would have the most impact in your environment. What's the biggest operational pain your security team faces today?"
