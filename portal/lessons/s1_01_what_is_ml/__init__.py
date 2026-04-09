"""
Lesson 1.1 — What is Machine Learning?
Flask Blueprint for the interactive digits dataset explorer.
"""

import numpy as np
import pandas as pd
from flask import Blueprint, render_template, jsonify, request
from sklearn.datasets import load_digits
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

bp = Blueprint(
    "s1_01",
    __name__,
    template_folder="templates",
)

LESSON_ID = "s1_01"
LESSON_TITLE = "What is Machine Learning?"

# ── Load and pre-compute at import time ─────────────────────────────────────

digits = load_digits()
X_all, y_all = digits.data, digits.target

averages = {}
for d in range(10):
    averages[d] = digits.images[digits.target == d].mean(axis=0).tolist()

pixel_std = digits.data.std(axis=0).reshape(8, 8).tolist()

df = pd.DataFrame(digits.data, columns=[f"pixel_{i}" for i in range(64)])
df["target"] = digits.target
corr_flat = df.corr()["target"].abs().drop("target").values
correlations = corr_flat.reshape(8, 8).tolist()

class_counts = [(digits.target == d).sum().item() for d in range(10)]

pair_similarities = []
for i in range(10):
    for j in range(i + 1, 10):
        diff = np.abs(np.array(averages[i]) - np.array(averages[j])).mean() / 16
        pair_similarities.append({"a": i, "b": j, "sim": round(1 - diff, 3)})
pair_similarities.sort(key=lambda x: x["sim"], reverse=True)

top_pixels = []
for rank, px in enumerate(np.argsort(corr_flat)[::-1][:10]):
    row, col = divmod(int(px), 8)
    top_pixels.append({
        "rank": rank + 1, "pixel": int(px),
        "row": row, "col": col,
        "corr": round(float(corr_flat[px]), 3),
    })

# ── Accuracy trap cache ─────────────────────────────────────────────────────

trap_cache = {}


def compute_trap_metrics(cls, pct):
    key = (cls, pct)
    if key in trap_cache:
        return trap_cache[key]

    mask_target = y_all == cls
    idx_target = np.where(mask_target)[0]
    idx_other = np.where(~mask_target)[0]

    keep = max(1, int(len(idx_target) * (1 - pct / 100)))
    np.random.seed(42)
    idx_keep = np.concatenate([
        np.random.choice(idx_target, size=keep, replace=False),
        idx_other,
    ])

    X = X_all[idx_keep]
    y = (y_all[idx_keep] == cls).astype(int)

    if y.sum() < 2:
        result = {"acc": round(1 - y.mean(), 3), "prec": 0, "rec": 0, "f1": 0,
                  "n_target": int(y.sum()), "n_total": len(y)}
        trap_cache[key] = result
        return result

    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3,
                                                random_state=42, stratify=y)
    model = LogisticRegression(max_iter=200, solver="lbfgs", random_state=42)
    model.fit(X_tr, y_tr)
    y_pred = model.predict(X_te)

    result = {
        "acc": round(accuracy_score(y_te, y_pred), 3),
        "prec": round(precision_score(y_te, y_pred, zero_division=0), 3),
        "rec": round(recall_score(y_te, y_pred, zero_division=0), 3),
        "f1": round(f1_score(y_te, y_pred, zero_division=0), 3),
        "n_target": keep,
        "n_total": len(idx_keep),
    }
    trap_cache[key] = result
    return result


for pct in range(0, 100, 5):
    compute_trap_metrics(9, pct)

# ── Step metadata ───────────────────────────────────────────────────────────

