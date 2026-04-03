# Facilitator Guide — Session 2.4: Overfitting & Cross-Validation

> **Stage:** 2  |  **Week:** 6  |  **Lecture deck:** `Lecture-9-Overfitting-CrossValidation.pptx`  |  **Total time:** 60 min

---

## Pre-Session Checklist

- [ ] Reviewed the lecture slides and all 4 exercise guides
- [ ] Run through the overfitting demo — confirmed the train/validation divergence plot renders correctly
- [ ] Prepared the bias-variance diagram: underfitting (high bias) on the left, overfitting (high variance) on the right, sweet spot in the middle
- [ ] Reviewed k-fold cross-validation and can draw the fold diagram (k blocks, one held out per iteration)

---

## Session Flow

| Time | Section | Activity |
|------|---------|----------|
| 0:00 – 0:05 | Bridge | "We've built decision trees, random forests, and clustering models. Every time we checked 'training accuracy' vs 'test accuracy.' Today we formalise why those numbers differ and how to make sure your model works on data it's never seen." |
| 0:05 – 0:15 | Overfitting curve | Demo Exercise 1 live. Plot training accuracy and validation accuracy against model complexity (tree depth). Walk through three zones: underfitting (both low), sweet spot (both high), overfitting (training high, validation drops). Ask: "Where would you deploy your model?" |
| 0:15 – 0:25 | Bias-variance trade-off | Draw the bias-variance diagram on the whiteboard. High bias = model too simple, misses real patterns. High variance = model too complex, memorises noise. Every model choice is a position on this spectrum. Connect to security: a simple model misses subtle attacks (bias); an overfit model triggers on training noise (variance). |
| 0:25 – 0:35 | K-fold cross-validation | Draw the k-fold diagram: 5 blocks of data, 5 iterations, each block serves as validation once. Explain why this is better than a single train/test split: every data point is validated exactly once, the score is an average of 5 estimates, and it wastes no data. Demo the variance in fold scores — some folds score higher than others. |
| 0:35 – 0:50 | Hands-on exercises | Participants work through Exercises 2-4: bias-variance exploration, k-fold cross-validation, validation curve. Circulate and help — the validation curve exercise ties everything together. |
| 0:50 – 0:55 | Regularisation and production reality | Reconvene. Briefly cover regularisation techniques: max_depth for trees, alpha for linear models, dropout for neural networks (preview). Connect to concept drift: "Your model was trained on last year's threats. This year's attacks look different. What happens?" |
| 0:55 – 1:00 | Wrap-up | Summarise Stage 2. "You can now engineer features, build ensembles, detect anomalies, and validate that your models generalise. Stage 3 introduces neural networks — but every concept from today carries forward. Overfitting doesn't care what algorithm you use." |

---

## Key Points to Emphasise

1. **Overfitting is the central failure mode in ML** — a model that performs brilliantly on training data but fails on new data is worthless in production. Every deployment decision should be based on validation or test performance, never training performance. This applies equally to decision trees, random forests, neural networks, and any future model participants encounter.
2. **Cross-validation gives you a trustworthy performance estimate** — a single train/test split is fragile: you might get lucky or unlucky with which data lands in each set. K-fold cross-validation averages over k different splits, producing a more stable and reliable estimate. If the fold scores vary wildly, that itself is information — your model's performance is unstable.
3. **Models degrade in production because the world changes** — a malware classifier trained on 2024 samples will miss 2025 techniques. This concept drift is the security-specific version of overfitting to the past. Regularisation and cross-validation help you build robust models, but periodic retraining on fresh data is non-negotiable in security.

---

## Discussion Prompts

- "Your random forest gets 97% accuracy on training data and 84% on validation data. Is this acceptable? What specific steps would you take to close the gap?"
- "You run 5-fold cross-validation and get scores of [0.91, 0.89, 0.92, 0.71, 0.90]. One fold is much lower than the others. What might explain this? Would you ignore it or investigate?"
- "Your phishing detection model was trained on data from January to June. By December, its recall has dropped from 0.88 to 0.62. What happened? How would you detect this problem before it hurts you?"

---

## Common Questions and Answers

**Q: How many folds should I use in cross-validation?**
A: Five or ten folds is standard. Five folds means each fold uses 80% for training and 20% for validation — a good balance between training set size and validation reliability. Ten folds use 90%/10% — slightly more training data per fold but ten iterations to run. With very small datasets, use more folds (or even leave-one-out). With very large datasets, five folds is sufficient and saves computation time.

**Q: If my model overfits, should I get more data or simplify the model?**
A: Both work, but they address different problems. More data helps when the model is learning real patterns but doesn't have enough examples to distinguish them from noise. Simplifying the model (reducing depth, adding regularisation) helps when the model has too much capacity for the amount of data. In practice, try simplification first because it's cheaper than collecting more labelled security data. If simplification hurts performance too much, then invest in more data.

**Q: What is concept drift and how do I handle it in security?**
A: Concept drift means the relationship between features and outcomes changes over time. In security, attackers constantly evolve: new malware families, new evasion techniques, new infrastructure. A model trained on last quarter's threats gradually becomes stale. Handle it by monitoring model performance on recent data (not just historical test sets), setting up alerts when metrics drop below a threshold, and retraining on fresh labelled data regularly — monthly or quarterly is common for security models.

---

## Facilitator Notes

- The overfitting demo (Exercise 1) is the emotional anchor. The moment participants see validation accuracy drop while training accuracy keeps climbing, the concept clicks. Project the plot large and trace both lines with your finger. Ask: "Which depth would you choose? Why?"
- The bias-variance diagram should stay on the whiteboard for the entire session. Every subsequent topic refers back to it: regularisation moves you left (toward bias), adding complexity moves you right (toward variance), cross-validation tells you where you currently sit.
- The k-fold exercise (Exercise 3) is procedural — participants follow steps. The real learning happens when they examine the fold-by-fold scores. If one fold is significantly worse, pause and discuss: "What might be in that fold that's different?" This teaches participants to interrogate their results, not just accept an average number.
- Concept drift often generates the best discussion of Stage 2. Security professionals instinctively understand that threats evolve. Connecting this intuition to "model performance degrades over time" makes the ML concept concrete. Ask: "How often would you retrain a phishing classifier? A malware classifier? A network anomaly model?"

---

## Connections to Sales Conversations

- **When a customer asks:** "How do you make sure your models stay accurate over time?"
- **You can now say:** "Every ML model degrades as the threat landscape evolves — it's called concept drift. We address this in three ways. First, we use cross-validation during training to ensure the model generalises rather than memorising historical patterns. Second, we monitor deployed model performance continuously — if recall drops below our threshold, we know immediately. Third, we retrain on fresh data regularly, incorporating the latest threat intelligence. A model that was excellent six months ago can be mediocre today if it hasn't been updated. Our pipeline is designed for continuous retraining, not one-time deployment."
