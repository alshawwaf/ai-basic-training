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

# ── Quiz ────────────────────────────────────────────────────────────────────

QUIZ = [
    {
        "q": "What does a decision tree actually <em>learn</em> during training?",
        "options": [
            "A set of weights and biases like a neural network",
            "A series of if/else split rules on the features",
            "The mean of the target column",
            "A list of memorised training examples",
        ],
        "answer": 1,
        "explanation": "A trained tree is a hierarchy of <strong>if/else rules</strong> like <em>'if connection_rate &gt; 50.5 then go left, else go right'</em>. Each split is chosen to maximise information gain. That's it &mdash; no weights, no gradients.",
    },
    {
        "q": "A node has <strong>60 benign and 40 attack</strong> samples. What is its Gini impurity?",
        "options": [
            "0.0",
            "0.24",
            "0.48",
            "1.0",
        ],
        "answer": 2,
        "explanation": "Gini = 1 &minus; (0.6&sup2; + 0.4&sup2;) = 1 &minus; 0.52 = <strong>0.48</strong>. Pure nodes (all one class) have Gini = 0; the worst case is 0.5 for a 50/50 split. The tree picks splits that <em>lower</em> the weighted Gini of the children.",
    },
    {
        "q": "Why are decision trees particularly valued in security ML compared to neural networks?",
        "options": [
            "They are always more accurate",
            "They are interpretable &mdash; you can read the rules and explain every prediction to a SOC analyst",
            "They train faster on GPUs",
            "They handle text data better",
        ],
        "answer": 1,
        "explanation": "Decision trees are <strong>interpretable</strong>. You can export the rule set and tell an analyst exactly <em>why</em> a connection was flagged. Try doing that with a 100-million-parameter neural network. Interpretability builds trust with auditors and incident responders.",
    },
    {
        "q": "Your tree has 100% training accuracy but 73% test accuracy. What's happening?",
        "options": [
            "The tree is well-tuned",
            "The tree is overfitting &mdash; it has memorised the training data, including noise",
            "The data is corrupted",
            "scikit-learn has a bug",
        ],
        "answer": 1,
        "explanation": "A 27-point train/test gap is a textbook <strong>overfitting</strong> signal. With unlimited depth, the tree creates a leaf for almost every training sample. The fix: limit <code>max_depth</code> or use <code>min_samples_leaf</code> to force the tree to generalise.",
    },
    {
        "q": "You plot training and test accuracy as you increase <code>max_depth</code> from 1 to 20. What pattern indicates the right depth to pick?",
        "options": [
            "The deepest tree wins &mdash; always pick depth=20",
            "Pick the depth where the gap between train and test accuracy starts to widen",
            "Pick depth=1 for safety",
            "Pick the smallest tree where both accuracies are zero",
        ],
        "answer": 1,
        "explanation": "Watch the <strong>train-test gap</strong>. While both curves rise together, you're learning real patterns. The moment they diverge (train keeps climbing, test plateaus or drops) you're starting to overfit. Pick the depth just before the divergence.",
    },
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
        "quiz_count": len(QUIZ),
        "is_quiz": False,
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
