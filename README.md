# AI Learning Journey

A 4-week hands-on AI/ML curriculum in Python, tailored for cybersecurity professionals.
Each stage builds on the last — from classic ML through to Generative AI.

---

## Curriculum Overview

| Stage | Topic | Week | Milestone Project |
|-------|-------|------|-------------------|
| [Stage 1](stage1_ml/README.md) | Classic Machine Learning | 1 | Phishing URL Classifier |
| [Stage 2](stage2_intermediate/README.md) | Intermediate ML | 2 | Network Intrusion Detector |
| [Stage 3](stage3_neural_networks/README.md) | Neural Networks | 3 | Malicious Packet Classifier |
| [Stage 4](stage4_genai/README.md) | Generative AI | 4 | Security Analyst Assistant (RAG) |

---

## Setup

Install all dependencies before starting:

```bash
pip install pandas scikit-learn matplotlib seaborn
# Added as you progress:
# pip install tensorflow transformers anthropic
```

**Python 3.10+ required.**

---

## How Each Lesson Works

1. Read the lesson markdown file for the concept explanation
2. Open the matching `.py` script — comments walk you through the code
3. Run it and observe the output
4. Tweak one value and see what changes

---

## Stage 1 — Classic Machine Learning

| Lesson | File | Topic |
|--------|------|-------|
| 1.1 | [1_concepts_and_data.py](stage1_ml/1_concepts_and_data.py) | What is ML? Exploring data |
| 1.2 | `2_linear_regression.py` | Predicting values (regression) |
| 1.3 | `3_logistic_regression.py` | Yes/No decisions (classification) |
| 1.4 | `4_decision_tree.py` | Rule-based classification |
| 1.5 | `5_model_evaluation.py` | Measuring how good your model is |
| Milestone | `milestone_phishing.py` | Phishing URL classifier |

## Stage 2 — Intermediate ML

| Lesson | File | Topic |
|--------|------|-------|
| 2.1 | `1_feature_engineering.py` | Turning raw logs into ML features |
| 2.2 | `2_random_forest.py` | Ensemble models (malware classifier) |
| 2.3 | `3_clustering.py` | Anomaly detection (unsupervised) |
| 2.4 | `4_overfitting.py` | Cross-validation & overfitting |
| Milestone | `milestone_intrusion.py` | Network intrusion detector (KDD Cup) |

## Stage 3 — Neural Networks

**Part A — From Scratch** (build intuition before using frameworks):

| File | What it introduces |
|------|--------------------|
| [from_scratch/p001](stage3_neural_networks/from_scratch/p001-Basic-Neuron-3-inputs.py) | Single neuron |
| [from_scratch/p002](stage3_neural_networks/from_scratch/p002-Basic-Neuron-Layer.py) | Layer of neurons |
| [from_scratch/p003](stage3_neural_networks/from_scratch/p003-Dot-Product.py) | Numpy dot product |
| [from_scratch/p004](stage3_neural_networks/from_scratch/p004-Layers-and-Object.py) | Layers as classes |
| [from_scratch/p005](stage3_neural_networks/from_scratch/p005-ReLU-Activation.py) | ReLU activation |
| [from_scratch/p006](stage3_neural_networks/from_scratch/p006-Softmax-Activation.py) | Softmax activation |
| [from_scratch/p007](stage3_neural_networks/from_scratch/p007-Categorical-Cross-Entropy-Loss.py) | Cross-entropy loss |
| [from_scratch/p008](stage3_neural_networks/from_scratch/p008-Categorical-Cross-Entropy-Loss-applied.py) | Full network + loss |

Source: [Sentdex/NNfSiX](https://github.com/Sentdex/NNfSiX/tree/master/Python)

**Part B — With Keras** (same concepts, industry-standard tools):

| Lesson | File | Topic |
|--------|------|-------|
| 3.1 | `1_first_neural_net.py` | Recreate Part A in Keras |
| 3.2 | `2_deeper_network.py` | Deeper networks, dropout |
| 3.3 | `3_cnn.py` | Convolutional networks for images |
| 3.4 | `4_hyperparameters.py` | Tuning for better accuracy |
| Milestone | `milestone_packets.py` | Neural network packet classifier |

## Stage 4 — Generative AI

| Lesson | File | Topic |
|--------|------|-------|
| 4.1 | `1_llm_concepts.py` | How LLMs work (tokens, embeddings) |
| 4.2 | `2_huggingface.py` | Pre-trained models (HuggingFace) |
| 4.3 | `3_claude_api.py` | Building with the Claude API |
| 4.4 | `4_rag.py` | RAG — AI over your own documents |
| Milestone | `milestone_security_assistant.py` | CVE/threat report Q&A bot |
