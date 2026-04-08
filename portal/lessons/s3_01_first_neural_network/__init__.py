"""
Lesson 3.1 — Your First Neural Network
Flask Blueprint — interactive neural network explorer using sklearn MLPClassifier.
"""

import numpy as np
from flask import Blueprint, render_template, jsonify, request
from sklearn.neural_network import MLPClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, roc_auc_score, confusion_matrix)

bp = Blueprint(
    "s3_01",
    __name__,
    template_folder="templates",
)

LESSON_ID = "s3_01"
LESSON_TITLE = "First Neural Network"

# ── Generate dataset ──────────────────────────────────────────────────────

np.random.seed(42)

X, y = make_classification(
    n_samples=2000, n_features=10, n_informative=7, n_redundant=2,
    weights=[0.88, 0.12], flip_y=0.03, random_state=42
)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)

ATTACK_RATE = round(float(y.mean() * 100), 1)

# ── Pre-train networks with different architectures ───────────────────────

ARCHITECTURES = {
    "tiny":   (16,),
    "small":  (32, 16),
    "medium": (64, 32),
    "large":  (64, 32, 16),
}

training_results = {}

for name, hidden in ARCHITECTURES.items():
    np.random.seed(42)
    mlp = MLPClassifier(
        hidden_layer_sizes=hidden,
        activation='relu',
        solver='adam',
        max_iter=1,
        warm_start=True,
        random_state=42,
        batch_size=32,
    )

    train_losses = []
    train_accs = []
    val_accs = []
    epochs = 60

    for epoch in range(epochs):
        mlp.fit(X_train_s, y_train)
        train_losses.append(round(float(mlp.loss_), 4))
        train_accs.append(round(float(accuracy_score(y_train, mlp.predict(X_train_s))), 4))
        val_accs.append(round(float(accuracy_score(y_test, mlp.predict(X_test_s))), 4))

    y_pred = mlp.predict(X_test_s)
    y_proba = mlp.predict_proba(X_test_s)[:, 1]
    cm = confusion_matrix(y_test, y_pred).tolist()

    params = sum(
        w.size + b.size for w, b in zip(mlp.coefs_, mlp.intercepts_)
    )

    training_results[name] = {
        "arch": list(hidden),
        "arch_str": " → ".join([str(10)] + [str(h) for h in hidden] + ["1"]),
        "params": params,
        "epochs": epochs,
        "train_losses": train_losses,
        "train_accs": train_accs,
        "val_accs": val_accs,
        "final": {
            "acc": round(float(accuracy_score(y_test, y_pred)), 3),
            "prec": round(float(precision_score(y_test, y_pred, zero_division=0)), 3),
            "rec": round(float(recall_score(y_test, y_pred, zero_division=0)), 3),
            "f1": round(float(f1_score(y_test, y_pred, zero_division=0)), 3),
            "auc": round(float(roc_auc_score(y_test, y_proba)), 3),
        },
        "confusion": cm,
    }

# ── LogisticRegression baseline ───────────────────────────────────────────

lr = LogisticRegression(max_iter=1000, random_state=42)
lr.fit(X_train_s, y_train)
lr_pred = lr.predict(X_test_s)
lr_proba = lr.predict_proba(X_test_s)[:, 1]
lr_cm = confusion_matrix(y_test, lr_pred).tolist()

baseline_results = {
    "acc": round(float(accuracy_score(y_test, lr_pred)), 3),
    "prec": round(float(precision_score(y_test, lr_pred, zero_division=0)), 3),
    "rec": round(float(recall_score(y_test, lr_pred, zero_division=0)), 3),
    "f1": round(float(f1_score(y_test, lr_pred, zero_division=0)), 3),
    "auc": round(float(roc_auc_score(y_test, lr_proba)), 3),
    "confusion": lr_cm,
}

# ── Param count examples ─────────────────────────────────────────────────

