# Challenge Cards — What Happens If...?

After each explore step, try the challenge below. Think first, then check the answer.

---

## Step 0 — First Look

**Challenge:** Run the script 10 times. Do you ever get a digit that's hard to recognize even as a human?

<details><summary>Aha moment</summary>

Some 8x8 images are genuinely ambiguous — even you can't tell if it's a 1 or a 7. If a human struggles, a model will too. This is called **irreducible error** — the noise floor no algorithm can beat.

</details>

---

## Step 1 — Draw a Digit

**Challenge:** Edit the grid to draw a digit 3. Then change just ONE pixel. Does it still look like a 3?

<details><summary>Aha moment</summary>

A single pixel change barely matters — the model looks at the whole pattern. This is why ML is robust to small noise but vulnerable to **adversarial examples** that change many pixels in a coordinated way.

</details>

---

## Step 2 — Spot the Difference

**Challenge:** Find the pair with the highest similarity. Now find the pair with the lowest. Why?

<details><summary>Aha moment</summary>

Digits that share structural elements (like 3 and 8 — both have curves) are hard to separate. Digits that are structurally different (like 0 and 1) are easy. A model's confusion matrix will mirror this — most errors happen between similar-looking classes.

</details>

---

## Step 3 — Dataset Shape

**Challenge:** Try accessing `digits.data[1797]`. What happens? Why?

<details><summary>Aha moment</summary>

`IndexError` — there are only 1,797 samples (indices 0–1796). This is a fundamental concept: datasets have boundaries. In production, your model only knows what it was trained on. Data outside that range is **out of distribution**.

</details>

---

## Step 4 — Useless Pixels

**Challenge:** Drag the slider to max. How many pixels survive? Could a model still work with just those?

<details><summary>Aha moment</summary>

At high thresholds, only ~10-15 center pixels remain — and yes, a model can still classify reasonably well with just those. This is the principle behind **dimensionality reduction**: fewer features can mean faster training and less overfitting.

</details>

---

## Step 5 — Class Balance

**Challenge:** Remove 95% of digit 5. Now look at the count. What would happen if a model just guessed the most common digit every time?

<details><summary>Aha moment</summary>

With ~9 samples of digit 5 vs ~1,600 of everything else, a model that **never predicts 5** gets ~99.5% accuracy. This is the setup for the accuracy trap in Step 6.

</details>

---

## Step 6 — Accuracy Trap

**Challenge:** Drag the slider slowly from 0% to 95%. At what point does recall drop below 50% while accuracy stays above 90%?

<details><summary>Aha moment</summary>

The trap springs around 70-80% removal. Accuracy barely moves because the majority class dominates the score. Recall collapses because the model stops trying to find the rare class. In security: a malware detector with 99% accuracy but 10% recall misses 9 out of 10 threats.

</details>

---

## Step 7 — Average Digits

**Challenge:** Click "Rank all pairs." Which pair is most similar? Now go back to Step 2 and compare the same pair. Do the results agree?

<details><summary>Aha moment</summary>

Yes — the most similar prototypes in Step 7 match the hardest-to-distinguish pairs in Step 2. Prototypes are what the model actually learns. When prototypes overlap, the **decision boundary** between classes becomes thin and error-prone.

</details>

---

## Step 8 — Pixel Importance

**Challenge:** Set correlation to 0.5 and click "Show on digit" several times. Can you still recognize the digits with only the important pixels?

<details><summary>Aha moment</summary>

Usually yes — the center pixels carry almost all the signal. This is exactly what **feature selection** does in security ML: drop noisy columns (like TTL or source MAC) and keep the signal (like entropy, byte distribution, timing patterns).

</details>

---

## Step 9 — Model's Eye View

**Challenge:** Try to get 5/5. If you can't, why not? What would make it easier?

<details><summary>Aha moment</summary>

Raw numbers are nearly impossible for humans but trivial for algorithms. The 8x8 grid helps you, but the model never sees it — it works with the flat array. This is why **feature engineering** matters: presenting data in a form that makes patterns easier to find.

</details>
