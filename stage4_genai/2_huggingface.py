# Lesson 4.2 — HuggingFace Pre-trained Models
#
# Use transformer models out-of-the-box — no training required.
# Tasks demonstrated:
#   - Sentiment analysis on threat reports
#   - Zero-shot classification → MITRE ATT&CK tactic detection
#   - Named entity recognition → IOC extraction from text
#   - Summarisation of threat intelligence
#
# pip install transformers torch (or transformers[torch])

from transformers import pipeline
import json

print("=" * 60)
print("  LESSON 4.2: HUGGINGFACE PRE-TRAINED MODELS")
print("=" * 60)
print("Note: First run downloads model weights (~250MB). Cached after that.\n")

# ── 1. Sentiment / urgency classification ─────────────────────────────────────
print("── 1. Sentiment Analysis on Security Alerts ──")
# Repurpose a sentiment model to score urgency of alerts
# (positive = calm/resolved, negative = alarming/urgent)

try:
    sentiment = pipeline(
        "text-classification",
        model="distilbert-base-uncased-finetuned-sst-2-english"
    )

    alerts = [
        "Critical: Active ransomware deployment detected on 47 endpoints. Immediate response required.",
        "Routine: Weekly vulnerability scan completed. No critical findings.",
        "WARNING: Unusual outbound traffic to known C2 infrastructure detected.",
        "INFO: Scheduled maintenance window completed successfully.",
        "ALERT: Brute force attack detected — 5000 failed login attempts in 2 minutes.",
    ]

    print("\nAlert urgency classification (NEGATIVE = alarming):")
    for alert in alerts:
        result = sentiment(alert[:512])[0]
        urgency = "🔴 HIGH" if result['label'] == 'NEGATIVE' else "🟢 LOW"
        print(f"\n  [{urgency}] Score: {result['score']:.3f}")
        print(f"  {alert[:80]}")

except Exception as e:
    print(f"Sentiment model error: {e}")

# ── 2. Zero-shot classification → MITRE ATT&CK tactic detection ───────────────
print("\n\n── 2. Zero-Shot MITRE ATT&CK Tactic Classification ──")
print("(No training data needed — model generalises from its pre-training)")

try:
    zsc = pipeline(
        "zero-shot-classification",
        model="facebook/bart-large-mnli"
    )

    # MITRE ATT&CK tactics
    tactics = [
        "Initial Access",
        "Execution",
        "Persistence",
        "Privilege Escalation",
        "Defense Evasion",
        "Credential Access",
        "Discovery",
        "Lateral Movement",
        "Collection",
        "Exfiltration",
        "Command and Control",
    ]

    log_entries = [
        "User account created with administrator privileges after hours",
        "PowerShell script downloaded and executed from remote URL",
        "SMB connections established to 23 internal hosts from compromised workstation",
        "Large volume of files copied to USB device by privileged user",
        "LSASS memory access detected by Mimikatz-like tool",
        "Phishing email with malicious attachment opened by finance team",
    ]

    print(f"\nClassifying log entries into MITRE ATT&CK tactics:")
    for entry in log_entries:
        result = zsc(entry, candidate_labels=tactics, multi_label=False)
        top = result['labels'][0]
        score = result['scores'][0]
        print(f"\n  Log: {entry[:70]}")
        print(f"  → Tactic: {top}  (confidence: {score:.3f})")
        # Show top 3
        for label, score in zip(result['labels'][:3], result['scores'][:3]):
            bar = '█' * int(score * 20)
            print(f"    {score:.3f} {bar} {label}")

except Exception as e:
    print(f"Zero-shot model error: {e}")

# ── 3. Named Entity Recognition — IOC extraction ──────────────────────────────
print("\n\n── 3. Named Entity Recognition — Extract IOCs from Threat Intel ──")

try:
    ner = pipeline("ner", model="dslim/bert-base-NER", grouped_entities=True)

    threat_reports = [
        "The Lazarus Group, linked to North Korea, used spear phishing emails targeting employees at aerospace companies in the United States and Israel.",
        "APT29 (Cozy Bear) has been observed exploiting vulnerabilities in Microsoft Exchange servers to gain initial access.",
        "Conti ransomware gang deployed their payload across the NHS network affecting hospitals in London and Birmingham.",
    ]

    print("\nExtracting named entities from threat intelligence reports:")
    for report in threat_reports:
        print(f"\n  Report: {report[:100]}...")
        entities = ner(report)
        if entities:
            for ent in entities:
                print(f"    [{ent['entity_group']:4}] '{ent['word']}' (score: {ent['score']:.3f})")
        else:
            print("    No named entities found")

except Exception as e:
    print(f"NER model error: {e}")

# ── 4. Summarisation of threat report ─────────────────────────────────────────
print("\n\n── 4. Automatic Threat Report Summarisation ──")

try:
    summariser = pipeline("summarization", model="facebook/bart-large-cnn")

    long_report = """
    A sophisticated threat actor group tracked as APT-X has been conducting targeted
    intrusion campaigns against critical infrastructure organisations in the energy sector
    since at least January 2024. The group leverages spear phishing emails with weaponised
    attachments to gain initial access. Once inside, they deploy a custom backdoor that
    communicates over HTTPS to command-and-control infrastructure hosted on compromised
    legitimate websites. The group has demonstrated advanced lateral movement capabilities,
    using legitimate tools such as PsExec and WMI for internal propagation. Observed
    targets include power generation facilities, oil refineries, and water treatment plants
    across Europe and North America. The group shows particular interest in operational
    technology (OT) networks and SCADA systems. Attribution is moderate-confidence to a
    nation-state actor based on TTPs, infrastructure patterns, and targeting priorities
    consistent with strategic intelligence collection rather than financial motivation.
    """

    summary = summariser(long_report.strip(), max_length=80, min_length=30, do_sample=False)
    print(f"\nOriginal: {len(long_report.split())} words")
    print(f"Summary : {summary[0]['summary_text']}")

except Exception as e:
    print(f"Summarisation model error: {e}")

print("\n" + "=" * 60)
print("All HuggingFace demos complete.")
print("Next: Lesson 4.3 — Building with the Claude API for more flexible, conversational AI.")
