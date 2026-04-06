"""
Lesson 2.4 — Overfitting & Cross-Validation
Flask Blueprint for the overfitting diagnosis and cross-validation workshop.
"""

from flask import Blueprint, render_template

bp = Blueprint(
    "s2_04",
    __name__,
    template_folder="templates",
)

LESSON_ID = "s2_04"
LESSON_TITLE = "Overfitting & Cross-Validation"

# ── Step metadata ───────────────────────────────────────────────────────────

STEPS = [
    {"id": 0, "title": "Overfitting Demo",
     "sub": "Watch train vs validation accuracy diverge as depth grows"},
    {"id": 1, "title": "Bias-Variance Tradeoff",
     "sub": "Underfit, good fit, overfit -- three regimes visualised"},
    {"id": 2, "title": "K-Fold Cross-Validation",
     "sub": "Reliable performance estimates with cross_val_score"},
    {"id": 3, "title": "Validation Curve",
     "sub": "Automated parameter sweep with validation_curve()"},
]

CHALLENGES = {
    0: {
        "q": "Your intrusion detector scores 100% on training data and 74% on validation data. The security team says 'the model works.' What do you tell them?",
        "a": "The 26-point gap is a <strong>massive overfitting signal</strong>. The model has memorised the training attacks but will fail on new attack variants it has never seen. In production, it would miss novel threats while appearing to work in testing. You need to <strong>reduce model complexity</strong> (lower max_depth, add regularisation) and retrain until the gap narrows to 2-3 points -- even if training accuracy drops to 97%.",
    },
    1: {
        "q": "A depth-1 tree and a depth-50 tree both fail in production, but for opposite reasons. Explain what each gets wrong.",
        "a": "The <strong>depth-1 tree</strong> (high bias) is too simple -- it uses a single split and misses most attack patterns. Both training and test accuracy are around 65%. The <strong>depth-50 tree</strong> (high variance) memorises every training sample, including noise. It scores 100% on training data but drops to ~92% on new data. In security, the depth-1 tree misses most attacks outright; the depth-50 tree catches training-set attacks but fails on new attack variants.",
    },
    2: {
        "q": "You get cross-validation scores of [0.98, 0.71, 0.95, 0.96, 0.94]. One fold is much lower. Should you worry?",
        "a": "Yes -- that 0.71 fold is a <strong>red flag</strong>. It means there is a subset of your data where the model performs terribly. In security, this could mean an entire attack category is being missed. Investigate which samples are in that fold. Possible causes: <strong>class imbalance</strong> concentrated in that fold, a distinct attack type the model cannot generalise to, or data quality issues in that subset. A single train/test split might never have caught this.",
    },
    3: {
        "q": "The validation curve shows that max_depth=5 gives the best validation score. Your manager asks you to use max_depth=15 because 'more is better.' How do you respond?",
        "a": "Show the validation curve plot. At depth 15, training accuracy is 100% but validation accuracy has <strong>dropped below the peak</strong>. The curve proves that extra depth memorises training noise rather than learning real patterns. In a security context, the depth-15 model would produce more <strong>false positives</strong> on benign traffic (because it learned noise patterns) and miss <strong>novel attacks</strong> (because it overfit to specific training examples). The validation curve is your evidence -- data beats opinions.",
    },
}

# ── Course materials mapping ────────────────────────────────────────────────

_base = "curriculum/stage2_intermediate/04_overfitting_crossval"

MATERIALS = {
    0: [("lecture", "Lecture", f"{_base}/1_overfitting_demo/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/1_overfitting_demo/handson.md"),
        ("solution", "Solution", f"{_base}/1_overfitting_demo/solution_overfitting_demo.py")],
    1: [("lecture", "Lecture", f"{_base}/2_bias_variance/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/2_bias_variance/handson.md"),
        ("solution", "Solution", f"{_base}/2_bias_variance/solution_bias_variance.py")],
    2: [("lecture", "Lecture", f"{_base}/3_kfold_crossval/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/3_kfold_crossval/handson.md"),
        ("solution", "Solution", f"{_base}/3_kfold_crossval/solution_kfold_crossval.py")],
    3: [("lecture", "Lecture", f"{_base}/4_validation_curve/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/4_validation_curve/handson.md"),
        ("solution", "Solution", f"{_base}/4_validation_curve/solution_validation_curve.py")],
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
    return render_template("s2_04/index.html",
                           steps=STEPS, lesson_id=LESSON_ID,
                           lesson_title=LESSON_TITLE,
                           url_prefix=f"/lesson/{LESSON_ID}")


@bp.route("/step/<int:n>")
def step(n):
    if n < 0 or n >= len(STEPS):
        return "Step not found", 404
    return render_template(f"s2_04/step_{n:02d}.html", **base_ctx(n))
