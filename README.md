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

Each lesson is a pair of files that live side by side in the module folder:

| File | Role |
|------|------|
| `N_topic_name.md` | **Read this first.** Explains the concept in plain English with analogies and security context. No code. |
| `N_topic_name.py` | **Run this.** Working code with inline comments that map directly back to the notes. |

**The recommended flow for every lesson:**

1. Read the `.md` file — understand the concept before touching code
2. Run the `.py` script — observe the output and printed explanations
3. Change one value or parameter — see what breaks or improves
4. Re-read the section of the notes that relates to what you changed
5. Move on when the output makes sense to you

You don't need to understand every line of code before moving forward. The goal is to build intuition — deep understanding comes from repetition across modules.

---

## Module 1 — Classic Machine Learning

> **Goal:** Understand how machines learn from labelled data, and build your first working classifiers.

Classic ML is the foundation everything else builds on. These algorithms are still widely used in production security tooling because they are fast, interpretable, and require far less data than neural networks. You will build a real phishing detector by the end of this module.

| # | Concept Notes | Python Script | What You Learn |
|---|---------------|---------------|----------------|
| 1.1 | [What is ML?](module1_classic_ml/lesson1_what_is_ml/1_what_is_ml.md) | [1_concepts_and_data.py](module1_classic_ml/lesson1_what_is_ml/1_concepts_and_data.py) | The ML workflow, how models learn from data, loading and exploring a dataset |
| 1.2 | [Linear Regression](module1_classic_ml/lesson2_linear_regression/2_linear_regression.md) | [2_linear_regression.py](module1_classic_ml/lesson2_linear_regression/2_linear_regression.py) | Predicting continuous values — server response time from traffic load |
| 1.3 | [Logistic Regression](module1_classic_ml/lesson3_logistic_regression/3_logistic_regression.md) | [3_logistic_regression.py](module1_classic_ml/lesson3_logistic_regression/3_logistic_regression.py) | Binary classification — URL features → phishing or legitimate |
| 1.4 | [Decision Trees](module1_classic_ml/lesson4_decision_trees/4_decision_trees.md) | [4_decision_tree.py](module1_classic_ml/lesson4_decision_trees/4_decision_tree.py) | Interpretable rule-based classification — network traffic labelled as threat or benign |
| 1.5 | [Model Evaluation](module1_classic_ml/lesson5_model_evaluation/5_model_evaluation.md) | [5_model_evaluation.py](module1_classic_ml/lesson5_model_evaluation/5_model_evaluation.py) | Precision, recall, F1-score, ROC AUC — and why accuracy alone is meaningless in security |
| — | **Milestone Project** | [milestone_phishing.py](module1_classic_ml/milestone/milestone_phishing.py) | End-to-end phishing URL classifier: feature extraction → training → evaluation |

**Key concepts covered:** supervised learning, features and labels, train/test split, underfitting, decision boundaries, confusion matrix, false positive rate

---

## Module 2 — Intermediate ML

> **Goal:** Handle real-world, messy data — build stronger models and detect threats without any labels.

Real security data is never clean. Logs have missing fields, features need to be engineered, and many of the most interesting problems have no labelled ground truth at all. This module covers the techniques used in real SOC tooling.

| # | Concept Notes | Python Script | What You Learn |
|---|---------------|---------------|----------------|
| 2.1 | [Feature Engineering](module2_intermediate/lesson1_feature_engineering/1_feature_engineering.md) | [1_feature_engineering.py](module2_intermediate/lesson1_feature_engineering/1_feature_engineering.py) | Extracting useful signals from raw firewall and NetFlow logs |
| 2.2 | [Random Forests](module2_intermediate/lesson2_random_forests/2_random_forests.md) | [2_random_forest.py](module2_intermediate/lesson2_random_forests/2_random_forest.py) | Ensemble of decision trees — malware vs. benign file classifier |
| 2.3 | [Clustering & Anomaly Detection](module2_intermediate/lesson3_clustering_anomaly/3_clustering_anomaly_detection.md) | [3_clustering.py](module2_intermediate/lesson3_clustering_anomaly/3_clustering.py) | k-Means clustering to find anomalous network connections without any labels |
| 2.4 | [Overfitting & Cross-Validation](module2_intermediate/lesson4_overfitting_crossval/4_overfitting_cross_validation.md) | [4_overfitting.py](module2_intermediate/lesson4_overfitting_crossval/4_overfitting.py) | Why models fail in production, k-fold cross-validation, the bias-variance tradeoff |
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

