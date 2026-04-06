# AI Basic Training — Ninja Program

### A Hands-On AI Curriculum for Security Architects and Engineers

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-Neural%20Networks-FF6F00?logo=tensorflow&logoColor=white)](https://www.tensorflow.org/)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-yellow)](https://huggingface.co/)

---

This curriculum teaches AI and machine learning from the ground up, using **real cybersecurity scenarios** in every lesson. It is the technical core of the **AI Ninja Program** — a selective, cohort-based training program for security architects and engineers across the Americas.

The program starts with AI positioning for customer conversations, progresses through classic ML algorithms and neural networks, builds a RAG-based security assistant, and culminates with hands-on mastery of Check Point's AI Security product suite.

**6 stages | 21 sessions | 67 exercises | 4 capstone projects | 3-tier certification**

### Quick Start

```bash
docker-compose up --build        # start the portal at http://localhost:5000
```

### Program Documents

| Document | Description |
|----------|-------------|
| [Program Syllabus](docs/PROGRAM_SYLLABUS.md) | 15-week schedule, tier system, assessment gates, participant expectations |
| [Ninja Program Blueprint](docs/NINJA_PROGRAM_BLUEPRINT.md) | Strategic plan, recommendations, and success metrics |
| [Facilitator Guides](ops/facilitator_guides/) | Teacher notes template and per-lecture delivery guides |
| [Assessments](ops/assessments/) | Quiz, challenge, review, and capstone rubrics per stage gate |
| [Security Corpus](curriculum/stage4_genai/data/) | 31 curated documents: CVEs, threat actors, runbooks, detection guides, and Check Point AI products |
| [Customer Demo Kit](ops/demo_kit/) | Packaged demo assistant, presentation script, architecture one-pager |
| [Program Operations](ops/program_ops/) | Welcome packet, recruitment pitch, skills survey, certificates, dry-run checklist |

---

## Table of Contents

- [Learning Path](#learning-path)
- [Who This Is For](#who-this-is-for)
- [Prerequisites](#prerequisites)
- [Environment Setup](#environment-setup)
- [How Lessons Are Structured](#how-lessons-are-structured)
- [Stage 0 — AI for Security Positioning](#stage-0--ai-for-security-positioning)
- [Stage 1 — Classic Machine Learning](#stage-1--classic-machine-learning)
- [Stage 2 — Intermediate ML](#stage-2--intermediate-ml)
- [Stage 3 — Neural Networks](#stage-3--neural-networks)
- [Stage 4 — Generative AI](#stage-4--generative-ai)
- [Stage 5 — Check Point AI Security](#stage-5--check-point-ai-security)
- [Repository Map](#repository-map)
- [Pacing Guide](#pacing-guide)
- [Tips for Success](#tips-for-success)

---

## Learning Path

The six stages follow a deliberate progression. Stage 0 builds your ability to discuss AI in sales and architecture contexts. Stages 1-4 build progressively deeper technical skill. Stage 5 connects everything to Check Point's AI Security products.

| | Stage 0 — Positioning | Stage 1 — Classic ML | Stage 2 — Intermediate ML | Stage 3 — Neural Networks | Stage 4 — Generative AI | Stage 5 — CP AI Security |
|---|---|---|---|---|---|---|
| **Topics** | AI landscape | Supervised learning | Feature engineering | Neurons & layers | Tokenisation | Workforce AI Security |
| | Competitor analysis | Linear regression | Random Forests | Activations & loss | Embeddings & attention | AI Agent Security + MCP |
| | Objection handling | Logistic regression | Clustering | Keras & CNNs | LLM APIs | AI Guardrails |
| | Discovery questions | Decision trees | Cross-validation | Hyperparameter tuning | RAG pipelines | Positioning & demos |
| | | Model evaluation | Anomaly detection | Regularisation | Prompt engineering | |
| **Project** | — | Phishing Classifier | Intrusion Detector | Packet Classifier | Security Assistant | Customer Demo |
| **Tier** | — | Tier 1: AI Foundations | Tier 1: AI Foundations | Tier 2: Practitioner | Tier 3: AI Ninja | Tier 3: AI Ninja |

> Stages 1-4 each end with a **capstone project**. Stage 5 connects your AI knowledge to Check Point's products and prepares you for customer-facing demos.

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

Each stage tells you exactly what to install when you reach it. You do not need to install anything beyond the virtual environment right now — just start Stage 1 and follow the instructions as you go.

---

## Stage 0 — AI for Security Positioning

> Learn how to talk about AI in cybersecurity — before writing a single line of code.

This stage is non-technical. It builds the vocabulary, market awareness, and conversational skill needed to discuss AI confidently with customers, partners, and internal stakeholders. Complete this before starting Stage 1.

| # | Session | Format | Time |
|---|---------|--------|------|
| 0.1 | [The AI Landscape in Cybersecurity](ops/stage0_positioning/01_ai_landscape/README.md) | Lecture + discussion | 60 min |
| 0.2 | [How Competitors Position AI](ops/stage0_positioning/02_competitor_analysis/README.md) | Lecture + group exercise | 60 min |
| 0.3 | [AI Objection Handling](ops/stage0_positioning/03_objection_handling/README.md) | Lecture + role-play | 60 min |
| 0.4 | [Discovery Questions for AI Use Cases](ops/stage0_positioning/04_discovery_questions/README.md) | Workshop | 60 min |

---

## How Lessons Are Structured

Every lesson follows the same three-part structure:

```
01_topic_name/
  ├── README.md                Theory + exercise overview — read first
  ├── 1_first_exercise/
  │   ├── lecture.md             Concept explanation
  │   ├── handson.md               Step-by-step instructions
  │   └── solution_*.py             Reference solution (open last)
  ├── 2_second_exercise/
  │   ├── lecture.md
  │   ├── handson.md
  │   └── solution_*.py
  └── ...
```

**Recommended workflow for each lesson:**

1. **Read** the theory (`README.md`) — understand the concept before writing code
2. **For each exercise folder:**
   - Read the **lecture** — it explains the concept and the methods you need
   - Follow the **handson** — step-by-step instructions to build your script
   - Run your script and verify output matches expected results
   - Compare against the **solution** file when you are done
3. **Move on** when the output makes sense — deep understanding comes from repetition across stages

---

## Stage 1 — Classic Machine Learning

> Understand how machines learn from labelled data, and build your first working classifiers.

Classic ML is the foundation everything else builds on. These algorithms are fast, interpretable, and still widely used in production security tooling — SIEM correlation rules, email filters, endpoint detection. You will build a real phishing detector by the end of this stage.

| # | Lesson | Exercises | What You Learn |
|---|--------|-----------|----------------|
| 1.1 | [What is ML?](curriculum/stage1_classic_ml/01_what_is_ml/README.md) | 5 | The ML workflow — loading data, exploring features, EDA, class balance |
| 1.2 | [Linear Regression](curriculum/stage1_classic_ml/02_linear_regression/README.md) | 4 | Predicting continuous values — server response time from traffic load |
| 1.3 | [Logistic Regression](curriculum/stage1_classic_ml/03_logistic_regression/README.md) | 4 | Binary classification — phishing or legitimate from URL features |
| 1.4 | [Decision Trees](curriculum/stage1_classic_ml/04_decision_trees/README.md) | 4 | Interpretable rule-based splits — network traffic as threat or benign |
| 1.5 | [Model Evaluation](curriculum/stage1_classic_ml/05_model_evaluation/README.md) | 5 | Precision, recall, F1, ROC AUC — why accuracy alone is meaningless in security |

**Project:** [Phishing URL Classifier](curriculum/stage1_classic_ml/project/phishing_detector.py) — end-to-end pipeline from feature extraction through training to evaluation on a real phishing dataset.

<details>
<summary><strong>Key concepts in this stage</strong></summary>

Supervised learning, features and labels, train/test split, underfitting, decision boundaries, confusion matrix, false positive rate, class imbalance, model selection
</details>

---

## Stage 2 — Intermediate ML

> Handle real-world messy data — build stronger models and detect threats without any labels.

Real security data is never clean. Logs have missing fields, features need to be engineered from raw text, and many of the most interesting problems have no labelled ground truth at all. This stage covers the techniques you will encounter in real SOC tooling and detection engineering.

| # | Lesson | Exercises | What You Learn |
|---|--------|-----------|----------------|
| 2.1 | [Feature Engineering](curriculum/stage2_intermediate/01_feature_engineering/README.md) | 4 | Extracting numerical signals from raw firewall and NetFlow logs |
| 2.2 | [Random Forests](curriculum/stage2_intermediate/02_random_forests/README.md) | 4 | Ensemble of decision trees — malware vs. benign file classifier |
| 2.3 | [Clustering & Anomaly Detection](curriculum/stage2_intermediate/03_clustering_anomaly/README.md) | 4 | K-Means to find anomalous network connections — no labels needed |
| 2.4 | [Overfitting & Cross-Validation](curriculum/stage2_intermediate/04_overfitting_crossval/README.md) | 4 | Why models fail in production — k-fold CV, bias-variance tradeoff |

**Project:** [Network Intrusion Detector](curriculum/stage2_intermediate/project/intrusion_detector.py) — full pipeline trained and evaluated on KDD Cup-style network connection data.

<details>
<summary><strong>Key concepts in this stage</strong></summary>

One-hot encoding, normalisation, missing value handling, ensemble methods, feature importance, unsupervised learning, silhouette score, bias-variance tradeoff, regularisation
</details>

---

## Stage 3 — Neural Networks

> Build a neural network piece by piece — understand every layer before using a framework.

This stage has two phases. **Phase 1** builds a neural network using only NumPy — neurons, layers, activations, and loss functions implemented from scratch. **Phase 2** rebuilds it in Keras, so every framework call maps to something you already understand from first principles.

### Phase 1 — From Scratch with NumPy (Lessons 3.1–3.8)

No ML framework — just arrays and arithmetic. Each script builds one component and connects it to the last.

| # | Script | What You Build |
|---|--------|----------------|
| 3.1 | [1_basic_neuron.py](curriculum/stage3_neural_networks/foundations/1_basic_neuron.py) | A single neuron — inputs x weights + bias |
| 3.2 | [2_neuron_layer.py](curriculum/stage3_neural_networks/foundations/2_neuron_layer.py) | Multiple neurons computing in parallel — a full layer |
| 3.3 | [3_dot_product.py](curriculum/stage3_neural_networks/foundations/3_dot_product.py) | Vectorising computation with NumPy matrix multiplication |
| 3.4 | [4_layers_as_classes.py](curriculum/stage3_neural_networks/foundations/4_layers_as_classes.py) | Structuring layers as reusable Python objects |
| 3.5 | [5_relu_activation.py](curriculum/stage3_neural_networks/foundations/5_relu_activation.py) | ReLU — adding non-linearity so the network can learn complex patterns |
| 3.6 | [6_softmax_activation.py](curriculum/stage3_neural_networks/foundations/6_softmax_activation.py) | Softmax — converting raw outputs into a probability distribution |
| 3.7 | [7_cross_entropy_loss.py](curriculum/stage3_neural_networks/foundations/7_cross_entropy_loss.py) | Cross-entropy loss — quantifying how wrong the predictions are |
| 3.8 | [8_full_forward_pass.py](curriculum/stage3_neural_networks/foundations/8_full_forward_pass.py) | Complete forward pass — input through layers, activations, to loss |

### Phase 2 — Keras and Real Security Data (Lessons 3.9–3.12)

| # | Lesson | Exercises | What You Learn |
|---|--------|-----------|----------------|
| 3.9 | [First Neural Network](curriculum/stage3_neural_networks/01_first_neural_network/README.md) | 4 | Rebuild the NumPy network in Keras in ~10 lines of code |
| 3.10 | [Dropout & Regularisation](curriculum/stage3_neural_networks/02_dropout_regularisation/README.md) | 4 | Dropout, batch normalisation, early stopping — prevent memorisation |
| 3.11 | [Convolutional Networks](curriculum/stage3_neural_networks/03_convolutional_networks/README.md) | 4 | CNNs for spatial data — applied to malware binary visualisation |
| 3.12 | [Hyperparameter Tuning](curriculum/stage3_neural_networks/04_hyperparameter_tuning/README.md) | 4 | Learning rate, batch size, architecture — systematic search |

**Project:** [Malicious Packet Classifier](curriculum/stage3_neural_networks/project/packet_classifier.py) — neural network trained on network packet feature vectors to classify malicious traffic.

<details>
<summary><strong>Key concepts in this stage</strong></summary>

Forward pass, backpropagation (conceptual), gradient descent, activation functions (ReLU, sigmoid, softmax), loss functions, dropout, batch normalisation, convolutional filters, pooling, epochs, batch size, learning rate
</details>

---

## Stage 4 — Generative AI

> Understand how LLMs work, use pre-trained models, and build a RAG-based security assistant.

This stage bridges traditional ML and modern AI. You will learn what an LLM actually is — not just how to call one — how to use open-source models from HuggingFace for security tasks, and how to build a grounded assistant that reasons over your own documents instead of hallucinating.

| # | Lesson | Exercises | What You Learn |
|---|--------|-----------|----------------|
| 4.1 | [How LLMs Work](curriculum/stage4_genai/01_how_llms_work/README.md) | 3 | Tokenisation, embeddings, attention — pure NumPy, no API key needed |
| 4.2 | [HuggingFace Models](curriculum/stage4_genai/02_huggingface/README.md) | 3 | Zero-shot classification, sentence embeddings, semantic search |
| 4.3 | [The LLM API](curriculum/stage4_genai/03_llm_api/README.md) | 4 | System prompts, structured JSON output, multi-turn conversation |
| 4.4 | [Retrieval-Augmented Generation](curriculum/stage4_genai/04_rag/README.md) | 3 | Document chunking, vector retrieval, full RAG pipeline |

**Project:** [Security Analyst Assistant](curriculum/stage4_genai/project/security_assistant.py) — interactive Q&A over a knowledge base of CVEs, threat reports, and security runbooks.

> **Multi-provider support:** All Stage 4 scripts work with Claude, OpenAI, Gemini, or Ollama. The [`llm_client.py`](curriculum/stage4_genai/llm_client.py) helper abstracts the provider — set whichever key you have.

<details>
<summary><strong>Key concepts in this stage</strong></summary>

Tokens and context windows, embeddings, cosine similarity, vector search, RAG pipeline, prompt engineering, system prompts, conversation state, hallucination and grounding, structured output
</details>

---

## Stage 5 — Check Point AI Security

> Apply everything you've learned to Check Point's AI Security products — and become the expert your customers need.

This stage connects your AI fundamentals to the products you sell. You will learn how Check Point's AI Security suite works under the hood, get hands-on with the MCP playground and Lakera-Demo, and build a customer-facing demo that positions all three products.

| # | Session | Format | Time | Hands-On |
|---|---------|--------|------|----------|
| 5.1 | [Workforce AI Security](curriculum/stage5_cp_ai_security/01_workforce_ai_security/README.md) | Lecture + walkthrough | 60 min | Dashboard exploration, policy design |
| 5.2 | [AI Agent Security + MCP](curriculum/stage5_cp_ai_security/02_ai_agent_security/README.md) | Lecture + lab | 90 min | [cp-agentic-mcp-playground](https://github.com/alshawwaf/cp-agentic-mcp-playground) |
| 5.3 | [AI Guardrails](curriculum/stage5_cp_ai_security/03_ai_guardrails/README.md) | Lecture + lab | 90 min | [Lakera-Demo](https://github.com/alshawwaf/Lakera-Demo) |
| 5.4 | [Positioning Check Point AI Security](curriculum/stage5_cp_ai_security/04_positioning_cp_ai/README.md) | Workshop | 60 min | Customer demo rehearsal |

<details>
<summary><strong>Key concepts in this stage</strong></summary>

AI governance, shadow AI, sensitive data classification, policy enforcement (allow/prevent/redact/detect/block/ask), AI agents, Model Context Protocol (MCP), least-privilege for agents, prompt injection defense, jailbreak detection, LLM guardrails, inbound/outbound scanning, competitive positioning
</details>

---

<details>
<summary><strong>Repository Map</strong></summary>

```
AI Basic Training/
├── Dockerfile                              Docker build for the portal + ML runtime
├── docker-compose.yml                      One-command startup
├── README.md                               This file
│
├── portal/                                 Web application (Flask)
│   ├── app.py                                  Main Flask app + content/run APIs
│   ├── config.py                               Stage/lesson registry
│   ├── runner.py                               Script executor (subprocess + matplotlib capture)
│   ├── requirements.txt                        Python dependencies
│   ├── static/                                 CSS + JS
│   ├── templates/                              Jinja2 base templates
│   └── lessons/                                Interactive lesson Blueprints (21 lessons, all stages)
│
├── curriculum/                             Course content (5 stages, 21 lessons, 67 exercises)
│   ├── stage1_classic_ml/                      5 lessons: ML basics → model evaluation
│   ├── stage2_intermediate/                    4 lessons: feature engineering → cross-validation
│   ├── stage3_neural_networks/                 4 lessons: Keras → CNNs → hyperparameter tuning
│   ├── stage4_genai/                           4 lessons: tokenisation → RAG pipelines
│   └── stage5_cp_ai_security/                  4 lessons: workforce AI → guardrails → demos
│
├── ops/                                    Program operations (non-technical)
│   ├── assessments/                            Stage gate quizzes and rubrics
│   ├── facilitator_guides/                     22 per-session delivery guides
│   ├── demo_kit/                               Customer demo assistant + scripts
│   ├── program_ops/                            Welcome packet, recruitment, certificates
│   ├── stage0_positioning/                     Pre-technical AI positioning sessions
│   └── assets/                                 Generated diagrams for lessons
│
└── docs/                                   Planning documents
    ├── PROGRAM_SYLLABUS.md                     15-week schedule + tier system
    └── NINJA_PROGRAM_BLUEPRINT.md              Strategic plan + recommendations
```

</details>

---

## Pacing Guide

There are no deadlines. Each lesson is self-contained enough to pause and resume without losing context.

| Pace | Daily commitment | Approximate timeline |
|------|-----------------|---------------------|
| Intensive | 6–8 hours/day | ~2 weeks |
| Evenings | 1–2 hours/day | 6–8 weeks |
| Weekends | 3–4 hours/weekend | 3–4 months |

Aim for consistency over speed. Completing one exercise per session is better than rushing through an entire stage and retaining nothing.

---

<details>
<summary><strong>Tips for Success</strong></summary>

**Work through stages in order.** Each one builds on the last. Stage 3 assumes you understand loss and evaluation from Stages 1–2. Stage 4 assumes you understand embeddings from Stage 3.

**Read the theory before writing code.** The `README.md` file in each lesson explains the concept, the intuition, and the security context. Skipping it means you will be copying code without understanding why it works.

**Run your code after every step.** The exercises are designed to produce output at each stage. Verify each result before moving on — a small mistake early compounds into confusing output later.

**Break things on purpose.** The best way to understand a parameter is to push it to an extreme. Set `max_depth=1` on a decision tree. Set the learning rate to `10.0`. Watch what happens. That intuition is worth more than any explanation.

**Use the solutions as a reference, not a shortcut.** Try each exercise yourself first, even if you get stuck. The struggle is where learning happens. Check the solution file only after you have a working (or broken) attempt of your own.

**The projects are checkpoints, not exams.** If a project script runs and produces reasonable output, you have the understanding you need to continue. You do not need to master every detail before moving forward.

</details>
