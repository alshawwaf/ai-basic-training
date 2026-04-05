# Facilitator Guide — Session 1.2: Linear Regression

> **Stage:** 1  |  **Week:** 2  |  **Lecture deck:** `Lecture-2-Linear-Regression.pptx`  |  **Total time:** 60 min

---

## Pre-Session Checklist

- [ ] Reviewed the lecture slides (21 slides) and all 4 exercise guides
- [ ] Run through the train/test split and fitting exercises yourself — confirmed outputs match expected results
- [ ] Prepared a whiteboard-friendly example of y = mx + b (e.g., "more firewall rules → longer processing time")
- [ ] Checked that participants completed Session 1.1 exercises successfully

---

## Session Flow

| Time | Section | Activity |
|------|---------|----------|
| 0:00 – 0:05 | Recap | Quick: "Name one thing from Session 1.1 that surprised you about how ML works." |
| 0:05 – 0:15 | Regression vs classification | Draw the distinction: regression predicts a number, classification predicts a category. Ask: "Is predicting a risk score regression or classification?" |
| 0:15 – 0:25 | The equation y = mx + b | Walk through the line equation on the whiteboard. Show how fitting a line means finding the best m (slope) and b (intercept). Use a concrete example: incident count vs response time. |
| 0:25 – 0:35 | Evaluation metrics | Cover MSE and R-squared. Draw a scatter plot with a line — show what residuals are. Ask: "An R-squared of 0.7 means what, in plain English?" |
| 0:35 – 0:50 | Hands-on exercises | Participants work through Exercises 1-4: understanding regression, train/test split, fit and predict, evaluate regression. Circulate and help. |
| 0:50 – 0:55 | Security applications | Discuss: "Where in security would you predict a continuous value?" Examples: mean time to respond, risk score, expected alert volume, estimated breach cost. |
| 0:55 – 1:00 | Wrap-up | Preview Session 1.3 (logistic regression). Key bridge: "What if instead of predicting a number, we need a yes/no answer — phishing or not phishing?" |

---

## Key Points to Emphasise

1. **Train/test split is non-negotiable** — evaluating a model on the data it trained on is like grading your own exam. Participants must internalise this before any further modelling.
2. **R-squared tells you proportion of variance explained** — an R-squared of 0.0 means the model is no better than predicting the average every time. An R-squared of 1.0 means perfect prediction. Most real-world security models land between 0.3 and 0.8.
3. **Linear regression is the foundation, not the destination** — every ML model builds on the idea of fitting data and measuring error. Understanding this one model makes every future model easier to grasp.

---

## Discussion Prompts

- "Your SOC manager wants to predict how many alerts the team will receive next Tuesday. Is this a regression or classification problem? What features would you use?"
- "You build a model to predict incident response time. It gets R-squared of 0.45. Is that good enough to use? What would you tell your manager?"
- "Why do we split data into training and testing sets? What goes wrong if we skip this step?"

---

## Common Questions and Answers

**Q: When would I actually use linear regression in security?**
A: Predicting continuous values: expected alert volume for capacity planning, mean time to detect/respond for SLA monitoring, risk scores for vulnerability prioritisation. It's less common than classification in security, but it's the conceptual foundation for everything that follows.

**Q: What does a negative R-squared mean?**
A: It means your model is worse than simply predicting the average for every data point. This usually signals a serious problem — wrong features, a bug in preprocessing, or a relationship that isn't linear. It's a red flag, not a score.

**Q: Why start with linear regression if classification is more useful in security?**
A: Linear regression is the simplest possible model — one equation, two parameters. It makes the core concepts visible: fitting, error, evaluation, train/test split. Logistic regression (next session) adds just one more idea — the sigmoid function — to turn this into a classifier. Building incrementally prevents confusion.

---

## Facilitator Notes

- Draw y = mx + b on a whiteboard. Physically sketch data points and draw lines through them. Ask participants which line "fits better" before introducing MSE. The visual intuition matters more than the formula.
- The train/test split exercise is critical. If a participant asks "why not use all the data for training?", have the group discuss before answering. This is a concept they need to own.
- Some participants may find this session less exciting than Session 1.1 (no images, no visual dataset). Anchor it by repeatedly connecting to the next session: "This is the engine. Next session we bolt on classification and attack phishing URLs."

---

## Connections to Sales Conversations

- **When a customer asks:** "Can your product predict how many incidents we'll have next month?"
- **You can now say:** "That's a regression problem — predicting a number from historical patterns. The model learns the relationship between factors like time of year, threat landscape changes, and your infrastructure size. The key metric is R-squared — it tells you how much of the variation the model actually captures vs random noise. Let me show you what that looks like with real data."
