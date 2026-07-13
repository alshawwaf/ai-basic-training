<div align="center">

# AI Basic Training

### A hands-on AI & machine-learning curriculum taught entirely through real cybersecurity scenarios, delivered as an interactive Flask portal.

Part of the [Dev Hub](https://github.com/alshawwaf/dev-hub) ecosystem — deploy the whole suite with [ubuntu-dokploy-ai](https://github.com/alshawwaf/ubuntu-dokploy-ai).

[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Portal-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-Classic%20ML-F7931E?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow--CPU-Neural%20Networks-FF6F00?logo=tensorflow&logoColor=white)](https://www.tensorflow.org/)
[![HuggingFace](https://img.shields.io/badge/%F0%9F%A4%97-Transformers-FFD21E)](https://huggingface.co/)
[![Docker](https://img.shields.io/badge/Docker-one%20command-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)

**5 stages · 21 lessons · 67 exercises · 4 capstone projects**

</div>

---

## Overview

Most AI material is either too abstract for engineers who need to *ship* or too shallow to explain what's actually happening. This curriculum is the middle path: every concept is taught through a working security example — phishing URLs, packet classification, intrusion detection, malware visualisation, RAG over a CVE corpus — and every lesson produces code you run, break, and modify.

The delivery vehicle is an interactive Flask portal. Each lesson is a guided, browser-based flow (explore → read → build → compare → reflect) with live server-side code execution, real matplotlib visualisations, per-browser progress tracking, and a login-gated admin console. It is also the technical core of the internal AI Ninja Program, a cohort-based training track for security architects and engineers — the `ops/` and `docs/` trees ship the facilitator guides, assessments, and program materials to run it as a cohort.

## Features

| | |
|---|---|
| **Interactive portal** | Flask web app that turns each lesson into a guided, browser-based experience — numbered step rail, lecture panels, live code execution, and per-lesson quizzes. |
| **21 lessons, 5 stages** | Classic ML → Intermediate ML → Neural Networks → Generative AI → Check Point AI Security. Every lesson has a lecture, hands-on exercises, and a reference solution. |
| **Live, sandboxed execution** | Run reference solutions in the browser; stdout, errors, and generated plots stream back to the panel. Only `solution_*.py` files under `curriculum/` run, in a subprocess with output caps and a 120 s timeout. |
| **4 capstone projects** | End-of-stage projects on real security data: phishing classifier, intrusion detector, packet classifier, security RAG assistant. |
| **Multi-provider Gen AI** | Stage 4 scripts work with Claude, OpenAI, Gemini, or local Ollama — pick whichever key you have. |
| **Progress & bookmarks** | Server-side SQLite store keyed by a per-browser token; visited steps and bookmarks survive cache clears. |
| **Admin console** | Login-gated `/admin` with usage analytics and a home-layout toggle (zigzag stage cards vs. neuron-mesh view). |
| **Facilitator-ready** | 26 delivery guides, stage-gate assessments, a customer-demo kit, and program-ops docs for running the curriculum as a cohort. |

## Curriculum

Five stages, ordered by difficulty and tier. Each ends with a capstone project.

| Stage | Focus | Lessons | Capstone | Tier |
|---|---|---|---|---|
| **1 · Classic ML** | Linear & logistic regression, decision trees, model evaluation | 5 | Phishing URL Classifier | Foundations |
| **2 · Intermediate ML** | Feature engineering, Random Forests, clustering, cross-validation | 4 | Network Intrusion Detector | Foundations |
| **3 · Neural Networks** | Neurons → Keras → CNNs → hyperparameter tuning (NumPy-first, then framework) | 4 + 8 foundations | Malicious Packet Classifier | Practitioner |
| **4 · Generative AI** | Tokenisation, embeddings, attention, LLM APIs, RAG | 4 | Security Analyst Assistant (RAG) | Ninja |
| **5 · Check Point AI Security** | Workforce AI, MCP agent security, guardrails, positioning | 4 | Customer Demo Rehearsal | Ninja |

<details>
<summary><strong>Stage 1 — Classic Machine Learning</strong></summary>

| # | Lesson | What you learn |
|---|---|---|
| 1.1 | [What is ML?](curriculum/stage1_classic_ml/01_what_is_ml/README.md) | The ML workflow — loading data, exploring features, class balance |
| 1.2 | [Linear Regression](curriculum/stage1_classic_ml/02_linear_regression/README.md) | Predicting continuous values — response time from traffic load |
| 1.3 | [Logistic Regression](curriculum/stage1_classic_ml/03_logistic_regression/README.md) | Binary classification — phishing vs. legitimate URLs |
| 1.4 | [Decision Trees](curriculum/stage1_classic_ml/04_decision_trees/README.md) | Interpretable rule-based splits — traffic as threat or benign |
| 1.5 | [Model Evaluation](curriculum/stage1_classic_ml/05_model_evaluation/README.md) | Precision, recall, F1, ROC AUC — why accuracy alone misleads |

**Capstone:** [Phishing URL Classifier](curriculum/stage1_classic_ml/project/phishing_detector.py) — feature extraction through training and evaluation on a phishing dataset.

</details>

<details>
<summary><strong>Stage 2 — Intermediate ML</strong></summary>

| # | Lesson | What you learn |
|---|---|---|
| 2.1 | [Feature Engineering](curriculum/stage2_intermediate/01_feature_engineering/README.md) | Extracting numerical signals from raw firewall and NetFlow logs |
| 2.2 | [Random Forests](curriculum/stage2_intermediate/02_random_forests/README.md) | Ensembles of trees — malware vs. benign file classifier |
| 2.3 | [Clustering & Anomaly Detection](curriculum/stage2_intermediate/03_clustering_anomaly/README.md) | K-Means to surface anomalous connections — no labels required |
| 2.4 | [Overfitting & Cross-Validation](curriculum/stage2_intermediate/04_overfitting_crossval/README.md) | Why models fail in production — k-fold CV, bias-variance tradeoff |

**Capstone:** [Network Intrusion Detector](curriculum/stage2_intermediate/project/intrusion_detector.py) — trained and evaluated on KDD Cup-style connection data.

</details>

<details>
<summary><strong>Stage 3 — Neural Networks</strong></summary>

**Phase 1 — from scratch with NumPy** ([foundations/](curriculum/stage3_neural_networks/foundations/)): eight scripts that build a network piece by piece — single neuron → layer → dot-product vectorisation → layers as classes → ReLU → softmax → cross-entropy loss → full forward pass.

**Phase 2 — Keras and real security data:**

| # | Lesson | What you learn |
|---|---|---|
| 3.1 | [First Neural Network](curriculum/stage3_neural_networks/01_first_neural_network/README.md) | Rebuild the NumPy network in Keras in ~10 lines |
| 3.2 | [Dropout & Regularisation](curriculum/stage3_neural_networks/02_dropout_regularisation/README.md) | Dropout, batch norm, early stopping — prevent memorisation |
| 3.3 | [Convolutional Networks](curriculum/stage3_neural_networks/03_convolutional_networks/README.md) | CNNs applied to malware binary visualisation |
| 3.4 | [Hyperparameter Tuning](curriculum/stage3_neural_networks/04_hyperparameter_tuning/README.md) | Learning rate, batch size, architecture — systematic search |

**Capstone:** [Malicious Packet Classifier](curriculum/stage3_neural_networks/project/packet_classifier.py) — a neural network trained on packet feature vectors.

</details>

<details>
<summary><strong>Stage 4 — Generative AI</strong></summary>

| # | Lesson | What you learn |
|---|---|---|
| 4.1 | [How LLMs Work](curriculum/stage4_genai/01_how_llms_work/README.md) | Tokenisation, embeddings, attention — pure NumPy, no API key |
| 4.2 | [HuggingFace Models](curriculum/stage4_genai/02_huggingface/README.md) | Zero-shot classification, sentence embeddings, semantic search |
| 4.3 | [The LLM API](curriculum/stage4_genai/03_llm_api/README.md) | System prompts, structured JSON output, multi-turn conversation |
| 4.4 | [Retrieval-Augmented Generation](curriculum/stage4_genai/04_rag/README.md) | Document chunking, vector retrieval, full RAG pipeline |

**Capstone:** [Security Analyst Assistant](curriculum/stage4_genai/project/security_assistant.py) — interactive Q&A over a curated corpus of CVEs, threat reports, and runbooks. Every Stage-4 script routes through [`llm_client.py`](curriculum/stage4_genai/llm_client.py) (Claude / OpenAI / Gemini / Ollama).

</details>

<details>
<summary><strong>Stage 5 — Check Point AI Security</strong></summary>

| # | Session | Hands-on |
|---|---|---|
| 5.1 | [Workforce AI Security](curriculum/stage5_cp_ai_security/01_workforce_ai_security/README.md) | Dashboard exploration, policy design |
| 5.2 | [AI Agent Security + MCP](curriculum/stage5_cp_ai_security/02_ai_agent_security/README.md) | [cp-agentic-mcp-playground](https://github.com/alshawwaf/cp-agentic-mcp-playground) |
| 5.3 | [AI Guardrails](curriculum/stage5_cp_ai_security/03_ai_guardrails/README.md) | [Lakera-Demo](https://github.com/alshawwaf/Lakera-Demo) |
| 5.4 | [Positioning Check Point AI Security](curriculum/stage5_cp_ai_security/04_positioning_cp_ai/README.md) | Customer demo rehearsal |

</details>

## Screenshots

_No screenshots yet. Drop a portal hero image at `ops/assets/portal_hero.png` and reference it here._

## Quick start

```bash
git clone https://github.com/alshawwaf/ai-basic-training.git
cd ai-basic-training
docker-compose up --build
```

Then open **http://localhost:5545** (Compose publishes the container's port 5000 on host port 5545).

<details>
<summary><strong>No Docker? Run it with a venv instead.</strong></summary>

```bash
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r portal/requirements.txt
cd portal && python app.py
```

In this mode the app binds **http://localhost:5000**.

</details>

> **Admin console:** the portal serves a login-gated view at `/admin`. The default password is `ninja` — set `PORTAL_ADMIN_PASSWORD` (and `PORTAL_SECRET_KEY`, so sessions survive a restart) before exposing it to anyone.

## Deployment

AI Basic Training deploys automatically as part of the [Dev Hub](https://github.com/alshawwaf/dev-hub) suite provisioned by [ubuntu-dokploy-ai](https://github.com/alshawwaf/ubuntu-dokploy-ai), reachable at **learn.\<your-domain\>** behind Traefik. Dokploy builds the image straight from the [`Dockerfile`](Dockerfile) — a multi-stage build that runs Gunicorn (4 workers, 180 s timeout) as a non-root `ninja` user. The [`docker-compose.yml`](docker-compose.yml) in this repo is the reference stack for local runs and mirrors the hardening applied in production (read-only root filesystem, `cap_drop: ALL`, `no-new-privileges`, CPU/memory limits) with a named volume holding the SQLite progress DB.

The portal is designed to be embedded in the Dev Hub desktop: `PORTAL_FRAME_ANCESTORS` (or, by default, an auto-derived `frame-ancestors` CSP scoped to the parent domain) lets a sibling app such as `hub.<domain>` iframe it while every other origin is refused.

## Configuration

All configuration is via environment variables — none are required to run locally.

| Variable | Default | Purpose |
|---|---|---|
| `PORTAL_ADMIN_PASSWORD` | `ninja` | Password for the `/admin` console. **Change before exposing.** |
| `PORTAL_SECRET_KEY` | random per-process | Flask session-signing key. Set it so admin sessions survive a restart. |
| `PORTAL_DB_PATH` | `portal/portal.db` | SQLite file for per-user progress. Compose points this at the `/data` volume. |
| `PORTAL_SETTINGS_PATH` | `portal/site_settings.json` | JSON store for per-deployment settings (e.g. home-page layout). |
| `PORTAL_FRAME_ANCESTORS` | auto-derived from host | CSP `frame-ancestors` override controlling who may iframe the portal. |
| `MPLBACKEND` | `Agg` | Matplotlib backend — headless figure rendering. |
| `AI_GUIDES_DIR` | Windows lab path | Directory of Stage-5 lab-guide PDFs served via `/api/pdf-guide`. Override per host. |

**Stage-4 Gen AI scripts** read a provider key at runtime (any one): `ANTHROPIC_API_KEY` (Claude), `OPENAI_API_KEY`, `GOOGLE_API_KEY` (Gemini), or `OLLAMA_MODEL` (local Ollama, no key). Without one, Stage 4's API/RAG exercises fall back to instructions on which key to set; the rest of the curriculum needs no keys.

## Tech stack

- **Backend:** Python 3.11, Flask, Gunicorn; SQLite for progress; `markdown` + `xhtml2pdf` for lecture/PDF rendering.
- **ML / data:** NumPy, pandas, scikit-learn, matplotlib, seaborn.
- **Deep learning:** TensorFlow-CPU (Keras); PyTorch (CPU) for the transformer stack.
- **Gen AI / NLP:** Hugging Face `transformers`, `sentence-transformers`; pluggable Claude / OpenAI / Gemini / Ollama clients.
- **Frontend:** server-rendered Jinja2 templates, vanilla CSS/JS (dark/light themes, gradient-mesh accents), no build step.
- **Packaging:** multi-stage Docker image, hardened `docker-compose.yml`.

## Development

The portal auto-discovers lessons. To add an interactive lesson:

1. Create `portal/lessons/<folder>/` with an `__init__.py` that defines a Flask `Blueprint` named `bp`.
2. Add step templates under `portal/lessons/<folder>/templates/<lesson_id>/`.
3. Register it in `portal/config.py` by adding the lesson entry with `has_app: True`.
4. Restart — `app.py` mounts the Blueprint at `/lesson/<lesson_id>` on startup.

Repo layout:

| Path | Purpose |
|---|---|
| `portal/` | Flask app — `app.py` (routes, content + run APIs), `config.py` (curriculum), `runner.py` (sandboxed executor), `users.py` (SQLite progress), `site_settings.py` |
| `portal/lessons/` | 21 lesson Blueprints, one per session |
| `portal/static/` · `portal/templates/` | CSS/JS, lecture assets · Jinja2 templates |
| `curriculum/` | Course content — Markdown lectures, `handson.md` exercises, `solution_*.py` references, capstone projects, Stage-4 security corpus |
| `ops/` | Non-technical program materials — facilitator guides, assessments, demo kit, program ops |
| `docs/` | Planning documents — syllabus, blueprint, exec summaries |

## Program documents

| Document | Description |
|---|---|
| [Program Syllabus](docs/PROGRAM_SYLLABUS.md) | Multi-week schedule, tier system, assessment gates |
| [Ninja Program Blueprint](docs/NINJA_PROGRAM_BLUEPRINT.md) | Strategic plan, recommendations, success metrics |
| [Facilitator Guides](ops/facilitator_guides/) | Per-lecture delivery guides |
| [Assessments](ops/assessments/) | Quiz, challenge, review, and capstone rubrics |
| [Stage 0 — AI Positioning](ops/stage0_positioning/) | Non-technical track: landscape, competitors, objections, discovery |
| [Security Corpus](curriculum/stage4_genai/data/) | Curated CVEs, threat-actor profiles, and IR runbooks for the RAG capstone |
| [Customer Demo Kit](ops/demo_kit/) | Packaged demo assistant, presentation script, architecture one-pager |
| [Program Operations](ops/program_ops/) | Welcome packet, recruitment pitch, skills survey, certificates |

## Contributing

Issues and pull requests are welcome — typos, broken links, confusing explanations, or exercises that could be clearer. If you're adapting the curriculum for another domain (financial services, healthcare), open a discussion issue first.
