# AI Learning Journey
### From Classic Machine Learning to Generative AI — Built for Cybersecurity Professionals

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-Neural%20Networks-FF6F00?logo=tensorflow&logoColor=white)](https://www.tensorflow.org/)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-yellow)](https://huggingface.co/)

A hands-on, 4-week Python curriculum that takes you from your first ML model all the way to building a working AI-powered security assistant. Every lesson is grounded in a real cybersecurity scenario — because abstract examples don't help you think about your actual job.

---

## Table of Contents

- [What You Will Build](#what-you-will-build)
- [Who This Is For](#who-this-is-for)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [How Each Lesson Works](#how-each-lesson-works)
- [Module 1 — Classic Machine Learning](#module-1--classic-machine-learning)
- [Module 2 — Intermediate ML](#module-2--intermediate-ml)
- [Module 3 — Neural Networks](#module-3--neural-networks)
- [Module 4 — Generative AI](#module-4--generative-ai)
- [Repository Structure](#repository-structure)
- [Learning Tips](#learning-tips)

---

## What You Will Build

Each module culminates in a milestone project — a complete, working application you can run end-to-end.

| Module | Milestone Project | What It Does |
|--------|------------------|--------------|
| 1 — Classic ML | **Phishing URL Classifier** | Detects malicious URLs based on structural features alone — no external lookup required |
| 2 — Intermediate ML | **Network Intrusion Detector** | Classifies KDD Cup-style connection records into attack categories vs. normal traffic |
| 3 — Neural Networks | **Malicious Packet Classifier** | Deep learning model trained on network traffic feature vectors |
| 4 — Generative AI | **Security Analyst Assistant** | Conversational AI that answers questions about CVEs and threat reports using RAG |

---

## Who This Is For

This curriculum is designed for **security professionals** who want to understand and apply AI/ML without switching careers.

You will get the most out of this if you:
- Write Python regularly (scripts, automation, tooling)
- Work in a security-adjacent role — SOC analyst, threat intel, red team, incident response, or similar
- Want to understand what AI tools are actually doing under the hood, not just how to call an API
- Have no prior ML or data science background

---

## Prerequisites

**Required:**
- Python 3.10 or higher
- Comfort with Python basics: loops, functions, classes, list comprehensions
- A terminal / command prompt

**Not required:**
- Prior ML, statistics, or data science experience
- Mathematics beyond basic algebra
- Any specific security certification or role

---

## Setup

### 1. Create a Virtual Environment

Always work inside a virtual environment — it keeps this project's packages isolated from the rest of your system and prevents version conflicts.

```bash
# Create the environment (one-time)
python -m venv venv

# Activate it — Windows
venv\Scripts\activate

# Activate it — Mac / Linux
source venv/bin/activate
```

Your terminal prompt will change to show `(venv)` when it's active. **All pip installs below must be run with the environment active.**

To deactivate when you're done for the day:
```bash
deactivate
```

### 2. Install Dependencies

Install packages per module as you reach them, or install everything upfront:

```bash
# Module 1 & 2 — Classic and Intermediate ML
pip install pandas scikit-learn matplotlib seaborn

# Module 3 — Neural Networks
pip install tensorflow nnfs

# Module 4 — Generative AI
pip install transformers sentence-transformers anthropic openai google-generativeai ollama
```

### API Key (Module 4 Only)

Module 4 connects to a live LLM. You need an API key from **one** of the following providers — the scripts auto-detect whichever key you have set, so no code changes are needed.

| Provider | Environment Variable | Where to Get It | Notes |
|----------|---------------------|-----------------|-------|
| Claude (Anthropic) | `ANTHROPIC_API_KEY` | [console.anthropic.com](https://console.anthropic.com) | Best quality responses |
| OpenAI | `OPENAI_API_KEY` | [platform.openai.com](https://platform.openai.com) | GPT-4o-mini used by default |
| Gemini (Google) | `GOOGLE_API_KEY` | [aistudio.google.com](https://aistudio.google.com) | Free tier available |
| Ollama (local) | `OLLAMA_MODEL=huihui_ai/qwen3.5-abliterated:2B` | [ollama.com](https://ollama.com) | Runs on your machine — no key, no internet, no cost |

**Set your key (or model name for Ollama):**

```bash
# Windows
set ANTHROPIC_API_KEY=your-key-here   # Claude
set OLLAMA_MODEL=huihui_ai/qwen3.5-abliterated:2B               # Ollama (no key — just install Ollama and pull a model)

# Mac / Linux
export ANTHROPIC_API_KEY=your-key-here
export OLLAMA_MODEL=huihui_ai/qwen3.5-abliterated:2B
```

> The `llm_client.py` helper in Module 4 handles provider selection automatically. Priority order: Claude → OpenAI → Gemini → Ollama. Set whichever you have — no code changes needed.

---

## How Each Lesson Works

Each lesson has three parts:

| File / Folder | Role |
|---------------|------|
| `N_topic_name.md` | **Read this first.** Explains the concept in plain English with analogies and security context. No code. Ends with a link to the workshop. |
| `workshop/` | **Do this next.** A guided set of exercises you complete yourself. Each exercise has its own `.md` guide and `.py` scaffold with `# >>> YOUR CODE HERE` markers. |
| `workshop/reference_solution.py` | **Open last.** Complete working implementation — compare against your own after finishing all exercises. |

**The recommended flow for every lesson:**

1. Read the `.md` theory file — understand the concept before touching code
2. Open `workshop/1_lab_guide.md` — read the exercise overview
3. For each exercise: read the `.md` guide, then fill in the `.py` file
4. Run the `.py` file after each task and verify your output matches the expected output
5. After all exercises pass, open `reference_solution.py` and compare your code
6. Move on when the output makes sense to you

**Running an exercise:**
```bash
# Activate your venv first, then from the repo root:
python module1_classic_ml/lesson1_what_is_ml/workshop/exercise1_loading_data.py
```

You don't need to understand every line before moving forward. The goal is to build intuition — deep understanding comes from repetition across modules.

---

## Module 1 — Classic Machine Learning

> **Goal:** Understand how machines learn from labelled data, and build your first working classifiers.

Classic ML is the foundation everything else builds on. These algorithms are still widely used in production security tooling because they are fast, interpretable, and require far less data than neural networks. You will build a real phishing detector by the end of this module.

| # | Theory | Workshop | What You Learn |
|---|--------|----------|----------------|
| 1.1 | [What is ML?](module1_classic_ml/lesson1_what_is_ml/1_what_is_ml.md) | [Workshop (5 exercises)](module1_classic_ml/lesson1_what_is_ml/workshop/1_lab_guide.md) | The ML workflow, loading and exploring a dataset, EDA, class balance |
| 1.2 | [Linear Regression](module1_classic_ml/lesson2_linear_regression/2_linear_regression.md) | [Workshop (4 exercises)](module1_classic_ml/lesson2_linear_regression/workshop/1_lab_guide.md) | Predicting continuous values — server response time from traffic load |
| 1.3 | [Logistic Regression](module1_classic_ml/lesson3_logistic_regression/3_logistic_regression.md) | [Workshop (4 exercises)](module1_classic_ml/lesson3_logistic_regression/workshop/1_lab_guide.md) | Binary classification — URL features → phishing or legitimate |
| 1.4 | [Decision Trees](module1_classic_ml/lesson4_decision_trees/4_decision_trees.md) | [Workshop (4 exercises)](module1_classic_ml/lesson4_decision_trees/workshop/1_lab_guide.md) | Interpretable rule-based classification — network traffic labelled as threat or benign |
| 1.5 | [Model Evaluation](module1_classic_ml/lesson5_model_evaluation/5_model_evaluation.md) | [Workshop (5 exercises)](module1_classic_ml/lesson5_model_evaluation/workshop/1_lab_guide.md) | Precision, recall, F1-score, ROC AUC — and why accuracy alone is meaningless in security |
| — | **Milestone Project** | [milestone_phishing.py](module1_classic_ml/milestone/milestone_phishing.py) | End-to-end phishing URL classifier: feature extraction → training → evaluation |

**Key concepts covered:** supervised learning, features and labels, train/test split, underfitting, decision boundaries, confusion matrix, false positive rate

---

## Module 2 — Intermediate ML

> **Goal:** Handle real-world, messy data — build stronger models and detect threats without any labels.

Real security data is never clean. Logs have missing fields, features need to be engineered, and many of the most interesting problems have no labelled ground truth at all. This module covers the techniques used in real SOC tooling.

| # | Theory | Workshop | What You Learn |
|---|--------|----------|----------------|
| 2.1 | [Feature Engineering](module2_intermediate/lesson1_feature_engineering/1_feature_engineering.md) | [Workshop (4 exercises)](module2_intermediate/lesson1_feature_engineering/workshop/1_lab_guide.md) | Extracting useful signals from raw firewall and NetFlow logs |
| 2.2 | [Random Forests](module2_intermediate/lesson2_random_forests/2_random_forests.md) | [Workshop (4 exercises)](module2_intermediate/lesson2_random_forests/workshop/1_lab_guide.md) | Ensemble of decision trees — malware vs. benign file classifier |
| 2.3 | [Clustering & Anomaly Detection](module2_intermediate/lesson3_clustering_anomaly/3_clustering_anomaly_detection.md) | [Workshop (4 exercises)](module2_intermediate/lesson3_clustering_anomaly/workshop/1_lab_guide.md) | k-Means clustering to find anomalous network connections without any labels |
| 2.4 | [Overfitting & Cross-Validation](module2_intermediate/lesson4_overfitting_crossval/4_overfitting_cross_validation.md) | [Workshop (4 exercises)](module2_intermediate/lesson4_overfitting_crossval/workshop/1_lab_guide.md) | Why models fail in production, k-fold cross-validation, the bias-variance tradeoff |
| — | **Milestone Project** | [milestone_intrusion.py](module2_intermediate/milestone/milestone_intrusion.py) | Network intrusion detector trained and evaluated on KDD Cup-style connection data |

**Key concepts covered:** one-hot encoding, normalisation, missing value handling, ensemble methods, feature importance, unsupervised learning, silhouette score, regularisation

---

## Module 3 — Neural Networks

> **Goal:** Build a neural network piece by piece — understand every layer before using a framework.

This module has two phases. The first eight lessons build a neural network using only NumPy, one component at a time: neurons, layers, activations, and loss functions. Once you have built it yourself, the second phase rebuilds it in Keras — now every Keras call maps to something you already understand.

### Phase 1 — Building the Network (NumPy Only)

These lessons work through the mathematics and mechanics of a neural network from first principles. No ML framework — just arrays and arithmetic.

| # | Script | What You Build |
|---|--------|----------------|
| 3.1 | [1_basic_neuron.py](module3_neural_networks/foundations/1_basic_neuron.py) | A single neuron: inputs × weights + bias |
| 3.2 | [2_neuron_layer.py](module3_neural_networks/foundations/2_neuron_layer.py) | Multiple neurons computing in parallel — a full layer |
| 3.3 | [3_dot_product.py](module3_neural_networks/foundations/3_dot_product.py) | Vectorising the computation with NumPy matrix multiplication |
| 3.4 | [4_layers_as_classes.py](module3_neural_networks/foundations/4_layers_as_classes.py) | Structuring layers as reusable Python objects |
| 3.5 | [5_relu_activation.py](module3_neural_networks/foundations/5_relu_activation.py) | Adding non-linearity so the network can learn complex patterns |
| 3.6 | [6_softmax_activation.py](module3_neural_networks/foundations/6_softmax_activation.py) | Converting raw outputs into a probability distribution |
| 3.7 | [7_cross_entropy_loss.py](module3_neural_networks/foundations/7_cross_entropy_loss.py) | Quantifying how wrong the model's predictions are |
| 3.8 | [8_full_forward_pass.py](module3_neural_networks/foundations/8_full_forward_pass.py) | Complete network: input → layers → activations → loss |

### Phase 2 — Keras and Real Security Data

| # | Theory | Workshop | What You Learn |
|---|--------|----------|----------------|
| 3.9 | [First Neural Network](module3_neural_networks/lesson9_first_neural_network/9_first_neural_network.md) | [Workshop (4 exercises)](module3_neural_networks/lesson9_first_neural_network/workshop/1_lab_guide.md) | Rebuild the same network in Keras in ~10 lines |
| 3.10 | [Dropout & Regularisation](module3_neural_networks/lesson10_dropout_regularisation/10_dropout_and_regularisation.md) | [Workshop (4 exercises)](module3_neural_networks/lesson10_dropout_regularisation/workshop/1_lab_guide.md) | Dropout, batch normalisation, early stopping — keeping the model from memorising |
| 3.11 | [Convolutional Networks](module3_neural_networks/lesson11_convolutional_networks/11_convolutional_networks.md) | [Workshop (4 exercises)](module3_neural_networks/lesson11_convolutional_networks/workshop/1_lab_guide.md) | CNNs for spatial data — applied to malware binary visualisation |
| 3.12 | [Hyperparameter Tuning](module3_neural_networks/lesson12_hyperparameter_tuning/12_hyperparameter_tuning.md) | [Workshop (4 exercises)](module3_neural_networks/lesson12_hyperparameter_tuning/workshop/1_lab_guide.md) | Learning rate, batch size, architecture choices — and how to search them systematically |
| — | **Milestone Project** | [milestone_packets.py](module3_neural_networks/milestone/milestone_packets.py) | Neural network trained on network packet feature vectors to classify malicious traffic |

**Key concepts covered:** forward pass, backpropagation (conceptual), gradient descent, activation functions, loss functions, regularisation, convolutional filters, pooling, epochs, batch size

---

## Module 4 — Generative AI

> **Goal:** Understand how large language models work, use pre-trained models, and build a RAG-based security assistant.

This module bridges traditional ML and modern AI. You will learn what an LLM actually is (not just how to call one), how to use open-source models from HuggingFace for security tasks, and how to build a grounded AI assistant that reasons over your own documents instead of hallucinating.

| # | Theory | Workshop | What You Learn |
|---|--------|----------|----------------|
| 4.1 | [How LLMs Work](module4_genai/lesson1_how_llms_work/1_how_llms_work.md) | [Workshop (3 exercises)](module4_genai/lesson1_how_llms_work/workshop/1_lab_guide.md) | Tokenisation, embeddings, attention — no API key required, pure NumPy |
| 4.2 | [HuggingFace Models](module4_genai/lesson2_huggingface/2_huggingface_pretrained_models.md) | [Workshop (3 exercises)](module4_genai/lesson2_huggingface/workshop/1_lab_guide.md) | Zero-shot classification, sentence embeddings, semantic search over security logs |
| 4.3 | [The LLM API](module4_genai/lesson3_llm_api/3_claude_api.md) | [Workshop (4 exercises)](module4_genai/lesson3_llm_api/workshop/1_lab_guide.md) | System prompts, structured JSON output, multi-turn conversation — threat intel assistant |
| 4.4 | [Retrieval-Augmented Generation](module4_genai/lesson4_rag/4_retrieval_augmented_generation.md) | [Workshop (3 exercises)](module4_genai/lesson4_rag/workshop/1_lab_guide.md) | Document chunking, vector retrieval, full RAG pipeline over security knowledge base |
| — | **Milestone Project** | [milestone_security_assistant.py](module4_genai/milestone/milestone_security_assistant.py) | Interactive Q&A assistant over a knowledge base of CVEs, threat reports, and security runbooks |

**Multi-provider support:** All Module 4 scripts work with Claude, OpenAI, Gemini, or Ollama (local). The `llm_client.py` helper abstracts the provider — set whichever key or model you have and the code handles the rest.

**Key concepts covered:** tokens and context windows, embeddings, cosine similarity, vector search, RAG pipeline, prompt engineering, system prompts, conversation state, hallucination and grounding

---

## Repository Structure

```
AI Basic Training/
│
├── assets/                         Diagrams embedded in lesson notes
│
├── module1_classic_ml/
│   ├── lesson1_what_is_ml/
│   │   ├── 1_what_is_ml.md             ← Theory (read first)
│   │   └── workshop/
│   │       ├── 1_lab_guide.md          ← Exercise overview
│   │       ├── exercise1_*.md          ← Per-exercise guide
│   │       ├── exercise1_*.py          ← Your code goes here
│   │       ├── exercise2_* ... 5_*     ← (repeated for each exercise)
│   │       └── reference_solution.py  ← Open after finishing
│   ├── lesson2_linear_regression/  (same structure, 4 exercises)
│   ├── lesson3_logistic_regression/ (same structure, 4 exercises)
│   ├── lesson4_decision_trees/     (same structure, 4 exercises)
│   ├── lesson5_model_evaluation/   (same structure, 5 exercises)
│   └── milestone/
│       └── milestone_phishing.py
│
├── module2_intermediate/
│   ├── lesson1_feature_engineering/    (4 exercises)
│   ├── lesson2_random_forests/         (4 exercises)
│   ├── lesson3_clustering_anomaly/     (4 exercises)
│   ├── lesson4_overfitting_crossval/   (4 exercises)
│   └── milestone/
│       └── milestone_intrusion.py
│
├── module3_neural_networks/
│   ├── foundations/                NumPy network from scratch (Lessons 3.1–3.8)
│   │   ├── 1_basic_neuron.py
│   │   ├── 2_neuron_layer.py
│   │   ├── 3_dot_product.py
│   │   ├── 4_layers_as_classes.py
│   │   ├── 5_relu_activation.py
│   │   ├── 6_softmax_activation.py
│   │   ├── 7_cross_entropy_loss.py
│   │   └── 8_full_forward_pass.py
│   ├── lesson9_first_neural_network/   (4 exercises)
│   ├── lesson10_dropout_regularisation/ (4 exercises)
│   ├── lesson11_convolutional_networks/ (4 exercises)
│   ├── lesson12_hyperparameter_tuning/ (4 exercises)
│   └── milestone/
│       └── milestone_packets.py
│
├── module4_genai/
│   ├── llm_client.py               Multi-provider LLM helper (Claude/OpenAI/Gemini/Ollama)
│   ├── lesson1_how_llms_work/      (3 exercises — no API key required)
│   ├── lesson2_huggingface/        (3 exercises — HuggingFace models)
│   ├── lesson3_llm_api/            (4 exercises — requires API key)
│   ├── lesson4_rag/                (3 exercises — requires API key for ex. 3)
│   └── milestone/
│       └── milestone_security_assistant.py
│
└── README.md                       You are here
```

---

## Learning Tips

**Work through modules in order.** Each one builds on the last. Module 3 will make much more sense if you understand loss functions from Module 2.

**Read the exercise `.md` before opening the `.py`.** The guide explains the concept and the exact API you need. The `.py` file gives you the task — the `.md` gives you the tools.

**Run after each task, not at the end.** The exercises are designed to give you output after every small step. Verify each one before moving on — a small error early becomes confusing output later.

**Break things intentionally.** The best way to understand a parameter is to set it to an extreme value and see what happens. What happens if you set `max_depth=1` in a decision tree? What about `max_depth=100`?

**The milestones are checkpoints, not the finish line.** If a milestone runs and produces reasonable output, you are ready to move on — even if you don't fully understand every detail.
