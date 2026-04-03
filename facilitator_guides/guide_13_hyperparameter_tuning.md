# Facilitator Guide — Session 3.4: Hyperparameter Tuning

> **Stage:** 3  |  **Week:** 9  |  **Lecture deck:** `Lecture-13-Hyperparameter-Tuning.pptx`  |  **Total time:** 60 min

---

## Pre-Session Checklist

- [ ] Reviewed the lecture slides and all 4 exercise guides
- [ ] Prepared a whiteboard list of hyperparameters encountered so far: learning rate, batch size, number of layers, neurons per layer, dropout rate, epochs
- [ ] Run through the learning rate sensitivity exercise — confirmed the three regimes (too low / just right / too high) are clearly visible in the loss curves
- [ ] Reviewed grid search, random search, and Bayesian optimisation at a high level — be ready to explain each with a simple analogy

---

## Session Flow

| Time | Section | Activity |
|------|---------|----------|
| 0:00 – 0:05 | Recap | Quick: "Across the last three sessions, we've set dozens of numbers by hand — learning rate, dropout rate, number of neurons. How did we choose those values?" Let participants admit it was mostly guesswork. Bridge into: "Today we learn systematic ways to find the best settings." |
| 0:05 – 0:15 | What are hyperparameters? | Walk through Exercise 1 concepts. Distinguish parameters (learned by training: weights, biases) from hyperparameters (set by you: learning rate, batch size, architecture). Build a categorised list on the whiteboard. Ask: "Which of these do you think matters most?" |
| 0:15 – 0:25 | Learning rate sensitivity | Demo Exercise 2 live. Show three training runs: LR too low (barely learns), LR just right (smooth convergence), LR too high (loss explodes or oscillates). Project all three loss curves side by side. This is the most impactful visual of the session. |
| 0:25 – 0:35 | Search strategies: grid, random, Bayesian | Explain grid search: "Try every combination — thorough but expensive." Random search: "Sample randomly — surprisingly effective because not all hyperparameters matter equally." Bayesian: "Use past results to decide what to try next — smart but more complex." Draw each strategy on the whiteboard as a 2D grid with sampled points. |
| 0:35 – 0:50 | Hands-on exercises | Participants work through Exercises 3-4: batch size effects and architecture search. Exercises 1-2 (hyperparameters and LR sensitivity) were covered earlier — participants can revisit. Circulate and help — architecture search may take longer to run. |
| 0:50 – 0:55 | Production trade-offs | Facilitate discussion: "In a SOC, model retraining happens on a schedule. You can't run a 200-combination grid search every week. How do you balance tuning thoroughness with operational constraints?" Guide toward practical answers: start with random search, narrow the range, then fine-tune. |
| 0:55 – 1:00 | Wrap-up | Summarise Stage 3: "You've built neural networks, regularised them, applied CNNs, and tuned hyperparameters. You now have the full deep learning workflow. Stage 4 brings generative AI — the technology behind large language models and the products your customers ask about every day." |

---

## Key Points to Emphasise

1. **Learning rate is the single most important hyperparameter** — it controls the step size during training. Too small and the model barely learns. Too large and it overshoots and diverges. Getting the learning rate right (or using a schedule that adapts it) has more impact than any other tuning decision. Always tune it first.
2. **Random search beats grid search in most practical scenarios** — research by Bergstra and Bengio (2012, published at the Journal of Machine Learning Research) showed that random search finds good hyperparameter combinations faster because it samples more values of the important dimensions. Grid search wastes evaluations on dimensions that do not matter.
3. **Hyperparameter tuning is a systematic process, not guesswork** — the goal of this session is to replace "I tried a few values and picked the best one" with a structured approach: define the search space, choose a strategy, evaluate with validation data, and pick the best result. This discipline is what separates a prototype from a production model.

---

## Discussion Prompts

- "You have a detection model that needs retraining weekly as new threat data arrives. You can afford 20 training runs per cycle. How do you allocate those 20 runs across hyperparameter tuning?"
- "Your model works well with a learning rate of 0.001. A colleague changes the batch size from 32 to 256 and performance drops. Why might changing one hyperparameter break another's optimal value?"
- "A vendor claims their model is 'auto-tuned with AI.' Based on what you've learned, what do you think that actually means? What questions would you ask?"

---

## Common Questions and Answers

**Q: How many hyperparameters should I tune at once?**
A: Start with the most impactful ones: learning rate and model size (layers and neurons). Once those are in a good range, tune secondary parameters like dropout rate and batch size. Trying to tune everything simultaneously creates an enormous search space that wastes compute. Prioritise based on the hyperparameter ranking covered in the slides.

**Q: What is the difference between a hyperparameter and a regular parameter?**
A: Parameters are the numbers the model learns during training — weights and biases in a neural network. You never set these manually. Hyperparameters are the settings you choose before training starts — learning rate, number of layers, dropout rate, batch size. They control how and how well the model learns its parameters.

**Q: Is Bayesian optimisation always better than random search?**
A: Not always. Bayesian optimisation shines when each training run is expensive (hours or days) because it uses past results to make smarter choices about what to try next. For fast-training models where you can run hundreds of experiments cheaply, random search is simpler and often sufficient. The right strategy depends on your compute budget and how long each run takes.

---

## Facilitator Notes

- The learning rate sensitivity demo (Exercise 2) is the visual centrepiece. Use three dramatically different learning rates (e.g., 0.0001, 0.001, 1.0) so the contrast is impossible to miss. When the high-LR loss curve explodes, participants understand viscerally why this hyperparameter matters.
- Exercise 4 (architecture search) may take longer to execute than other exercises because it trains multiple models. Warn participants to start it early and let it run while they review results from earlier exercises. If machines are slow, reduce the search space in advance.
- The distinction between parameters and hyperparameters (Exercise 1) seems simple but confuses many participants. Use a concrete analogy: "Parameters are what the student learns. Hyperparameters are how the teacher structures the course — class size, pace, difficulty. The teacher sets those before the course starts."
- This session wraps up Stage 3. Take a moment at the end to acknowledge progress: participants have gone from linear regression to CNNs and hyperparameter tuning. That is a genuine accomplishment. A brief retrospective ("What was the hardest concept? What clicked?") can reinforce learning and build momentum for Stage 4.

---

## Connections to Sales Conversations

- **When a customer asks:** "How do you optimise your detection models for our specific environment?"
- **You can now say:** "Every environment is different — network traffic patterns, user behaviour baselines, and threat profiles vary across organisations. We use systematic hyperparameter tuning to optimise detection models for each deployment. That means we define a search space of model configurations, evaluate each against your validation data, and select the combination that maximises detection while minimising false positives for your specific alert volume. It's not a one-size-fits-all model — it's a tuned model that reflects your operational reality."
