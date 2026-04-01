# Exercise 1 — Zero-Shot Classification

> Read this guide fully before opening the exercise file.

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

---

## Concept: How It Works — Natural Language Inference

Zero-shot classification uses **Natural Language Inference (NLI)**:

```
Premise:    "Outbound connection to suspicious IP after powershell"
Hypothesis: "This is an example of malicious activity"
→ Model predicts: ENTAILMENT (0.87) / NEUTRAL (0.09) / CONTRADICTION (0.04)
```

The entailment score becomes the classification probability. This works because NLI models were trained to reason about whether one statement follows from another.

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

## Expected Outputs at a Glance

**Task 3**
```
Log 1: Outbound LDAP connection to 185.219.47.33 immediately...
  → malicious activity (0.9123)

Log 2: User jsmith authenticated successfully from 10.0.1.50...
  → normal traffic (0.8234)

Log 3: nmap -sS -O scan detected from 10.0.1.200 targeting...
  → malicious activity (0.7845)

Log 4: Firewall rule updated by admin: allow port 443 outbound...
  → configuration change (0.7231)

Log 5: CPU utilisation 99% on DB-01 sustained for 45 minutes...
  → system anomaly (0.6512)
```

(Exact scores vary by model version.)

---

## Common Mistakes

**`OSError: We couldn't connect to huggingface.co`**
You need internet for the first download. After that, models are cached locally at `~/.cache/huggingface/`.

**Download too slow**
Use the lighter model: `model="typeform/distilbart-mnli-12-1"` (~250MB vs ~550MB). Accuracy is slightly lower.

**Results seem wrong**
Descriptive labels work better than generic ones. "malicious network activity" outperforms "bad". Try rephrasing.

---

## Now Open the Exercise File

[exercise1_zero_shot_classification.py](exercise1_zero_shot_classification.py)

---

## Next

[exercise2_sentence_embeddings.md](exercise2_sentence_embeddings.md) — encode sentences as vectors and measure semantic similarity.