| # | Concept Notes | Python Script | What You Learn |
|---|---------------|---------------|----------------|
| 3.9 | [First Neural Network](module3_neural_networks/lesson9_first_neural_network/9_first_neural_network.md) | [1_first_neural_net.py](module3_neural_networks/lesson9_first_neural_network/1_first_neural_net.py) | Rebuild the same network in Keras in ~10 lines |
| 3.10 | [Dropout & Regularisation](module3_neural_networks/lesson10_dropout_regularisation/10_dropout_and_regularisation.md) | [2_deeper_network.py](module3_neural_networks/lesson10_dropout_regularisation/2_deeper_network.py) | Dropout, batch normalisation, early stopping — keeping the model from memorising |
| 3.11 | [Convolutional Networks](module3_neural_networks/lesson11_convolutional_networks/11_convolutional_networks.md) | [3_cnn.py](module3_neural_networks/lesson11_convolutional_networks/3_cnn.py) | CNNs for spatial data — applied to malware binary visualisation |
| 3.12 | [Hyperparameter Tuning](module3_neural_networks/lesson12_hyperparameter_tuning/12_hyperparameter_tuning.md) | [4_hyperparameters.py](module3_neural_networks/lesson12_hyperparameter_tuning/4_hyperparameters.py) | Learning rate, batch size, architecture choices — and how to search them systematically |
| — | **Milestone Project** | [milestone_packets.py](module3_neural_networks/milestone/milestone_packets.py) | Neural network trained on network packet feature vectors to classify malicious traffic |

**Key concepts covered:** forward pass, backpropagation (conceptual), gradient descent, activation functions, loss functions, regularisation, convolutional filters, pooling, epochs, batch size

---

## Module 4 — Generative AI

> **Goal:** Understand how large language models work, use pre-trained models, and build a RAG-based security assistant.

This module bridges traditional ML and modern AI. You will learn what an LLM actually is (not just how to call one), how to use open-source models from HuggingFace for security tasks, and how to build a grounded AI assistant that reasons over your own documents instead of hallucinating.

| # | Concept Notes | Python Script | What You Learn |
|---|---------------|---------------|----------------|
| 4.1 | [How LLMs Work](module4_genai/lesson1_how_llms_work/1_how_llms_work.md) | [1_llm_concepts.py](module4_genai/lesson1_how_llms_work/1_llm_concepts.py) | Tokenisation, embeddings, attention, and next-token prediction — explained without hype |
| 4.2 | [HuggingFace Models](module4_genai/lesson2_huggingface/2_huggingface_pretrained_models.md) | [2_huggingface.py](module4_genai/lesson2_huggingface/2_huggingface.py) | Zero-shot MITRE ATT&CK technique classification and named entity recognition on threat reports |
| 4.3 | [The LLM API](module4_genai/lesson3_llm_api/3_claude_api.md) | [3_claude_api.py](module4_genai/lesson3_llm_api/3_claude_api.py) | System prompts, conversation history, streaming — build a threat intelligence assistant |
| 4.4 | [Retrieval-Augmented Generation](module4_genai/lesson4_rag/4_retrieval_augmented_generation.md) | [4_rag.py](module4_genai/lesson4_rag/4_rag.py) | Ground AI responses in your own CVE and threat report documents — eliminate hallucination |
| — | **Milestone Project** | [milestone_security_assistant.py](module4_genai/milestone/milestone_security_assistant.py) | Interactive Q&A assistant over a knowledge base of CVEs, threat reports, and security runbooks |

**Multi-provider support:** All Module 4 scripts work with Claude, OpenAI, Gemini, or Ollama (local). The `llm_client.py` helper abstracts the provider — set whichever key or model you have and the code handles the rest. Ollama is a good option if you need to keep data local or don't want to sign up for a cloud service.

