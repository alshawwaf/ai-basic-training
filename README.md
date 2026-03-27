# AI Learning Journey

A 4-week hands-on AI/ML curriculum in Python, tailored for cybersecurity professionals.
Each module builds on the last — from classic ML through to Generative AI.

---

## Curriculum Overview

| Module | Topic | Week | Milestone Project |
|--------|-------|------|-------------------|
| [Module 1](stage1_ml/README.md) | Classic Machine Learning | 1 | Phishing URL Classifier |
| [Module 2](stage2_intermediate/README.md) | Intermediate ML | 2 | Network Intrusion Detector |
| [Module 3](stage3_neural_networks/README.md) | Neural Networks | 3 | Malicious Packet Classifier |
| [Module 4](stage4_genai/README.md) | Generative AI | 4 | Security Analyst Assistant (RAG) |

---

## Setup

Install all dependencies before starting:

```bash
pip install pandas scikit-learn matplotlib seaborn
# Added as you progress:
# pip install tensorflow transformers anthropic sentence-transformers
```

**Python 3.10+ required.**

---

## How Each Lesson Works

1. Read the lesson markdown file for the concept explanation
2. Open the matching `.py` script — comments walk you through the code
3. Run it and observe the output
4. Tweak one value and see what changes

---

## Module 1 — Classic Machine Learning

| Lesson | File | Topic |
|--------|------|-------|
| 1.1 | [1_concepts_and_data.py](stage1_ml/1_concepts_and_data.py) | What is ML? Exploring data |
| 1.2 | [2_linear_regression.py](stage1_ml/2_linear_regression.py) | Predicting values (regression) |
| 1.3 | [3_logistic_regression.py](stage1_ml/3_logistic_regression.py) | Yes/No decisions (classification) |
| 1.4 | [4_decision_tree.py](stage1_ml/4_decision_tree.py) | Rule-based classification |
| 1.5 | [5_model_evaluation.py](stage1_ml/5_model_evaluation.py) | Measuring how good your model is |
| Milestone | [milestone_phishing.py](stage1_ml/milestone_phishing.py) | Phishing URL classifier |

## Module 2 — Intermediate ML

| Lesson | File | Topic |
|--------|------|-------|
| 2.1 | [1_feature_engineering.py](stage2_intermediate/1_feature_engineering.py) | Turning raw logs into ML features |
| 2.2 | [2_random_forest.py](stage2_intermediate/2_random_forest.py) | Ensemble models (malware classifier) |
| 2.3 | [3_clustering.py](stage2_intermediate/3_clustering.py) | Anomaly detection (unsupervised) |
| 2.4 | [4_overfitting.py](stage2_intermediate/4_overfitting.py) | Cross-validation & overfitting |
| Milestone | [milestone_intrusion.py](stage2_intermediate/milestone_intrusion.py) | Network intrusion detector |

## Module 3 — Neural Networks

| Lesson | File | Topic |
|--------|------|-------|
| 3.1 | [p001-Basic-Neuron-3-inputs.py](stage3_neural_networks/foundations/p001-Basic-Neuron-3-inputs.py) | Building your first neuron |
| 3.2 | [p002-Basic-Neuron-Layer.py](stage3_neural_networks/foundations/p002-Basic-Neuron-Layer.py) | A layer of neurons |
| 3.3 | [p003-Dot-Product.py](stage3_neural_networks/foundations/p003-Dot-Product.py) | Vectorising with NumPy |
| 3.4 | [p004-Layers-and-Object.py](stage3_neural_networks/foundations/p004-Layers-and-Object.py) | Layers as Python classes |
| 3.5 | [p005-ReLU-Activation.py](stage3_neural_networks/foundations/p005-ReLU-Activation.py) | ReLU activation function |
| 3.6 | [p006-Softmax-Activation.py](stage3_neural_networks/foundations/p006-Softmax-Activation.py) | Softmax activation function |
| 3.7 | [p007-Categorical-Cross-Entropy-Loss.py](stage3_neural_networks/foundations/p007-Categorical-Cross-Entropy-Loss.py) | Cross-entropy loss |
| 3.8 | [p008-Categorical-Cross-Entropy-Loss-applied.py](stage3_neural_networks/foundations/p008-Categorical-Cross-Entropy-Loss-applied.py) | Full network + loss |
| 3.9 | [1_first_neural_net.py](stage3_neural_networks/1_first_neural_net.py) | Building with Keras |
| 3.10 | [2_deeper_network.py](stage3_neural_networks/2_deeper_network.py) | Deeper networks + regularisation |
| 3.11 | [3_cnn.py](stage3_neural_networks/3_cnn.py) | Convolutional networks |
| 3.12 | [4_hyperparameters.py](stage3_neural_networks/4_hyperparameters.py) | Tuning your network |
| Milestone | [milestone_packets.py](stage3_neural_networks/milestone_packets.py) | Neural network packet classifier |

## Module 4 — Generative AI

| Lesson | File | Topic |
|--------|------|-------|
| 4.1 | [1_llm_concepts.py](stage4_genai/1_llm_concepts.py) | How LLMs work (tokens, embeddings) |
| 4.2 | [2_huggingface.py](stage4_genai/2_huggingface.py) | Pre-trained models (HuggingFace) |
| 4.3 | [3_claude_api.py](stage4_genai/3_claude_api.py) | Building with the Claude API |
| 4.4 | [4_rag.py](stage4_genai/4_rag.py) | RAG — AI over your own documents |
| Milestone | [milestone_security_assistant.py](stage4_genai/milestone_security_assistant.py) | CVE/threat report Q&A bot |
