# Discussion Guide — Session 0.3: AI Objection Handling

> **For facilitators and self-study.** Use these exercises during the live session or work through them independently.

---

## Exercise 1: Objection Sorting (5 min)

Classify each objection by its root cause. Understanding WHY the customer objects tells you how to respond.

| Objection | Root Cause: Fear / Misunderstanding / Bad Experience / Legitimate Concern |
|-----------|-------------------------------------------------------------------------|
| "AI is just pattern matching" | |
| "We tried ML and it was all false positives" | |
| "AI will replace our analysts" | |
| "What about adversarial attacks?" | |
| "Our data is too sensitive" | |
| "We don't have enough data" | |
| "How do we know it's making the right decisions?" | |
| "How is this different from our SIEM rules?" | |

**Discussion:** Does the root cause change how you structure your ACE response? Which root causes require the most empathy in the Acknowledge step?

---

## Exercise 2: ACE Practice — Written (10 min)

Write a complete ACE response for each of these objections you might encounter in the field. These are NOT from the session — they're new variations.

### Objection A
> "We're a small team. We don't have the resources to manage an AI system on top of everything else."

- **A** (Acknowledge):
- **C** (Clarify):
- **E** (Educate):

### Objection B
> "Our board wants to see ROI on AI investments. How do we measure the value of something that prevents attacks that might not have happened?"

- **A** (Acknowledge):
- **C** (Clarify):
- **E** (Educate):

### Objection C
> "Every vendor says they have AI now. It's become meaningless. I just want something that works."

- **A** (Acknowledge):
- **C** (Clarify):
- **E** (Educate):

**Share with your pair partner. Did they structure their responses differently?**

---

## Exercise 3: Role-Play Scenarios (20 min)

Pair up. One person is the customer, one is the architect. Use ACE. Rotate after each round.

### Round 1 — The Sceptical SOC Manager (5 min)
> "We've been through three 'AI-powered' tools in five years. Each one promised to reduce our alert volume. None of them did. I'm done chasing the AI dragon."

### Round 2 — The Compliance-Focused CISO (5 min)
> "We're under SOX and PCI-DSS. If your AI makes an automated decision that impacts our audit trail, I need to explain exactly why it made that decision to our auditors. Can you guarantee explainability?"

### Round 3 — The Technical Architect Who Knows ML (5 min)
> "I've taken ML courses. I know your 'AI' is probably a random forest trained on labelled netflow data. What makes yours better than what I could build in scikit-learn in an afternoon?"

### Round 4 — The Budget-Constrained Director (5 min)
> "AI sounds great in theory, but we're cutting budgets this year. I can't justify a new AI tool when my team doesn't even have enough headcount to handle current alerts."

### Debrief
- Which scenario was hardest? Why?
- Did the Clarify step reveal a different concern than the stated objection?
- Where did technical specificity (from Sessions 0.1 and 0.2) help?

---

## Exercise 4: Build Your Objection Playbook (10 min)

Based on your own field experience, write down 3 AI objections you've personally heard from customers that are NOT covered in this session.

For each one:
1. State the objection
2. Identify the root cause (fear, misunderstanding, bad experience, legitimate concern)
3. Write your ACE response
4. Identify which Stage 1-4 concept gives you the technical ammunition

| # | Objection | Root Cause | ACE Response (brief) | Technical Anchor |
|---|-----------|-----------|---------------------|-----------------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

**Share with the group. Add the best ones to the cohort's shared playbook.**

---

## Exercise 5: The Anti-Pattern Spotting (5 min)

These are BAD responses to AI objections. For each one, identify what's wrong and rewrite it using ACE.

### Bad Response A
> Customer: "AI is just hype."
> Architect: "No, our AI is genuinely different. We use advanced neural networks with proprietary algorithms."

**What's wrong:**
**Better response:**

### Bad Response B
> Customer: "We tried ML and got too many false positives."
> Architect: "That was probably the vendor's fault. Our solution is much more accurate."

**What's wrong:**
**Better response:**

### Bad Response C
> Customer: "How do we know the AI is making correct decisions?"
> Architect: "You just have to trust the model. It's been validated on millions of events."

**What's wrong:**
**Better response:**

---

## Self-Study Reflection Questions

1. What's the hardest AI objection you've personally faced? Could ACE have helped?
2. Which of the 8 objections in this session do you feel LEAST confident answering? What would you need to learn (in Stages 1-4) to close that gap?
3. Think about your own product's AI. If a customer used the 5-question framework from Session 0.1, which objection would they most likely raise?
4. Is there an objection where the honest answer is "you're right, AI isn't the best solution for this problem"? When is the right move to NOT sell AI?
