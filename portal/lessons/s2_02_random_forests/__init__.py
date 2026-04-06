"""
Lesson 2.2 — Random Forests
Flask Blueprint for the malware classification with random forests workshop.
"""

from flask import Blueprint, render_template

bp = Blueprint(
    "s2_02",
    __name__,
    template_folder="templates",
)

LESSON_ID = "s2_02"
LESSON_TITLE = "Random Forests"

# ── Step metadata ───────────────────────────────────────────────────────────

STEPS = [
    {"id": 0, "title": "From Tree to Forest",
     "sub": "Why a single tree overfits and how bagging fixes it"},
    {"id": 1, "title": "Train a Random Forest",
     "sub": "RandomForestClassifier, OOB score, tree vs forest"},
    {"id": 2, "title": "Feature Importance",
     "sub": "Stable importance rankings across many trees"},
    {"id": 3, "title": "Tune the Forest",
     "sub": "n_estimators sweep, max_features, learning curve"},
]

CHALLENGES = {
    0: {
        "q": "A single decision tree with no depth limit reaches 100% training accuracy on your malware dataset. Is that good news?",
        "a": "No -- it is a <strong>red flag</strong>. 100% training accuracy with an unbounded tree means the tree has memorised every training sample, including noise and outliers. On new malware samples it has never seen, accuracy drops significantly. This is <strong>overfitting</strong>. Bagging (Random Forest) fixes this by averaging many trees, each trained on a different bootstrap sample, which cancels out the individual trees' memorised noise.",
    },
    1: {
        "q": "You train a Random Forest with oob_score=True and get OOB accuracy of 0.94. Your test accuracy is 0.95. What does the close match tell you?",
        "a": "The close match between OOB and test accuracy is a <strong>good sign</strong>. OOB samples are data points each tree never saw during training (~37% per tree), so OOB accuracy is a built-in cross-validation estimate. When it closely matches the held-out test score, it confirms the model is <strong>generalising well</strong> and not overfitting. In a SOC context, this means your malware classifier should perform reliably on new samples arriving in production.",
    },
    2: {
        "q": "Your random forest says file_entropy is the most important feature for malware detection. An attacker learns this. What could they do?",
        "a": "The attacker could craft malware with <strong>artificially lowered entropy</strong> -- for example, by padding the binary with structured data or using a custom packer that produces output with entropy similar to benign files. This is <strong>adversarial evasion</strong>: once attackers know which features the model relies on, they can manipulate those exact features. This is why security teams should <strong>not publicise model feature importances</strong> and should use diverse, hard-to-manipulate features.",
    },
    3: {
        "q": "You sweep n_estimators from 10 to 500. Accuracy plateaus at 100 trees but training time keeps climbing. What do you recommend?",
        "a": "Recommend <strong>100 trees</strong> (the elbow of the learning curve). Beyond this point, each additional tree costs CPU time but adds less than 0.1% accuracy. In a security pipeline processing thousands of PE files per hour, <strong>inference speed matters</strong>. A 500-tree forest takes 5x longer to predict with negligible accuracy gain. Always pick the <strong>most cost-effective</strong> configuration -- especially when the model runs in a real-time detection pipeline.",
    },
}

# ── Course materials mapping ────────────────────────────────────────────────

_base = "curriculum/stage2_intermediate/02_random_forests"

MATERIALS = {
    0: [("lecture", "Lecture", f"{_base}/1_from_tree_to_forest/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/1_from_tree_to_forest/handson.md"),
        ("solution", "Solution", f"{_base}/1_from_tree_to_forest/solution_from_tree_to_forest.py")],
    1: [("lecture", "Lecture", f"{_base}/2_train_random_forest/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/2_train_random_forest/handson.md"),
        ("solution", "Solution", f"{_base}/2_train_random_forest/solution_train_random_forest.py")],
    2: [("lecture", "Lecture", f"{_base}/3_feature_importance/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/3_feature_importance/handson.md"),
        ("solution", "Solution", f"{_base}/3_feature_importance/solution_feature_importance.py")],
    3: [("lecture", "Lecture", f"{_base}/4_tune_the_forest/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/4_tune_the_forest/handson.md"),
        ("solution", "Solution", f"{_base}/4_tune_the_forest/solution_tune_the_forest.py")],
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
    return render_template("s2_02/index.html",
                           steps=STEPS, lesson_id=LESSON_ID,
                           lesson_title=LESSON_TITLE,
                           url_prefix=f"/lesson/{LESSON_ID}")


@bp.route("/step/<int:n>")
def step(n):
    if n < 0 or n >= len(STEPS):
        return "Step not found", 404
    return render_template(f"s2_02/step_{n:02d}.html", **base_ctx(n))
