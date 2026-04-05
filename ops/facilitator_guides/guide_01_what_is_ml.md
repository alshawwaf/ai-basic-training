# Facilitator Guide — Session 1.1: What is Machine Learning?

> **Stage:** 1  |  **Week:** 1  |  **Lecture deck:** `Lecture-1-What-is-ML.pptx`  |  **Total time:** 60 min

---

## Pre-Session Checklist

- [ ] Reviewed the lecture slides (29 slides) and all 5 exercise guides
- [ ] Verified Python environment: scikit-learn, matplotlib, pandas installed and working
- [ ] Loaded the digits dataset yourself — confirmed `load_digits()` runs without errors
- [ ] Prepared a brief phishing example to illustrate "rules vs learning"

---

## Session Flow

| Time | Section | Activity |
|------|---------|----------|
| 0:00 – 0:05 | Welcome | Transition from Stage 0 to Stage 1. Set expectations: "We're writing code now." |
| 0:05 – 0:15 | Rules vs ML | Walk through traditional if/else phishing rules vs a model that learns from data. Draw the contrast: rules break when attackers adapt, ML generalises. |
| 0:15 – 0:25 | Three types of ML | Cover supervised, unsupervised, reinforcement learning. Ask: "Which type do you think most security products use?" (Answer: supervised.) |
| 0:25 – 0:35 | ML workflow and EDA | Walk through the training loop and the full ML workflow. Introduce exploratory data analysis with the digits dataset. Demo Exercise 1 (loading data) live. |
| 0:35 – 0:50 | Hands-on exercises | Participants work through Exercises 2-5: statistics, class balance, visualisation, what the model sees. Circulate and help with Python issues. |
| 0:50 – 0:55 | Class imbalance discussion | Tie Exercise 3 (class balance) back to security: "In real phishing data, 99% of emails are legitimate. What does that mean for your model?" |
| 0:55 – 1:00 | Wrap-up | Preview Session 1.2 (linear regression). Assign: "Think about a security metric you'd want to predict as a number — we'll use that next session." |

---

## Key Points to Emphasise

1. **ML is pattern recognition, not magic** — a model finds statistical patterns in data. If the pattern isn't in the data, the model can't learn it. This grounds every future discussion.
2. **Supervised learning dominates security** — labelled examples of "malicious" and "benign" are the foundation. The quality of those labels determines everything.
3. **Class imbalance is the default in security data** — attacks are rare events. A model that predicts "benign" every time gets 99%+ accuracy but catches nothing. This concept resurfaces in every remaining session.

---

## Discussion Prompts

- "You have a rule that blocks emails containing 'click here to verify your account.' An attacker changes the wording. What happens to your rule? What would happen with a trained model?"
- "If you had to label 10,000 network connections as normal or malicious, how would you get those labels? What could go wrong?"
- "Look at the digits dataset — each image is just 64 numbers. What security data could you represent as a grid of numbers like this?"

---

## Common Questions and Answers

**Q: Do I need to understand the maths behind ML to use it in security?**
A: Not deeply. You need to understand what a model does (finds patterns), what it needs (labelled data), and how to measure whether it works (metrics). The Python libraries handle the maths. This programme gives you the intuition without requiring calculus.

**Q: Why are we using a handwritten digits dataset instead of security data?**
A: The digits dataset is small, clean, and visual — you can literally see what the model sees. This lets you build intuition without fighting messy data. We introduce security datasets in Session 1.3 (logistic regression with phishing URLs) and continue from there.

**Q: How is ML different from the AI we discussed in Stage 0?**
A: ML is the engine inside most "AI" security products. Stage 0 gave you the vocabulary to evaluate vendor claims. Stage 1 gives you the hands-on understanding of what those products actually do under the hood.

---

## Facilitator Notes

- This is the first coding session. Expect 5-10 minutes of environment issues (wrong Python version, missing packages, Jupyter not launching). Front-load troubleshooting before the exercises.
- The digits dataset is deliberately non-security. If participants push back, explain: "We learn to drive on quiet roads before hitting the motorway. Security data comes in Session 1.3."
- Exercise 5 (what the model sees) is the "aha moment" — when participants see a digit as a pixel grid, they understand that all ML input is just numbers. Give this exercise enough time.

---

## Connections to Sales Conversations

- **When a customer asks:** "How does your product use AI to detect threats?"
- **You can now say:** "Our detection engine is a supervised ML model — it learns from labelled examples of known threats and generalises to catch variants. Let me explain what that actually means: the model takes raw data, converts it to numerical features, and finds patterns that separate malicious from benign. The key question is always: what data was it trained on, and how do we handle the fact that attacks are rare compared to normal traffic?"
