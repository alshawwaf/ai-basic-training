# Facilitator Guide — Session 3.2: Dropout & Regularisation

> **Stage:** 3  |  **Week:** 9  |  **Lecture deck:** `Lecture-11-Dropout-Regularisation.pptx`  |  **Total time:** 60 min

---

## Pre-Session Checklist

- [ ] Reviewed the lecture slides and all 4 exercise guides
- [ ] Prepared a whiteboard sketch of a network with neurons crossed out (dropout visual) — participants need to see neurons disappearing
- [ ] Run through the overfitting demonstration exercise — confirmed the train/validation loss divergence is clearly visible in the plot
- [ ] Reviewed the three techniques (dropout, batch normalisation, early stopping) — be ready to explain when to use each

---

## Session Flow

| Time | Section | Activity |
|------|---------|----------|
| 0:00 – 0:05 | Recap | Quick: "Last session your model's training loss dropped to near zero. Was that a good thing?" Let participants recall the train vs validation gap from Session 3.1. Bridge into: "Today we learn why that gap appears and three tools to close it." |
| 0:05 – 0:15 | Demonstrate overfitting | Walk through Exercise 1 live. Train a network that clearly overfits: training accuracy climbs while validation accuracy stalls or drops. Project the loss curves side by side. Ask: "Would you deploy this model to your SOC?" |
| 0:15 – 0:25 | Dropout — the visual | Draw a network on the whiteboard. Randomly cross out neurons with a marker. Explain: "During each training step, Keras randomly disables a fraction of neurons. The network can't rely on any single neuron, so it learns redundant representations." Connect to security: "It's like cross-training your SOC team — if one analyst is out, the team still functions." |
| 0:25 – 0:35 | Batch normalisation and early stopping | Briefly explain batch normalisation: "It standardises the inputs to each layer, which stabilises and speeds up training." Then early stopping: "Stop training when validation loss stops improving — don't let the model keep memorising." Show the comparison chart from the slides. |
| 0:35 – 0:50 | Hands-on exercises | Participants work through Exercises 2-4: add dropout, batch normalisation, early stopping. Exercise 1 (overfitting demo) was done live — participants can revisit. Circulate and help participants compare their loss curves with and without regularisation. |
| 0:50 – 0:55 | Comparison discussion | Facilitate: "Which technique made the biggest difference? Can you combine them? When would you use one over another?" Build a quick reference on the whiteboard summarising all three techniques with their trade-offs. |
| 0:55 – 1:00 | Wrap-up | Summarise: "Overfitting is the silent failure of neural networks — the model looks great on paper but fails in production. Dropout, batch norm, and early stopping are your defences. Next session: convolutional networks for image and binary data." |

---

## Key Points to Emphasise

1. **Overfitting is the number one failure mode in production security models** — a model that memorises training data will miss new attack variants it has never seen. Every new malware family, every novel phishing technique becomes a blind spot. Regularisation is not optional; it is the difference between a lab demo and a production system.
2. **Dropout forces the network to learn robust features** — by randomly disabling neurons during training, dropout prevents the network from relying on fragile, co-adapted patterns. The result is a model that generalises better to unseen data. A 0.2–0.5 dropout rate is a common starting point.
3. **Early stopping is the simplest and most underused technique** — it costs nothing to implement, adds no complexity to the model, and prevents wasted training time. Monitor validation loss and stop when it stops improving. In production pipelines, early stopping should be the default, not an afterthought.

---

## Discussion Prompts

- "You train a phishing detection model on last year's phishing campaigns. It scores 98% on that data. A new phishing campaign launches next month with different tactics. What happens to your model's performance? How does regularisation help?"
- "Dropout rate of 0.5 means half the neurons are disabled each step. What happens if you set it to 0.9? What about 0.01? Where's the sweet spot?"
- "Your model uses dropout, batch normalisation, and early stopping — but it's still overfitting. What else could be going wrong? (Hint: think about the data itself.)"

---

## Common Questions and Answers

**Q: If dropout disables neurons randomly, doesn't that make the model worse?**
A: Only during training. At inference time, all neurons are active — but their outputs are scaled down to compensate. The effect is that the network learns multiple redundant pathways to the same answer, making it more robust. Think of it as training with intentional handicaps so the full team performs better on game day.

**Q: Can I use all three techniques together?**
A: Yes, and it is common to do so. A typical setup is: batch normalisation after each dense layer, dropout after batch norm, and early stopping monitoring validation loss. They address different aspects of the problem — batch norm stabilises training, dropout prevents co-adaptation, and early stopping prevents training too long.

**Q: How do I know if my model is overfitting?**
A: Compare training metrics to validation metrics. If training loss is much lower than validation loss, or training accuracy is much higher than validation accuracy, the model is overfitting. The gap between the two curves is your overfitting signal. Exercise 1 makes this visually obvious — the curves diverge like an opening pair of scissors.

---

## Facilitator Notes

- The overfitting demonstration (Exercise 1) is the emotional anchor. Make the divergence between train and validation loss as dramatic as possible — use a small dataset and a large network to exaggerate the effect. When participants see the gap, the concept clicks permanently.
- The dropout visual on the whiteboard is critical. Physically crossing out neurons with a marker makes the abstract concept tangible. After drawing it, ask a participant to explain back what is happening — this confirms understanding.
- Batch normalisation is the most technically dense topic in this session. Keep the explanation at the intuition level: "It re-centres and re-scales the data flowing through each layer." If participants want the maths, point them to the original paper (Ioffe & Szegedy, 2015), but do not derail the session with formulas.
- Some participants may conflate regularisation with data augmentation. Clarify: "Regularisation constrains the model. Data augmentation increases the diversity of training data. Both fight overfitting, but they work differently."

---

## Connections to Sales Conversations

- **When a customer asks:** "How do you ensure your detection models work on threats they haven't seen before?"
- **You can now say:** "Generalisation is the core challenge in security ML — attacks evolve constantly, so a model that only memorises known threats is useless against the next campaign. We apply multiple regularisation techniques during training: dropout to prevent the model from relying on fragile patterns, batch normalisation to stabilise learning, and early stopping to prevent overtraining. The result is a model that captures the underlying structure of malicious behaviour, not just the specific samples it trained on. That's how we maintain detection rates as threats evolve."
