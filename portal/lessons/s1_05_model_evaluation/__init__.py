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

# ── Quiz ────────────────────────────────────────────────────────────────────

QUIZ = [
    {
        "q": "Your malware detector reports <strong>99.95% accuracy</strong> on a feed where 0.05% of events are malicious. What can you conclude?",
        "options": [
            "The model is excellent",
            "Almost nothing &mdash; a model that always predicts 'benign' would also score 99.95% and catch zero malware",
            "The model has memorised the training data",
            "The dataset is corrupted",
        ],
        "answer": 1,
        "explanation": "When the positive class is 0.05%, accuracy is dominated by the majority class. You must check <strong>recall</strong> &mdash; what fraction of actual malware was flagged? Without that number, the accuracy figure is meaningless.",
    },
    {
        "q": "Your IDS produces: <strong>TP=45, FP=300, FN=5, TN=9650</strong>. What is the precision?",
        "options": [
            "13%",
            "90%",
            "45%",
            "95%",
        ],
        "answer": 0,
        "explanation": "Precision = TP / (TP + FP) = 45 / (45 + 300) = <strong>13%</strong>. Of every 8 alerts, only 1 is real. The recall is 90% (it catches most attacks), but the precision is poor &mdash; analysts will burn most of their time on false alarms.",
    },
    {
        "q": "Two models for the same job: Model A has precision=0.95, recall=0.60. Model B has precision=0.70, recall=0.95. Which one would you deploy for <strong>scanning incoming email for phishing</strong>?",
        "options": [
            "Model A &mdash; high precision is always better",
            "Model B &mdash; missing a phishing email leads to credential theft, so recall matters more here",
            "Neither &mdash; both are unacceptable",
            "It doesn't matter",
        ],
        "answer": 1,
        "explanation": "For email scanning, the cost of a <strong>false negative</strong> (missed phishing &rarr; credential theft &rarr; lateral movement) is much higher than the cost of a <strong>false positive</strong> (a legit email goes to quarantine for review). Pick the model that maximises recall.",
    },
    {
        "q": "Model X has AUC = 0.92. Model Y has AUC = 0.95. Should you always pick Y?",
        "options": [
            "Yes &mdash; AUC is the only number that matters",
            "Not necessarily &mdash; AUC averages across all thresholds, but you only operate at one; check the ROC curve in the region you care about",
            "No &mdash; lower AUC is better",
            "Yes &mdash; AUC=0.95 means 95% accuracy",
        ],
        "answer": 1,
        "explanation": "AUC summarises performance across <em>every</em> threshold. But in production you operate at <strong>one</strong> threshold &mdash; usually in the low-FPR region. Model X might dominate Y in that specific region. Always plot the ROC curve, not just the single AUC number.",
    },
    {
        "q": "Your SOC team can handle 50 alerts/day. At threshold 0.3 the model produces 200 alerts; at 0.6 it produces 30 but misses 60% of attacks. What's the right move?",
        "options": [
            "Pick 0.6 &mdash; it's under capacity",
            "Pick 0.3 and accept the 200 alerts",
            "Find a middle threshold (~0.45) that balances capacity and recall, or add auto-triage to handle volume at 0.3",
            "Ignore the threshold entirely",
        ],
        "answer": 2,
        "explanation": "Threshold tuning is an <strong>operational</strong> decision, not just a math problem. 0.6 hits the capacity number but loses 60% of attacks &mdash; unacceptable. Either find a balanced threshold or invest in <em>auto-triage</em> so analysts only see the alerts that matter most.",
    },
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
        "quiz_count": len(QUIZ),
        "is_quiz": False,
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
