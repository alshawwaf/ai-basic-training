# Exercise 1 — Unsupervised Framing

> Back to [1_lab_guide.md](1_lab_guide.md)

## What You Will Learn

- Why labels are often unavailable in security monitoring
- What clustering discovers (behavioural groups without predefined labels)
- Why normal behaviour clusters naturally into dense groups
- Why attacks appear as outliers far from any cluster centre

---

## Concept: The Unsupervised Setting

In supervised learning (Lessons 1.2–2.2), every training sample has a label. In the real world:
- Security analysts cannot label every network connection
- New attack types have no historical labels
- Zero-day exploits look nothing like past attacks

Unsupervised learning finds structure without labels. K-Means groups samples by similarity. The insight: normal traffic is **repetitive and predictable** — same devices, same services, same ports, day after day. This repetition creates dense clusters. Attacks are **unusual** — different traffic patterns, unexpected ports, abnormal volumes — and appear far from the dense normal clusters.

> **Want to go deeper?** [Anomaly detection (Wikipedia)](https://en.wikipedia.org/wiki/Anomaly_detection)

---

## Concept: Why Normal Behaviour Clusters

Imagine monitoring a corporate network:
- Web browsing: many connections, ~443, moderate bytes, short duration → cluster A
- File server access: internal IPs, large bytes, long duration → cluster B
- DNS: small packets, UDP, frequent, port 53 → cluster C

These patterns are stable and reproducible. Any connection that doesn't fit any of these known patterns is suspicious.

---

## Concept: The Dataset

The dataset has 3000 samples with the true labels hidden (simulating an unlabelled dataset). The features are the same network traffic features from Lesson 1.4, but this time we pretend we don't know which samples are benign vs attack.

---

## What Each Task Asks You to Do

### Task 1 — Load the Dataset (No Labels)
Create the dataset but pretend the labels don't exist. Print the shape of X (features only) and describe it.

### Task 2 — Show That "No Labels" Is Realistic
Print the feature distributions. Can you tell from looking at a scatter plot whether any sample is an attack? (Spoiler: not obviously — that's why we need ML.)

### Task 3 — Hypothesis: Normal Flows Form Clusters
Plot a 2D scatter of two features (connection_rate vs bytes_sent) coloured by the true label (reveal labels just for this diagnostic, not for training). Visually confirm that attacks and benign form separate regions.

### Task 4 (BONUS) — Describe What You Would Look For
Write 3 comments describing what cluster pattern you would expect if the dataset contains: DoS attacks, port scans, and data exfiltration alongside benign traffic.

---

## Expected Outputs

```
TASK 1 — Dataset (no labels used):
Shape: (3000, 6)
Features: connection_rate, bytes_sent, bytes_received, unique_dest_ports,
          duration_seconds, failed_connections

TASK 2 — Feature distributions:
All features look like a mix — can't easily separate by eye.

TASK 3 — Scatter plot (diagnostic):
Plot shows 4 natural groupings:
- Bottom-left cluster: low rate, moderate bytes (benign)
- Top-left cluster: very high rate, low bytes (DoS)
- Right cluster: low rate, high bytes_sent (exfil)
- Middle cluster: moderate rate, very low bytes (port_scan)
```

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Using labels during K-Means training | No longer unsupervised — defeats the purpose | Never pass labels to KMeans.fit() |
| Expecting perfect separation | Clusters will overlap with real data | Anomaly detection is probabilistic |
| Forgetting to scale before clustering | Large-scale features (bytes_sent) dominate distance calculations | Always scale before K-Means |

---

> Next: [exercise2_kmeans_and_visualisation.md](exercise2_kmeans_and_visualisation.md)
