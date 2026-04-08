"""
Lesson 1.4 — Decision Trees
Flask Blueprint for the network traffic classification workshop.
"""

from flask import Blueprint, render_template

bp = Blueprint(
    "s1_04",
    __name__,
    template_folder="templates",
)

LESSON_ID = "s1_04"
LESSON_TITLE = "Decision Trees"

# ── Step metadata ───────────────────────────────────────────────────────────

STEPS = [
    {"id": 0, "title": "How Trees Make Decisions",
     "sub": "If/else rules, Gini impurity, information gain",
     "icon": "tree-branches"},
    {"id": 1, "title": "Train and Read the Tree",
     "sub": "Visualise the tree and extract learned rules",
     "icon": "tree-train"},
    {"id": 2, "title": "Feature Importance",
     "sub": "Which features drive predictions?",
     "icon": "bar-ranked"},
    {"id": 3, "title": "Depth and Overfitting",
     "sub": "Finding the sweet-spot between too simple and too complex",
     "icon": "tree-depth"},
]

CHALLENGES = {
    0: {
        "q": "A node has 60 benign and 40 attack samples. Calculate its Gini impurity by hand. What Gini would a perfect split produce?",
        "a": "Gini = 1 - (0.6\u00b2 + 0.4\u00b2) = 1 - (0.36 + 0.16) = <strong>0.48</strong>. A perfect split produces two pure nodes with Gini = 0.0 each. The weighted average is 0.0 \u2014 that's maximum information gain. In practice, perfect splits are rare; the tree picks the <em>best available</em> split.",
    },
    1: {
        "q": "Export the tree as text and find the first rule. Could you explain this rule to a non-technical SOC analyst?",
        "a": "Example: <em>'If connection_rate > 50.5 and unique_dest_ports > 20, classify as port_scan.'</em> This is why decision trees are valuable in security \u2014 you can <strong>explain every prediction</strong> to a human. Try doing that with a neural network. Interpretability builds trust with analysts and auditors.",
    },
    2: {
        "q": "If you remove the top feature (connection_rate) and retrain, what happens to accuracy? Does the second feature become more important?",
        "a": "Accuracy drops because you removed the most discriminative signal. The second feature (<code>bytes_sent</code>) absorbs some of the lost signal and its importance score increases. This reveals <strong>feature redundancy</strong> \u2014 correlated features can partially substitute for each other.",
    },
    3: {
        "q": "Plot training and test accuracy for depths 1\u201320. At what depth does the gap between them start growing fast?",
        "a": "Typically around depth 5\u20137. Training accuracy keeps rising toward 100%, but test accuracy plateaus or drops. The growing gap is the <strong>overfitting signal</strong>. In production security models, you'd pick the depth just before the gap starts widening \u2014 maximising generalisation to new, unseen traffic.",
    },
}

# ── Course materials mapping ────────────────────────────────────────────────

_base = "curriculum/stage1_classic_ml/04_decision_trees"

MATERIALS = {
    0: [("lecture", "Lecture", f"{_base}/1_how_trees_make_decisions/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/1_how_trees_make_decisions/handson.md"),
        ("solution", "Solution", f"{_base}/1_how_trees_make_decisions/solution_how_trees_make_decisions.py")],
    1: [("lecture", "Lecture", f"{_base}/2_train_and_read_the_tree/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/2_train_and_read_the_tree/handson.md"),
        ("solution", "Solution", f"{_base}/2_train_and_read_the_tree/solution_train_and_read_the_tree.py")],
    2: [("lecture", "Lecture", f"{_base}/3_feature_importance/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/3_feature_importance/handson.md"),
        ("solution", "Solution", f"{_base}/3_feature_importance/solution_feature_importance.py")],
    3: [("lecture", "Lecture", f"{_base}/4_depth_and_overfitting/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/4_depth_and_overfitting/handson.md"),
        ("solution", "Solution", f"{_base}/4_depth_and_overfitting/solution_depth_and_overfitting.py")],
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
    return render_template("s1_04/index.html",
                           steps=STEPS, lesson_id=LESSON_ID,
                           lesson_title=LESSON_TITLE,
                           url_prefix=f"/lesson/{LESSON_ID}")


@bp.route("/step/<int:n>")
def step(n):
    if n < 0 or n >= len(STEPS):
        return "Step not found", 404
    return render_template(f"s1_04/step_{n:02d}.html", **base_ctx(n))
