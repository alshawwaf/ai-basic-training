# =============================================================================
# LESSON 4.2 | WORKSHOP | Exercise 1 of 3
# Zero-Shot Classification
# =============================================================================
# WHAT YOU WILL LEARN
# -------------------
# - How to classify text with labels defined at inference time (no training)
# - How HuggingFace pipelines abstract model complexity to a single function call
# - Practical zero-shot classification on security log entries
#
# RUN THIS FILE
# -------------
#   python module4_genai/lesson2_huggingface/workshop/exercise1_zero_shot_classification.py
#
# FIRST RUN: downloads model weights (~500MB) — subsequent runs use local cache
# =============================================================================

from transformers import pipeline

# Security log entries for classification
LOGS = [
    "Outbound LDAP connection to 185.219.47.33 immediately after encoded PowerShell execution on WORKSTATION-042",
    "User jsmith authenticated successfully from 10.0.1.50 at 09:15 — normal working hours",
    "nmap -sS -O scan detected from 10.0.1.200 targeting subnet 10.0.2.0/24",
    "Firewall rule updated by admin: allow port 443 outbound for all endpoints",
    "CPU utilisation 99% on DB-01 sustained for 45 minutes — no scheduled job running",
]

CANDIDATE_LABELS = ["malicious activity", "normal traffic", "configuration change", "system anomaly"]

# =============================================================================
# BACKGROUND
# =============================================================================
# Zero-shot classification uses Natural Language Inference (NLI):
#   Premise:    the log entry you want to classify
#   Hypothesis: "This is an example of [candidate_label]"
#   Score:      how strongly does the log ENTAIL the hypothesis?
#
# Best model:   facebook/bart-large-mnli  (~550MB, high accuracy)
# Lighter alt:  typeform/distilbart-mnli-12-1  (~250MB, slightly lower accuracy)

# =============================================================================
# TASK 1 — Load the zero-shot classification pipeline
# =============================================================================
# Create:
#   classifier = pipeline("zero-shot-classification",
#                         model="facebook/bart-large-mnli")
#
# Print: "Model loaded. Ready to classify security logs."
#
# EXPECTED OUTPUT:
#   Model loaded. Ready to classify security logs.

# >>> YOUR CODE HERE


# =============================================================================
# TASK 2 — Classify one log entry
# =============================================================================
# Run: result = classifier(LOGS[0], candidate_labels=CANDIDATE_LABELS)
#
# The result dict has:
#   result["labels"]  → list of labels sorted by score descending
#   result["scores"]  → corresponding confidence scores
#
# Print:
#   Log: [first 70 chars of LOGS[0]]
#   Top label: malicious activity (0.9123)
#
# EXPECTED OUTPUT (approximate):
#   Log: Outbound LDAP connection to 185.219.47.33 immediately after encoded...
#   Top label: malicious activity (0.9123)

# >>> YOUR CODE HERE


# =============================================================================
# TASK 3 — Classify all 5 log entries
# =============================================================================
# Loop over all LOGS (use enumerate for numbering).
# For each log:
#   - Run classifier(log, candidate_labels=CANDIDATE_LABELS)
#   - Print: "Log N: [first 65 chars]..."
#   - Print: "  → [top label] ([score:.4f])"
#
# EXPECTED OUTPUT (approximate):
#   Log 1: Outbound LDAP connection to 185.219.47.33 immediately afte...
#     → malicious activity (0.9123)
#   Log 2: User jsmith authenticated successfully from 10.0.1.50 at 0...
#     → normal traffic (0.8234)
#   Log 3: nmap -sS -O scan detected from 10.0.1.200 targeting subnet...
#     → malicious activity (0.7845)
#   Log 4: Firewall rule updated by admin: allow port 443 outbound for...
#     → configuration change (0.7231)
#   Log 5: CPU utilisation 99% on DB-01 sustained for 45 minutes — no...
#     → system anomaly (0.6512)

# >>> YOUR CODE HERE


# =============================================================================
# TASK 4 — Multi-label mode (BONUS)
# =============================================================================
# Run the classifier on LOGS[4] (CPU spike) with multi_label=True.
# Print ALL labels and their scores.
# Compare to single-label results — what changes?
#
# multi_label=True  → scores are independent (each label scored separately, not softmax)
# multi_label=False → scores sum to 1.0 via softmax (mutually exclusive)

# >>> YOUR CODE HERE


print("\n--- Exercise 1 complete. Move to exercise2_sentence_embeddings.py ---")
