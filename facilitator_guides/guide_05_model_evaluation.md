# Facilitator Guide — Session 1.5: Model Evaluation

> **Stage:** 1  |  **Week:** 3  |  **Lecture deck:** `Lecture-5-Model-Evaluation.pptx`  |  **Total time:** 60 min

---

## Pre-Session Checklist

- [ ] Reviewed the lecture slides (22 slides) and all 5 exercise guides
- [ ] Prepared the "accuracy trap" example: a model that predicts "benign" every time on data with 99% benign samples
- [ ] Run through the ROC/AUC exercise — confirmed the curve plots correctly
- [ ] Reviewed precision, recall, F1 definitions — be ready to explain each with a security analogy

---

## Session Flow

| Time | Section | Activity |
|------|---------|----------|
| 0:00 – 0:05 | Recap | Quick: "We've built three models across four sessions. If someone asks 'which one is best?', what do you say?" Let the group struggle with this before proceeding. |
| 0:05 – 0:15 | The accuracy trap | Present the 99% accuracy model that catches zero attacks. Ask: "Would you deploy this?" Walk through why accuracy fails when classes are imbalanced. Demo Exercise 1 live. |
| 0:15 – 0:25 | Confusion matrix | Draw the 2x2 matrix on the whiteboard. Label each cell with a security example: TP = caught a real attack, FP = blocked a legitimate user, FN = missed a real attack, TN = correctly allowed legitimate traffic. |
| 0:25 – 0:35 | Precision, recall, F1 | Build each metric from the confusion matrix. Use the analogy: precision = "of everything I flagged, how much was real?" Recall = "of everything real, how much did I catch?" F1 = the balance between them. |
| 0:35 – 0:45 | ROC/AUC and threshold tuning | Walk through the ROC curve: what the axes mean, what the diagonal represents, why AUC summarises model quality. Connect to threshold tuning from Session 1.3. |
| 0:45 – 0:55 | Hands-on exercises | Participants work through Exercises 2-5: confusion matrix, precision/recall/F1, ROC and AUC, threshold tuning. Exercise 1 (accuracy trap) was demoed earlier — participants can revisit. |
| 0:55 – 1:00 | Wrap-up | Summarise Stage 1. Preview Stage 2: "You now understand the building blocks. Next we combine models, handle real-world messy data, and tackle harder problems." |

---

## Key Points to Emphasise

1. **Accuracy is misleading in security** — when 99% of data is benign, a model that never flags anything scores 99% accuracy. This is the single most important evaluation lesson for security professionals. Drill it until it's automatic.
2. **False negatives are the expensive mistakes in security** — a missed breach costs orders of magnitude more than a false alert. This means recall often matters more than precision in security contexts, though the right balance depends on the specific use case.
3. **The threshold is a policy lever, not a technical setting** — the ROC curve shows all possible operating points. Choosing where to sit on that curve is a risk decision made by security leadership, not by the model. AUC tells you how good the model is overall; the threshold tells you how you want to use it.

---

## Discussion Prompts

- "Your email security model has precision 0.95 and recall 0.60. That means 5% of flagged emails are legitimate, but you're missing 40% of phishing attacks. Is this acceptable? Who in your organisation decides?"
- "A vendor says their detection model has 99.9% accuracy. What's the first thing you ask? (Hint: what's the class distribution?)"
- "You're choosing between two models: Model A has higher precision, Model B has higher recall. For ransomware detection, which do you pick? What about for spam filtering?"

---

## Common Questions and Answers

**Q: Which metric should I care about most — precision, recall, or F1?**
A: It depends on the cost of errors. If a false negative is catastrophic (missed ransomware, undetected breach), optimise for recall. If false positives are expensive (blocking legitimate transactions, alert fatigue), optimise for precision. F1 is a balanced compromise. In most security detection scenarios, recall gets priority — missing an attack is worse than a false alarm.

**Q: What's a "good" AUC score?**
A: AUC of 0.5 means the model is no better than random coin flipping. AUC of 1.0 means perfect separation. In practice, AUC above 0.9 is strong, 0.8-0.9 is decent, and below 0.8 usually needs improvement. But context matters — a 0.85 AUC model detecting a critical threat may be more valuable than a 0.95 AUC model detecting low-severity spam.

**Q: How do I explain the ROC curve to a non-technical stakeholder?**
A: "Think of it as a dial. Turn it one way: we catch more attacks but also bother more users with false alarms. Turn it the other way: fewer false alarms but we miss more attacks. The ROC curve shows every possible position of that dial. The AUC score tells you how good the dial is overall — a better model gives you better options at every position."

---

## Facilitator Notes

- The accuracy trap (Exercise 1) is the emotional anchor of this session. Do not rush it. When participants see a 99% accurate model that catches nothing, the lesson sticks permanently. Ask: "Would you trust your network security to this model?"
- The confusion matrix should be drawn large on the whiteboard and left visible for the entire session. Every subsequent metric is derived from those four cells. Point back to the matrix constantly.
- This session is the most metrics-heavy in Stage 1. Watch for participants who get lost in formulas. Redirect to the security analogies: "Forget the formula — precision answers: of everything we flagged, how much was real?" Keep it concrete.
- Threshold tuning connects back to Session 1.3 (logistic regression). Remind participants: "This is the same idea — you're choosing where to draw the line. Now you have the tools to make that choice rigorously."

---

## Connections to Sales Conversations

- **When a customer asks:** "Your competitor claims 99.9% detection accuracy. How do you compare?"
- **You can now say:** "Accuracy is the wrong metric for security — and that's not just our opinion, it's how evaluation works. If 99% of traffic is benign, any model gets 99% accuracy by doing nothing. The real questions are: what's the recall — how many actual attacks does it catch? What's the false positive rate — how many alerts are noise? And at what threshold are those numbers measured? We report precision, recall, and AUC because those metrics tell you what actually matters for your security operations."