PARAM_EXAMPLES = [
    {"name": "Tiny",   "layers": [10, 16, 1],           "params": (10*16+16) + (16*1+1)},
    {"name": "Small",  "layers": [10, 32, 16, 1],       "params": (10*32+32) + (32*16+16) + (16*1+1)},
    {"name": "Medium", "layers": [10, 64, 32, 1],       "params": (10*64+64) + (64*32+32) + (32*1+1)},
    {"name": "Large",  "layers": [10, 128, 64, 32, 1],  "params": (10*128+128) + (128*64+64) + (64*32+32) + (32*1+1)},
    {"name": "Huge",   "layers": [10, 256, 128, 64, 1], "params": (10*256+256) + (256*128+128) + (128*64+64) + (64*1+1)},
]

# ── Step metadata ─────────────────────────────────────────────────────────

STEPS = [
    {"id": 0, "title": "What is a Neuron?",    "sub": "Weighted sum + activation",                "icon": "neuron"},
    {"id": 1, "title": "Activation Functions",  "sub": "ReLU, sigmoid, and softmax",               "icon": "activation-curve"},
    {"id": 2, "title": "Build a Network",       "sub": "Layers, widths, and parameter counts",     "icon": "network-layers"},
    {"id": 3, "title": "The Forward Pass",      "sub": "Data flows through layers",                "icon": "forward-pass"},
    {"id": 4, "title": "The Training Loop",     "sub": "Epochs, batches, and loss curves",         "icon": "training-loop"},
    {"id": 5, "title": "Overfitting",           "sub": "When the model memorises instead of learns", "icon": "overfit-curve"},
    {"id": 6, "title": "Neural Net vs Baseline", "sub": "Is deeper always better?",                "icon": "vs-compare"},
    {"id": 7, "title": "When to Go Deep",       "sub": "The right tool for the job",               "icon": "depth-stack"},
]

CHALLENGES = {
    0: {
        "q": "Set all weights to 0. What does the neuron output for any input? Why is this a problem?",
        "a": "With all weights at 0, the dot product is always 0, so the output is just bias + activation(0). The neuron learns <strong>nothing</strong> from the input. This is called the <strong>dead neuron problem</strong> — why weight initialisation matters.",
    },
    1: {
        "q": "ReLU outputs 0 for all negative inputs. What happens if a neuron's weights cause it to always receive negative values?",
        "a": "It's permanently 'dead' — always outputs 0, gradient is 0, so weights never update. This is the <strong>dying ReLU problem</strong>. Solutions: LeakyReLU (small slope for negatives) or careful initialisation.",
    },
    2: {
        "q": "A network with 10 inputs and layers [256, 128, 64, 1] has 44,000+ parameters but only 2,000 training samples. What happens?",
        "a": "More parameters than samples = <strong>overfitting guaranteed</strong>. The network memorises training data instead of learning patterns. Rule of thumb: keep parameters well below 10x your training samples.",
    },
    3: {
        "q": "Click 'New random weights' several times. Does the same input always produce the same output?",
        "a": "No — different random weights produce different outputs. Before training, the network is <strong>random guessing</strong>. Training adjusts weights so the output matches the correct labels.",
    },
    4: {
        "q": "Watch the loss curve. Does it ever go UP during training? Why?",
        "a": "Yes — individual batches can increase loss (noise from random batch selection). But the <strong>trend</strong> should be downward. If the overall trend goes up, the learning rate is too high.",
    },
    5: {
        "q": "At what epoch does the validation accuracy peak for the medium network? What should you do about it?",
        "a": "Check the chart — val accuracy typically peaks around epoch 20-30 then plateaus or drops. You should <strong>stop training at the peak</strong>. This is called <strong>early stopping</strong> — a key regularisation technique.",
    },
    6: {
        "q": "The neural network and logistic regression have similar AUC. Which would you deploy in a production SOC?",
        "a": "Deploy <strong>LogisticRegression</strong>. Same performance, but simpler: faster inference, easier to explain to analysts, fewer things to break. Only use neural nets when they clearly outperform the baseline.",
    },
    7: {
        "q": "Your team has 500 labelled malware samples and 50,000 benign samples. Should you use a neural network?",
        "a": "Probably not. With severe class imbalance and limited data, <strong>tree-based models</strong> (Random Forest, XGBoost) often work better. Neural networks need more data to generalise. Start simple, go deep only if the data supports it.",
    },
}


