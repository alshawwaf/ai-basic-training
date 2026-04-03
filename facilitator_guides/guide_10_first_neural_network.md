# Facilitator Guide — Session 3.1: First Neural Network in Keras

> **Stage:** 3  |  **Week:** 8  |  **Lecture deck:** `Lecture-10-First-Neural-Network.pptx`  |  **Total time:** 60 min

---

## Pre-Session Checklist

- [ ] Reviewed the lecture slides and all 4 exercise guides
- [ ] Confirmed Keras/TensorFlow installs work on participant machines — run a quick `import tensorflow as tf; print(tf.__version__)` test
- [ ] Prepared a whiteboard diagram of a 3-layer network (input → hidden → output) with neuron counts labelled
- [ ] Run through the compile-and-train exercise — confirmed the loss curve plots correctly and training completes in under 30 seconds

---

## Session Flow

| Time | Section | Activity |
|------|---------|----------|
| 0:00 – 0:05 | Recap | Quick: "In Stage 2 we used sklearn for everything. Today we add a new tool — Keras. Why do we need a second framework?" Let participants speculate before revealing the answer: neural networks need gradient-based training that sklearn doesn't provide. |
| 0:05 – 0:15 | Network architecture | Draw a 3-layer network on the whiteboard: input layer (number of features), hidden layer (e.g., 64 neurons), output layer (1 neuron for binary, N for multi-class). Label weights on the arrows. Explain: "Every arrow is a number the model learns." |
| 0:15 – 0:25 | Define → Compile → Train | Walk through the three-step Keras workflow. Define = choose layers and sizes. Compile = pick optimiser, loss function, and metrics. Train = feed data with `model.fit()`. Relate each step to something they already know from sklearn: define ≈ choosing the model class, compile ≈ setting hyperparameters, train ≈ `.fit()`. |
| 0:25 – 0:35 | Loss curves | Show a live training run and project the loss curve. Explain: "The curve tells you whether the model is still learning. Flat = done. Going up = something is wrong." Briefly compare training loss vs validation loss — full treatment comes in Session 3.2. |
| 0:35 – 0:50 | Hands-on exercises | Participants work through Exercises 1-4: from numpy to keras, build the network, compile and train, evaluate and improve. Circulate and help — environment issues are most common in this session. |
| 0:50 – 0:55 | sklearn vs Keras comparison | Facilitate a group discussion: "When would you still use sklearn? When do you reach for Keras?" Build a quick comparison on the whiteboard — sklearn for tabular/classical ML, Keras when you need deep learning, custom architectures, or GPU acceleration. |
| 0:55 – 1:00 | Wrap-up | Summarise: "You've built your first neural network. It's not magic — it's layers of simple maths. Next session we tackle the biggest risk: overfitting, and the tools to fight it." |

---

## Key Points to Emphasise

1. **A neural network is just layers of weighted sums plus activation functions** — strip away the hype and a single hidden-layer network is a sequence of matrix multiplications followed by non-linear squashing. Participants who understood linear and logistic regression already grasp the building blocks. Reinforce this continuity.
2. **Define → Compile → Train is the universal Keras workflow** — every neural network they will ever build in Keras follows the same three steps. Nail this rhythm now and every subsequent session becomes easier. If participants remember nothing else, they should remember this sequence.
3. **The loss curve is your first diagnostic tool** — before looking at accuracy, precision, or recall, look at the loss curve. A curve that plateaus early means the model has limited capacity. A curve that diverges between train and validation means overfitting. Reading loss curves is a skill they will use in every future session.

---

## Discussion Prompts

- "You have a tabular dataset of firewall logs with 15 features. Would you reach for a decision tree or a neural network first? What would change your answer?"
- "The network has 64 neurons in the hidden layer. What happens if you use 4? What about 4096? How would you decide?"
- "Your model's training loss drops to near zero but validation loss stays high. What does this tell you, and what would you try next?"

---

## Common Questions and Answers

**Q: Why can't I just use sklearn for neural networks?**
A: sklearn has a basic `MLPClassifier`, but it lacks GPU support, fine-grained layer control, and the ecosystem for deep learning (custom layers, callbacks, pre-trained models). Keras gives you the flexibility to build architectures that sklearn simply cannot express — and for the deep learning sessions ahead, that flexibility is essential.

**Q: How do I know how many neurons or layers to use?**
A: There is no formula. Start simple — one hidden layer with a number of neurons between the input size and the output size. Train, evaluate, then adjust. Exercise 4 walks through this iterative process. In practice, architecture search (covered in Session 3.4) can help automate the decision.

**Q: What is an "epoch" and how many should I use?**
A: One epoch means the model has seen every training sample once. More epochs give the model more chances to learn, but too many lead to overfitting. Watch the loss curve: when validation loss stops decreasing, you've trained long enough. Early stopping (covered in Session 3.2) automates this decision.

---

## Facilitator Notes

- This is the first session using Keras/TensorFlow. Budget extra time for environment issues — GPU drivers, version mismatches, and import errors are common. Having a pre-configured fallback environment (e.g., Google Colab link) ready can save the session.
- Exercise 1 (from numpy to keras) bridges the gap from manual computation to the Keras API. Do not skip it — participants who see the numpy version first understand that Keras is automating steps they already know, not performing magic.
- The loss curve in Exercise 3 is the visual anchor for this session. Project it on screen and annotate it live: "Here the model is learning fast. Here it slows down. Here it has converged." This builds the intuition needed for every subsequent neural network session.
- Some participants may ask about activation functions. Keep it brief: "ReLU for hidden layers, sigmoid for binary output, softmax for multi-class. We'll explore why in later sessions — for now, treat these as defaults."

---

## Connections to Sales Conversations

- **When a customer asks:** "Why does your product use neural networks instead of simpler models?"
- **You can now say:** "We use the right model for the right job. For structured log data with clear features, classical models like decision trees are fast, interpretable, and effective. But for complex patterns — like correlating dozens of signals across network sessions, or classifying file behaviour — neural networks can capture relationships that simpler models miss. The key is that we understand both approaches and choose based on the problem, not the hype. I can walk you through how a basic neural network works in under five minutes."
