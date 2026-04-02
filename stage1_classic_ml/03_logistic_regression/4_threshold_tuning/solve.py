import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, f1_score, precision_recall_curve

# Reuse the same dataset, split, scaling, and model from exercise 3
np.random.seed(42)
n, half = 1000, 500
def make_urls(n_legit, n_phish):
    legit = pd.DataFrame({
        'url_length':     np.random.normal(45, 12, n_legit).clip(10, 100).astype(int),
        'num_dots':       np.random.poisson(2.1, n_legit),
        'has_at_symbol':  (np.random.rand(n_legit) < 0.05).astype(int),
        'uses_https':     (np.random.rand(n_legit) < 0.82).astype(int),
        'num_subdomains': np.random.poisson(0.8, n_legit),
        'has_ip_address': (np.random.rand(n_legit) < 0.02).astype(int),
        'num_hyphens':    np.random.poisson(0.3, n_legit),
        'path_length':    np.random.normal(15, 8, n_legit).clip(0, 60).astype(int),
        'is_phishing':    0
    })
    phish = pd.DataFrame({
        'url_length':     np.random.normal(98, 25, n_phish).clip(30, 250).astype(int),
        'num_dots':       np.random.poisson(4.8, n_phish),
        'has_at_symbol':  (np.random.rand(n_phish) < 0.31).astype(int),
        'uses_https':     (np.random.rand(n_phish) < 0.61).astype(int),
        'num_subdomains': np.random.poisson(2.5, n_phish),
        'has_ip_address': (np.random.rand(n_phish) < 0.21).astype(int),
        'num_hyphens':    np.random.poisson(2.1, n_phish),
        'path_length':    np.random.normal(48, 18, n_phish).clip(0, 150).astype(int),
        'is_phishing':    1
    })
    return pd.concat([legit, phish], ignore_index=True).sample(frac=1, random_state=42)
df = make_urls(half, half)
FEATURES = ['url_length', 'num_dots', 'has_at_symbol', 'uses_https',
            'num_subdomains', 'has_ip_address', 'num_hyphens', 'path_length']
X = df[FEATURES]
y = df['is_phishing']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train_scaled, y_train)

print("=" * 60)
print("TASK 1 — Probability scores vs hard labels")
print("=" * 60)
# Get raw probabilities instead of hard 0/1 predictions
probs = model.predict_proba(X_test_scaled)[:, 1]
# Show probability alongside the default threshold=0.5 label and the true label
results = pd.DataFrame({
    'P(phishing)':      probs,
    'predicted_label':  (probs >= 0.5).astype(int),
    'actual':           y_test.values
})
print(results.head(10).to_string(index=False))
# "Close calls" are samples near the boundary — these are hardest for the model
close_calls = results[(results['P(phishing)'] > 0.4) & (results['P(phishing)'] < 0.6)]
print(f"\nClose calls (P between 0.4 and 0.6): {len(close_calls)}")

print("\n" + "=" * 60)
print("TASK 2 — Threshold comparison table")
print("=" * 60)
# Lower thresholds flag more URLs (higher recall but lower precision) — and vice versa
thresholds = [0.2, 0.3, 0.5, 0.7, 0.8]
print(f"{'Threshold':>10} | {'Precision':>9} | {'Recall':>7} | {'F1':>6} | {'Flagged':>8}")
print("-" * 55)
for thresh in thresholds:
    y_pred = (probs >= thresh).astype(int)
    p = precision_score(y_test, y_pred, zero_division=0)
    r = recall_score(y_test, y_pred)
    f = f1_score(y_test, y_pred)
    flagged = y_pred.sum()
    print(f"{thresh:>10.2f} | {p:>9.3f} | {r:>7.3f} | {f:>6.3f} | {flagged:>8}")

print("\n" + "=" * 60)
print("TASK 3 — Find threshold for recall >= 0.95")
print("=" * 60)
# In security, missing a phishing URL (FN) is worse than a false alarm (FP)
# So we search for the highest threshold that still catches >=95% of phishing URLs
for thresh in np.arange(0.9, 0.0, -0.01):
    y_pred = (probs >= thresh).astype(int)
    r = recall_score(y_test, y_pred)
    if r >= 0.95:
        p = precision_score(y_test, y_pred, zero_division=0)
        flagged = y_pred.sum()
        print(f"Lowest threshold for recall>=0.95: {thresh:.2f}")
        print(f"  Actual recall:    {r:.3f}")
        print(f"  Precision:        {p:.3f}")
        print(f"  URLs flagged:     {flagged} / {len(y_test)}")
        break

print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Precision-recall curve")
print("=" * 60)
print("\n--- Exercise 4 complete. Lesson 1.3 workshop done! ---")
print("--- Next: stage1_classic_ml/04_decision_trees/ ---")
# PR curve shows the precision/recall trade-off across all possible thresholds
precision_vals, recall_vals, thresholds_pr = precision_recall_curve(y_test, probs)
plt.figure(figsize=(8, 6))
plt.plot(recall_vals, precision_vals, label='PR Curve')
# Mark the default threshold=0.5 on the curve for reference
idx_05 = np.argmin(np.abs(thresholds_pr - 0.5))
plt.scatter(recall_vals[idx_05], precision_vals[idx_05],
            color='red', zorder=5, label='Threshold=0.5')
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve — Phishing Classifier')
plt.legend()
plt.grid(True)
plt.show()