STEPS = [
    {"id": 0, "title": "What is Machine Learning?", "sub": "Data, features, and labels — the ML vocabulary", "icon": "first-look"},  # mag glass over a 3x3 sample
    {"id": 1, "title": "Loading a Dataset",   "sub": "Pixels are just numbers",            "icon": "draw-digit"},        # pixel-art "1" inside a grid
    {"id": 2, "title": "Spot the Difference", "sub": "Models see differences, not images", "icon": "spot-difference"},   # two grids with ≠ between
    {"id": 3, "title": "Dataset Shape",       "sub": "1,797 samples x 64 features",        "icon": "dataset-shape"},     # rows×cols table outline
    {"id": 4, "title": "Useless Pixels",      "sub": "Zero-variance features",             "icon": "useless-pixels"},    # lit center, X-marked edges
    {"id": 5, "title": "Class Balance",       "sub": "Not all classes are equal",          "icon": "class-balance"},     # uneven bar chart
    {"id": 6, "title": "Accuracy Trap",       "sub": "When 99% accuracy is a lie",         "icon": "accuracy-trap"},     # warning triangle with "99%"
    {"id": 7, "title": "Average Digits",      "sub": "Prototype confusion",                "icon": "average-digits"},    # two overlapping circles
    {"id": 8, "title": "Pixel Importance",    "sub": "Which features matter?",             "icon": "pixel-importance"},  # bullseye + crosshair
    {"id": 9, "title": "Model's Eye View",    "sub": "Just numbers in a row",              "icon": "model-eye-view"},    # rows of monospace numbers
]

# ── Quiz ────────────────────────────────────────────────────────────────────
# Five multiple-choice questions covering the lesson's key takeaways. Rendered
# by portal/templates/quiz.html via the /quiz route below.

QUIZ = [
    {
        "q": "What does a machine learning model actually 'see' when it looks at an 8&times;8 digit image?",
        "options": [
            "A picture file (like a PNG)",
            "A flat array of 64 numbers, one per pixel",
            "The original handwriting strokes",
            "A 28&times;28 grayscale grid",
        ],
        "answer": 1,
        "explanation": "The model never sees an image &mdash; it sees a <strong>flat array of 64 numbers</strong> (the pixel intensities). The 8&times;8 grid is just for humans. This is why <em>feature engineering</em> matters: presenting data so the patterns are easy for the algorithm to find.",
    },
    {
        "q": "Your malware detector reports <strong>99% accuracy</strong> on a dataset where 1% of files are malicious. Why is this almost certainly worthless?",
        "options": [
            "Because 99% is mathematically impossible",
            "A model that always predicts 'benign' would also score 99% &mdash; and catch zero malware",
            "Because accuracy can never be that high in security",
            "Because the model overfits at exactly 99%",
        ],
        "answer": 1,
        "explanation": "This is the <strong>accuracy trap</strong>. With 1% positives, predicting 'benign' for everything yields 99% accuracy and 0% recall. Always check <em>recall</em> when classes are imbalanced &mdash; what fraction of real threats did you actually catch?",
    },
    {
        "q": "In the digits dataset, the <strong>corner pixels</strong> are almost always zero. What does this tell you about them as features?",
        "options": [
            "They are the most important features",
            "They have near-zero variance and carry no signal &mdash; they could be dropped",
            "They prevent overfitting",
            "They are required for image reconstruction",
        ],
        "answer": 1,
        "explanation": "Features with <strong>zero variance</strong> never change between samples, so they cannot help the model distinguish classes. Dropping them is a basic form of <em>feature selection</em> &mdash; fewer features means faster training and less noise.",
    },
    {
        "q": "When you average all the '3' digits and all the '8' digits and look at the prototypes side by side, they look very similar. What does this predict about the model?",
        "options": [
            "The model will perfectly distinguish 3s from 8s",
            "3s and 8s will be a frequent source of confusion in the confusion matrix",
            "The model will refuse to predict either class",
            "Accuracy will be exactly 50% for those two classes",
        ],
        "answer": 1,
        "explanation": "When prototypes <strong>overlap visually</strong>, the decision boundary between those classes is thin and error-prone. You will see this exact pattern as confused cells in the model's confusion matrix &mdash; 3s mistaken for 8s and vice versa.",
    },
    {
        "q": "You want to know which features matter most for predicting digit class. Which technique gives you the answer fastest?",
        "options": [
            "Train a giant neural network and hope",
            "Compute the correlation between each pixel and the target label",
            "Manually inspect every single sample",
            "Drop all the features and see what happens",
        ],
        "answer": 1,
        "explanation": "<strong>Feature&ndash;target correlation</strong> is a quick, model-free way to rank features by signal. High correlation means the pixel value tracks the label (predictive); low correlation means it is noise. In security ML this is how you decide which fields in a log are worth feeding to the model.",
    },
]


