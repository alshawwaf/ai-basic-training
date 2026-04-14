# Zero-Shot Classification

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

**Zero-shot classification — pipeline at a glance**

| Stage | What it is | Example value |
|---|---|---|
| 1. Input text | the document you want to classify | `"Outbound connection from workstation to 185.234.219.47:443 after powershell execution"` |
| 2. Candidate labels | the classes you invent at inference time | `["malicious activity", "normal traffic", "configuration change"]` |
| 3. NLI scoring | BART-large-MNLI asks "does the text entail each label?" | one entailment score per label |
| 4. Result | labels ranked by entailment score | see below |

| Label | Score | |
|---|---:|---|
| malicious activity | 0.87 | ← top |
| normal traffic | 0.09 | |
| configuration change | 0.04 | |

<div class="lecture-visual">
  <img src="/static/lecture_assets/gn_zeroshot_pipeline.png" alt="A four-stage pipeline diagram. Left grey 'INPUT TEXT' box contains a security log entry about an outbound connection. Below it an orange 'CANDIDATE LABELS' box lists three labels invented at inference time: 'malicious activity', 'normal traffic', 'configuration change'. Both flow into a central cyan 'BART-large MNLI' box that asks 'for each label, does the text entail it?'. An arrow then leads to a green 'RANKED RESULT' box on the right showing 'malicious activity 0.87' (highlighted as winner), 'normal traffic 0.09', 'configuration change 0.04'.">
  <div class="vis-caption">The full zero-shot classification pipeline in one picture. The novel part is that the candidate labels are invented at inference time — the model never trained on them. NLI scoring asks "does this text entail this label as a hypothesis?" once per label, and the entailment scores become the classification probabilities.</div>
</div>

---

## Concept: How It Works — Natural Language Inference

Zero-shot classification uses **Natural Language Inference (NLI)**:

```
Premise:    "Outbound connection to suspicious IP after powershell"
Hypothesis: "This is an example of malicious activity"
→ Model predicts: ENTAILMENT (0.87) / NEUTRAL (0.09) / CONTRADICTION (0.04)
```

The entailment score becomes the classification probability. This works because NLI models were trained to reason about whether one statement follows from another.

**NLI scoring — what the model actually computes for one label**

| Field | Value |
|---|---|
| Premise | `"Outbound connection to suspicious IP after powershell"` |
| Hypothesis | `"This is an example of malicious activity"` |

| NLI prediction | Score | Used as |
|---|---:|---|
| **ENTAILMENT** | 0.87 | the classification score for this label |
| NEUTRAL | 0.09 | discarded |
| CONTRADICTION | 0.04 | discarded |

The pipeline runs this NLI step once per candidate label, then ranks the labels by their entailment scores.

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
