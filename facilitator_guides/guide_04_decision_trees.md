# Facilitator Guide — Session 1.4: Decision Trees

> **Stage:** 1  |  **Week:** 3  |  **Lecture deck:** `Lecture-4-Decision-Trees.pptx`  |  **Total time:** 60 min

---

## Pre-Session Checklist

- [ ] Reviewed the lecture slides (20 slides) and all 4 exercise guides
- [ ] Run through the tree visualisation exercise — confirmed `plot_tree` renders correctly
- [ ] Prepared an example of a security decision as a tree (e.g., "Is the source IP internal? → Is the port above 1024? → Is it during business hours?")
- [ ] Reviewed Gini impurity at a high level — be ready to explain it without formulas

---

## Session Flow

| Time | Section | Activity |
|------|---------|----------|
| 0:00 – 0:05 | Recap | Quick: "In logistic regression, the model draws a line. What if the real boundary between malicious and benign isn't a straight line?" |
| 0:05 – 0:15 | Tree as flowchart | Draw a simple decision tree on the whiteboard using a security example: "Is source external? → Does the payload contain a known signature? → Is the destination a critical server?" Ask: "How is this different from a rule-based SIEM?" |
| 0:15 – 0:25 | How trees split — Gini impurity | Explain that the tree picks the feature and threshold that best separates classes at each node. Use the "sorting laundry" analogy: each split should make the piles more pure. Avoid heavy maths — focus on intuition. |
| 0:25 – 0:35 | Feature importance and overfitting | Show that trees rank features by importance. Then demonstrate overfitting: an unlimited tree memorises the training data. Introduce max_depth as the control. |
| 0:35 – 0:50 | Hands-on exercises | Participants work through Exercises 1-4: how trees decide, train and read the tree, feature importance, depth and overfitting. Circulate and help. |
| 0:50 – 0:55 | Interpretability discussion | Discuss: "Your CISO asks why the model flagged a connection. With logistic regression, you show coefficients. With a decision tree, you show the path. Which is easier to explain in an incident report?" |
| 0:55 – 1:00 | Wrap-up | Preview Session 1.5 (model evaluation). Key bridge: "We've built three models. How do we know which one is actually best? Accuracy alone won't tell us." |

---

## Key Points to Emphasise

1. **Decision trees are the most interpretable ML model** — you can print the tree and trace exactly why any prediction was made. In regulated industries and incident response, this explainability is a genuine competitive advantage.
2. **Feature importance tells you what matters** — a tree trained on network data might reveal that destination port and packet size are the top two features. This guides threat hunting: if the model says port matters most, analysts know where to look.
3. **Overfitting is visible and controllable** — an unlimited tree perfectly fits training data but fails on new data. max_depth is a single knob that controls the trade-off. This is the most intuitive introduction to the bias-variance trade-off.

---

## Discussion Prompts

- "Your tree's top feature is 'time_of_day.' It splits at 2:00 AM. What does this mean for your detection? Is it a real pattern or an artefact?"
- "An auditor asks you to explain why your model blocked a transaction. Compare explaining a logistic regression coefficient vs walking through a decision tree path. Which would the auditor prefer?"
- "You train a tree with max_depth=20 and get 99% training accuracy but 60% test accuracy. What happened? What do you do?"

---

## Common Questions and Answers

**Q: How is a decision tree different from a rule-based system?**
A: A rule-based system uses hand-written rules: "IF port=445 AND source=external THEN block." A decision tree learns the rules from data. The tree might discover splits you'd never think to write. It also adapts when you retrain on new data — hand-written rules don't.

**Q: What is Gini impurity in plain English?**
A: It measures how mixed a group is. If a node contains 50% malicious and 50% benign, Gini is at its maximum — the group is maximally impure. If a node is 100% malicious, Gini is 0 — perfectly pure. The tree picks splits that make children nodes as pure as possible.

**Q: Why not just set max_depth really high to get better accuracy?**
A: A deeper tree memorises the training data, including its noise and quirks. It performs great on training data but poorly on new data — this is overfitting. The exercise on depth vs overfitting makes this visible: you'll see training accuracy climb while test accuracy drops.

---

## Facilitator Notes

- The tree visualisation in Exercise 2 is a powerful visual. Project it on screen and walk through one prediction path as a group before participants explore on their own.
- Feature importance (Exercise 3) generates good security discussion. When participants see the ranked features, ask: "Does this match your intuition? Any surprises?" Surprises often reveal either a data quality issue or a genuine insight.
- The overfitting exercise (Exercise 4) is the conceptual climax. Have participants plot training accuracy vs test accuracy at different depths. The moment the lines diverge is the "aha moment" — make sure everyone sees it.

---

## Connections to Sales Conversations

- **When a customer asks:** "Can your model explain why it flagged this alert?"
- **You can now say:** "Absolutely. Our detection logic can be traced step by step — which features mattered, what thresholds were crossed, and why this specific event was flagged. That's not just useful for analysts triaging alerts; it's essential for compliance teams that need to document detection rationale. Let me walk you through an example of how a decision path looks."
