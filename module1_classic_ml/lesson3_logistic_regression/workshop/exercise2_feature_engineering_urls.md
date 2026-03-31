# Exercise 2 — Feature Engineering for URL Phishing Detection

> Back to [1_lab_guide.md](1_lab_guide.md)
> Exercise file: [exercise2_feature_engineering_urls.py](exercise2_feature_engineering_urls.py)

## What You Will Learn

- Why specific URL features are predictive of phishing
- How to generate and inspect a realistic synthetic phishing dataset
- How to explore feature distributions to understand your data
- How to check for class imbalance before modelling

---

## Concept: Why These URL Features Matter

Phishing URLs share structural patterns that differ measurably from legitimate ones. Security researchers have identified the following as highly discriminative:

| Feature | Why phishing URLs score higher |
|---------|-------------------------------|
| `url_length` | Phishing URLs often pad with random characters to obscure the real domain |
| `num_dots` | Subdomains like `login.bank.com.phish.evil.com` inflate dot count |
| `has_at_symbol` | `user@evil.com/redirect?url=bank.com` — the browser ignores everything before `@` |
| `uses_https` | Counter-intuitive: many phishing sites now use HTTPS; absence is suspicious but presence is not proof of legitimacy |
| `num_subdomains` | Deep subdomain nesting (`a.b.c.d.evil.com`) is a phishing indicator |
| `has_ip_address` | `http://192.168.1.1/login` instead of a domain name — often malicious |
| `num_hyphens` | `secure-login-paypal.com` — hyphens used to mimic legitimate domains |
| `path_length` | Long paths often contain encoded redirect parameters |

These features are **binary** (0/1) or **integer counts** — all numeric, so sklearn can use them directly without encoding.

---

## Concept: Synthetic Datasets

We cannot ship real phishing URLs as training data, so we generate a synthetic dataset with realistic statistical properties:

- Phishing features are sampled from distributions with higher means
- Legitimate features are sampled from distributions with lower means
- Some overlap is intentional: not all long URLs are phishing, not all short URLs are legitimate

The dataset has **1,000 rows** and **8 features** plus a `is_phishing` label (0/1).

---

## Concept: Class Balance

Before modelling, always check the ratio of positive to negative examples:

```python
df['is_phishing'].value_counts()
```

If one class is much rarer (e.g., 5% positive), the model can achieve high accuracy by predicting "legitimate" for everything. This is the **accuracy trap** — explored more deeply in Lesson 1.5.

For this dataset we use a 50/50 split so the model is not tempted to cheat. In practice, phishing datasets are often imbalanced.

---

## Concept: Feature Distribution Analysis

Plotting the distribution of each feature split by class reveals which features discriminate well:

- **Well-separated distributions** → strong predictive power
- **Overlapping distributions** → weaker predictor, but possibly useful in combination
- **Binary features** → use bar charts or proportion tables

A quick technique: `df.groupby('is_phishing').mean()` shows the average feature value for each class — a table that immediately reveals which features differ most between phishing and legitimate.

---

## What Each Task Asks You to Do

### Task 1 — Generate and Inspect the Dataset
Create the synthetic dataset using the provided seed. Print its shape, the class balance, and the first 5 rows. Confirm there are no missing values.

### Task 2 — Compare Feature Means by Class
Compute `df.groupby('is_phishing').mean()` and print the result. Identify which 3 features show the largest difference between phishing and legitimate samples.

### Task 3 — Plot Feature Distributions
Choose 4 numeric features (e.g., url_length, num_dots, num_subdomains, path_length). Plot side-by-side histograms for phishing vs legitimate. Do the distributions overlap or are they well-separated?

### Task 4 (BONUS) — Correlation Analysis
Compute `df.corr()['is_phishing'].sort_values(ascending=False)`. Print the top 4 features most positively correlated with phishing and comment on whether this matches your expectations.

---

## Expected Outputs

```
TASK 1 — Dataset inspection:
Shape: (1000, 9)
Class balance:
  is_phishing=0 (legitimate): 500 (50.0%)
  is_phishing=1 (phishing):   500 (50.0%)
Missing values: 0

TASK 2 — Feature means by class:
                     url_length  num_dots  has_at_symbol  uses_https  \
is_phishing
0 (legitimate)          45.2       2.1           0.05        0.82
1 (phishing)            98.7       4.8           0.31        0.61

Biggest gaps: url_length (53.5), num_dots (2.7), has_at_symbol (0.26)

TASK 3 — Distribution plots displayed.

TASK 4 (BONUS) — Correlation with is_phishing:
url_length       0.61
num_dots         0.47
has_at_symbol    0.39
num_subdomains   0.35
...
```

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Forgetting `np.random.seed()` | Different dataset each run | Set seed before data generation |
| Treating binary columns as continuous for plotting | Box plots work; histograms look weird for 0/1 | Use `value_counts()` or bar plots for binary features |
| Ignoring class imbalance | Model performance metrics are misleading | Always print `value_counts()` |
| Using the full dataset stats before splitting | Feature leakage downstream | Split first, then analyse (or use EDA only for exploration, not for feature construction) |

---

> Next: [exercise3_train_and_evaluate.md](exercise3_train_and_evaluate.md)
