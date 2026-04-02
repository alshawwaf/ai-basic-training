# AI Basic Training

### A Hands-On Curriculum for Cybersecurity Professionals

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-Neural%20Networks-FF6F00?logo=tensorflow&logoColor=white)](https://www.tensorflow.org/)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-yellow)](https://huggingface.co/)
[![Claude API](https://img.shields.io/badge/Claude-API-cc785c)](https://docs.anthropic.com/)

---

This curriculum teaches AI and machine learning from the ground up, using **real cybersecurity scenarios** in every lesson. It starts with classic ML algorithms and progresses through neural networks to generative AI — the same trajectory the field itself followed.

Everything is self-paced. There are no deadlines, no quizzes, and no abstract toy datasets. Every exercise uses security data — phishing URLs, network traffic, threat reports, CVEs — so the skills transfer directly to your work.

**4 modules | 17 lessons | 67 exercises | 79 runnable files**

---

## Table of Contents

- [Learning Path](#learning-path)
- [Who This Is For](#who-this-is-for)
- [Prerequisites](#prerequisites)
- [Environment Setup](#environment-setup)
- [How Lessons Are Structured](#how-lessons-are-structured)
- [Module 1 — Classic Machine Learning](#module-1--classic-machine-learning)
- [Module 2 — Intermediate ML](#module-2--intermediate-ml)
- [Module 3 — Neural Networks](#module-3--neural-networks)
- [Module 4 — Generative AI](#module-4--generative-ai)
- [Repository Map](#repository-map)
- [Pacing Guide](#pacing-guide)
- [Tips for Success](#tips-for-success)

---

## Learning Path

The four modules follow a deliberate progression. Each one builds on the concepts and intuition developed in the previous stage.

```
Module 1                Module 2                Module 3                Module 4
Classic ML              Intermediate ML         Neural Networks         Generative AI
─────────────────────── ─────────────────────── ─────────────────────── ───────────────────────
 Supervised learning     Feature engineering     Neurons & layers        Tokenisation
 Linear regression       Random Forests          Activations & loss      Embeddings & attention
 Logistic regression     Clustering              Keras & CNNs            LLM APIs
 Decision trees          Cross-validation        Hyperparameter tuning   RAG pipelines
 Model evaluation        Anomaly detection       Regularisation          Prompt engineering
─────────────────────── ─────────────────────── ─────────────────────── ───────────────────────
       Milestone:              Milestone:              Milestone:              Milestone:
  Phishing Classifier   Intrusion Detector      Packet Classifier      Security Assistant
```

> Each module ends with a **milestone project** — a complete, working application you build from scratch and can run end-to-end.

---

## Who This Is For

This curriculum is designed for **Security Engineers and Security Architects** who want to understand and apply AI/ML — not just consume tools that happen to contain it.

You will get the most out of this if you:

- Design, build, or evaluate security controls and architectures
- Write Python regularly — automation, tooling, detection logic, integrations
- Want to understand what AI-powered security products are actually doing under the hood
- Need to make informed decisions about where ML fits (and where it doesn't) in your security stack
- Have **no prior ML or data science background**

This is not a data science bootcamp. It is a structured, technical introduction to the parts of AI/ML that matter most to people who design security systems, evaluate detection capabilities, and architect defences.

---

## Prerequisites

**Required:**

- Python 3.10 or higher
- Comfort with Python fundamentals — variables, loops, functions, classes, list comprehensions
- A terminal or command prompt you are comfortable working in

**Not required:**

- Prior ML, statistics, or data science experience
- Mathematics beyond basic algebra
- Any specific security certification

---

## Environment Setup

### Step 1 — Create a Virtual Environment

A virtual environment isolates this project's packages from the rest of your system and prevents version conflicts. All commands below assume you are inside the activated environment.

```bash
# Create the environment (one-time setup)
python -m venv venv        # Windows
python3 -m venv venv       # Mac / Linux

# Activate — Windows
venv\Scripts\activate

# Activate — Mac / Linux
source venv/bin/activate
```

> **Mac / Linux note:** On most Mac and Linux systems, the command is `python3`, not `python`. If `python --version` shows Python 2 or "command not found", use `python3` instead for all commands throughout this curriculum.

Your terminal prompt will show `(venv)` when the environment is active. To deactivate when you are done:

```bash
deactivate
```

### Step 2 — Install Dependencies

Each module tells you exactly what to install when you reach it. You do not need to install anything beyond the virtual environment right now — just start Module 1 and follow the instructions as you go.

---

## How Lessons Are Structured

Every lesson follows the same three-part structure:

```
notes.md                Read first — explains the concept in plain English with security context
  │
  └── workshop/
        ├── 00_overview.md         Exercise list and objectives
        ├── 01_guide_*.md          Concept guide for exercise 1
        ├── 01_lab_*.md            Step-by-step lab instructions
        ├── 01_solution_*.py       Reference solution (open last)
        ├── 02_guide_*.md          Exercise 2 ...
        ├── 02_lab_*.md
        ├── 02_solution_*.py
        └── ...
```

**Recommended workflow for each lesson:**

1. **Read** the theory (`notes.md`) — understand the concept before writing code
2. **Open** the workshop overview (`00_overview.md`) — see what you will build
3. **For each exercise:**
   - Read the **guide** — it explains the concept and the methods you need
   - Follow the **lab** — step-by-step instructions to build your script
   - Run your script and verify output matches expected results
   - Compare against the **solution** file when you are done
4. **Move on** when the output makes sense — deep understanding comes from repetition across modules

---

## Module 1 — Classic Machine Learning

> Understand how machines learn from labelled data, and build your first working classifiers.

Classic ML is the foundation everything else builds on. These algorithms are fast, interpretable, and still widely used in production security tooling — SIEM correlation rules, email filters, endpoint detection. You will build a real phishing detector by the end of this module.

| # | Lesson | Workshop | What You Learn |
|---|--------|----------|----------------|
| 1.1 | [What is ML?](module1_classic_ml/lesson1_what_is_ml/notes.md) | [5 exercises](module1_classic_ml/lesson1_what_is_ml/workshop/00_overview.md) | The ML workflow — loading data, exploring features, EDA, class balance |
| 1.2 | [Linear Regression](module1_classic_ml/lesson2_linear_regression/notes.md) | [4 exercises](module1_classic_ml/lesson2_linear_regression/workshop/00_overview.md) | Predicting continuous values — server response time from traffic load |
| 1.3 | [Logistic Regression](module1_classic_ml/lesson3_logistic_regression/notes.md) | [4 exercises](module1_classic_ml/lesson3_logistic_regression/workshop/00_overview.md) | Binary classification — phishing or legitimate from URL features |
| 1.4 | [Decision Trees](module1_classic_ml/lesson4_decision_trees/notes.md) | [4 exercises](module1_classic_ml/lesson4_decision_trees/workshop/00_overview.md) | Interpretable rule-based splits — network traffic as threat or benign |
| 1.5 | [Model Evaluation](module1_classic_ml/lesson5_model_evaluation/notes.md) | [5 exercises](module1_classic_ml/lesson5_model_evaluation/workshop/00_overview.md) | Precision, recall, F1, ROC AUC — why accuracy alone is meaningless in security |

**Milestone:** [Phishing URL Classifier](module1_classic_ml/milestone/milestone_phishing.py) — end-to-end pipeline from feature extraction through training to evaluation on a real phishing dataset.

<details>
<summary><strong>Key concepts in this module</strong></summary>

Supervised learning, features and labels, train/test split, underfitting, decision boundaries, confusion matrix, false positive rate, class imbalance, model selection
</details>

---

## Module 2 — Intermediate ML

> Handle real-world messy data — build stronger models and detect threats without any labels.

Real security data is never clean. Logs have missing fields, features need to be engineered from raw text, and many of the most interesting problems have no labelled ground truth at all. This module covers the techniques you will encounter in real SOC tooling and detection engineering.

| # | Lesson | Workshop | What You Learn |
|---|--------|----------|----------------|
| 2.1 | [Feature Engineering](module2_intermediate/lesson1_feature_engineering/notes.md) | [4 exercises](module2_intermediate/lesson1_feature_engineering/workshop/00_overview.md) | Extracting numerical signals from raw firewall and NetFlow logs |
| 2.2 | [Random Forests](module2_intermediate/lesson2_random_forests/notes.md) | [4 exercises](module2_intermediate/lesson2_random_forests/workshop/00_overview.md) | Ensemble of decision trees — malware vs. benign file classifier |
| 2.3 | [Clustering & Anomaly Detection](module2_intermediate/lesson3_clustering_anomaly/notes.md) | [4 exercises](module2_intermediate/lesson3_clustering_anomaly/workshop/00_overview.md) | K-Means to find anomalous network connections — no labels needed |
| 2.4 | [Overfitting & Cross-Validation](module2_intermediate/lesson4_overfitting_crossval/notes.md) | [4 exercises](module2_intermediate/lesson4_overfitting_crossval/workshop/00_overview.md) | Why models fail in production — k-fold CV, bias-variance tradeoff |

**Milestone:** [Network Intrusion Detector](module2_intermediate/milestone/milestone_intrusion.py) — full pipeline trained and evaluated on KDD Cup-style network connection data.

<details>
<summary><strong>Key concepts in this module</strong></summary>

One-hot encoding, normalisation, missing value handling, ensemble methods, feature importance, unsupervised learning, silhouette score, bias-variance tradeoff, regularisation
</details>

---

## Module 3 — Neural Networks

> Build a neural network piece by piece — understand every layer before using a framework.

This module has two phases. **Phase 1** builds a neural network using only NumPy — neurons, layers, activations, and loss functions implemented from scratch. **Phase 2** rebuilds it in Keras, so every framework call maps to something you already understand from first principles.

### Phase 1 — From Scratch with NumPy (Lessons 3.1–3.8)

No ML framework — just arrays and arithmetic. Each script builds one component and connects it to the last.

| # | Script | What You Build |
|---|--------|----------------|
| 3.1 | [1_basic_neuron.py](module3_neural_networks/foundations/1_basic_neuron.py) | A single neuron — inputs x weights + bias |
| 3.2 | [2_neuron_layer.py](module3_neural_networks/foundations/2_neuron_layer.py) | Multiple neurons computing in parallel — a full layer |
| 3.3 | [3_dot_product.py](module3_neural_networks/foundations/3_dot_product.py) | Vectorising computation with NumPy matrix multiplication |
| 3.4 | [4_layers_as_classes.py](module3_neural_networks/foundations/4_layers_as_classes.py) | Structuring layers as reusable Python objects |
| 3.5 | [5_relu_activation.py](module3_neural_networks/foundations/5_relu_activation.py) | ReLU — adding non-linearity so the network can learn complex patterns |
| 3.6 | [6_softmax_activation.py](module3_neural_networks/foundations/6_softmax_activation.py) | Softmax — converting raw outputs into a probability distribution |
| 3.7 | [7_cross_entropy_loss.py](module3_neural_networks/foundations/7_cross_entropy_loss.py) | Cross-entropy loss — quantifying how wrong the predictions are |
| 3.8 | [8_full_forward_pass.py](module3_neural_networks/foundations/8_full_forward_pass.py) | Complete forward pass — input through layers, activations, to loss |

### Phase 2 — Keras and Real Security Data (Lessons 3.9–3.12)

| # | Lesson | Workshop | What You Learn |
|---|--------|----------|----------------|
| 3.9 | [First Neural Network](module3_neural_networks/lesson9_first_neural_network/notes.md) | [4 exercises](module3_neural_networks/lesson9_first_neural_network/workshop/00_overview.md) | Rebuild the NumPy network in Keras in ~10 lines of code |
| 3.10 | [Dropout & Regularisation](module3_neural_networks/lesson10_dropout_regularisation/notes.md) | [4 exercises](module3_neural_networks/lesson10_dropout_regularisation/workshop/00_overview.md) | Dropout, batch normalisation, early stopping — prevent memorisation |
| 3.11 | [Convolutional Networks](module3_neural_networks/lesson11_convolutional_networks/notes.md) | [4 exercises](module3_neural_networks/lesson11_convolutional_networks/workshop/00_overview.md) | CNNs for spatial data — applied to malware binary visualisation |
| 3.12 | [Hyperparameter Tuning](module3_neural_networks/lesson12_hyperparameter_tuning/notes.md) | [4 exercises](module3_neural_networks/lesson12_hyperparameter_tuning/workshop/00_overview.md) | Learning rate, batch size, architecture — systematic search |

**Milestone:** [Malicious Packet Classifier](module3_neural_networks/milestone/milestone_packets.py) — neural network trained on network packet feature vectors to classify malicious traffic.

<details>
<summary><strong>Key concepts in this module</strong></summary>

Forward pass, backpropagation (conceptual), gradient descent, activation functions (ReLU, sigmoid, softmax), loss functions, dropout, batch normalisation, convolutional filters, pooling, epochs, batch size, learning rate
</details>

---

## Module 4 — Generative AI

> Understand how LLMs work, use pre-trained models, and build a RAG-based security assistant.

This module bridges traditional ML and modern AI. You will learn what an LLM actually is — not just how to call one — how to use open-source models from HuggingFace for security tasks, and how to build a grounded assistant that reasons over your own documents instead of hallucinating.

| # | Lesson | Workshop | What You Learn |
|---|--------|----------|----------------|
| 4.1 | [How LLMs Work](module4_genai/lesson1_how_llms_work/notes.md) | [3 exercises](module4_genai/lesson1_how_llms_work/workshop/00_overview.md) | Tokenisation, embeddings, attention — pure NumPy, no API key needed |
| 4.2 | [HuggingFace Models](module4_genai/lesson2_huggingface/notes.md) | [3 exercises](module4_genai/lesson2_huggingface/workshop/00_overview.md) | Zero-shot classification, sentence embeddings, semantic search |
| 4.3 | [The LLM API](module4_genai/lesson3_llm_api/notes.md) | [4 exercises](module4_genai/lesson3_llm_api/workshop/00_overview.md) | System prompts, structured JSON output, multi-turn conversation |
| 4.4 | [Retrieval-Augmented Generation](module4_genai/lesson4_rag/notes.md) | [3 exercises](module4_genai/lesson4_rag/workshop/00_overview.md) | Document chunking, vector retrieval, full RAG pipeline |

**Milestone:** [Security Analyst Assistant](module4_genai/milestone/milestone_security_assistant.py) — interactive Q&A over a knowledge base of CVEs, threat reports, and security runbooks.

> **Multi-provider support:** All Module 4 scripts work with Claude, OpenAI, Gemini, or Ollama. The [`llm_client.py`](module4_genai/llm_client.py) helper abstracts the provider — set whichever key you have.

<details>
<summary><strong>Key concepts in this module</strong></summary>

Tokens and context windows, embeddings, cosine similarity, vector search, RAG pipeline, prompt engineering, system prompts, conversation state, hallucination and grounding, structured output
</details>

---

## Repository Map

```
AI Basic Training/
│
├── module1_classic_ml/                          Module 1 — Classic ML (5 lessons)
│   ├── lesson1_what_is_ml/
│   │   ├── notes.md                                 Theory — read first
│   │   └── workshop/
│   │       ├── 00_overview.md                       Exercise overview
│   │       ├── 01_guide_*.md / 01_lab_*.md          Guide + lab for exercise 1
│   │       ├── 01_solution_*.py                     Reference solution
│   │       └── ...                                  (repeated per exercise)
│   ├── lesson2_linear_regression/                   Same structure — 4 exercises
│   ├── lesson3_logistic_regression/                 Same structure — 4 exercises
│   ├── lesson4_decision_trees/                      Same structure — 4 exercises
│   ├── lesson5_model_evaluation/                    Same structure — 5 exercises
│   └── milestone/
│       └── milestone_phishing.py
│
├── module2_intermediate/                        Module 2 — Intermediate ML (4 lessons)
│   ├── lesson1_feature_engineering/                 4 exercises
│   ├── lesson2_random_forests/                      4 exercises
│   ├── lesson3_clustering_anomaly/                  4 exercises
│   ├── lesson4_overfitting_crossval/                4 exercises
│   └── milestone/
│       └── milestone_intrusion.py
│
├── module3_neural_networks/                     Module 3 — Neural Networks (12 lessons)
│   ├── foundations/                                  Lessons 3.1–3.8 (NumPy from scratch)
│   │   ├── 1_basic_neuron.py
│   │   ├── 2_neuron_layer.py
│   │   ├── ...
│   │   └── 8_full_forward_pass.py
│   ├── lesson9_first_neural_network/                4 exercises
│   ├── lesson10_dropout_regularisation/             4 exercises
│   ├── lesson11_convolutional_networks/             4 exercises
│   ├── lesson12_hyperparameter_tuning/              4 exercises
│   └── milestone/
│       └── milestone_packets.py
│
├── module4_genai/                               Module 4 — Generative AI (4 lessons)
│   ├── llm_client.py                                Multi-provider LLM helper
│   ├── lesson1_how_llms_work/                       3 exercises
│   ├── lesson2_huggingface/                         3 exercises
│   ├── lesson3_llm_api/                             4 exercises
│   ├── lesson4_rag/                                 3 exercises
│   └── milestone/
│       └── milestone_security_assistant.py
│
├── assets/                                      Diagrams embedded in lesson notes
└── README.md                                    This file
```

---

## Pacing Guide

There are no deadlines. Each lesson is self-contained enough to pause and resume without losing context.

| Pace | Daily commitment | Approximate timeline |
|------|-----------------|---------------------|
| Intensive | 6–8 hours/day | ~2 weeks |
| Evenings | 1–2 hours/day | 6–8 weeks |
| Weekends | 3–4 hours/weekend | 3–4 months |

Aim for consistency over speed. Completing one exercise per session is better than rushing through an entire module and retaining nothing.

---

## Tips for Success

**Work through modules in order.** Each one builds on the last. Module 3 assumes you understand loss and evaluation from Modules 1–2. Module 4 assumes you understand embeddings from Module 3.

**Read the theory before writing code.** The `notes.md` file for each lesson explains the concept, the intuition, and the security context. Skipping it means you will be copying code without understanding why it works.

**Run your code after every step.** The exercises are designed to produce output at each stage. Verify each result before moving on — a small mistake early compounds into confusing output later.

**Break things on purpose.** The best way to understand a parameter is to push it to an extreme. Set `max_depth=1` on a decision tree. Set the learning rate to `10.0`. Watch what happens. That intuition is worth more than any explanation.

**Use the solutions as a reference, not a shortcut.** Try each exercise yourself first, even if you get stuck. The struggle is where learning happens. Check the solution file only after you have a working (or broken) attempt of your own.

**The milestones are checkpoints, not exams.** If a milestone script runs and produces reasonable output, you have the understanding you need to continue. You do not need to master every detail before moving forward.
