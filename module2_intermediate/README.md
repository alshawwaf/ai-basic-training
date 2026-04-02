# Module 2 — Intermediate Machine Learning

## Goal
Handle real-world messiness: engineer features from raw logs, build more powerful models, detect overfitting, and work with unsupervised data.

---

## What's New in Module 2

| Concept | Why it matters |
|---------|---------------|
| Feature engineering | Raw logs are useless to ML — you must extract signal |
| Random Forests | More powerful and robust than a single decision tree |
| Unsupervised learning | Detect anomalies without labelled attack data |
| Cross-validation | Reliably measure model performance without overfitting your evaluation |

---

## Key Idea: Most Security Data Is Unlabelled

In Stage 1, every sample had a label (attack / benign). In the real world, you often don't have labels. No one has hand-labelled every connection in your firewall logs.

This is where **unsupervised learning** comes in — the model finds unusual patterns without needing to be told what an attack looks like.

---

## Lessons

### Lesson 2.1 — [Feature Engineering](lesson1_feature_engineering/notes.md)
**Workshop:** [lesson1_feature_engineering/workshop/00_overview.md](lesson1_feature_engineering/workshop/00_overview.md)
Turn raw log lines into ML-ready numerical features.

### Lesson 2.2 — [Random Forests](lesson2_random_forests/notes.md)
**Workshop:** [lesson2_random_forests/workshop/00_overview.md](lesson2_random_forests/workshop/00_overview.md)
Ensemble of decision trees — more accurate and less prone to overfitting.

### Lesson 2.3 — [Clustering & Anomaly Detection](lesson3_clustering_anomaly/notes.md)
**Workshop:** [lesson3_clustering_anomaly/workshop/00_overview.md](lesson3_clustering_anomaly/workshop/00_overview.md)
Find anomalous network behaviour without needing attack labels.

### Lesson 2.4 — [Overfitting & Cross-Validation](lesson4_overfitting_crossval/notes.md)
**Workshop:** [lesson4_overfitting_crossval/workshop/00_overview.md](lesson4_overfitting_crossval/workshop/00_overview.md)
Reliably estimate real-world model performance.

### Milestone — [Network Intrusion Detector](milestone/milestone_intrusion.py)
**Script:** [milestone/milestone_intrusion.py](milestone/milestone_intrusion.py)
Full pipeline on KDD Cup-style network intrusion data.

---

## Dependencies

```bash
pip install pandas scikit-learn matplotlib seaborn
```