**Key concepts covered:** tokens and context windows, embeddings, cosine similarity, vector search, RAG pipeline, prompt engineering, system prompts, conversation state, hallucination and grounding

---

## Repository Structure

```
AI Basic Training/
│
├── assets/                         Diagrams embedded in lesson notes
│
├── module1_classic_ml/             Module 1 — Classic ML
│   ├── lesson1_what_is_ml/                    What is ML?
│   │   ├── 1_what_is_ml.md
│   │   └── 1_concepts_and_data.py
│   ├── lesson2_linear_regression/                    Linear Regression
│   │   ├── 2_linear_regression.md
│   │   └── 2_linear_regression.py
│   ├── lesson3_logistic_regression/                    Logistic Regression
│   │   ├── 3_logistic_regression.md
│   │   └── 3_logistic_regression.py
│   ├── lesson4_decision_trees/                    Decision Trees
│   │   ├── 4_decision_trees.md
│   │   └── 4_decision_tree.py
│   ├── lesson5_model_evaluation/                    Model Evaluation
│   │   ├── 5_model_evaluation.md
│   │   └── 5_model_evaluation.py
│   └── milestone/
│       └── milestone_phishing.py
│
├── module2_intermediate/           Module 2 — Intermediate ML
│   ├── lesson1/ — 1_feature_engineering.md / .py
│   ├── lesson2/ — 2_random_forests.md / .py
│   ├── lesson3/ — 3_clustering_anomaly_detection.md / .py
│   ├── lesson4/ — 4_overfitting_cross_validation.md / .py
│   └── milestone/ — milestone_intrusion.py
│
├── module3_neural_networks/        Module 3 — Neural Networks
│   ├── foundations/                NumPy network from scratch (Lessons 3.1–3.8)
│   │   ├── 1_basic_neuron.py
│   │   ├── 2_neuron_layer.py
│   │   ├── 3_dot_product.py
│   │   ├── 4_layers_as_classes.py
│   │   ├── 5_relu_activation.py
│   │   ├── 6_softmax_activation.py
│   │   ├── 7_cross_entropy_loss.py
│   │   └── 8_full_forward_pass.py
│   ├── lesson9_first_neural_network/  — 9_first_neural_network.md / 1_first_neural_net.py
│   ├── lesson10_dropout_regularisation/ — 10_dropout_and_regularisation.md / 2_deeper_network.py
│   ├── lesson11_convolutional_networks/ — 11_convolutional_networks.md / 3_cnn.py
│   ├── lesson12_hyperparameter_tuning/ — 12_hyperparameter_tuning.md / 4_hyperparameters.py
│   └── milestone/ — milestone_packets.py
│
├── module4_genai/                  Module 4 — Generative AI
│   ├── llm_client.py               Multi-provider LLM helper (Claude/OpenAI/Gemini/Ollama)
│   ├── lesson1/ — 1_how_llms_work.md / 1_llm_concepts.py
│   ├── lesson2/ — 2_huggingface_pretrained_models.md / 2_huggingface.py
│   ├── lesson3/ — 3_claude_api.md / 3_claude_api.py
│   ├── lesson4/ — 4_retrieval_augmented_generation.md / 4_rag.py
│   └── milestone/ — milestone_security_assistant.py
│
└── README.md                       You are here
```

---

## Learning Tips

**Work through modules in order.** Each one builds on the last. Module 3 will make much more sense if you understand loss functions from Module 2.

**Run before you read deeply.** See the output first, then go back to the notes. Real output gives the concept something to anchor to.

**Break things intentionally.** The best way to understand a parameter is to set it to an extreme value and see what happens. What happens if you set `max_depth=1` in a decision tree? What about `max_depth=100`?

**Focus on the shape of the output.** You don't need to understand every line of code. Ask yourself: what went in, what came out, and does that make sense given what the notes say the model does?

**The milestones are checkpoints, not the finish line.** If a milestone runs and produces reasonable output, you are ready to move on — even if you don't fully understand every detail.
