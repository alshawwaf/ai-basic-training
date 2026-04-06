"""
Lesson 3.2 — Dropout & Regularisation
Flask Blueprint for the dropout, batch normalisation, and early stopping workshop.
"""

from flask import Blueprint, render_template

bp = Blueprint(
    "s3_02",
    __name__,
    template_folder="templates",
)

LESSON_ID = "s3_02"
LESSON_TITLE = "Dropout & Regularisation"

STEPS = [
    {"id": 0, "title": "Demonstrate Overfitting",  "sub": "Build a deliberately oversized network"},
    {"id": 1, "title": "Add Dropout",              "sub": "Randomly silence neurons to regularise"},
    {"id": 2, "title": "Batch Normalisation",       "sub": "Stabilise training with normalised activations"},
    {"id": 3, "title": "Early Stopping",            "sub": "Stop training at the right moment"},
]

CHALLENGES = {
    0: {
        "q": "A network has 134,000 parameters but only 1,600 training samples. What ratio does that give, and why is it a problem for a security ML model?",
        "a": "<strong>84 parameters per sample</strong> — the network can memorise every training example, including noise. In security, an overfit IDS memorises exact attack signatures from training but <strong>misses novel attack variants</strong> because it never learned the underlying pattern (e.g. high connection rate + many failed logins = brute force).",
    },
    1: {
        "q": "A SOC deploys a model with Dropout(0.5). During inference on live traffic, are neurons still being dropped? What would happen if they were?",
        "a": "No — Dropout is <strong>automatically disabled during inference</strong> (Keras handles this via the <code>training</code> flag). If neurons were still dropped during inference, predictions would be <strong>random and inconsistent</strong> — the same packet could be classified as malicious one second and benign the next. That is unacceptable for production alerting.",
    },
    2: {
        "q": "Without BatchNorm, layer 2 receives inputs with mean=0.5 at epoch 1 but mean=2.1 at epoch 10. How does this 'internal covariate shift' affect a malware classifier in practice?",
        "a": "Layer 2 must constantly re-adapt to a <strong>moving target distribution</strong>, slowing convergence and requiring a lower learning rate. For a malware classifier, this means <strong>longer training times</strong> and more sensitivity to weight initialisation. BatchNorm fixes the input distribution at each layer, allowing higher learning rates and <strong>faster, more stable training</strong>.",
    },
    3: {
        "q": "You set patience=5 and the model's best val_loss was at epoch 25. Training stopped at epoch 30. With restore_best_weights=True, which epoch's weights does the model use for prediction?",
        "a": "Epoch <strong>25</strong> — the epoch with the best validation loss. Without <code>restore_best_weights=True</code>, the model would use the <strong>epoch 30 weights</strong>, which are worse. In security ML, this matters because those last 5 epochs of overfitting could cause the model to <strong>miss new attack patterns</strong> it had previously learned to detect.",
    },
}

_base = "curriculum/stage3_neural_networks/02_dropout_regularisation"

MATERIALS = {
    0: [("lecture", "Demonstrate Overfitting", f"{_base}/1_demonstrate_overfitting/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/1_demonstrate_overfitting/handson.md"),
        ("solution", "Solution", f"{_base}/1_demonstrate_overfitting/solution_demonstrate_overfitting.py")],
    1: [("lecture", "Add Dropout", f"{_base}/2_add_dropout/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/2_add_dropout/handson.md"),
        ("solution", "Solution", f"{_base}/2_add_dropout/solution_add_dropout.py")],
    2: [("lecture", "Batch Normalisation", f"{_base}/3_batch_normalisation/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/3_batch_normalisation/handson.md"),
        ("solution", "Solution", f"{_base}/3_batch_normalisation/solution_batch_normalisation.py")],
    3: [("lecture", "Early Stopping", f"{_base}/4_early_stopping/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/4_early_stopping/handson.md"),
        ("solution", "Solution", f"{_base}/4_early_stopping/solution_early_stopping.py")],
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
    }


@bp.route("/")
def index():
    return render_template("s3_02/index.html",
                           steps=STEPS, lesson_id=LESSON_ID,
                           lesson_title=LESSON_TITLE,
                           url_prefix=f"/lesson/{LESSON_ID}")


@bp.route("/step/<int:n>")
def step(n):
    if n < 0 or n >= len(STEPS):
        return "Step not found", 404
    return render_template(f"s3_02/step_{n:02d}.html", **base_ctx(n))
