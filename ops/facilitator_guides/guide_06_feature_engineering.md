# Facilitator Guide — Session 2.1: Feature Engineering

> **Stage:** 2  |  **Week:** 5  |  **Lecture deck:** `Lecture-6-Feature-Engineering.pptx`  |  **Total time:** 60 min

---

## Pre-Session Checklist

- [ ] Reviewed the lecture slides and all 4 exercise guides
- [ ] Prepared a sample raw firewall log (3-4 rows) to project — including strings, timestamps, and mixed-type columns that will break sklearn
- [ ] Run through Exercise 1 yourself — confirmed the `ValueError` from feeding raw strings to a classifier
- [ ] Reviewed the five feature types (numeric, categorical, binary, derived, temporal) and can give a security example for each

---

## Session Flow

| Time | Section | Activity |
|------|---------|----------|
| 0:00 – 0:05 | Bridge from Stage 1 | "In Stage 1, every dataset was pre-cleaned. Real security data is not. Today we learn the skill that separates a working model from a broken one." |
| 0:05 – 0:15 | Why raw logs fail | Show a raw NetFlow log row on screen. Ask: "Can sklearn work with IP addresses, timestamps, and protocol names?" Demo Exercise 1 live — feed raw data to a classifier and watch it crash. The error message is the lesson. |
| 0:15 – 0:25 | The five feature types | Walk through each type with a firewall log example: numeric (bytes, packets), categorical (protocol, port category), binary (is_internal_ip), derived (bytes_per_packet), temporal (hour_of_day, is_weekend). Draw a table on the whiteboard mapping raw columns to engineered features. |
| 0:25 – 0:35 | Pipeline and correlation | Explain the feature engineering pipeline: extract, encode, scale. Show that correlated features are redundant — if bytes and packets move together, keeping both adds noise. Introduce correlation matrices as a diagnostic tool. |
| 0:35 – 0:50 | Hands-on exercises | Participants work through Exercises 2-4: numeric feature extraction, categorical encoding, scaling and validation. Circulate and help — encoding is where most participants hit unexpected errors. |
| 0:50 – 0:55 | Impact on accuracy | Reconvene. Compare model accuracy before and after feature engineering (Exercise 4 results). Ask: "How much did accuracy improve? What does that tell you about where to invest your time — algorithm tuning or feature engineering?" |
| 0:55 – 1:00 | Wrap-up | Preview Session 2.2 (random forests). Key bridge: "Now that you can turn raw data into features, we need models powerful enough to exploit them. Single trees aren't enough — next we combine many trees." |

---

## Key Points to Emphasise

1. **Feature engineering is where domain expertise meets ML** — the model can only learn from what you give it. A security analyst who knows that bytes-per-packet ratios distinguish C2 beacons from web browsing creates better features than any automated tool. Your SOC knowledge is the competitive advantage.
2. **Raw data is never model-ready** — every real security dataset (firewall logs, EDR telemetry, DNS queries) contains strings, timestamps, and mixed types that sklearn cannot process. The gap between raw data and model input is filled entirely by feature engineering. Skipping this step is the number one reason real-world ML projects fail.
3. **More features are not always better** — correlated features add redundancy, irrelevant features add noise, and high-dimensional data slows training. Selecting and validating features matters as much as creating them. The correlation matrix is your first diagnostic.

---

## Discussion Prompts

- "You have a NetFlow log with source IP, destination IP, port, bytes, packets, and timestamp. Without writing code, list five features you'd engineer. Which one do you think would be most useful for detecting data exfiltration?"
- "A colleague encodes destination port as a raw number — port 443 becomes the integer 443, port 80 becomes 80. Why is this problematic? What does the model 'think' about port 443 being five times larger than port 80?"
- "Your model accuracy jumps from 72% to 91% after adding a 'bytes_per_second' derived feature. What does that tell you about where the signal was hiding in the raw data?"

---

## Common Questions and Answers

**Q: How do I know which features to create? There are infinite possibilities.**
A: Start with domain knowledge. Ask: "What would a human analyst look at?" For network traffic, analysts look at rates (bytes per second), ratios (packets in vs out), time patterns (connections at 3 AM), and categorisations (internal vs external IP). Those intuitions become features. After building an initial set, use feature importance from a decision tree or random forest to see which ones the model actually uses.

**Q: Should I scale all features before training?**
A: It depends on the algorithm. Tree-based models (decision trees, random forests) do not need scaling — they split on thresholds, so magnitude doesn't matter. Distance-based models (k-means, logistic regression, k-nearest neighbours) do need scaling because a feature measured in bytes (millions) will dominate a feature measured in seconds (single digits). When in doubt, scale — it rarely hurts and often helps.

**Q: What's the difference between one-hot encoding and label encoding for categorical features?**
A: Label encoding assigns integers: TCP=0, UDP=1, ICMP=2. This implies an order (UDP is "between" TCP and ICMP) that doesn't exist. One-hot encoding creates separate binary columns: is_TCP, is_UDP, is_ICMP. This avoids the false ordering. Use one-hot encoding for categories with no natural order. Label encoding is acceptable only when there is a genuine ordinal relationship (e.g., severity: low < medium < high).

---

## Facilitator Notes

- Exercise 1 (why raw logs fail) should be demoed live. The sklearn error message — `ValueError: could not convert string to float` — is memorable and makes the case for feature engineering immediately concrete. Let participants try it themselves and hit the same wall.
- Categorical encoding (Exercise 3) is the conceptual stumbling block. Many participants instinctively want to convert "TCP" to a number. Walk through why ordinal numbers create false relationships. The one-hot encoding diagram on the slide is worth projecting and discussing.
- This is the first session where participants work with data that resembles real SOC output. Expect questions like "Can we use our own logs?" Encourage it as a follow-up project, but keep the session focused on the provided dataset to ensure everyone can follow along.
- The accuracy comparison at the end (raw data vs engineered features) is the payoff. Make sure participants record both numbers — the improvement is usually dramatic and reinforces the lesson.

---

## Connections to Sales Conversations

- **When a customer asks:** "We have terabytes of firewall logs. Can we just feed them into your ML engine?"
- **You can now say:** "Raw logs are the starting point, not the input. Before any model touches the data, we extract meaningful features — rates, ratios, behavioural patterns, temporal signals. This feature engineering step is where security domain expertise matters most. A model trained on well-engineered features from your specific environment will outperform a generic model every time. That's why our approach includes a tuning phase where we engineer features from your actual data sources."