# ── Course materials mapping ────────────────────────────────────────────────

_base = "curriculum/stage3_neural_networks/01_first_neural_network"

MATERIALS = {
    0: [("lecture", "From NumPy to Keras", f"{_base}/1_from_numpy_to_keras/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/1_from_numpy_to_keras/handson.md"),
        ("solution", "Solution", f"{_base}/1_from_numpy_to_keras/solution_from_numpy_to_keras.py")],
    1: [("lecture", "From NumPy to Keras", f"{_base}/1_from_numpy_to_keras/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/1_from_numpy_to_keras/handson.md"),
        ("solution", "Solution", f"{_base}/1_from_numpy_to_keras/solution_from_numpy_to_keras.py")],
    2: [("lecture", "Build the Network", f"{_base}/2_build_the_network/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/2_build_the_network/handson.md"),
        ("solution", "Solution", f"{_base}/2_build_the_network/solution_build_the_network.py")],
    3: [("lecture", "Build the Network", f"{_base}/2_build_the_network/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/2_build_the_network/handson.md"),
        ("solution", "Solution", f"{_base}/2_build_the_network/solution_build_the_network.py")],
    4: [("lecture", "Compile & Train", f"{_base}/3_compile_and_train/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/3_compile_and_train/handson.md"),
        ("solution", "Solution", f"{_base}/3_compile_and_train/solution_compile_and_train.py")],
    5: [("lecture", "Compile & Train", f"{_base}/3_compile_and_train/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/3_compile_and_train/handson.md"),
        ("solution", "Solution", f"{_base}/3_compile_and_train/solution_compile_and_train.py")],
    6: [("lecture", "Evaluate & Improve", f"{_base}/4_evaluate_and_improve/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/4_evaluate_and_improve/handson.md"),
        ("solution", "Solution", f"{_base}/4_evaluate_and_improve/solution_evaluate_and_improve.py")],
    7: [("lecture", "Neural Networks Overview", f"{_base}/README.md")],
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


# ── Routes ────────────────────────────────────────────────────────────────

@bp.route("/")
def index():
    return render_template("s3_01/index.html",
                           steps=STEPS, lesson_id=LESSON_ID,
                           lesson_title=LESSON_TITLE,
                           url_prefix=f"/lesson/{LESSON_ID}")


@bp.route("/step/<int:n>")
def step(n):
    if n < 0 or n >= len(STEPS):
        return "Step not found", 404

    ctx = base_ctx(n)

    if n == 2:
        ctx["param_examples"] = PARAM_EXAMPLES

    elif n == 4:
        ctx["training"] = training_results["medium"]

    elif n == 5:
        ctx["architectures"] = {
            k: {
                "arch_str": v["arch_str"],
                "train_accs": v["train_accs"],
                "val_accs": v["val_accs"],
                "train_losses": v["train_losses"],
            } for k, v in training_results.items()
        }

    elif n == 6:
        ctx["nn_results"] = {k: v["final"] for k, v in training_results.items()}
        ctx["nn_confusion"] = {k: v["confusion"] for k, v in training_results.items()}
        ctx["baseline"] = baseline_results
        ctx["arch_strings"] = {k: v["arch_str"] for k, v in training_results.items()}

    elif n == 7:
        ctx["best_nn"] = training_results["medium"]["final"]
        ctx["baseline"] = baseline_results
        ctx["attack_rate"] = ATTACK_RATE

    return render_template(f"s3_01/step_{n:02d}.html", **ctx)


# ── API ───────────────────────────────────────────────────────────────────

@bp.route("/api/training-data/<arch>")
def api_training_data(arch):
    if arch not in training_results:
        return jsonify({"error": "Unknown architecture"}), 400
    r = training_results[arch]
    return jsonify({
        "arch_str": r["arch_str"],
        "params": r["params"],
        "train_losses": r["train_losses"],
        "train_accs": r["train_accs"],
        "val_accs": r["val_accs"],
        "final": r["final"],
        "confusion": r["confusion"],
    })
