# Facilitator Guide — Session 5.1: Workforce AI Security

> **Stage:** 5  |  **Week:** 14  |  **Content:** `stage5_cp_ai_security/01_workforce_ai_security/`  |  **Total time:** 60 min

---

## Pre-Session Checklist

- [ ] Reviewed the README.md and discussion_guide.md in the content folder
- [ ] Prepared a live demo environment for the Workforce AI Security dashboard (or screenshots as backup)
- [ ] Familiarised yourself with the 6 policy actions and can explain each without notes

---

## Session Flow

| Time | Section | Activity |
|------|---------|----------|
| 0:00 – 0:05 | Recap | Recap Stage 4 capstone. Ask: "What was the hardest part of building your RAG assistant — and what did it teach you about how AI actually works?" |
| 0:05 – 0:15 | AI security challenge | Introduce the problem: employees are adopting AI tools faster than security teams can track. Frame the question: "What happens when you block AI entirely vs allow it with no controls?" |
| 0:15 – 0:30 | Dashboard walkthrough | Live demo of the Workforce AI Security dashboard. Walk through: discovered apps, user activity, sensitive data events. Ask: "What would your CISO want to see first?" |
| 0:30 – 0:40 | Policy design deep dive | Cover the 6 policy actions in detail. For each action, ask: "When would you use this instead of the others?" Emphasise that the goal is enablement, not blocking. |
| 0:40 – 0:55 | Discussion exercises | Run the exercises from the discussion guide. Focus on real-world scenarios participants encounter in their accounts. |
| 0:55 – 1:00 | Wrap-up | Summarise the session. Preview Session 5.2: "Now that we've covered securing the humans using AI, next we'll cover securing the AI agents themselves." |

---

## Key Points to Emphasise

1. **Blocking AI creates shadow AI** — when security teams ban AI tools outright, employees find workarounds (personal devices, browser extensions, copy-paste to personal accounts). The risk doesn't disappear; it becomes invisible. Managed access is always safer than blanket prohibition.
2. **Sensitive data classification is ML in production** — the engine that detects PII, source code, and financial data in AI prompts uses the same classification and NLP techniques participants learned in Stages 1-4. This is a concrete example of ML they already understand.
3. **Managed vs unmanaged is the critical metric** — the most important number on the dashboard isn't "how many AI tools are in use" but "how many are managed vs unmanaged." An organisation with 50 managed AI tools has better security posture than one with 5 unmanaged tools.

---

## Discussion Prompts

- "If you ran the discovery scan on your largest customer's environment right now, how many AI tools do you think it would find? What would surprise the CISO most?"
- "A customer says they've solved this by putting AI tools on an allow-list. What gaps does that approach leave?"
- "How would you design different policies for the engineering team vs the finance team vs the executive team?"

---

## Common Questions and Answers

**Q: How is this different from DLP?**
A: Traditional DLP monitors data leaving through known channels — email, file shares, web uploads. Workforce AI Security specifically understands the AI application layer: it can parse prompts, detect when sensitive data is being sent to an AI model, and apply policies that are context-aware (which AI tool, which user, what type of data). DLP doesn't understand the difference between a Google search and a ChatGPT prompt — this does.

**Q: What if the customer has no AI tools in their environment?**
A: They almost certainly do — they just don't know it. The discovery capability is the opening move. Run a 30-day assessment and the results will speak for themselves. In nearly every deployment, the number of discovered AI tools is 3-5x what the customer expected.

**Q: Can this see encrypted AI traffic?**
A: The solution works at the application layer, not by breaking encryption. It integrates with browsers, endpoints, and cloud access points to inspect AI interactions before they're encrypted for transit. It sees what the user types into the AI tool, not by decrypting the wire but by sitting at the point of interaction.

---

## Facilitator Notes

- This is the first session of Stage 5. Participants are transitioning from building AI (Stage 4) to securing AI. Make the bridge explicit: "You now know how these systems work under the hood — that's what makes you credible when selling security for them."
- The dashboard demo creates the most impact. If you can show a live environment with real discovered apps and data events, it will land far better than slides. Prepare a backup set of screenshots in case the demo environment is unavailable.
- Watch for participants who dismiss this as "just another CASB." The key differentiator is AI-native understanding — prompt inspection, model-aware policies, and GenAI-specific data classification.

---

## Connections to Sales Conversations

- **When a customer says:** "Our employees are using AI tools everywhere and we have no visibility."
- **You can now say:** "That's exactly the problem Workforce AI Security solves. Let me show you what a typical discovery scan reveals — most organisations find 3-5x more AI tools than they expected. From there, we build policies that let your teams use AI productively while keeping sensitive data under control."
