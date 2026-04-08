"""
Lesson 1.3 — Logistic Regression
Flask Blueprint for the phishing URL classification workshop.
"""

from flask import Blueprint, render_template

bp = Blueprint(
    "s1_03",
    __name__,
    template_folder="templates",
)

LESSON_ID = "s1_03"
LESSON_TITLE = "Logistic Regression"

# ── Step metadata ───────────────────────────────────────────────────────────

STEPS = [
    {"id": 0, "title": "From Regression to Classification",
     "sub": "The sigmoid function and why linear regression fails for yes/no",
     "icon": "sigmoid-curve"},
    {"id": 1, "title": "Feature Engineering URLs",
     "sub": "Turn raw URLs into numbers a model can learn from",
     "icon": "url-tokens"},
    {"id": 2, "title": "Train and Evaluate",
     "sub": "Scaling, fitting, confusion matrix, classification report",
     "icon": "train-evaluate"},
    {"id": 3, "title": "Threshold Tuning",
     "sub": "predict_proba() and the precision-recall tradeoff",
     "icon": "threshold-slider"},
]

CHALLENGES = {
    0: {
        "q": "Feed a z-value of 0 into the sigmoid. What probability do you get? What does this mean for a URL with perfectly balanced evidence?",
        "a": "σ(0) = 0.5 \u2014 the model is completely uncertain. This is the <strong>decision boundary</strong>: when the weighted features sum to zero, the model cannot decide. In security, sitting on the boundary means you need more features or more data to break the tie.",
    },
    1: {
        "q": "A phishing URL uses HTTPS and has a valid certificate. Does that make it safe? Which features would still catch it?",
        "a": "<code>uses_https = 1</code> alone does not indicate safety \u2014 most phishing sites now use HTTPS. But features like <strong>high url_length</strong>, <strong>has_at_symbol</strong>, <strong>has_ip_address</strong>, and <strong>num_hyphens</strong> would still flag it. This is why ML uses <em>multiple</em> features, not just one.",
    },
    2: {
        "q": "Your model has 95% accuracy but only 60% recall on phishing. Your boss says '95% is great'. What do you tell them?",
        "a": "60% recall means <strong>40% of phishing URLs get through</strong> to users. If 100 phishing emails arrive daily, 40 reach inboxes. Accuracy is misleading when classes are imbalanced \u2014 the model gets credit for correctly labelling the easy majority class. <strong>Recall is the metric that matters</strong> when missing a positive is dangerous.",
    },
    3: {
        "q": "An email security gateway processes 1 million URLs per day. At threshold 0.3, precision is 85%. How many false alarms per day if 1% of URLs are phishing?",
        "a": "10,000 phishing URLs. At 85% precision, for every 100 flagged URLs, 15 are false alarms. If recall is ~95%, we flag ~9,500 true positives. Total flagged \u2248 9,500 / 0.85 \u2248 11,176. False alarms \u2248 11,176 - 9,500 = <strong>~1,676 per day</strong>. That's ~70 per hour \u2014 manageable if automated triage handles most of them.",
    },
}

# ── Course materials mapping ────────────────────────────────────────────────

_base = "curriculum/stage1_classic_ml/03_logistic_regression"

MATERIALS = {
    0: [("lecture", "Lecture", f"{_base}/1_from_regression_to_classification/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/1_from_regression_to_classification/handson.md"),
        ("solution", "Solution", f"{_base}/1_from_regression_to_classification/solution_from_regression_to_classification.py")],
    1: [("lecture", "Lecture", f"{_base}/2_feature_engineering_urls/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/2_feature_engineering_urls/handson.md"),
        ("solution", "Solution", f"{_base}/2_feature_engineering_urls/solution_feature_engineering_urls.py")],
    2: [("lecture", "Lecture", f"{_base}/3_train_and_evaluate/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/3_train_and_evaluate/handson.md"),
        ("solution", "Solution", f"{_base}/3_train_and_evaluate/solution_train_and_evaluate.py")],
    3: [("lecture", "Lecture", f"{_base}/4_threshold_tuning/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/4_threshold_tuning/handson.md"),
        ("solution", "Solution", f"{_base}/4_threshold_tuning/solution_threshold_tuning.py")],
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
    return render_template("s1_03/index.html",
                           steps=STEPS, lesson_id=LESSON_ID,
                           lesson_title=LESSON_TITLE,
                           url_prefix=f"/lesson/{LESSON_ID}")


@bp.route("/step/<int:n>")
def step(n):
    if n < 0 or n >= len(STEPS):
        return "Step not found", 404
    return render_template(f"s1_03/step_{n:02d}.html", **base_ctx(n))
