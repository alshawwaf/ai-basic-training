# Exercise 1 — Zero-Shot Classification

> Read this guide fully before opening the lab.

---

## What You Will Learn

- What zero-shot classification is and why it matters for security
- How the HuggingFace pipeline API works in one line of code
- How to classify text with candidate labels defined at inference time
- The limitations of zero-shot vs fine-tuned models

---

## Concept: Zero-Shot Classification

Traditional classification requires labelled training data for each class. Zero-shot classification lets you define classes at inference time — no training required:

```python
from transformers import pipeline

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

result = classifier(
    "Outbound connection from workstation to 185.234.219.47:443 after powershell execution",
    candidate_labels=["malicious activity", "normal traffic", "configuration change"]
)
# result["labels"][0]  → "malicious activity"
# result["scores"][0]  → 0.87
```

The model has never seen your labels before. It uses its general understanding of language to assess how well each label fits the input text.

```
Zero-Shot Classification Flow
──────────────────────────────────────────────────────────────

 Input text                       Candidate labels
 "Outbound connection from         "malicious activity"
  workstation to 185.234..."       "normal traffic"
                                   "configuration change"
               │                            │
               ▼                            ▼
            NLI Model (BART-large-MNLI)
            "does text entail each label?"
                        │
                        ▼

 | Label              | Score |       |
 |--------------------|-------|-------|
 | malicious activity | 0.87  | ← top |
 | normal traffic     | 0.09  |       |
 | config change      | 0.04  |       |
```

---

## Concept: How It Works — Natural Language Inference

Zero-shot classification uses **Natural Language Inference (NLI)**:

```
Premise:    "Outbound connection to suspicious IP after powershell"
Hypothesis: "This is an example of malicious activity"
→ Model predicts: ENTAILMENT (0.87) / NEUTRAL (0.09) / CONTRADICTION (0.04)
```

The entailment score becomes the classification probability. This works because NLI models were trained to reason about whether one statement follows from another.

```
NLI Scoring for one label
──────────────────────────────────────────────────────
 Premise:    "Outbound connection to suspicious IP..."
 Hypothesis: "This is an example of malicious activity"
                           │
                           ▼
                      NLI Model
                           │
                           ▼

 | Prediction     | Score | Note                  |
 |----------------|-------|-----------------------|
 | ENTAILMENT     | 0.87  | → score for this label |
 | NEUTRAL        | 0.09  |                       |
 | CONTRADICTION  | 0.04  |                       |
```

---

## Concept: Security Use Cases

| Task | Candidate labels |
|------|----------------|
| Log triage | ["attack", "normal", "error", "maintenance"] |
| Phishing detection | ["phishing", "legitimate", "spam"] |
| Malware family | ["ransomware", "trojan", "adware", "spyware", "worm"] |
| Incident severity | ["critical", "high", "medium", "low", "informational"] |
| MITRE tactic | ["initial access", "lateral movement", "persistence", "exfiltration"] |

---

## What Each Task Asks You to Do

### Task 1 — Load the pipeline
Load `facebook/bart-large-mnli` as a `zero-shot-classification` pipeline. Print a confirmation.

### Task 2 — Classify one log entry
Classify one security log entry with 3 candidate labels. Print the top label and its score.

### Task 3 — Classify 5 log entries
Loop over 5 log entries. For each, print the truncated log, top label, and confidence.

### Task 4 — Multi-label mode (Bonus)
Use `multi_label=True` to allow multiple labels simultaneously. Compare scores with single-label mode.

---

## Common Mistakes

**`OSError: We couldn't connect to huggingface.co`**
You need internet for the first download. After that, models are cached locally at `~/.cache/huggingface/`.

**Download too slow**
Use the lighter model: `model="typeform/distilbart-mnli-12-1"` (~250MB vs ~550MB). Accuracy is slightly lower.

**Results seem wrong**
Descriptive labels work better than generic ones. "malicious network activity" outperforms "bad". Try rephrasing.

---

## Now Open the Lab

[handson.md](handson.md)
## Next

[../2_sentence_embeddings/lecture.md](../2_sentence_embeddings/lecture.md) — encode sentences as vectors and measure semantic similarity.
