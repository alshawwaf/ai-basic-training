# Facilitator Guide — Session 2.2: Random Forests

> **Stage:** 2  |  **Week:** 5  |  **Lecture deck:** `Lecture-7-Random-Forests.pptx`  |  **Total time:** 60 min

---

## Pre-Session Checklist

- [ ] Reviewed the lecture slides and all 4 exercise guides
- [ ] Run through the single tree vs forest comparison exercise — confirmed the accuracy gap is visible
- [ ] Prepared the "crowd wisdom" analogy: 100 people guessing jelly beans in a jar (average beats any individual)
- [ ] Reviewed OOB error and can explain why it works as a free validation set

---

## Session Flow

| Time | Section | Activity |
|------|---------|----------|
| 0:00 – 0:05 | Recap | "Last session we engineered features from raw logs. Today we build a model powerful enough to use them. In Session 1.4, a single decision tree overfitted. What if we used many trees instead?" |
| 0:05 – 0:15 | Ensemble voting | Explain the core idea: train many trees on different random subsets of data, then let them vote. Use the jelly-bean analogy — individual guesses are noisy, but the average is surprisingly accurate. Draw the ensemble voting diagram on the whiteboard. |
| 0:15 – 0:25 | Tree vs forest comparison | Demo Exercise 1 live. Train a single tree and a 100-tree forest on the same data. Show side-by-side accuracy: the forest should win convincingly on test data. Ask: "Why does averaging reduce errors?" Answer: individual trees make different mistakes, so they cancel out. |
| 0:25 – 0:35 | OOB error and feature importance | Explain OOB: each tree is trained on a bootstrap sample (~63% of data), so the remaining ~37% is a free validation set. OOB error approximates test error without needing a separate holdout. Then show feature importance — the forest ranks which features matter most across all trees. |
| 0:35 – 0:50 | Hands-on exercises | Participants work through Exercises 2-4: train random forest, feature importance, tune the forest (n_estimators, max_depth, max_features). Circulate and help — tuning is where participants need the most guidance. |
| 0:50 – 0:55 | Learning curve discussion | Reconvene. Ask: "As you added more trees, did accuracy keep improving? When did it plateau?" Discuss diminishing returns — going from 10 to 100 trees helps a lot, 100 to 1000 helps a little, 1000 to 10000 helps almost none. |
| 0:55 – 1:00 | Wrap-up | Preview Session 2.3 (clustering and anomaly detection). Key bridge: "Random forests need labels — malicious or benign. What if you don't have labels? What if the attack is something you've never seen before?" |

---

## Key Points to Emphasise

1. **Ensembles beat single models because errors cancel out** — each tree overfits in its own unique way. When you average their predictions, the individual mistakes wash out and the true signal remains. This is the mathematical basis for why random forests outperform single decision trees on virtually every real-world dataset.
2. **Random forests are the workhorse of security ML** — many production malware classifiers, network intrusion detectors, and phishing classifiers use random forests or their gradient-boosted cousins. They handle mixed feature types, tolerate missing values, and resist overfitting. When in doubt, start with a random forest.
3. **Feature importance from a forest is more reliable than from a single tree** — a single tree's importance rankings are unstable (change with different random seeds). A forest averages importance across hundreds of trees, producing a stable and trustworthy ranking. This is a practical tool for threat hunting: "the model says bytes_per_second and dst_port are the top two features — let's investigate those."

---

## Discussion Prompts

- "You train a random forest with 500 trees on your malware dataset. Training takes 30 seconds. Your colleague says 'just use 5000 trees to be safe.' What's the trade-off? When would you say no?"
- "Your forest's top three features for detecting lateral movement are: destination port, bytes per second, and time of day. Does this match your security intuition? What feature would you expect to see that's missing?"
- "A single decision tree gives you an explainable path for every prediction. A random forest averages 100 trees. How do you explain a forest's prediction to your CISO? Is the trade-off worth it?"

---

## Common Questions and Answers

**Q: How many trees should I use in a random forest?**
A: Start with 100. Increase to 500 if you have enough data and time. Beyond 500, you typically see diminishing returns — accuracy improves by fractions of a percent while training time grows linearly. Use the OOB error or validation accuracy to find the point where adding more trees stops helping. For production security models, 200-500 trees is a common sweet spot.

**Q: What's the difference between a random forest and gradient boosting (XGBoost)?**
A: Both are ensembles of trees. A random forest trains all trees independently in parallel, then averages them. Gradient boosting trains trees sequentially — each new tree corrects the mistakes of the previous ones. Gradient boosting often achieves slightly higher accuracy but is harder to tune and more prone to overfitting. Random forests are more forgiving and a better starting point. We focus on random forests here because the concepts transfer directly.

**Q: Can random forests handle the engineered features from last session?**
A: Perfectly. Random forests handle numeric, binary, and encoded categorical features without requiring scaling. They also naturally handle feature interactions — a tree can split on bytes_per_second at one node and dst_port at another, effectively learning the combination. This is why feature engineering and random forests together are such a powerful combination for security data.

---

## Facilitator Notes

- The single-tree vs forest comparison (Exercise 1) is the hook. Make sure the accuracy gap is visible on screen. If the gap is small on a particular dataset, increase the noise or reduce the single tree's max_depth to make the contrast starker.
- Feature importance (Exercise 3) generates excellent security discussion. Project the importance bar chart and ask: "If you were a threat hunter, where would you focus based on this?" This connects ML output to SOC workflows.
- Tuning (Exercise 4) can feel overwhelming — there are many hyperparameters. Focus on three: `n_estimators` (number of trees), `max_depth` (tree depth), and `max_features` (features per split). Advise participants to tune one at a time while holding others fixed.
- Some participants will ask about XGBoost or LightGBM. Acknowledge these exist and are powerful, but redirect: "Random forests teach the core ensemble concepts. Once you understand why averaging trees works, gradient boosting is a natural next step."

---

## Connections to Sales Conversations

- **When a customer asks:** "What algorithm does your malware detection use?"
- **You can now say:** "Our detection leverages ensemble methods — the same family as random forests. Instead of relying on a single model that can be fooled, we train hundreds of models that each see the data differently and then combine their judgments. This makes the detection more robust against evasion: an attacker might fool one tree, but fooling the majority vote of hundreds of trees is vastly harder. The ensemble also ranks which features matter most, which helps our threat research team understand evolving attack patterns."
