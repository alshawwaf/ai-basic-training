# Facilitator Guide — Session 0.3: AI Objection Handling

> **Stage:** 0  |  **Week:** 2  |  **Content:** `stage0_positioning/03_objection_handling/`  |  **Total time:** 60 min

---

## Pre-Session Checklist

- [ ] Reviewed the README.md and discussion_guide.md
- [ ] Prepared to demonstrate ACE live on an objection (model it before participants try)
- [ ] Printed or shared the 8 objections list for quick reference

---

## Session Flow

| Time | Section | Activity |
|------|---------|----------|
| 0:00 – 0:05 | Recap | "What competitor positioning insight stuck with you from last session?" |
| 0:05 – 0:15 | ACE framework | Introduce Acknowledge-Clarify-Educate. Demonstrate it live on Objection #2 (false positives) — show what a bad response looks like, then an ACE response. |
| 0:15 – 0:30 | Walk through objections | Cover objections 1-4 (pattern matching, false positives, SIEM rules, analyst replacement). Pause after each: "Has anyone heard this one? How did you respond?" |
| 0:30 – 0:35 | Objections 5-8 | Cover adversarial attacks, data sensitivity, not enough data, explainability. Faster pace — these are more technical. |
| 0:35 – 0:55 | Role-play | 3 rounds of paired role-play (scenarios from discussion guide). Rotate roles. Debrief after each round. |
| 0:55 – 1:00 | Wrap-up | Preview Session 0.4 (discovery questions). Ask participants to think of a customer engagement where better discovery could have changed the outcome. |

---

## Key Points to Emphasise

1. **ACE works because it doesn't argue** — Acknowledge validates the customer's experience. Most AI objections come from past disappointments, not ignorance.
2. **The Clarify step is the most important** — the stated objection is rarely the full picture. "We tried AI and it didn't work" could mean false positives, integration issues, or budget problems.
3. **Technical specificity is the differentiator** — "the false positive rate is a threshold tuning issue" beats "our AI is better" every time.

---

## Discussion Prompts

- "Which objection do you hear most often in your region? Is it the same across the group?"
- "Think of a time you responded poorly to an AI objection. What would you do differently with ACE?"
- "Is there an objection where the honest answer is 'you're right, AI isn't the best solution here'?"

---

## Common Questions and Answers

**Q: What if the customer is technically right and our AI does have the limitation they're raising?**
A: Honesty wins. Acknowledge the limitation, then pivot to what you do about it (monitoring, retraining, human-in-the-loop). "You're right that no ML model is adversarial-proof. Here's how we mitigate that risk" is far more credible than dodging the question.

**Q: How do I handle an objection I've never heard before?**
A: ACE handles any objection. Acknowledge, ask a clarifying question, and if you don't know the technical answer, say "That's a great question — I'll get you a specific answer from our engineering team." Never bluff.

**Q: The customer's previous AI experience was genuinely bad. How do I overcome that?**
A: Don't try to overcome it — validate it. "That's a common experience, and it usually comes from one of three causes: wrong threshold, training data mismatch, or unsupervised models without tuning. Which sounds closest to what happened?" This shows you understand the failure modes, not just the success stories.

---

## Facilitator Notes

- The role-play is the most valuable part of this session. Resist the urge to cut it short for more lecture content.
- If participants are shy about role-play, go first — demonstrate a full ACE exchange with a volunteer, then break into pairs.
- Watch for participants who skip the Clarify step and jump straight to Educate. This is the most common mistake. Pause and redirect: "Before you explain, what question would you ask first?"

---

## Connections to Sales Conversations

- **When a customer says:** "We tried ML-based detection and it generated too many false positives."
- **You can now say:** "That's a very common experience. Was it unsupervised anomaly detection, or supervised classification? Because the false positive problem usually comes from one of three specific causes, and each has a different fix."
