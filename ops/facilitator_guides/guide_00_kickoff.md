# Facilitator Guide — Week 0: Program Kickoff

> **Stage:** Pre-program  |  **Week:** 0  |  **Total time:** 90 min  |  **Format:** Live, all participants

---

## Pre-Session Checklist

- [ ] All participants have received and completed the pre-program skills survey
- [ ] Reviewed survey results — identified Python comfort spread and AI exposure levels
- [ ] Pair assignments drafted (cross-region, complementary skill levels)
- [ ] Welcome packet sent to all participants at least 3 days before kickoff
- [ ] Confirmed all participants have Python 3.10+ installed and virtual environment created
- [ ] Tested screen sharing, video conferencing, and recording setup
- [ ] Cohort Slack/Teams channel created and all participants invited

---

## Session Flow

| Time | Section | Activity |
|------|---------|----------|
| 0:00 – 0:10 | Welcome and introductions | Tech lead sets the tone. Each participant: name, region, role, one sentence on why they joined. |
| 0:10 – 0:25 | Why this program exists | The problem: customers ask about AI daily, most SEs can't go beyond marketing slides. The opportunity: an architect who can demo a working AI system in a customer meeting is 10x more valuable. Share a personal story of a customer conversation where AI knowledge (or lack of it) made the difference. |
| 0:25 – 0:40 | Program structure walkthrough | Walk through the 5 stages, 3 tiers, and 13-week timeline. Explain the assessment gates. Be explicit: "This is not a watch-and-forget webinar. There are 4 graded assessments. You will build real things." |
| 0:40 – 0:55 | What you will build | Show the Stage 4 Security Analyst Assistant running live. Ask a question, show the retrieval, show the answer. Then say: "By Week 12, every one of you will have built this — customised with your own documents — and you'll demo it to stakeholders in Week 13." |
| 0:55 – 1:05 | Expectations and logistics | Weekly rhythm: 3-4 hrs self-paced + 1 hr live. Pair partners announced. Slack channel norms: post weekly, ask questions publicly, no question is too basic. What happens if you fall behind: reach out early, recorded sessions available, 2-week retake window for assessments. |
| 1:05 – 1:15 | Environment setup — live | Walk through creating and activating the virtual environment together. Have everyone run `python --version` and `pip --version` in their terminal. Troubleshoot on the spot. This is the #1 thing that blocks people in Week 1. |
| 1:15 – 1:25 | Q&A | Open floor. Expect questions about time commitment, assessment difficulty, and whether this will be relevant to their specific role. |
| 1:25 – 1:30 | Send-off | Assign Week 1 reading: Stage 0 Session 0.1 (AI Landscape) + Stage 1 Lesson 1.1 (What is ML?). Remind them to post an introduction in the Slack channel by end of week. "See you at the first live Q&A." |

---

## Key Points to Emphasise

1. **This is selective and earned** — They were nominated because their manager believes they have the potential. The 12-16 cohort size is intentional. This is not a mass training — it's an investment in a small group who will become the AI experts in their region.

2. **You will build real things, not just watch slides** — 67 hands-on exercises, 4 capstone projects, a customer demo kit. The difference between this program and a LinkedIn Learning course is that you walk away with working code you built yourself.

3. **The cohort is the support system** — Pair partners, Slack channel, weekly live sessions. Nobody should be stuck alone for more than 24 hours. If you're stuck, post in the channel. Someone else probably has the same question.

---

## Discussion Prompts

- "What's one thing you wish you understood better about AI in our product stack?"
- "Have you ever been in a customer meeting where AI came up and you didn't know how to respond? What happened?"
- "What does success look like for you personally at the end of 13 weeks?"

---

## Common Questions and Answers

**Q: I'm not sure my Python is strong enough. Will I be able to keep up?**
A: If you can write functions, use loops, and install pip packages, you're ready. The exercises are step-by-step with reference solutions. Stage 1 starts from absolute basics. If the survey flagged you as needing extra Python support, we'll pair you with a stronger Python partner.

**Q: What happens if I fail an assessment gate?**
A: You get specific feedback on what to improve and a retake window of 2 weeks. The assessments are designed to confirm understanding, not trick you. If you're doing the exercises, you'll pass.

**Q: My customer meetings are mostly about [endpoint / cloud / network]. Is this relevant?**
A: Every stage uses cybersecurity examples from across the stack. Stage 0 specifically covers how AI applies to each domain. But more importantly — the customer doesn't care which domain the AI knowledge came from. They care that you can speak technically and credibly about it.

**Q: How much time is this really going to take?**
A: Plan for 5 hours per week. Some weeks will be lighter (Stage 0 is discussion-based), some heavier (Stage 3 neural networks). The self-paced component is flexible — you can do it at 6am or 11pm, whatever works for your schedule. The one fixed commitment is the 1-hour weekly live session.

**Q: Can I skip Stage 0 if I'm already good at positioning?**
A: No. Stage 0 introduces frameworks (5-question evaluation, ACE, PDFC) that the rest of the program references. It's 4 hours total. Even experienced SEs find value in the competitive analysis and objection handling sessions.

---

## Facilitator Notes

- The live demo of the Security Analyst Assistant (0:40–0:55) is the most important moment of the kickoff. It makes the 13-week commitment feel tangible. Practice this beforehand — have 3 pre-built queries ready and make sure the demo runs cleanly.
- If a participant can't get Python set up during the session, don't let it derail the group. Note their issue, move on, and schedule a 15-minute troubleshooting call after the session.
- The environment setup section exists because "install Python and create a venv" is where 30% of participants get stuck and silently disengage. Doing it live with the group prevents that.
- Read the survey results before the session. If most participants have zero ML exposure, emphasise the "no prior ML required" message more. If several have some exposure, raise the bar: "You'll be surprised how much deeper this goes than what you've seen before."
- The pair partner assignments should be cross-region where possible (e.g., an NA architect with a LATAM one). Announce them during the expectations section. Pairs review each other's capstone code in Week 13.

---

## After the Kickoff

Within 24 hours:
- [ ] Send a follow-up message to the Slack channel with links to Week 1 reading
- [ ] Confirm all participants have a working Python environment (follow up individually with anyone who didn't get set up)
- [ ] Post pair partner assignments in the channel
- [ ] Share the recording for anyone who needs to review

Within 1 week:
- [ ] Check that all participants have posted their introduction in Slack
- [ ] Follow up privately with anyone who hasn't — early silence is the #1 predictor of dropout
