"""
Lesson 3.4 — Hyperparameter Tuning
Flask Blueprint for the hyperparameter exploration workshop.
"""

from flask import Blueprint, render_template

bp = Blueprint(
    "s3_04",
    __name__,
    template_folder="templates",
)

LESSON_ID = "s3_04"
LESSON_TITLE = "Hyperparameter Tuning"

STEPS = [
    {"id": 0, "title": "What Are Hyperparameters?",     "sub": "Parameters vs hyperparameters",            "icon": "dial-tuning"},
    {"id": 1, "title": "Learning Rate Sensitivity",     "sub": "The most important knob to turn",          "icon": "learning-rate"},
    {"id": 2, "title": "Batch Size Effects",            "sub": "Gradient noise vs training stability",     "icon": "batch-stack"},
    {"id": 3, "title": "Architecture Search",           "sub": "Systematic search over width and depth",   "icon": "arch-search"},
]

# ── Quiz ────────────────────────────────────────────────────────────────────

QUIZ = [
    {
        "q": "What is the difference between a <strong>parameter</strong> and a <strong>hyperparameter</strong>?",
        "options": [
            "There is no difference",
            "Parameters (weights, biases) are <em>learned</em> by gradient descent during training; hyperparameters (learning rate, batch size, depth) are <em>set by the engineer</em> before training",
            "Hyperparameters are bigger numbers",
            "Parameters live in the cloud, hyperparameters live locally",
        ],
        "answer": 1,
        "explanation": "The model <strong>learns</strong> weights and biases. The engineer <strong>chooses</strong> hyperparameters. This distinction matters for reproducibility &mdash; hyperparameters must be version-controlled because the same training script with different hyperparameters produces a different model.",
    },
    {
        "q": "You train with <code>lr=0.1</code> and the loss oscillates wildly. You switch to <code>lr=0.0001</code> and the loss barely moves after 50 epochs. What should you try next?",
        "options": [
            "Give up on neural networks",
            "<code>lr=0.001</code> &mdash; the Adam default. 0.1 overshoots the minimum (steps too big), 0.0001 takes steps too small to make progress; the middle ground balances stability and speed",
            "Use lr=10 to be safe",
            "Use lr=0",
        ],
        "answer": 1,
        "explanation": "Learning rate is the <strong>most important hyperparameter</strong>. Too high = oscillation/divergence; too low = slow or no progress. <code>1e-3</code> is the Adam default for a reason &mdash; it's a sane starting point for most problems.",
    },
    {
        "q": "You train a phishing detector with <code>batch_size=1024</code> on 10,000 samples (~10 updates per epoch). What's the likely problem?",
        "options": [
            "Nothing &mdash; bigger batches always help",
            "Very smooth gradients that may converge to a sharp minimum that generalises poorly; few updates per epoch reduces variety; try batch_size=32 or 64 for noisier gradients that escape sharp minima",
            "The model will train too slowly",
            "scikit-learn won't allow it",
        ],
        "answer": 1,
        "explanation": "Tiny batch counts per epoch produce very smooth gradients that find <em>sharp minima</em> &mdash; areas of low training loss but poor generalisation. Smaller batches add gradient noise that helps the model escape sharp minima and find <strong>flatter, better-generalising</strong> ones.",
    },
    {
        "q": "Your grid search tests <strong>3 widths &times; 3 depths &times; 3 learning rates &times; 3 batch sizes = 81 models</strong>, each taking 2 minutes. What's a faster alternative that often finds equally good hyperparameters?",
        "options": [
            "Run the grid search twice for redundancy",
            "<strong>Random search</strong> &mdash; sample 20-30 random combinations; Bergstra &amp; Bengio (2012) showed it finds good hyperparameters in fewer trials than grid search",
            "Skip tuning entirely",
            "Use only the default values",
        ],
        "answer": 1,
        "explanation": "Random search wins because grid search wastes effort on unimportant dimensions (e.g. testing 3 batch sizes when only learning rate matters). Random search explores <strong>more unique values per dimension</strong> in the same number of trials &mdash; usually finding better configurations faster.",
    },
    {
        "q": "Why must you document and version-control your hyperparameters?",
        "options": [
            "It's a legal requirement",
            "Reproducibility &mdash; if a security model's detection rate changes after a retrain, you need to know exactly which hyperparameters changed to debug what happened",
            "It speeds up training",
            "It improves accuracy directly",
        ],
        "answer": 1,
        "explanation": "Hyperparameters are part of the model's identity. If your IDS recall drops from 92% to 78% after a retrain, the first question is <em>'what did we change?'</em>. Without versioned hyperparameters, you can't answer that &mdash; and you can't roll back.",
    },
]


