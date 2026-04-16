<div align="center">

# AI Basic Training

### A hands-on AI & machine-learning curriculum built around real cybersecurity scenarios.

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Portal-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-Classic%20ML-F7931E?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-Neural%20Networks-FF6F00?logo=tensorflow&logoColor=white)](https://www.tensorflow.org/)
[![HuggingFace](https://img.shields.io/badge/%F0%9F%A4%97-Transformers-FFD21E)](https://huggingface.co/)
[![Docker](https://img.shields.io/badge/Docker-one%20command-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)

**5 technical stages · 21 lessons · 67 exercises · 4 capstone projects**

[Quick start](#quick-start) · [The Portal](#the-portal) · [Curriculum](#curriculum) · [Who this is for](#who-this-is-for) · [Docs](#program-documents)

</div>

---

## Why this exists

Most AI material is either too abstract for engineers who need to *ship*, or too shallow for people who need to understand what's actually happening. This curriculum is the middle path: every concept is taught through a working cybersecurity example — phishing URLs, packet classification, intrusion detection, malware visualisation, RAG over CVE databases — and every lesson produces code you run, break, and modify.

It is also the technical core of the **AI Ninja Program**, a selective cohort-based training track for security architects and engineers.

## What's in the box

| | |
|---|---|
| **Interactive portal** | A Flask web app that turns each lesson into a guided, browser-based experience with live code execution, visualisations, and progress tracking. `docker-compose up` and you're in. |
| **21 lessons** | Across five stages: Classic ML → Intermediate ML → Neural Networks → Generative AI → Check Point AI Security. Every lesson has a lecture, hands-on exercises, and a reference solution. |
| **4 capstone projects** | End-of-stage projects with real security datasets: phishing classifier, intrusion detector, packet classifier, security RAG assistant. |
| **Cybersecurity framing** | Every concept is introduced through a security scenario. You learn logistic regression by building a phishing detector, not by classifying flowers. |
| **Multi-provider LLM support** | Stage 4 works with Claude, OpenAI, Gemini, or local Ollama — pick whichever key you have. |
| **Facilitator-ready** | 22 per-session delivery guides, stage-gate assessments, and a customer-demo kit for running the program as a cohort. |

---

## Quick start

```bash
git clone https://github.com/alshawwaf/ai-basic-training.git
cd ai-basic-training
docker-compose up --build
```

Then open **http://localhost:5000**.

<details>
<summary><strong>No Docker? Run it with a venv instead.</strong></summary>

```bash
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r portal/requirements.txt
python -m portal.app
```

</details>

---

## The Portal

The portal is not a static notebook viewer — it's an interactive learning environment. Each lesson is a sequence of **Explore → Read → Build → Compare → Reflect** steps, with live visualisations and code that runs server-side.

| Feature | What it does |
|---|---|
| **Per-stage theming** | Each stage has its own accent palette — you always know where you are in the curriculum. |
| **Guided lesson flow** | Numbered, pill-shaped step rail with active-state indication, shimmer trail, and keyboard navigation. |
| **Lecture panels** | Theory rendered from Markdown with real matplotlib figures — every concept gets a visual before the code. |
| **Live code execution** | Run exercises in the browser; outputs, errors, and generated plots stream back to the same panel. |
| **Interactive demos** | Per-lesson widgets — pixel-grid digit viewers, clustering playgrounds, token/embedding explorers, RAG retrievers. |
| **Progress & bookmarks** | Track completed steps per lesson; bookmark any step and jump back later. |
| **Light / dark mode** | Unified Inter-based typography, deep-violet palette, glassmorphism and gradient-mesh accents. |

> To add a hero screenshot, drop a PNG at `ops/assets/portal_hero.png` and reference it here.

---

## Curriculum

> Five stages, ordered by difficulty and tier. Each stage ends with a capstone project.

| Stage | Focus | Lessons | Project | Tier |
|---|---|---|---|---|
| **1 · Classic ML** | Supervised learning, linear & logistic regression, decision trees, evaluation | 5 | Phishing URL Classifier | Foundations |
| **2 · Intermediate ML** | Feature engineering, Random Forests, clustering, cross-validation | 4 | Network Intrusion Detector | Foundations |
| **3 · Neural Networks** | Neurons → Keras → CNNs → hyperparameter tuning (NumPy-first, then framework) | 4 + 8 foundations | Malicious Packet Classifier | Practitioner |
| **4 · Generative AI** | Tokenisation, embeddings, attention, LLM APIs, RAG pipelines | 4 | Security Analyst Assistant (RAG) | Ninja |
| **5 · Check Point AI Security** | Workforce AI, MCP agent security, guardrails, customer demos | 4 | Customer Demo Rehearsal | Ninja |

<details>
<summary><strong>Stage 1 — Classic Machine Learning</strong></summary>

| # | Lesson | Exercises | What you learn |
|---|---|---|---|
| 1.1 | [What is ML?](curriculum/stage1_classic_ml/01_what_is_ml/README.md) | 5 | ML workflow — loading data, exploring features, EDA, class balance |
| 1.2 | [Linear Regression](curriculum/stage1_classic_ml/02_linear_regression/README.md) | 4 | Predicting continuous values — server response time from traffic load |
| 1.3 | [Logistic Regression](curriculum/stage1_classic_ml/03_logistic_regression/README.md) | 4 | Binary classification — phishing or legitimate from URL features |
| 1.4 | [Decision Trees](curriculum/stage1_classic_ml/04_decision_trees/README.md) | 4 | Interpretable rule-based splits — network traffic as threat or benign |
| 1.5 | [Model Evaluation](curriculum/stage1_classic_ml/05_model_evaluation/README.md) | 5 | Precision, recall, F1, ROC AUC — why accuracy alone is misleading |

**Capstone:** [Phishing URL Classifier](curriculum/stage1_classic_ml/project/phishing_detector.py) — end-to-end pipeline from feature extraction through training to evaluation on a real phishing dataset.

</details>

<details>
<summary><strong>Stage 2 — Intermediate ML</strong></summary>

| # | Lesson | Exercises | What you learn |
|---|---|---|---|
| 2.1 | [Feature Engineering](curriculum/stage2_intermediate/01_feature_engineering/README.md) | 4 | Extracting numerical signals from raw firewall and NetFlow logs |
| 2.2 | [Random Forests](curriculum/stage2_intermediate/02_random_forests/README.md) | 4 | Ensemble of decision trees — malware vs. benign file classifier |
| 2.3 | [Clustering & Anomaly Detection](curriculum/stage2_intermediate/03_clustering_anomaly/README.md) | 4 | K-Means to find anomalous connections — no labels required |
| 2.4 | [Overfitting & Cross-Validation](curriculum/stage2_intermediate/04_overfitting_crossval/README.md) | 4 | Why models fail in production — k-fold CV, bias-variance tradeoff |

**Capstone:** [Network Intrusion Detector](curriculum/stage2_intermediate/project/intrusion_detector.py) — trained and evaluated on KDD Cup-style network connection data.

</details>

<details>
<summary><strong>Stage 3 — Neural Networks</strong></summary>

**Phase 1 — From scratch with NumPy.** No framework. Each script builds one piece and connects to the last.

| # | Script | What you build |
|---|---|---|
| 3.1 | [1_basic_neuron.py](curriculum/stage3_neural_networks/foundations/1_basic_neuron.py) | A single neuron — inputs × weights + bias |
| 3.2 | [2_neuron_layer.py](curriculum/stage3_neural_networks/foundations/2_neuron_layer.py) | Multiple neurons computing in parallel — a full layer |
| 3.3 | [3_dot_product.py](curriculum/stage3_neural_networks/foundations/3_dot_product.py) | Vectorising computation with NumPy matrix multiplication |
| 3.4 | [4_layers_as_classes.py](curriculum/stage3_neural_networks/foundations/4_layers_as_classes.py) | Structuring layers as reusable Python objects |
| 3.5 | [5_relu_activation.py](curriculum/stage3_neural_networks/foundations/5_relu_activation.py) | ReLU — adding non-linearity |
| 3.6 | [6_softmax_activation.py](curriculum/stage3_neural_networks/foundations/6_softmax_activation.py) | Softmax — raw outputs → probability distribution |
| 3.7 | [7_cross_entropy_loss.py](curriculum/stage3_neural_networks/foundations/7_cross_entropy_loss.py) | Cross-entropy loss — quantifying prediction error |
| 3.8 | [8_full_forward_pass.py](curriculum/stage3_neural_networks/foundations/8_full_forward_pass.py) | Complete forward pass — input through layers, activations, to loss |

**Phase 2 — Keras and real security data.**

| # | Lesson | Exercises | What you learn |
|---|---|---|---|
| 3.9 | [First Neural Network](curriculum/stage3_neural_networks/01_first_neural_network/README.md) | 4 | Rebuild the NumPy network in Keras in ~10 lines |
| 3.10 | [Dropout & Regularisation](curriculum/stage3_neural_networks/02_dropout_regularisation/README.md) | 4 | Dropout, batch norm, early stopping — prevent memorisation |
| 3.11 | [Convolutional Networks](curriculum/stage3_neural_networks/03_convolutional_networks/README.md) | 4 | CNNs applied to malware binary visualisation |
| 3.12 | [Hyperparameter Tuning](curriculum/stage3_neural_networks/04_hyperparameter_tuning/README.md) | 4 | Learning rate, batch size, architecture — systematic search |

**Capstone:** [Malicious Packet Classifier](curriculum/stage3_neural_networks/project/packet_classifier.py) — neural network trained on packet feature vectors.

</details>

<details>
<summary><strong>Stage 4 — Generative AI</strong></summary>

| # | Lesson | Exercises | What you learn |
|---|---|---|---|
| 4.1 | [How LLMs Work](curriculum/stage4_genai/01_how_llms_work/README.md) | 3 | Tokenisation, embeddings, attention — pure NumPy, no API key needed |
| 4.2 | [HuggingFace Models](curriculum/stage4_genai/02_huggingface/README.md) | 3 | Zero-shot classification, sentence embeddings, semantic search |
| 4.3 | [The LLM API](curriculum/stage4_genai/03_llm_api/README.md) | 4 | System prompts, structured JSON output, multi-turn conversation |
| 4.4 | [Retrieval-Augmented Generation](curriculum/stage4_genai/04_rag/README.md) | 3 | Document chunking, vector retrieval, full RAG pipeline |

**Capstone:** [Security Analyst Assistant](curriculum/stage4_genai/project/security_assistant.py) — interactive Q&A over a curated corpus of CVEs, threat reports, and runbooks.

> Every Stage-4 script works with Claude, OpenAI, Gemini, or Ollama via [`llm_client.py`](curriculum/stage4_genai/llm_client.py).

</details>

<details>
<summary><strong>Stage 5 — Check Point AI Security</strong></summary>

| # | Session | Format | Hands-on |
|---|---|---|---|
| 5.1 | [Workforce AI Security](curriculum/stage5_cp_ai_security/01_workforce_ai_security/README.md) | Lecture + walkthrough | Dashboard exploration, policy design |
| 5.2 | [AI Agent Security + MCP](curriculum/stage5_cp_ai_security/02_ai_agent_security/README.md) | Lecture + lab | [cp-agentic-mcp-playground](https://github.com/alshawwaf/cp-agentic-mcp-playground) |
| 5.3 | [AI Guardrails](curriculum/stage5_cp_ai_security/03_ai_guardrails/README.md) | Lecture + lab | [Lakera-Demo](https://github.com/alshawwaf/Lakera-Demo) |
| 5.4 | [Positioning Check Point AI Security](curriculum/stage5_cp_ai_security/04_positioning_cp_ai/README.md) | Workshop | Customer demo rehearsal |

</details>

---

## Who this is for

Security engineers and architects who want to **understand and apply** AI/ML — not just consume tools that happen to contain it.

You'll get the most out of this if you:

- Design, build, or evaluate security controls and architectures
- Write Python regularly — automation, tooling, detection logic, integrations
- Want to know what "AI-powered" security products are actually doing under the hood
- Need to decide where ML fits (and where it doesn't) in a security stack

No prior ML, statistics, or data science background required. If you can read Python and understand a `for` loop, you can finish this curriculum.

## Prerequisites

- **Python 3.10+** — [python.org/downloads](https://www.python.org/downloads/)
- **Docker** (optional but recommended) — for one-command portal startup
- Comfort with variables, loops, functions, classes, and list comprehensions

## How lessons are structured

```
01_topic_name/
├── README.md                    Theory — read first
├── 1_first_exercise/
│   ├── lecture.md                 Concept + methods you need
│   ├── handson.md                 Step-by-step instructions
│   └── solution_*.py              Reference solution (open last)
├── 2_second_exercise/
│   └── ...
```

**Recommended flow for each lesson:** read the theory → work through each exercise bottom-up (lecture → handson → your code → compare with solution) → move on when the output makes sense. Repetition across stages deepens understanding faster than perfection on any single lesson.

## Pacing

| Pace | Daily commitment | Approximate timeline |
|---|---|---|
| Intensive | 6–8 hours/day | ~2 weeks |
| Evenings | 1–2 hours/day | 6–8 weeks |
| Weekends | 3–4 hours/weekend | 3–4 months |

Consistency beats speed. One exercise per session, every session, beats a rushed stage you don't remember.

---

## Program documents

| Document | Description |
|---|---|
| [Program Syllabus](docs/PROGRAM_SYLLABUS.md) | 15-week schedule, tier system, assessment gates |
| [Ninja Program Blueprint](docs/NINJA_PROGRAM_BLUEPRINT.md) | Strategic plan, recommendations, success metrics |
| [Facilitator Guides](ops/facilitator_guides/) | Per-lecture delivery guides |
| [Assessments](ops/assessments/) | Quiz, challenge, review, and capstone rubrics |
| [Stage 0 — AI Positioning](ops/stage0_positioning/) | Non-technical track: landscape, competitors, objections, discovery |
| [Security Corpus](curriculum/stage4_genai/data/) | 31 curated documents — CVEs, threat actors, runbooks |
| [Customer Demo Kit](ops/demo_kit/) | Packaged demo assistant, presentation script, architecture one-pager |
| [Program Operations](ops/program_ops/) | Welcome packet, recruitment pitch, skills survey, certificates |

---

<details>
<summary><strong>Repository map</strong></summary>

| Path | Purpose |
|---|---|
| `portal/` | Flask web application — the interactive learning environment |
| `portal/app.py` | Main app, content + run APIs |
| `portal/lessons/` | 21 interactive lesson blueprints, one per session |
| `portal/static/` | CSS, JS, lecture image assets |
| `portal/templates/` | Jinja2 base templates |
| `curriculum/` | Course content — Markdown lectures, exercises, reference solutions |
| `curriculum/stage1_classic_ml/` | 5 lessons: ML basics → model evaluation |
| `curriculum/stage2_intermediate/` | 4 lessons: feature engineering → cross-validation |
| `curriculum/stage3_neural_networks/` | 8 NumPy foundations + 4 Keras lessons → CNN → hyperparams |
| `curriculum/stage4_genai/` | 4 lessons: tokenisation → RAG |
| `curriculum/stage5_cp_ai_security/` | 4 sessions: Check Point AI product mastery |
| `ops/` | Non-technical program materials — assessments, facilitator guides, demo kit |
| `docs/` | Planning documents — syllabus, blueprint |
| `Dockerfile` / `docker-compose.yml` | One-command portal startup |

</details>

<details>
<summary><strong>Tips for getting the most out of this</strong></summary>

**Work through stages in order.** Each builds on the last. Stage 3 assumes evaluation fluency from Stages 1–2; Stage 4 assumes embeddings from Stage 3.

**Read theory before code.** The `README.md` in each lesson explains the concept, intuition, and security context. Skipping it means you copy code without understanding why.

**Run after every step.** Every exercise produces output along the way. Verify each result — a small mistake early compounds into confusing output later.

**Break things on purpose.** Set `max_depth=1` on a decision tree. Set the learning rate to `10.0`. Push parameters to extremes. That intuition is worth more than any explanation.

**Solutions are a reference, not a shortcut.** Try the exercise first, even if you get stuck. Check the solution after you have a working (or broken) attempt of your own.

**Projects are checkpoints, not exams.** If the script runs and produces reasonable output, you have enough understanding to move forward. You don't need to master every detail before the next stage.

</details>

---

## Contributing

Issues and pull requests are welcome. If you spot a typo, a broken link, a confusing explanation, or an exercise that could be clearer, open an issue. If you're adapting the curriculum for a different domain (e.g., financial services, healthcare), a discussion issue is the best place to start.
