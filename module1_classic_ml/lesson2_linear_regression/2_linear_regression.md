# Lesson 1.2 — Linear Regression

**Script:** [2_linear_regression.py](2_linear_regression.py)

---

## Concept: Predicting a Number

Linear regression answers the question: **"Given input X, what number do I expect for output Y?"**

It fits a straight line through your data:

```
Response
Time (ms)
  500 |          .                          /
      |      .      .                    . /
  400 |   .            .              . /
      |        .          .        ./
  300 |   .                .    ./  <-- line of best fit
      |               .    . /
  200 |          .       /
      |             . /
  100 |          /
      +-----+-----+-----+-----+-----+------> Requests/sec
            100   200   300   400   500
```

```
y = (weight × x) + bias
       |               |
  how many ms        baseline ms
  per extra req/s    when traffic = 0
```

The model learns the best `weight` and `bias` to minimise the gap between its predictions and the actual values.

---

## Real-Life Example: Server Response Time

You're monitoring a web server. As traffic increases, response time goes up.
Can you predict response time from requests-per-second?

**Why this matters for security:**
- Build a "normal behaviour" baseline
- If predicted response time = 120ms but actual = 4000ms → possible DoS attack or resource exhaustion
- This is the foundation of anomaly detection

---

## The Maths (plain English)

```
response_time = coefficient × requests_per_second + intercept
```

- **Coefficient** — how many extra milliseconds per additional request/second
- **Intercept** — baseline response time when traffic = 0
- **R² score** — how well the line fits (0 = useless, 1.0 = perfect)
- **RMSE** — average prediction error in the same units as your target (ms)

---

## Key sklearn API

Say you have collected 200 measurements: requests-per-second at a given moment, paired with the response time the server returned. Each row is one measurement; `X` is the traffic column, `y` is the response time column. Here's how you train and apply the model:

```python
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)        # learn the line from 160 measurements
y_pred = model.predict(X_test)     # predict response time for the remaining 40
```

---

## What to Notice When You Run It

1. The coefficient — roughly how many ms per req/s
2. R² score — should be close to 1.0 on clean synthetic data
3. The scatter plot — your line should cut through the middle of the cloud
4. The security insight printed at the end — this is the real-world use case

---

## Limitations

Linear regression only captures **linear** relationships. Real servers often have non-linear behaviour (fine at low load, then suddenly slow). We'll handle that with neural networks in Stage 3.

---

## Try It Yourself

After running the script, try changing:
```python
requests_per_second = np.random.uniform(10, 500, n_samples)
```
to
```python
requests_per_second = np.random.uniform(10, 2000, n_samples)
```
Does the model still perform well? What changes in the plot?

---

## Next Lesson

**[Lesson 1.3 — Logistic Regression](3_logistic_regression.md):** Make yes/no decisions — phishing URL or legitimate?


---

## Ready for the Workshop?

You have covered the concepts. Now build it yourself.

**[Open workshop/1_lab_guide.md](workshop/1_lab_guide.md)**
