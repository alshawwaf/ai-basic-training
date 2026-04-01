import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, LogisticRegression

# Generate synthetic URL-length data: legit URLs cluster around 40 chars, phishing around 90
np.random.seed(42)
url_lengths_legit   = np.random.normal(40, 10, 50).clip(10, 80)
url_lengths_phish   = np.random.normal(90, 20, 50).clip(40, 250)
url_lengths = np.concatenate([url_lengths_legit, url_lengths_phish])
labels = np.array([0]*50 + [1]*50)   # 0=legitimate, 1=phishing
demo_df = pd.DataFrame({"url_length": url_lengths, "is_phishing": labels})

print("=" * 60)
print("TASK 1 — Linear regression gives invalid probabilities")
print("=" * 60)
# Fit linear regression on a binary target to show why it fails for classification
X_demo = demo_df[['url_length']]
y_demo  = demo_df['is_phishing']
lin_model = LinearRegression().fit(X_demo, y_demo)
# Extreme URL lengths produce predictions outside [0,1] — not valid probabilities
for length in [5, 500]:
    pred = lin_model.predict([[length]])[0]
    valid = "valid" if 0 <= pred <= 1 else "INVALID — outside [0,1]!"
    print(f"url_length={length:4d}: prediction={pred:.3f}  ← {valid}")

print("\n" + "=" * 60)
print("TASK 2 — Sigmoid function plot")
print("=" * 60)

print("\n" + "=" * 60)
print("TASK 3 — Logistic regression probabilities")
print("=" * 60)
# Logistic regression outputs proper probabilities, always between 0 and 1
log_model = LogisticRegression().fit(demo_df[['url_length']], demo_df['is_phishing'])
# predict_proba returns [P(class 0), P(class 1)] — we grab column 1 for P(phishing)
for length in [20, 50, 80, 120, 200]:
    prob = log_model.predict_proba([[length]])[0, 1]
    label = "phishing" if prob >= 0.5 else "legitimate"
    print(f"url_length={length:4d}: P(phishing)={prob:.2f} → {label}")

print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Decision boundary")
print("=" * 60)
# The decision boundary is where P(phishing) = 0.5, i.e. where coef*x + intercept = 0
coef      = log_model.coef_[0][0]
intercept = log_model.intercept_[0]
boundary  = -intercept / coef
print(f"Decision boundary: url_length = {boundary:.1f} characters")
print("URLs longer than this are classified as phishing by the model.")
