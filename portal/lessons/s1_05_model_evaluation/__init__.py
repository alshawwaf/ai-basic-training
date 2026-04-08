"""
Lesson 1.5 — Model Evaluation
Flask Blueprint for the security-focused evaluation metrics workshop.
"""

from flask import Blueprint, render_template

bp = Blueprint(
    "s1_05",
    __name__,
    template_folder="templates",
)

LESSON_ID = "s1_05"
LESSON_TITLE = "Model Evaluation"

# ── Step metadata ───────────────────────────────────────────────────────────

STEPS = [
    {"id": 0, "title": "The Accuracy Trap",
     "sub": "Why 99% accuracy can mean zero detections",
     "icon": "accuracy-trap"},
    {"id": 1, "title": "Confusion Matrix",
     "sub": "TP, TN, FP, FN — the four outcomes of every prediction",
     "icon": "confusion-matrix"},
    {"id": 2, "title": "Precision, Recall, F1",
     "sub": "The metrics that actually matter in security",
     "icon": "pr-formula"},
    {"id": 3, "title": "ROC Curve and AUC",
     "sub": "Compare classifiers across all thresholds",
     "icon": "roc-curve"},
    {"id": 4, "title": "Threshold Tuning",
     "sub": "Choose the right operating point for your SOC",
     "icon": "threshold-slider"},
]

CHALLENGES = {
    0: {
        "q": "Your malware detector has 99.9% accuracy on enterprise telemetry where 0.05% of events are malicious. How many real threats does it catch?",
        "a": "If the model always predicts 'benign', it gets 99.95% accuracy \u2014 even <em>better</em> than 99.9%. Your 99.9% model might be catching <strong>zero</strong> threats. The only way to know is to check <strong>recall</strong>: what fraction of actual malware was flagged?",
    },
    1: {
        "q": "Your IDS produced: TP=45, FP=300, FN=5, TN=9650. Calculate precision and recall. Is this a good system?",
        "a": "Precision = 45/(45+300) = <strong>13%</strong>. Recall = 45/(45+5) = <strong>90%</strong>. It catches 90% of attacks but only 1 in 8 alerts is real. Whether this is 'good' depends on your SOC's capacity. 300 false alarms/day might be acceptable if they're auto-triaged; unacceptable if humans must investigate each one.",
    },
    2: {
        "q": "Two models: Model A has precision=0.95, recall=0.60. Model B has precision=0.70, recall=0.95. Which do you deploy for email phishing?",
        "a": "For phishing email scanning, <strong>Model B</strong>. Missing a phishing email (FN) can lead to credential theft and lateral movement. A false positive only means one legitimate email gets quarantined. Recall matters more here. But for auto-blocking at a firewall? Model A \u2014 blocking legitimate traffic has business impact.",
    },
    3: {
        "q": "Model X has AUC=0.92, Model Y has AUC=0.95. Can you always pick Model Y?",
        "a": "Not necessarily. AUC averages performance across <strong>all</strong> thresholds, but you only operate at <strong>one</strong>. Model X might outperform Y in the low-FPR region you actually care about. Always check the ROC curve shape, not just the AUC number. In security, the region near FPR=0.01 often matters most.",
    },
    4: {
        "q": "Your SOC team says they can handle 50 alerts per day. Your model produces 200 at threshold 0.3 and 30 at threshold 0.6. What threshold do you recommend?",
        "a": "Threshold 0.6 keeps alerts under capacity (30/day), but check how many real attacks it misses. If recall drops from 95% to 40%, you're missing 60% of threats. The answer might be: deploy at <strong>0.45</strong> (find the threshold that produces ~50 alerts), or add <strong>auto-triage</strong> to handle volume at 0.3. The threshold decision is operational, not just mathematical.",
    },
}

# ── Course materials mapping ────────────────────────────────────────────────

_base = "curriculum/stage1_classic_ml/05_model_evaluation"

MATERIALS = {
    0: [("lecture", "Lecture", f"{_base}/1_the_accuracy_trap/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/1_the_accuracy_trap/handson.md"),
        ("solution", "Solution", f"{_base}/1_the_accuracy_trap/solution_the_accuracy_trap.py")],
    1: [("lecture", "Lecture", f"{_base}/2_confusion_matrix/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/2_confusion_matrix/handson.md"),
        ("solution", "Solution", f"{_base}/2_confusion_matrix/solution_confusion_matrix.py")],
    2: [("lecture", "Lecture", f"{_base}/3_precision_recall_f1/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/3_precision_recall_f1/handson.md"),
        ("solution", "Solution", f"{_base}/3_precision_recall_f1/solution_precision_recall_f1.py")],
    3: [("lecture", "Lecture", f"{_base}/4_roc_and_auc/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/4_roc_and_auc/handson.md"),
        ("solution", "Solution", f"{_base}/4_roc_and_auc/solution_roc_and_auc.py")],
    4: [("lecture", "Lecture", f"{_base}/5_threshold_tuning/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/5_threshold_tuning/handson.md"),
        ("solution", "Solution", f"{_base}/5_threshold_tuning/solution_threshold_tuning.py")],
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
    return render_template("s1_05/index.html",
                           steps=STEPS, lesson_id=LESSON_ID,
                           lesson_title=LESSON_TITLE,
                           url_prefix=f"/lesson/{LESSON_ID}")


@bp.route("/step/<int:n>")
def step(n):
    if n < 0 or n >= len(STEPS):
        return "Step not found", 404
    return render_template(f"s1_05/step_{n:02d}.html", **base_ctx(n))
