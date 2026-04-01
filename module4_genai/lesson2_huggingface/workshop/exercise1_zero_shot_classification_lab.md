# Lab — Exercise 1: Zero-Shot Classification

> Follow each step in order. Copy the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `exercise1_zero_shot_classification.py` in this folder.

> First run downloads model weights (~550 MB). Subsequent runs use the local cache at `~/.cache/huggingface/`.

---

## Step 2: Add the imports and data

The `pipeline` function from the `transformers` library wraps the entire model behind a single callable. The log entries and labels are defined here so you can see at a glance what you are classifying.

```python
from transformers import pipeline

LOGS = [
    "Outbound LDAP connection to 185.219.47.33 immediately after encoded PowerShell execution on WORKSTATION-042",
    "User jsmith authenticated successfully from 10.0.1.50 at 09:15 — normal working hours",
    "nmap -sS -O scan detected from 10.0.1.200 targeting subnet 10.0.2.0/24",
    "Firewall rule updated by admin: allow port 443 outbound for all endpoints",
    "CPU utilisation 99% on DB-01 sustained for 45 minutes — no scheduled job running",
]

CANDIDATE_LABELS = ["malicious activity", "normal traffic", "configuration change", "system anomaly"]
```

---

## Step 3: Load the zero-shot classification pipeline

This single call downloads (first time) or loads (subsequent runs) the `facebook/bart-large-mnli` model, which was trained on Natural Language Inference and can assess how well any label fits any input text.

Add this to your file:

```python
classifier = pipeline("zero-shot-classification",
                      model="facebook/bart-large-mnli")

print("Model loaded. Ready to classify security logs.")
```

Run your file. You should see:
```
Model loaded. Ready to classify security logs.
```

---

## Step 4: Classify one log entry

`result["labels"]` and `result["scores"]` are sorted by confidence descending, so index 0 is always the top prediction.

Add this to your file:

```python
result = classifier(LOGS[0], candidate_labels=CANDIDATE_LABELS)
print(f"\nLog: {LOGS[0][:70]}...")
print(f"Top label: {result['labels'][0]} ({result['scores'][0]:.4f})")
```

Run your file. You should see (approximate scores):
```
Log: Outbound LDAP connection to 185.219.47.33 immediately after encoded...
Top label: malicious activity (0.9123)
```

---

## Step 5: Classify all 5 log entries

Looping over all logs with `enumerate` gives you a 1-based index for the output.

Add this to your file:

```python
print("\nClassifying all logs:")
for i, log in enumerate(LOGS, 1):
    result = classifier(log, candidate_labels=CANDIDATE_LABELS)
    print(f"Log {i}: {log[:65]}...")
    print(f"  → {result['labels'][0]} ({result['scores'][0]:.4f})")
```

Run your file. You should see (approximate scores):
```
Classifying all logs:
Log 1: Outbound LDAP connection to 185.219.47.33 immediately afte...
  → malicious activity (0.9123)
Log 2: User jsmith authenticated successfully from 10.0.1.50 at 0...
  → normal traffic (0.8234)
Log 3: nmap -sS -O scan detected from 10.0.1.200 targeting subnet...
  → malicious activity (0.7845)
Log 4: Firewall rule updated by admin: allow port 443 outbound for...
  → configuration change (0.7231)
Log 5: CPU utilisation 99% on DB-01 sustained for 45 minutes — no...
  → system anomaly (0.6512)
```

---

## Step 6: Multi-label mode (Bonus Task 4)

With `multi_label=True` each label is scored independently rather than via softmax, so scores no longer sum to 1. This is useful when a log entry could fit multiple categories simultaneously.

Add this to your file:

```python
print("\nMulti-label classification for Log 5 (CPU spike):")
result_ml = classifier(LOGS[4], candidate_labels=CANDIDATE_LABELS, multi_label=True)
for label, score in zip(result_ml["labels"], result_ml["scores"]):
    print(f"  {label:<25} {score:.4f}")

print("\n--- Exercise 1 complete. Move to exercise2_sentence_embeddings.py ---")
```

Run your file. You should see all four labels with independent scores (note they no longer sum to 1.0):
```
Multi-label classification for Log 5 (CPU spike):
  system anomaly            0.7234
  malicious activity        0.4512
  normal traffic            0.1023
  configuration change      0.0812

--- Exercise 1 complete. Move to exercise2_sentence_embeddings.py ---
```

---

## Your completed script

At this point your file contains all the working code. Compare it against `reference_solution.py` if anything looks different.
