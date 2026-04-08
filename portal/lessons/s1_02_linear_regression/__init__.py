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
     "sub": "Regression vs classification, scatter plots, EDA",
     "icon": "regression-line"},
    {"id": 1, "title": "What Is a Model?",
     "sub": "A model is two numbers — drag the knobs and BE the algorithm",
     "icon": "model-knobs"},
    {"id": 2, "title": "Train / Test Split",
     "sub": "Why we split data and how to avoid data leakage",
     "icon": "train-test-split"},
    {"id": 3, "title": "Fit and Predict",
     "sub": "Slope, intercept, and the regression line",
     "icon": "fit-predict"},
    {"id": 4, "title": "Evaluate and Detect",
     "sub": "MSE, RMSE, R² — build a security baseline",
     "icon": "metrics-gauge"},
]

# ── Quiz ────────────────────────────────────────────────────────────────────
# Multiple-choice questions covering the lesson's key concepts. Each entry:
#   q          : the question
#   options    : list of choices
#   answer     : 0-based index of the correct choice
#   explanation: shown after the user reveals or answers the question
#
# The quiz is rendered by the shared portal/templates/quiz.html template via
# the /quiz route below. State is persisted to localStorage per-lesson so
# learners can come back, see what they got right, and retake.

QUIZ = [
    {
        "q": "Linear regression is best suited for predicting which kind of value?",
        "options": [
            "A category, like spam vs. not-spam",
            "A continuous number, like response time in milliseconds",
            "A cluster assignment for unlabeled data",
            "A probability between 0 and 1 only",
        ],
        "answer": 1,
        "explanation": "Linear regression outputs a real number with no upper bound. Categories are the job of <strong>logistic regression</strong> or trees; bounded probabilities are <strong>logistic</strong>; clusters come from unsupervised methods like K-means.",
    },
    {
        "q": "In <code>y = w·x + b</code>, what are <code>w</code> and <code>b</code> after training?",
        "options": [
            "Hyperparameters you tune by hand",
            "Random initialisation values",
            "The slope and intercept &mdash; the entire model",
            "Two pointers into the training data",
        ],
        "answer": 2,
        "explanation": "For one-feature linear regression, the model <em>is</em> those two numbers. Once fit, you can throw the training data away and ship just <code>w</code> and <code>b</code>. That's the whole point of step 1: <strong>a model is two numbers</strong>.",
    },
    {
        "q": "Why do we split data into a train set and a test set?",
        "options": [
            "It makes training faster",
            "scikit-learn refuses to fit otherwise",
            "To detect overfitting and estimate real-world performance",
            "To save memory during fitting",
        ],
        "answer": 2,
        "explanation": "The test set simulates data the model has never seen. If train R&sup2; is much higher than test R&sup2;, the model has memorised the training rows and will fail in production &mdash; classic <strong>overfitting</strong>.",
    },
    {
        "q": "Your response-time model reports <strong>RMSE = 15 ms</strong>. What does that mean?",
        "options": [
            "The model is wrong 15% of the time",
            "Predictions are off by roughly 15 ms on average",
            "There are 15 outliers in the dataset",
            "Training took 15 milliseconds",
        ],
        "answer": 1,
        "explanation": "RMSE is in the <em>same units</em> as the target. ~15 ms is the typical magnitude of prediction error &mdash; useful because you can compare it directly to the response times you're predicting.",
    },
    {
        "q": "You're using <code>k&sigma;</code> residual thresholding to flag slow responses. What does the choice of <code>k</code> trade off?",
        "options": [
            "Training time vs. inference time",
            "Linear vs. polynomial features",
            "Detection rate vs. false alarms (and analyst fatigue)",
            "Memory usage vs. CPU usage",
        ],
        "answer": 2,
        "explanation": "Lower <code>k</code> (e.g. 2&sigma;) catches more anomalies but also fires on more benign noise. Higher <code>k</code> (e.g. 3&sigma;) is conservative but misses subtle attacks. This is the classic <strong>alert fatigue</strong> tradeoff every SOC faces.",
    },
]


CHALLENGES = {
    0: {
        "q": "Change the data range from 0\u2013200 rps to 0\u20132000 rps. Does the scatter plot still look linear? What does that tell you about the model's assumptions?",
        "a": "At very high loads, real servers saturate \u2014 response times spike exponentially. The scatter would curve upward, and a straight line would under-predict at high loads. This is why <strong>linear regression only works when the true relationship is approximately linear</strong>. For non-linear patterns you need polynomial features or a different model.",
    },
    1: {
        "q": "Run <code>explore_model_knobs.py</code>. By hand, try to push the RMSE below 20 ms. Then click \"Let the algorithm do it\". By how much did the algorithm beat your best score, and why?",
        "a": "Most learners can get the RMSE into the 20\u201340 ms range by eye. The algorithm typically lands at <strong>~15 ms</strong> \u2014 better, but not by orders of magnitude. The algorithm wins because it solves the optimal <code>w</code>, <code>b</code> analytically (the <em>normal equation</em>) instead of guessing. The key insight isn't that the algorithm is smart \u2014 it's that <strong>the model is just those two numbers</strong>, and the algorithm's only job is picking them. Once it has, the algorithm is done; you ship the numbers.",
    },
    2: {
        "q": "What happens if you evaluate the model on the training data instead of the test set? Try it \u2014 is R\u00b2 higher or lower?",
        "a": "Training R\u00b2 is almost always higher (better) than test R\u00b2 because the model has already memorised the training examples. The gap between them is the <strong>overfitting indicator</strong>. In security ML, this means your malware detector may look perfect in the lab but fail on live traffic.",
    },
    3: {
        "q": "The slope is ~1.82 ms per rps. If you doubled the server's CPU, what would you expect to happen to the slope? What about the intercept?",
        "a": "A faster server would have a <strong>lower slope</strong> (less added latency per extra request) and possibly a <strong>lower intercept</strong> (less baseline overhead). The model's parameters have physical meaning \u2014 that's the power of interpretable models in security. You can explain to a SOC analyst <em>why</em> the alert fired.",
    },
    4: {
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
    1: [("solution", "Explore Script", f"{_base}/0_interactive_intro/explore_model_knobs.py")],
    2: [("lecture", "Lecture", f"{_base}/2_train_test_split/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/2_train_test_split/handson.md"),
        ("solution", "Solution", f"{_base}/2_train_test_split/solution_train_test_split.py")],
    3: [("lecture", "Lecture", f"{_base}/3_fit_and_predict/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/3_fit_and_predict/handson.md"),
        ("solution", "Solution", f"{_base}/3_fit_and_predict/solution_fit_and_predict.py")],
    4: [("lecture", "Lecture", f"{_base}/4_evaluate_regression/lecture.md"),
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
        "quiz_count": len(QUIZ),
        "is_quiz": False,
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


@bp.route("/quiz")
def quiz():
    return render_template(
        "quiz.html",
        steps=STEPS,
        current=len(STEPS) - 1,  # keep last step "complete" in progress bar
        lesson_id=LESSON_ID,
        lesson_title=LESSON_TITLE,
        url_prefix=f"/lesson/{LESSON_ID}",
        quiz=QUIZ,
        quiz_count=len(QUIZ),
        is_quiz=True,
    )
