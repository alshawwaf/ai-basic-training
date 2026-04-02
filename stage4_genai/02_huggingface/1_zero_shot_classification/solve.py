# Exercise 1 — Zero-Shot Classification
#
# Uses a HuggingFace NLI model to classify security log entries into
# categories you define at inference time -- no training data needed.
# The model generalises from its pre-training on natural language inference.
#
# pip install transformers torch

from transformers import pipeline

# ============================================================
#   TASK 1: Load the zero-shot classification pipeline
# ============================================================
print("=" * 60)
print("  TASK 1: Load the Pipeline")
print("=" * 60)

# facebook/bart-large-mnli is trained on Natural Language Inference (NLI).
# It decides whether a hypothesis ("this is malicious activity") is
# entailed by the premise (the log entry). The entailment score becomes
# the classification probability.
print("\nLoading facebook/bart-large-mnli (downloads ~550MB on first run)...")
classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli",
)
print("Pipeline loaded successfully.")


# ============================================================
#   TASK 2: Classify one log entry
# ============================================================
print("\n" + "=" * 60)
print("  TASK 2: Classify One Log Entry")
print("=" * 60)

# Three candidate labels -- the model has never seen these during training
candidate_labels = ["malicious activity", "normal traffic", "configuration change"]

log_entry = "Outbound LDAP connection to 185.219.47.33 immediately after encoded PowerShell execution"

result = classifier(log_entry, candidate_labels=candidate_labels, multi_label=False)

print(f"\nLog: {log_entry}")
print(f"Top label: {result['labels'][0]}  (confidence: {result['scores'][0]:.4f})")
print("\nAll labels ranked:")
for label, score in zip(result["labels"], result["scores"]):
    bar = "#" * int(score * 30)
    print(f"  {score:.4f} {bar} {label}")


# ============================================================
#   TASK 3: Classify 5 log entries
# ============================================================
print("\n" + "=" * 60)
print("  TASK 3: Classify 5 Log Entries")
print("=" * 60)

# Broader label set to cover more scenarios
labels = [
    "malicious activity",
    "normal traffic",
    "configuration change",
    "system anomaly",
    "authentication event",
]

log_entries = [
    "Outbound LDAP connection to 185.219.47.33 immediately after encoded PowerShell execution",
    "User jsmith authenticated successfully from 10.0.1.50 via single sign-on",
    "nmap -sS -O scan detected from 10.0.1.200 targeting the DMZ subnet",
    "Firewall rule updated by admin: allow port 443 outbound for proxy servers",
    "CPU utilisation 99% on DB-01 sustained for 45 minutes with no scheduled jobs",
]

print(f"\nClassifying {len(log_entries)} log entries into {len(labels)} categories:\n")
for i, entry in enumerate(log_entries, 1):
    result = classifier(entry, candidate_labels=labels, multi_label=False)
    top_label = result["labels"][0]
    top_score = result["scores"][0]
    print(f"  Log {i}: {entry[:70]}...")
    print(f"    -> {top_label} ({top_score:.4f})")
    # Show top 3 labels
    for label, score in zip(result["labels"][:3], result["scores"][:3]):
        bar = "#" * int(score * 20)
        print(f"       {score:.3f} {bar} {label}")
    print()


# ============================================================
#   TASK 4 (Bonus): Multi-label mode
# ============================================================
print("=" * 60)
print("  TASK 4 (Bonus): Multi-Label Classification")
print("=" * 60)

# multi_label=True: each label is scored independently.
# A log entry can belong to multiple categories simultaneously.
# In single-label mode, scores sum to 1.0; in multi-label mode they don't.
multi_entry = "Brute force SSH attack detected: 5000 failed logins from 45.33.32.156 in 2 minutes"

print(f"\nLog: {multi_entry}\n")

single_result = classifier(multi_entry, candidate_labels=labels, multi_label=False)
multi_result = classifier(multi_entry, candidate_labels=labels, multi_label=True)

print("Single-label mode (scores sum to ~1.0):")
for label, score in zip(single_result["labels"], single_result["scores"]):
    print(f"  {score:.4f}  {label}")
print(f"  Sum: {sum(single_result['scores']):.4f}")

print("\nMulti-label mode (each label scored independently):")
for label, score in zip(multi_result["labels"], multi_result["scores"]):
    print(f"  {score:.4f}  {label}")
print(f"  Sum: {sum(multi_result['scores']):.4f}")

print("\nKey difference: multi-label allows an entry to be flagged as")
print("both 'malicious activity' AND 'authentication event' simultaneously.")

print("\n--- Exercise 1 complete. Move to ../2_sentence_embeddings/solve.py ---")
