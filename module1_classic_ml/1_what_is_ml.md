# Lesson 1.1 — What is ML? Exploring Data

**Script:** [1_concepts_and_data.py](1_concepts_and_data.py)

---

## Concept: Before You Train Anything, Look at Your Data

One of the most common mistakes beginners make is jumping straight into training a model without understanding what the data looks like. Every experienced ML practitioner spends significant time on **exploratory data analysis (EDA)** first.

In cybersecurity terms: you wouldn't write detection rules without first looking at what the malicious traffic actually looks like. Same principle.

---

## The Dataset We Use

We use scikit-learn's built-in **breast cancer dataset** as a warm-up. Why?
- It's clean and well-understood
- It's a **binary classification** problem (malignant vs benign)
- This is the *exact same structure* as "is this traffic an attack or not?"

The features are measurements of cell nuclei from a biopsy image:
- `mean radius`, `mean texture`, `mean perimeter`, etc.

In a real security project, these would instead be:
- `bytes_sent`, `packet_rate`, `entropy`, `port_number`, `connection_duration`, etc.

---

## What the Script Does

### Step 1 — Load the data
```python
data = load_breast_cancer()
df = pd.DataFrame(data.data, columns=data.feature_names)
df["target"] = data.target   # 0 = malignant, 1 = benign
```

### Step 2 — Inspect the shape
```python
df.shape        # (569, 31) → 569 samples, 30 features + 1 label
df.head()       # first 5 rows
df.describe()   # mean, std, min, max for each feature
```

Always check:
- How many rows do you have? (more is generally better)
- How many features? (too many can cause problems — "curse of dimensionality")

### Step 3 — Check class balance
```python
df["target_name"].value_counts()
# benign      357
# malignant   212
```

**Class imbalance** is a major issue in cybersecurity ML. If 99% of traffic is normal and 1% is an attack, a model that always says "normal" gets 99% accuracy — but it's useless. You'll learn how to handle this in Stage 2.

### Step 4 — Visualise feature distributions
```python
ax.hist(group[feature], alpha=0.6, label=label, bins=30)
```

If the malignant and benign histograms **don't overlap much** → this feature is a strong signal for the model.
If they **heavily overlap** → this feature alone isn't very useful, but combined with others it might be.

---

## What to Look for When You Run It

1. **Shape** — 569 rows, 31 columns
2. **Class balance** — 357 benign vs 212 malignant (roughly 63/37 split)
3. **Histograms** — `mean radius` should separate the classes well; you'll see two distinct humps

---

## The Key Takeaway

> A model is only as good as your understanding of the data.

Spend time here. Ask questions like:
- Do I have enough data?
- Are the classes balanced?
- Do any features look like strong predictors?
- Are there missing values? (check with `df.isnull().sum()`)

---

## Try It Yourself

After running the script, open Python and try:

```python
# Are there any missing values?
print(df.isnull().sum())

# Which features have the highest correlation with the target?
print(df.corr()["target"].sort_values(ascending=False).head(10))
```

The second line is a quick way to find your most predictive features — very useful when you're dealing with hundreds of columns in a real security dataset.

---

## Next Lesson

**[Lesson 1.2 — Linear Regression](2_linear_regression.md):** Predict a continuous number (server response time from traffic volume) using your first ML model.
