# AI Learning Journey
### From Classic Machine Learning to Generative AI — Built for Cybersecurity Professionals

A hands-on, 4-week Python curriculum that takes you from your first ML model all the way to building a working AI security assistant. Every lesson uses a real cybersecurity example so the concepts stick.

---

## What You Will Build

| Module | Project | Description |
|--------|---------|-------------|
| 1 | **Phishing URL Classifier** | Detect malicious URLs from their structure alone |
| 2 | **Network Intrusion Detector** | Classify attack types from connection logs |
| 3 | **Malicious Packet Classifier** | Neural network trained on network traffic features |
| 4 | **Security Analyst Assistant** | Ask questions about CVEs and threat reports in plain English |

---

## Prerequisites

- Python 3.10+
- Basic Python comfort (loops, functions, classes)
- No prior ML or AI knowledge needed

---

## Setup

```bash
# Module 1 & 2
pip install pandas scikit-learn matplotlib seaborn

# Module 3
pip install tensorflow nnfs

# Module 4
pip install transformers sentence-transformers anthropic
```

For Module 4, you will also need a free Anthropic API key:
```bash
set ANTHROPIC_API_KEY=your-key-here
```
Get one at [console.anthropic.com](https://console.anthropic.com)

---

## How Each Lesson Works

Each lesson is a pair of files that live side by side:

| File | Purpose |
|------|---------|
| `N_topic_name.md` | Read this first — concept explanation, analogies, key ideas |
| `N_topic_name.py` | Run this — working code with inline comments |

1. Read the `.md` file to understand the concept
2. Run the `.py` script and observe the output
3. Change one value — see what breaks or improves
4. Move to the next lesson

---

## Module 1 — Classic Machine Learning
> **Goal:** Understand how machines learn from data and build your first classifiers

| # | Notes | Script | What You Learn |
|---|-------|--------|----------------|
| 1.1 | [What is ML?](stage1_ml/1_what_is_ml.md) | [1_concepts_and_data.py](stage1_ml/1_concepts_and_data.py) | How ML works, exploring a dataset |
| 1.2 | [Linear Regression](stage1_ml/2_linear_regression.md) | [2_linear_regression.py](stage1_ml/2_linear_regression.py) | Predict server response time from traffic load |
| 1.3 | [Logistic Regression](stage1_ml/3_logistic_regression.md) | [3_logistic_regression.py](stage1_ml/3_logistic_regression.py) | Classify URLs as phishing or legitimate |
| 1.4 | [Decision Trees](stage1_ml/4_decision_trees.md) | [4_decision_tree.py](stage1_ml/4_decision_tree.py) | Classify network traffic with readable rules |
| 1.5 | [Model Evaluation](stage1_ml/5_model_evaluation.md) | [5_model_evaluation.py](stage1_ml/5_model_evaluation.py) | Precision, recall, F1, ROC — what they actually mean |
| — | **Milestone** | [milestone_phishing.py](stage1_ml/milestone_phishing.py) | End-to-end phishing URL classifier |

---

## Module 2 — Intermediate ML
> **Goal:** Handle real-world messy data, build stronger models, and detect anomalies without labels

| # | Notes | Script | What You Learn |
|---|-------|--------|----------------|
| 2.1 | [Feature Engineering](stage2_intermediate/1_feature_engineering.md) | [1_feature_engineering.py](stage2_intermediate/1_feature_engineering.py) | Turn raw firewall logs into ML-ready features |
| 2.2 | [Random Forests](stage2_intermediate/2_random_forests.md) | [2_random_forest.py](stage2_intermediate/2_random_forest.py) | Malware classifier using an ensemble of trees |
| 2.3 | [Clustering & Anomaly Detection](stage2_intermediate/3_clustering_anomaly_detection.md) | [3_clustering.py](stage2_intermediate/3_clustering.py) | Find anomalous connections without any labels |
| 2.4 | [Overfitting & Cross-Validation](stage2_intermediate/4_overfitting_cross_validation.md) | [4_overfitting.py](stage2_intermediate/4_overfitting.py) | Know if your model will actually work on new data |
| — | **Milestone** | [milestone_intrusion.py](stage2_intermediate/milestone_intrusion.py) | Network intrusion detector on KDD Cup-style data |

---

## Module 3 — Neural Networks
> **Goal:** Build a neural network from a single neuron up, then use Keras for real security classification

**Lessons 3.1–3.8** build the network piece by piece using only NumPy — so you understand exactly what is happening before using a framework.
**Lessons 3.9–3.12** rebuild it in Keras and add depth, regularisation, and tuning.

| # | Script | What You Learn |
|---|--------|----------------|
| 3.1 | [p001 — Basic Neuron](stage3_neural_networks/foundations/p001-Basic-Neuron-3-inputs.py) | A single neuron with 3 inputs |
| 3.2 | [p002 — Neuron Layer](stage3_neural_networks/foundations/p002-Basic-Neuron-Layer.py) | A full layer of neurons |
| 3.3 | [p003 — Dot Product](stage3_neural_networks/foundations/p003-Dot-Product.py) | Vectorising with NumPy |
| 3.4 | [p004 — Layers as Classes](stage3_neural_networks/foundations/p004-Layers-and-Object.py) | Structuring layers as Python objects |
| 3.5 | [p005 — ReLU Activation](stage3_neural_networks/foundations/p005-ReLU-Activation.py) | Introducing non-linearity |
| 3.6 | [p006 — Softmax Activation](stage3_neural_networks/foundations/p006-Softmax-Activation.py) | Turning outputs into probabilities |
| 3.7 | [p007 — Cross-Entropy Loss](stage3_neural_networks/foundations/p007-Categorical-Cross-Entropy-Loss.py) | Measuring how wrong the model is |
| 3.8 | [p008 — Full Forward Pass](stage3_neural_networks/foundations/p008-Categorical-Cross-Entropy-Loss-applied.py) | Complete network with loss calculation |
| 3.9 | [9_first_neural_network.md](stage3_neural_networks/9_first_neural_network.md) · [1_first_neural_net.py](stage3_neural_networks/1_first_neural_net.py) | Rebuild in Keras — 10 lines |
| 3.10 | [10_dropout_and_regularisation.md](stage3_neural_networks/10_dropout_and_regularisation.md) · [2_deeper_network.py](stage3_neural_networks/2_deeper_network.py) | Dropout, batch norm, early stopping |
| 3.11 | [11_convolutional_networks.md](stage3_neural_networks/11_convolutional_networks.md) · [3_cnn.py](stage3_neural_networks/3_cnn.py) | CNNs — image analysis and malware visualisation |
| 3.12 | [12_hyperparameter_tuning.md](stage3_neural_networks/12_hyperparameter_tuning.md) · [4_hyperparameters.py](stage3_neural_networks/4_hyperparameters.py) | Learning rate, batch size, architecture |
| — | **Milestone** · [milestone_packets.py](stage3_neural_networks/milestone_packets.py) | Neural network packet classifier |

---

## Module 4 — Generative AI
> **Goal:** Understand how LLMs work, use pre-trained models, and build a RAG-based security assistant

| # | Notes | Script | What You Learn |
|---|-------|--------|----------------|
| 4.1 | [How LLMs Work](stage4_genai/1_how_llms_work.md) | [1_llm_concepts.py](stage4_genai/1_llm_concepts.py) | Tokens, embeddings, and next-token prediction |
| 4.2 | [HuggingFace Models](stage4_genai/2_huggingface_pretrained_models.md) | [2_huggingface.py](stage4_genai/2_huggingface.py) | Zero-shot ATT&CK classification, NER on threat reports |
| 4.3 | [The Claude API](stage4_genai/3_claude_api.md) | [3_claude_api.py](stage4_genai/3_claude_api.py) | Build a conversational threat intelligence assistant |
| 4.4 | [Retrieval-Augmented Generation](stage4_genai/4_retrieval_augmented_generation.md) | [4_rag.py](stage4_genai/4_rag.py) | Ground AI answers in your own security documents |
| — | **Milestone** | [milestone_security_assistant.py](stage4_genai/milestone_security_assistant.py) | Interactive Q&A over CVEs and threat reports |

---

## Repository Structure

```
├── stage1_ml/                  Module 1 — Classic ML
├── stage2_intermediate/        Module 2 — Intermediate ML
├── stage3_neural_networks/
│   └── foundations/            Lessons 3.1–3.8 (NumPy network)
├── stage4_genai/               Module 4 — Generative AI
└── README.md                   You are here
```
