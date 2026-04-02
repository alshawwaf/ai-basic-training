# Lesson 4.2 — HuggingFace Pre-trained Models

---

## Concept: Use What Already Exists

Training a transformer model from scratch would require months of compute time and billions of tokens. You don't need to do that.

HuggingFace hosts thousands of pre-trained models you can load and use in a few lines of code — or fine-tune on your own security data in hours.

---

## The Pipeline API

The simplest way to use a pre-trained model. Say you have a string of text — a log line, a threat report excerpt, anything — and you want to run it through a classifier without training anything. Three lines:

```python
from transformers import pipeline

# Load a sentiment classifier
classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")
result = classifier("This threat intelligence report is alarming.")
# [{'label': 'NEGATIVE', 'score': 0.98}]
```

HuggingFace handles tokenisation, model loading, and post-processing automatically.

---

## Tasks Available Out-of-the-Box

| Task | Pipeline name | Security use |
|------|--------------|--------------|
| Text classification | `text-classification` | Classify log severity, phishing detection |
| Named entity recognition | `ner` | Extract IPs, CVEs, malware names from reports |
| Summarisation | `summarization` | Summarise threat intel reports |
| Question answering | `question-answering` | Extract answers from policy documents |
| Zero-shot classification | `zero-shot-classification` | Classify text into custom categories without training |

---

## Zero-Shot Classification (Powerful for Security)

Classify text into *any* categories — no training data needed. Say you have a raw SIEM alert and want to map it to a MITRE ATT&CK tactic without any labelled training data. Define your categories at call time and the model figures out the best fit:

```python
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

result = classifier(
    "Lateral movement detected: SMB connections to 15 internal hosts from workstation",
    candidate_labels=["lateral movement", "data exfiltration", "persistence", "normal traffic"]
)
# Labels sorted by confidence
```

This can turn any security log line into a structured MITRE ATT&CK tactic classification.

---

## Named Entity Recognition (NER) for Threat Intel

Extract structured IOCs from unstructured threat reports. Say you have a paragraph of threat intel text and you want to pull out the actor names, IP addresses, and CVE numbers automatically — without writing any regex:

```python
ner = pipeline("ner", grouped_entities=True)
result = ner("The Lazarus Group used 192.168.1.1 and CVE-2021-44228 in the attack.")
# Extracts: ORG: Lazarus Group, IP: 192.168.1.1, ...
```

---

## What to Notice When You Run It

1. How fast inference is vs training (seconds vs hours)
2. The confidence scores on each prediction
3. Zero-shot performance on security-specific text — no fine-tuning at all
4. NER on a sample threat intelligence report

---

## Next Lesson

**[Lesson 4.3 — The Claude API](../03_llm_api/README.md):** Move from fixed pipelines to a conversational AI you can direct with natural language instructions.

---

## Ready for the Workshop?

You have covered the concepts. Now build it yourself.

**[Open README.md](README.md)**

---

## What This Workshop Covers

You will use HuggingFace's `transformers` and `sentence-transformers` libraries to apply pre-trained models without training anything from scratch. Starting with zero-shot classification on security logs, you will progress to semantic similarity search — the foundation of all modern RAG systems.

Work through them in order — each exercise builds on the previous.

---

## Exercise Overview

| # | Guide | Lab | Topic |
|---|-------|---------------|-------|
| 1 | [lecture.md](1_zero_shot_classification/lecture.md) | [handson.md](1_zero_shot_classification/handson.md) | Classify security logs with no training — zero-shot NLI pipeline |
| 2 | [lecture.md](2_sentence_embeddings/lecture.md) | [handson.md](2_sentence_embeddings/handson.md) | Encode sentences as vectors; cosine similarity; semantic distance |
| 3 | [lecture.md](3_semantic_search/lecture.md) | [handson.md](3_semantic_search/handson.md) | Build a semantic search engine over a security knowledge base |

**For each exercise:** read the guide first, then open the matching `_handson.md` file and follow the steps.

## Setup

```bash
pip install transformers sentence-transformers torch
```

## Running an Exercise

```bash
cd "C:/Users/admin/Desktop/AI Basic Training"
python stage4_genai/02_huggingface/1_zero_shot_classification/solution_huggingface.py
```

## Tips

- First run downloads model weights (~200MB–500MB) — subsequent runs are instant (cached)
- If internet is slow, use lighter models: `typeform/distilbart-mnli-12-1` for Exercise 1, `paraphrase-MiniLM-L3-v2` for Exercise 2
- All exercises work on CPU — no GPU required

## After This Workshop

Move to [Lesson 4.3 — LLM API](../../03_llm_api/README.md)
