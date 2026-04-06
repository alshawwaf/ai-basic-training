# Lesson 1.1 — Challenge Cards

After you've played with each `explore_*.py`, come back here and try
the challenges. Each one has a hidden answer — try to think it through
before you peek.

> Tip: in GitHub or VS Code, click the small triangle on each
> `<details>` block to expand the spoiler.

---

## Step 0 — First Look

**Q1.** You ran the script 10 times. How many digits were *immediately*
obvious to you? How many made you hesitate?

<details>
<summary>What this means</summary>

If even *you* hesitate on some digits, a model will too. The hard
samples are why we measure accuracy on a test set instead of trusting
the training score. A model that scores 100% on training data has
almost certainly memorised the easy samples and overfit to the noise
on the hard ones.
</details>

---

## Step 1 — Draw a Digit

**Q1.** You set every pixel to either 0 or 16 (no shades of grey). Did
your digit still look like a digit?

<details>
<summary>Answer</summary>

Probably yes, but blockier. The 16-level greyscale in the real dataset
isn't there because the model needs it — it's there because the original
scanner produced it. You'll see in later lessons that you can
**threshold** images to 0/1 and barely lose accuracy. This is your first
hint that not every detail in your data carries information.
</details>

**Q2.** You replaced `MY_DIGIT` with random noise. Could the model
still classify it?

<details>
<summary>Answer</summary>

It will produce *some* prediction — the model always returns one of
the 10 classes. But the prediction will be meaningless and the
confidence will be split across several classes. This is why you'll
later learn about **calibration** and **uncertainty** — a model that
says "I don't know" is more useful than one that confidently picks a
random label.
</details>

---

## Step 2 — Spot the Difference

**Q1.** Which digit pair has the *least* difference?

<details>
<summary>Answer</summary>

Usually **(1, 7)** or **(3, 8)**, depending on which samples you drew.
Both pairs share a vertical stroke that dominates the image. Your eye
can spot the differences (the horizontal bar on the 7, the closed loops
on the 8) but a linear model that only looks at one pixel at a time
needs many examples to learn those patterns.
</details>

**Q2.** You picked (1, 7) and clicked "New pair" five times. Did the
difference map stay similar or change a lot?

<details>
<summary>Answer</summary>

The difference map *moves around*. That's because the digit 1 is drawn
in many different positions and slants — sometimes leaning left,
sometimes centred. This **within-class variation** is what makes
classification hard. A naive "compare to one example" approach would
fail; the model has to learn what's *consistently* true across all 1s.
</details>

---

## Step 3 — Dataset Shape (Jupyter)

**Q1.** What's the average brightness of all 8s vs all 1s? Why?

<details>
<summary>Answer</summary>

8s are noticeably brighter on average. They have two closed loops with
ink everywhere; 1s are mostly white space with a single vertical
stroke. **Total brightness** is by itself a (weak) feature for the
classification task — and that's exactly the kind of thing the model
discovers automatically when you give it the raw pixels.
</details>

---

## Step 4 — Useless Pixels

**Q1.** At threshold 0, how many pixels are "useless"?

<details>
<summary>Answer</summary>

Usually around **2-4 pixels** are exactly zero across the whole
dataset — they're at the very corners. Push the slider to 5 and you'll
drop ~12 more pixels. Push it to 10 and you're down to ~30 useful
pixels. The model could plausibly classify with just 30 pixels and lose
maybe 1-2% accuracy. That's a 50% reduction in features for almost no
cost.
</details>

**Q2.** The dropped pixels concentrate where? Why?

<details>
<summary>Answer</summary>

The corners of the 8x8 image. Almost no digit is drawn all the way to
the edge — the scanner centred each sample. Those corner pixels are
near-zero in every sample, so they have near-zero variance, so they
contribute nothing to telling the classes apart.
</details>

---

## Step 5 — Class Balance

**Q1.** You shrunk class 0 to 10 samples. What's the new imbalance
ratio?

<details>
<summary>Answer</summary>