CHALLENGES = {
    0: {
        "q": "Your colleague says 'the model learned a learning rate of 0.001.' Why is this statement wrong, and why does the distinction matter for reproducible security ML?",
        "a": "Learning rate is a <strong>hyperparameter</strong> — set by the engineer before training, not learned by gradient descent. The model learns <strong>weights and biases</strong> (parameters). This matters because hyperparameters must be <strong>documented and version-controlled</strong> for reproducibility. If a security model's detection rate drops after retraining, you need to know exactly which hyperparameters changed.",
    },
    1: {
        "q": "You train a threat classifier with lr=0.1 and the loss oscillates wildly, never converging. You switch to lr=0.0001 and the loss barely moves after 50 epochs. What should you try, and why?",
        "a": "Try <strong>lr=0.001</strong> — the Adam optimizer default. Learning rate 0.1 overshoots the loss minimum (too large steps), while 0.0001 takes steps too small to make progress in your epoch budget. In security ML, time matters: you need the model retrained and deployed <strong>before the threat landscape shifts</strong>. The middle ground balances convergence speed with stability.",
    },
    2: {
        "q": "You train a phishing detector with batch_size=1024 on 10,000 samples. That is only ~10 gradient updates per epoch. What problem might this cause, and what batch size would you try instead?",
        "a": "With only 10 updates per epoch, the gradient is very <strong>smooth but may converge to a sharp minimum</strong> that generalises poorly. The model also sees very little variety per update. Try <strong>batch_size=32 or 64</strong> — giving 156-312 updates per epoch. The noisier gradients help escape sharp minima and often find <strong>flatter minima that generalise better</strong> to unseen phishing samples.",
    },
    3: {
        "q": "Your grid search tests 3 widths x 3 depths x 3 learning rates x 3 batch sizes = 81 models. Each takes 2 minutes to train. How long does this take, and what is a faster alternative?",
        "a": "81 models x 2 min = <strong>162 minutes (2.7 hours)</strong>. A faster alternative is <strong>random search</strong>: sample 20-30 random combinations from the same space. Research by Bergstra & Bengio (2012) showed random search finds good hyperparameters in <strong>fewer trials</strong> than grid search because it explores more unique values per dimension. For security teams with limited compute, random search is the practical choice.",
    },
}

_base = "curriculum/stage3_neural_networks/04_hyperparameter_tuning"

MATERIALS = {
    0: [("lecture", "What Are Hyperparameters", f"{_base}/1_what_are_hyperparameters/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/1_what_are_hyperparameters/handson.md"),
        ("solution", "Solution", f"{_base}/1_what_are_hyperparameters/solution_what_are_hyperparameters.py")],
    1: [("lecture", "Learning Rate Sensitivity", f"{_base}/2_learning_rate_sensitivity/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/2_learning_rate_sensitivity/handson.md"),
        ("solution", "Solution", f"{_base}/2_learning_rate_sensitivity/solution_learning_rate_sensitivity.py")],
    2: [("lecture", "Batch Size Effects", f"{_base}/3_batch_size_effects/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/3_batch_size_effects/handson.md"),
        ("solution", "Solution", f"{_base}/3_batch_size_effects/solution_batch_size_effects.py")],
    3: [("lecture", "Architecture Search", f"{_base}/4_architecture_search/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/4_architecture_search/handson.md"),
        ("solution", "Solution", f"{_base}/4_architecture_search/solution_architecture_search.py")],
}


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


@bp.route("/")
def index():
    return render_template("s3_04/index.html",
                           steps=STEPS, lesson_id=LESSON_ID,
                           lesson_title=LESSON_TITLE,
                           url_prefix=f"/lesson/{LESSON_ID}")


@bp.route("/step/<int:n>")
def step(n):
    if n < 0 or n >= len(STEPS):
        return "Step not found", 404
    return render_template(f"s3_04/step_{n:02d}.html", **base_ctx(n))


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
