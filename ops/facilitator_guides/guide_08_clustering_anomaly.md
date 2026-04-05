# Facilitator Guide — Session 2.3: Clustering & Anomaly Detection

> **Stage:** 2  |  **Week:** 6  |  **Lecture deck:** `Lecture-8-Clustering-Anomaly-Detection.pptx`  |  **Total time:** 60 min

---

## Pre-Session Checklist

- [ ] Reviewed the lecture slides and all 4 exercise guides
- [ ] Run through the k-means visualisation exercise — confirmed cluster plots render correctly with distinct colours
- [ ] Prepared an explanation of unsupervised vs supervised learning using a security scenario (monitoring without labels)
- [ ] Reviewed the elbow method and can explain why the "elbow" indicates diminishing returns

---

## Session Flow

| Time | Section | Activity |
|------|---------|----------|
| 0:00 – 0:05 | Bridge | "Every model so far needed labels — malicious or benign. What happens when you have no labels? When the attack is something you've never seen before? Today we learn to find structure without being told what to look for." |
| 0:05 – 0:15 | Supervised vs unsupervised | Draw two columns on the whiteboard: supervised (labels required, predicts known categories) vs unsupervised (no labels, discovers structure). Walk through Exercise 1 concepts: why labels are often unavailable in security monitoring. Ask: "How much of your network traffic is actually labelled?" |
| 0:15 – 0:25 | K-means step by step | Walk through the k-means algorithm: place k centroids randomly, assign each point to the nearest centroid, recompute centroids as the mean of assigned points, repeat. Draw 3-4 iterations on the whiteboard showing centroids moving. Emphasise: normal traffic clusters tightly, anomalies sit far from any centroid. |
| 0:25 – 0:35 | Elbow method and choosing k | "How do you pick k?" Show the elbow plot: inertia drops as k increases, but the rate of improvement slows. The "elbow" is where adding more clusters gives diminishing returns. Demo Exercise 3 live — project the elbow plot and ask the group to identify the bend. |
| 0:35 – 0:50 | Hands-on exercises | Participants work through Exercises 2-4: k-means and visualisation, choosing k, anomaly scoring. Circulate and help — the anomaly scoring exercise is the most conceptually important. |
| 0:50 – 0:55 | Anomaly detection discussion | Reconvene. Ask: "In Exercise 4, which points had the highest anomaly scores? Were they far from all clusters or between clusters?" Discuss: distance from nearest centroid as a proxy for "unusualness." Connect to real-world security: insider threats, lateral movement, and zero-day attacks all appear as outliers. |
| 0:55 – 1:00 | Wrap-up | Preview Session 2.4 (overfitting and cross-validation). Key bridge: "We've now built supervised and unsupervised models. But how do we know they'll work on data they haven't seen? Next session we tackle the hardest problem in ML: making sure your model generalises." |

---

## Key Points to Emphasise

1. **Unsupervised learning finds what you didn't know to look for** — supervised models catch known attack types. Clustering and anomaly detection surface unknown unknowns: unusual behaviour patterns that no analyst labelled and no signature matches. This is the foundation of behavioural analytics in modern security products.
2. **Normal behaviour is repetitive; attacks are unusual** — corporate network traffic follows predictable patterns: same services, same ports, same time windows. K-means exploits this by grouping normal behaviour into dense clusters. Anything far from all clusters — high anomaly score — deserves investigation. The model doesn't need to know what an attack looks like; it only needs to know what normal looks like.
3. **Choosing k is a judgment call, not a formula** — the elbow method gives guidance, but the "right" k depends on how many distinct behaviour groups exist in your environment. Too few clusters lump different normal behaviours together (masking anomalies within a cluster). Too many clusters overfit to noise. Security teams typically iterate: start with the elbow, examine the clusters, adjust.

---

## Discussion Prompts

- "Your k-means model clusters all network traffic into 5 groups. Cluster 3 contains only 0.2% of connections. Is cluster 3 an anomaly cluster? What would you do with those connections?"
- "Darktrace markets itself as detecting threats 'without signatures or rules' using unsupervised learning. Based on what you've learned today, what is it actually doing? What are its limitations?"
- "An insider threat — a trusted employee slowly exfiltrating data over weeks — might look normal on any single day. How would you design features so that k-means can detect the slow drift?"

---

## Common Questions and Answers

**Q: If k-means doesn't know what attacks look like, how can it detect them?**
A: K-means doesn't detect attacks directly. It learns what normal looks like — the dense clusters of routine behaviour. Anything that doesn't fit the normal clusters (high distance from all centroids) gets flagged as anomalous. An analyst then investigates the anomaly. The model surfaces the unusual; the human determines whether it's malicious. This is why anomaly detection generates investigation leads, not definitive verdicts.

**Q: Why not just use supervised learning with labelled attack data?**
A: Supervised learning only catches attack types present in the training data. If a new attack variant emerges that doesn't match any trained label, supervised models miss it. Unsupervised anomaly detection catches anything unusual, regardless of whether it matches a known pattern. In practice, mature security operations use both: supervised models for known threats and unsupervised models for unknown threats. They are complementary, not competing approaches.

**Q: K-means seems simple. Do real security products actually use it?**
A: K-means itself is a building block. Production systems often use more sophisticated clustering (DBSCAN, Gaussian mixture models) or isolation forests for anomaly detection. But the core principle is identical: learn the shape of normal behaviour, flag deviations. Understanding k-means gives you the foundation to evaluate any anomaly detection product, because the underlying logic is the same: define normal, measure distance from normal, investigate the outliers.

---

## Facilitator Notes

- The supervised vs unsupervised distinction (Exercise 1) is a conceptual shift. Participants have spent five sessions in supervised mode. Give them time to absorb the idea that a model can be useful without ever seeing a labelled attack. The question "How much of your network traffic is actually labelled?" usually drives the point home.
- The k-means visualisation (Exercise 2) is the centrepiece. Project the scatter plot with coloured clusters and walk through what each cluster represents. If participants can point at a cluster and say "that's web browsing traffic," the lesson has landed.
- Anomaly scoring (Exercise 4) is the most important exercise for security application. Make sure participants understand that distance-from-centroid is the anomaly score. Ask them to sort points by score and examine the top 10 — are they genuinely unusual, or is the model confused? This mirrors real SOC triage.
- Some participants will ask about false positives in anomaly detection. This is an excellent discussion: unsupervised models have high false positive rates by design — they flag anything unusual, not just threats. The analyst's role is to filter signal from noise. This is why anomaly detection is a triage tool, not an automated response trigger.

---

## Connections to Sales Conversations

- **When a customer asks:** "Can your product detect zero-day threats that have no signatures?"
- **You can now say:** "Yes, and here's how. Our behavioural analytics build a model of what normal looks like in your specific environment — your traffic patterns, your users, your services. Anything that deviates significantly from that baseline gets flagged for investigation. This isn't signature matching; it's anomaly detection. A novel attack that bypasses every signature still looks unusual compared to your baseline. The key advantage is that we don't need to have seen the attack before — we just need to know what your normal looks like."