CHALLENGES = {
    0: {
        "q": "Run 'New digit' 10 times. Do you ever get one that's hard to recognize even as a human?",
        "a": "Some 8x8 images are genuinely ambiguous — even you can't tell if it's a 1 or a 7. If a human struggles, a model will too. This is called <strong>irreducible error</strong> — the noise floor no algorithm can beat.",
    },
    1: {
        "q": "Edit the grid to draw a 3. Then change just ONE pixel. Does it still look like a 3?",
        "a": "A single pixel change barely matters — the model looks at the whole pattern. This is why ML is robust to small noise but vulnerable to <strong>adversarial examples</strong> that change many pixels in a coordinated way.",
    },
    2: {
        "q": "Find the pair with the highest similarity. Now find the pair with the lowest. Why?",
        "a": "Digits that share structural elements (like 3 and 8 — both have curves) are hard to separate. Digits that are structurally different (like 0 and 1) are easy. A model's <strong>confusion matrix</strong> mirrors this.",
    },
    3: {
        "q": "Try entering index 1797. What happens? Why?",
        "a": "<code>Index out of range</code> — there are only 1,797 samples (indices 0–1796). In production, your model only knows what it was trained on. Data outside that range is <strong>out of distribution</strong>.",
    },
    4: {
        "q": "Drag the slider to max. How many pixels survive? Could a model still work with just those?",
        "a": "At high thresholds, only ~10-15 center pixels remain — and yes, a model can still classify reasonably well. This is <strong>dimensionality reduction</strong>: fewer features can mean faster training and less overfitting.",
    },
    5: {
        "q": "Remove 95% of digit 5. What would happen if a model just guessed the most common digit every time?",
        "a": "With ~9 samples of digit 5 vs ~1,600 of everything else, a model that <strong>never predicts 5</strong> gets ~99.5% accuracy. This sets up the accuracy trap in Step 6.",
    },
    6: {
        "q": "At what removal % does recall drop below 50% while accuracy stays above 90%?",
        "a": "The trap springs around 70-80% removal. Accuracy barely moves because the majority class dominates. <strong>Recall collapses</strong> because the model stops finding the rare class. A malware detector with 99% accuracy but 10% recall misses 9 out of 10 threats.",
    },
    7: {
        "q": "Click 'Rank all pairs.' Which pair is most similar? Go back to Step 2 — do the results agree?",
        "a": "Yes — the most similar prototypes match the hardest-to-distinguish pairs. Prototypes are what the model learns. When prototypes overlap, the <strong>decision boundary</strong> becomes thin and error-prone.",
    },
    8: {
        "q": "Set correlation to 0.5 and click 'Show on digit' several times. Can you still recognize the digits?",
        "a": "Usually yes — center pixels carry almost all the signal. This is <strong>feature selection</strong>: drop noisy columns (like TTL or source MAC) and keep the signal (entropy, byte distribution, timing patterns).",
    },
    9: {
        "q": "Try to get 5/5. If you can't, what would make it easier?",
        "a": "Raw numbers are nearly impossible for humans but trivial for algorithms. The 8x8 grid helps you, but the model never sees it. This is why <strong>feature engineering</strong> matters: presenting data in a form that makes patterns easier to find.",
    },
}


