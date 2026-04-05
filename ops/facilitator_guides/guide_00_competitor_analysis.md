# Facilitator Guide — Session 0.2: How Competitors Position AI

> **Stage:** 0  |  **Week:** 1  |  **Content:** `stage0_positioning/02_competitor_analysis/`  |  **Total time:** 60 min

---

## Pre-Session Checklist

- [ ] Reviewed the README.md and discussion_guide.md
- [ ] Checked for recent competitor announcements (Charlotte AI, Purple AI, XSIAM, Copilot updates)
- [ ] Participants were assigned to bring a competitor datasheet with an AI claim

---

## Session Flow

| Time | Section | Activity |
|------|---------|----------|
| 0:00 – 0:05 | Recap | Quick: "Name one thing from Session 0.1 that changed how you think about AI claims." |
| 0:05 – 0:20 | Vendor deep dives | Walk through CrowdStrike, Palo Alto, and SentinelOne. Focus on "What's under the hood" and "How to position against." |
| 0:20 – 0:30 | Darktrace + Microsoft | Cover the two outliers — unsupervised (Darktrace) vs LLM-first (Microsoft). |
| 0:30 – 0:40 | Competitive matrix | Show the summary table. Ask: "Which vendor's approach is closest to ours? Where are we genuinely different?" |
| 0:40 – 0:55 | Battlecard exercise | Groups of 2-3 create a one-page battlecard for the vendor they compete against most. Present to the group. |
| 0:55 – 1:00 | Wrap-up | Preview Session 0.3 (objection handling). |

---

## Key Points to Emphasise

1. **Every vendor's AI has a real core** — dismissing competitors as "just hype" loses credibility. Acknowledge what's real, then expose the gaps.
2. **Darktrace is genuinely different** — unsupervised approach with different trade-offs (high FP, baseline poisoning). Don't lump it with the endpoint vendors.
3. **LLM copilots are the new battleground** — the differentiator is data access and integration depth, not the LLM model itself.

---

## Discussion Prompts

- "Which vendor's AI positioning do customers find most compelling? Why?"
- "If you were building a competitive demo, what single question would you ask about the competitor's AI that they couldn't answer well?"
- "Which vendor's limitation is most relevant to your customers' environments?"

---

## Common Questions and Answers

**Q: How current is this information? Vendors update their products constantly.**
A: The underlying ML architectures change slowly — a vendor built on gradient-boosted trees won't switch to transformers overnight. The LLM copilot layer moves faster. Encourage participants to follow vendor engineering blogs for updates, but the fundamental positioning holds.

**Q: What if I don't know the competitor the customer is evaluating?**
A: The 5-question framework from Session 0.1 works for any vendor. You don't need vendor-specific knowledge — you need a framework that surfaces the right information from any AI claim.

**Q: Should we be worried about Microsoft Security Copilot?**
A: Copilot is an investigation assistant, not a detection engine. It makes analysts faster but doesn't find threats that Defender's existing models miss. Position against it by asking: "What net-new detections does Copilot provide?"

---

## Facilitator Notes

- This session generates the most engagement — participants have strong opinions about competitors. Let the discussion run if it's productive.
- If participants work at the same company, the battlecard exercise becomes immediately actionable. Consider collecting the best battlecards into a shared resource.
- Watch for participants who get defensive about their own product's AI. Gently redirect: "The same framework applies to us. Let's be honest about where our AI is strong and where it's not."

---

## Connections to Sales Conversations

- **When a customer asks:** "CrowdStrike says they have AI-native detection. How are you different?"
- **You can now say:** "CrowdStrike's ML is genuinely strong for known threat families. Their models are gradient-boosted trees trained on endpoint telemetry. Where we differentiate is [specific capability] — and the question to ask them is how their model performs on threats specific to YOUR industry."
