# Facilitator Guide — Session 1.3: Logistic Regression

> **Stage:** 1  |  **Week:** 2  |  **Lecture deck:** `Lecture-3-Logistic-Regression.pptx`  |  **Total time:** 60 min

---

## Pre-Session Checklist

- [ ] Reviewed the lecture slides (20 slides) and all 4 exercise guides
- [ ] Run through the phishing URL feature engineering exercise — confirmed the feature extraction code works
- [ ] Prepared 3-4 example URLs (mix of legitimate and phishing) to demonstrate feature engineering live
- [ ] Reviewed the sigmoid function — be ready to sketch it on the whiteboard

---

## Session Flow

| Time | Section | Activity |
|------|---------|----------|
| 0:00 – 0:05 | Recap | Quick: "Last session we predicted a number. Today we predict a category. What's the bridge between them?" |
| 0:05 – 0:15 | From regression to classification | Introduce the sigmoid function. Draw it on the whiteboard: linear output goes in, probability between 0 and 1 comes out. Ask: "Why can't we just use linear regression for yes/no problems?" |
| 0:15 – 0:25 | Feature engineering for URLs | Show how a raw URL becomes numbers a model can use: length, number of dots, presence of IP address, use of HTTPS, suspicious keywords. Demo 2-3 URLs live. |
| 0:25 – 0:30 | Coefficients and interpretation | Show model coefficients. Ask: "If the coefficient for url_length is positive, what does that tell us about longer URLs?" Connect to security: which features matter most for phishing detection. |
| 0:30 – 0:45 | Hands-on exercises | Participants work through Exercises 1-4: from regression to classification, feature engineering URLs, train and evaluate, threshold tuning. Circulate and help. |
| 0:45 – 0:55 | Threshold tuning discussion | After Exercise 4, discuss as a group: "Your model outputs 0.6 probability of phishing. Do you block the email? What if it's 0.4? Who decides the threshold?" Introduce the precision/recall trade-off. |
| 0:55 – 1:00 | Wrap-up | Preview Session 1.4 (decision trees). Key bridge: "Logistic regression draws a single line between phishing and legitimate. What if the boundary isn't a straight line?" |

---

## Key Points to Emphasise

1. **Feature engineering is where security expertise meets ML** — the model is only as good as the features you give it. Knowing that "IP address in URL" is suspicious is domain knowledge no algorithm can replace.
2. **predict_proba is more useful than predict** — a hard yes/no answer hides the model's uncertainty. The probability score lets you set thresholds, escalate uncertain cases, and make risk-based decisions.
3. **Threshold choice is a business decision, not a technical one** — moving the threshold trades precision for recall. In security, this is the trade-off between blocking legitimate emails (false positives) and missing phishing attacks (false negatives). The SOC decides, not the data scientist.

---

## Discussion Prompts

- "You're building a phishing URL classifier for a hospital. Doctors sometimes receive legitimate links from medical device vendors that look suspicious. How do you set the threshold?"
- "Your model's top 3 features are url_length, num_dots, and has_ip_address. A new phishing campaign uses short URLs with no dots and no IP. What happens? How do you fix it?"
- "A colleague says 'The model is 95% accurate, we're done.' What's the first question you ask?"

---

## Common Questions and Answers

**Q: Why use logistic regression instead of something more powerful like deep learning?**
A: Logistic regression is interpretable — you can see exactly which features push the prediction toward "phishing" and by how much. In security, explainability matters for incident response, compliance, and tuning. You can't tune what you can't understand. More complex models come later in the programme.

**Q: What happens when attackers change their URLs to avoid the features we engineered?**
A: This is the adversarial nature of security ML. Features that work today may not work tomorrow. This is why feature engineering is ongoing, not one-time. Production systems retrain regularly and add new features as attack patterns evolve. It's an arms race.

**Q: What's the difference between predict and predict_proba in scikit-learn?**
A: `predict` gives you the final label (0 or 1) using the default 0.5 threshold. `predict_proba` gives you the probability — a number between 0 and 1 — for each class. Always use `predict_proba` and choose your own threshold. The default 0.5 is almost never the right choice for security data.

---

## Facilitator Notes

- This is the first session with real security data (phishing URLs). Expect higher engagement. Let participants explore the data — some will find interesting patterns on their own.
- The feature engineering exercise is the highlight. Give it plenty of time. If participants suggest features not in the exercise (e.g., domain age, TLD type), praise the thinking and note: "That's exactly how production models get better — domain experts suggest features."
- Threshold tuning (Exercise 4) is conceptually difficult. Use a concrete analogy: "A metal detector at an airport. Turn up the sensitivity: catch every weapon, but also every belt buckle. Turn it down: faster lines, but you might miss something. Where do you set it?"

---

## Connections to Sales Conversations

- **When a customer asks:** "How does your product decide if a URL is phishing?"
- **You can now say:** "The model extracts features from the URL — length, structure, presence of suspicious patterns — and calculates a probability score. It's not a binary yes/no; it's a confidence level. We can tune the threshold based on your risk tolerance: tighter for high-security environments, looser if false positives are disrupting your users. The key differentiator is which features we extract and how often we retrain."