# ── Course materials mapping ────────────────────────────────────────────────

_base = "curriculum/stage1_classic_ml/01_what_is_ml"
_ex = f"{_base}/2_coding_exercises"

# NOTE on the mapping below:
# The five hands-on labs (1_loading_data … 5_what_model_sees) are reused
# across the ten explore steps. Each MATERIALS entry uses a label that
# tells the truth about the lab the learner is about to open, so the
# drawer header always matches the content. Lectures whose underlying
# .md file covers more than one explore-step topic are titled to reflect
# both topics (e.g. Step 5 + Step 6 share the same Class Balance & the
# Accuracy Trap lab).
MATERIALS = {
    0: [("lecture", "What is Machine Learning?", f"{_base}/README.md")],
    1: [("lecture", "Loading a Dataset", f"{_ex}/1_loading_data/lecture.md"),
        ("lab", "Lab — Loading a Dataset", f"{_ex}/1_loading_data/handson.md"),
        ("solution", "Solution", f"{_ex}/1_loading_data/solution_loading_data.py")],
    2: [("lecture", "Visualising Your Data", f"{_ex}/4_visualise/lecture.md"),
        ("lab", "Lab — Visualising Your Data", f"{_ex}/4_visualise/handson.md"),
        ("solution", "Solution", f"{_ex}/4_visualise/solution_visualise.py")],
    3: [("lecture", "Loading a Dataset", f"{_ex}/1_loading_data/lecture.md"),
        ("lab", "Lab — Loading a Dataset", f"{_ex}/1_loading_data/handson.md"),
        ("solution", "Solution", f"{_ex}/1_loading_data/solution_loading_data.py")],
    4: [("lecture", "Shape, Statistics, and Missing Values", f"{_ex}/2_statistics/lecture.md"),
        ("lab", "Lab — Shape, Statistics, and Missing Values", f"{_ex}/2_statistics/handson.md"),
        ("solution", "Solution", f"{_ex}/2_statistics/solution_statistics.py")],
    5: [("lecture", "Class Balance & the Accuracy Trap", f"{_ex}/3_class_balance/lecture.md"),
        ("lab", "Lab — Class Balance & the Accuracy Trap", f"{_ex}/3_class_balance/handson.md"),
        ("solution", "Solution", f"{_ex}/3_class_balance/solution_class_balance.py")],
    6: [("lecture", "Class Balance & the Accuracy Trap", f"{_ex}/3_class_balance/lecture.md"),
        ("lab", "Lab — Class Balance & the Accuracy Trap", f"{_ex}/3_class_balance/handson.md"),
        ("solution", "Solution", f"{_ex}/3_class_balance/solution_class_balance.py")],
    7: [("lecture", "Visualising Your Data", f"{_ex}/4_visualise/lecture.md"),
        ("lab", "Lab — Visualising Your Data", f"{_ex}/4_visualise/handson.md"),
        ("solution", "Solution", f"{_ex}/4_visualise/solution_visualise.py")],
    8: [("lecture", "What the Model Actually Sees", f"{_ex}/5_what_model_sees/lecture.md"),
        ("lab", "Lab — What the Model Actually Sees", f"{_ex}/5_what_model_sees/handson.md"),
        ("solution", "Solution", f"{_ex}/5_what_model_sees/solution_what_model_sees.py")],
    9: [("lecture", "What the Model Actually Sees", f"{_ex}/5_what_model_sees/lecture.md"),
        ("lab", "Lab — What the Model Actually Sees", f"{_ex}/5_what_model_sees/handson.md"),
        ("solution", "Solution", f"{_ex}/5_what_model_sees/solution_what_model_sees.py")],
}


# ── Helper to build template context ────────────────────────────────────────