The other classes have ~180 samples each, so the ratio jumps to ~18:1.
That doesn't sound catastrophic, but in security workloads you're often
looking at 1000:1 or worse. The principle scales: as the rare class
shrinks, accuracy stops being meaningful.
</details>

**Q2.** Does the *worst* class matter, or only the *rarest*?

<details>
<summary>Answer</summary>

Both — but for different reasons. The *rarest* class drives the
imbalance ratio and breaks the accuracy metric. The *hardest* class
(the one whose prototype overlaps with others) drives the model's
mistakes. They're often not the same class. You need to look at
**per-class recall** to see which is which.
</details>

---

## Step 6 — Accuracy Trap

**Q1.** At 5 attack samples, what's the accuracy? What's the recall?

<details>
<summary>Answer</summary>

Accuracy stays around **99.6%**. Recall on the attack class drops to
**0%**. The model has learned the optimal lazy strategy: predict
"normal" for everything. Accuracy rewards it, the test set rewards it,
and it catches **zero** attacks. This is the most important takeaway
of Lesson 1.1.
</details>

**Q2.** Why is the model making this choice?

<details>
<summary>Answer</summary>

LogisticRegression's loss function rewards correct **counts**, not
correct **kinds**. With 1617 normal samples and 5 attack samples,
predicting "normal" for everything misclassifies 5 samples; predicting
"attack" for everything misclassifies 1617. The math favours the lazy
strategy. The fix is **class weights**, **resampling**, or **a metric
that punishes the lazy strategy** (recall, F1). You'll meet all three
in later lessons.
</details>

---

## Step 7 — Average Digits

**Q1.** Which digit pair has the smallest distance between prototypes?

<details>
<summary>Answer</summary>

Usually **(4, 9)** or **(3, 8)**. Both pairs share most of their ink in
the same places. A nearest-prototype classifier confuses them
constantly. A real classifier learns the subtle differences (the closed
top of a 9, the horizontal bar of a 4) — but only because it has
hundreds of examples of each.
</details>

**Q2.** Which pair has the largest?

<details>
<summary>Answer</summary>

Usually **(0, 1)** or **(1, 8)**. The digit 1 is mostly empty space; 0
and 8 are mostly ink. They're so visually different that even the
naive prototype classifier nearly always gets them right.
</details>

---

## Step 8 — Pixel Importance

**Q1.** The most predictive pixels cluster in two regions. Where?

<details>
<summary>Answer</summary>

Usually the **upper-middle** and **lower-middle** of the image. Those
are the rows where the *body* of most digits sits — and where the
biggest differences between classes happen (open top of a 7 vs closed
top of a 9, for instance). Edge rows are less predictive because
they're either empty or shared across many classes.
</details>

**Q2.** High-variance != high-correlation. Why?

<details>
<summary>Answer</summary>

A pixel can have high variance (lots of different brightnesses) without
that variation lining up with the class label. Imagine a pixel that's
randomly bright or dark for any digit — it has high variance but zero
correlation with the label. **Variance tells you a feature has
information; correlation tells you that information is *useful for the
task you care about*.** This is the difference between unsupervised
exploration and supervised learning.
</details>

---

## Step 9 — Model's Eye View

**Q1.** You played 5 rounds. How did you score? How did the model do
on the same task?

<details>
<summary>Answer</summary>

A trained LogisticRegression gets ~95% on these digits. You probably
got something between 1/5 and 3/5. The model isn't smarter than you —
it's seen 1257 training examples and learned to spot statistical
patterns across all 64 numbers at once. Your brain is doing image
recognition; the model is doing **arithmetic on a feature vector**.
That arithmetic generalises to network logs, sensor readings, and
medical records — anywhere you can encode the input as a list of
numbers.
</details>

---

## After all 10 challenges

If you've answered most of these without peeking, you understand the
core ideas of Lesson 1.1: **what data is, why class balance matters,
why accuracy lies, how features carry signal, and what the model
actually sees.**

You're ready for Lesson 1.2.
