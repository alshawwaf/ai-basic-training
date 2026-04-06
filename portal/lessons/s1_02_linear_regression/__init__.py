"""
Lesson 1.2 — Linear Regression
Flask Blueprint for the server response-time regression workshop.
"""

from flask import Blueprint, render_template

bp = Blueprint(
    "s1_02",
    __name__,
    template_folder="templates",
)

LESSON_ID = "s1_02"
LESSON_TITLE = "Linear Regression"

# ── Step metadata ───────────────────────────────────────────────────────────

STEPS = [
    {"id": 0, "title": "Understanding Regression",
     "sub": "Regression vs classification, scatter plots, EDA"},
    {"id": 1, "title": "Train / Test Split",
     "sub": "Why we split data and how to avoid data leakage"},
    {"id": 2, "title": "Fit and Predict",
     "sub": "Slope, intercept, and the regression line"},
    {"id": 3, "title": "Evaluate and Detect",
     "sub": "MSE, RMSE, R² — build a security baseline"},
]

CHALLENGES = {
    0: {
        "q": "Change the data range from 0\u2013200 rps to 0\u20132000 rps. Does the scatter plot still look linear? What does that tell you about the model's assumptions?",
        "a": "At very high loads, real servers saturate \u2014 response times spike exponentially. The scatter would curve upward, and a straight line would under-predict at high loads. This is why <strong>linear regression only works when the true relationship is approximately linear</strong>. For non-linear patterns you need polynomial features or a different model.",
    },
    1: {
        "q": "What happens if you evaluate the model on the training data instead of the test set? Try it \u2014 is R\u00b2 higher or lower?",
        "a": "Training R\u00b2 is almost always higher (better) than test R\u00b2 because the model has already memorised the training examples. The gap between them is the <strong>overfitting indicator</strong>. In security ML, this means your malware detector may look perfect in the lab but fail on live traffic.",
    },
    2: {
        "q": "The slope is ~1.82 ms per rps. If you doubled the server's CPU, what would you expect to happen to the slope? What about the intercept?",
        "a": "A faster server would have a <strong>lower slope</strong> (less added latency per extra request) and possibly a <strong>lower intercept</strong> (less baseline overhead). The model's parameters have physical meaning \u2014 that's the power of interpretable models in security. You can explain to a SOC analyst <em>why</em> the alert fired.",
    },
    3: {
        "q": "At k=2\u03c3, you flag ~7% of observations. At k=3\u03c3, you flag ~2%. A SOC analyst can handle 10 alerts per day from this system. Which threshold should you choose?",
        "a": "If normal volume is 1440 observations/day (one per minute), k=2\u03c3 produces ~100 alerts and k=3\u03c3 produces ~29. Neither fits 10 alerts. You'd need k\u22483.5\u03c3. This is <strong>threshold tuning</strong> \u2014 balancing detection rate against analyst capacity. Too many alerts = alert fatigue = real threats get ignored.",
    },
}

# ── Course materials mapping ────────────────────────────────────────────────

_base = "curriculum/stage1_classic_ml/02_linear_regression"

MATERIALS = {
    0: [("lecture", "Lecture", f"{_base}/1_understanding_regression/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/1_understanding_regression/handson.md"),
        ("solution", "Solution", f"{_base}/1_understanding_regression/solution_understanding_regression.py")],
    1: [("lecture", "Lecture", f"{_base}/2_train_test_split/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/2_train_test_split/handson.md"),
        ("solution", "Solution", f"{_base}/2_train_test_split/solution_train_test_split.py")],
    2: [("lecture", "Lecture", f"{_base}/3_fit_and_predict/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/3_fit_and_predict/handson.md"),
        ("solution", "Solution", f"{_base}/3_fit_and_predict/solution_fit_and_predict.py")],
    3: [("lecture", "Lecture", f"{_base}/4_evaluate_regression/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/4_evaluate_regression/handson.md"),
        ("solution", "Solution", f"{_base}/4_evaluate_regression/solution_evaluate_regression.py")],
}


# ── Helper ──────────────────────────────────────────────────────────────────

def base_ctx(step_num):
    return {
        "steps": STEPS,
        "current": step_num,
        "challenge": CHALLENGES[step_num],
        "lesson_id": LESSON_ID,
        "lesson_title": LESSON_TITLE,
        "url_prefix": f"/lesson/{LESSON_ID}",
        "materials": MATERIALS.get(step_num, []),
    }


# ── Routes ──────────────────────────────────────────────────────────────────

@bp.route("/")
def index():
    return render_template("s1_02/index.html",
                           steps=STEPS, lesson_id=LESSON_ID,
                           lesson_title=LESSON_TITLE,
                           url_prefix=f"/lesson/{LESSON_ID}")


@bp.route("/step/<int:n>")
def step(n):
    if n < 0 or n >= len(STEPS):
        return "Step not found", 404
    return render_template(f"s1_02/step_{n:02d}.html", **base_ctx(n))