def base_ctx(step_num):
    return {
        "steps": STEPS,
        "current": step_num,
        "challenge": CHALLENGES[step_num],
        "lesson_id": LESSON_ID,
        "lesson_title": LESSON_TITLE,
        "url_prefix": f"/lesson/{LESSON_ID}",
        "materials": MATERIALS.get(step_num, []),
        "quiz_count": len(QUIZ),
        "is_quiz": False,
    }


# ── Routes ──────────────────────────────────────────────────────────────────

@bp.route("/")
def index():
    return render_template("s1_01/index.html",
                           steps=STEPS, lesson_id=LESSON_ID,
                           lesson_title=LESSON_TITLE,
                           url_prefix=f"/lesson/{LESSON_ID}")


@bp.route("/quiz")
def quiz():
    return render_template(
        "quiz.html",
        steps=STEPS,
        current=len(STEPS) - 1,
        lesson_id=LESSON_ID,
        lesson_title=LESSON_TITLE,
        url_prefix=f"/lesson/{LESSON_ID}",
        quiz=QUIZ,
        quiz_count=len(QUIZ),
        is_quiz=True,
    )


@bp.route("/step/<int:n>")
def step(n):
    if n < 0 or n >= len(STEPS):
        return "Step not found", 404

    ctx = base_ctx(n)

    if n == 0:
        idx = np.random.randint(len(digits.images))
        ctx["image"] = digits.images[idx].tolist()
        ctx["label"] = int(digits.target[idx])
        ctx["flat"] = digits.data[idx].astype(int).tolist()

    elif n == 1:
        sample_7 = digits.images[digits.target == 7][0].astype(int).tolist()
        ctx["real_digit"] = sample_7

    elif n == 2:
        ctx["averages"] = averages
        ctx["pairs"] = pair_similarities

    elif n == 3:
        ctx["shape"] = list(digits.data.shape)
        ctx["class_counts"] = class_counts
        ctx["n_samples"] = len(digits.data)

    elif n == 4:
        ctx["pixel_std"] = pixel_std

    elif n == 5:
        ctx["class_counts"] = class_counts

    elif n == 7:
        ctx["averages"] = averages
        ctx["pairs"] = pair_similarities

    elif n == 8:
        ctx["correlations"] = correlations
        ctx["top_pixels"] = top_pixels

    elif n == 9:
        idx = np.random.randint(len(digits.images))
        ctx["flat"] = digits.data[idx].astype(int).tolist()
        ctx["image"] = digits.images[idx].tolist()
        ctx["label"] = int(digits.target[idx])

    return render_template(f"s1_01/step_{n:02d}.html", **ctx)


# ── API endpoints ───────────────────────────────────────────────────────────

@bp.route("/api/random-digit")
def api_random_digit():
    idx = np.random.randint(len(digits.images))
    return jsonify({
        "image": digits.images[idx].tolist(),
        "flat": digits.data[idx].astype(int).tolist(),
        "label": int(digits.target[idx]),
    })


@bp.route("/api/random-digit/<int:d>")
def api_random_digit_class(d):
    if d < 0 or d > 9:
        return jsonify({"error": "Digit must be 0-9"}), 400
    indices = np.where(digits.target == d)[0]
    idx = np.random.choice(indices)
    return jsonify({
        "image": digits.images[idx].astype(int).tolist(),
        "flat": digits.data[idx].astype(int).tolist(),
        "label": int(digits.target[idx]),
    })


@bp.route("/api/sample/<int:idx>")
def api_sample(idx):
    if idx < 0 or idx >= len(digits.data):
        return jsonify({"error": f"Index must be 0–{len(digits.data) - 1}"}), 400
    return jsonify({
        "image": digits.images[idx].tolist(),
        "flat": digits.data[idx].astype(int).tolist(),
        "label": int(digits.target[idx]),
    })


@bp.route("/api/trap-all")
def api_trap_all():
    cls = int(request.args.get("cls", 9))
    results = {}
    for pct in range(0, 100, 5):
        results[str(pct)] = compute_trap_metrics(cls, pct)
    return jsonify(results)
