"""
Lesson 2.1 — Feature Engineering
Flask Blueprint for the interactive firewall-log feature engineering explorer.
"""

import numpy as np
import pandas as pd
from flask import Blueprint, render_template, jsonify, request
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

bp = Blueprint(
    "s2_01",
    __name__,
    template_folder="templates",
)

LESSON_ID = "s2_01"
LESSON_TITLE = "Feature Engineering"

# ── Generate synthetic firewall log at import time ─────────────────────────

np.random.seed(42)
N = 200

raw_df = pd.DataFrame({
    'timestamp':    pd.date_range('2024-01-15 08:00', periods=N, freq='2min'),
    'src_ip':       [f"192.168.{np.random.randint(0,10)}.{np.random.randint(1,255)}"
                     for _ in range(N)],
    'dst_ip':       [f"{np.random.randint(1,223)}.{np.random.randint(0,255)}."
                     f"{np.random.randint(0,255)}.{np.random.randint(1,255)}"
                     for _ in range(N)],
    'src_port':     np.random.randint(49152, 65535, N),
    'dst_port':     np.random.choice([80, 443, 22, 53, 3389, 21, 8080], N,
                                     p=[0.30, 0.30, 0.10, 0.10, 0.05, 0.05, 0.10]),
    'protocol':     np.random.choice(['TCP', 'UDP', 'ICMP'], N, p=[0.7, 0.25, 0.05]),
    'bytes_sent':   np.random.lognormal(7, 1.2, N).astype(int).clip(100, 100000),
    'bytes_recv':   np.random.lognormal(8, 1.5, N).astype(int).clip(100, 500000),
    'packets':      np.random.poisson(40, N).clip(1, 200),
    'duration_str': [f"{d:.2f}s" for d in np.random.exponential(15, N).clip(0.05, 300)],
    'action':       np.random.choice(['ALLOW', 'BLOCK'], N, p=[0.85, 0.15]),
})

# ── Derive all features ───────────────────────────────────────────────────

raw_df['duration'] = raw_df['duration_str'].str.rstrip('s').astype(float)
raw_df['bytes_per_second'] = np.where(
    raw_df['duration'] > 0, raw_df['bytes_sent'] / raw_df['duration'], 0
)
raw_df['packet_rate'] = np.where(
    raw_df['duration'] > 0, raw_df['packets'] / raw_df['duration'], 0
)
raw_df['bytes_ratio'] = raw_df['bytes_sent'] / (raw_df['bytes_recv'] + 1)
raw_df['hour_of_day'] = raw_df['timestamp'].dt.hour
raw_df['is_business_hours'] = (
    (raw_df['hour_of_day'] >= 9) & (raw_df['hour_of_day'] <= 17)
).astype(int)

PORT_RISK_MAP = {80: 1, 443: 1, 53: 2, 22: 3, 21: 4, 3389: 5, 8080: 1}
raw_df['port_risk_score'] = raw_df['dst_port'].apply(
    lambda p: PORT_RISK_MAP.get(p, 3 if p < 1024 else 1)
)

# Label: high bytes + short duration = suspicious
raw_df['label'] = (
    (raw_df['bytes_sent'] > raw_df['bytes_sent'].quantile(0.85)) &
    (raw_df['duration'] < raw_df['duration'].quantile(0.30))
).astype(int)

# ── Pre-compute encodings ─────────────────────────────────────────────────

le = LabelEncoder()
raw_df['protocol_label'] = le.fit_transform(raw_df['protocol'])
label_mapping = {cls: int(idx) for idx, cls in enumerate(le.classes_)}

ohe = OneHotEncoder(sparse_output=False, drop='first')
ohe_matrix = ohe.fit_transform(raw_df[['protocol']])
ohe_names = list(ohe.get_feature_names_out(['protocol']))
ohe_dropped = str(ohe.categories_[0][0])

proto_dummies = pd.get_dummies(raw_df['protocol'], prefix='proto', drop_first=True)

# ── Pre-compute scaling comparison ────────────────────────────────────────

bps_values = raw_df['bytes_per_second'].values.reshape(-1, 1)
ss = StandardScaler()
bps_standard = ss.fit_transform(bps_values).flatten()
mm = MinMaxScaler()
bps_minmax = mm.fit_transform(bps_values).flatten()

# Histogram bins for scaling comparison
def histogram_data(values, n_bins=20):
    counts, edges = np.histogram(values, bins=n_bins)
    return {
        "counts": counts.tolist(),
        "edges": [round(float(e), 3) for e in edges],
    }

scaling_comparison = {
    "original": histogram_data(raw_df['bytes_per_second'].values),
    "standard": histogram_data(bps_standard),
    "minmax": histogram_data(bps_minmax),
    "stats": {
        "original": {
            "mean": round(float(raw_df['bytes_per_second'].mean()), 1),
            "std": round(float(raw_df['bytes_per_second'].std()), 1),
            "min": round(float(raw_df['bytes_per_second'].min()), 1),
            "max": round(float(raw_df['bytes_per_second'].max()), 1),
        },
        "standard": {
            "mean": round(float(bps_standard.mean()), 3),
            "std": round(float(bps_standard.std()), 3),
            "min": round(float(bps_standard.min()), 2),
            "max": round(float(bps_standard.max()), 2),
        },
        "minmax": {
            "mean": round(float(bps_minmax.mean()), 3),
            "std": round(float(bps_minmax.std()), 3),
            "min": round(float(bps_minmax.min()), 2),
            "max": round(float(bps_minmax.max()), 2),
        },
    }
}

# ── Pre-compute feature impact (train with different feature subsets) ─────

ALL_FEATURES = [
    'bytes_sent', 'bytes_recv', 'packets', 'duration',
    'bytes_per_second', 'packet_rate', 'bytes_ratio',
    'port_risk_score', 'hour_of_day', 'is_business_hours',
]

feature_impact_cache = {}


def train_with_features(feature_list):
    key = tuple(sorted(feature_list))
    if key in feature_impact_cache:
        return feature_impact_cache[key]

    X_base = raw_df[list(feature_list)].copy()
    X = pd.concat([X_base, proto_dummies], axis=1)
    y = raw_df['label']

    if y.sum() < 2:
        return {"acc": 0, "prec": 0, "rec": 0, "f1": 0}

    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_tr_s = scaler.fit_transform(X_tr)
    X_te_s = scaler.transform(X_te)

    model = LogisticRegression(max_iter=500, random_state=42)
    model.fit(X_tr_s, y_tr)
    y_pred = model.predict(X_te_s)

    result = {
        "acc": round(float(accuracy_score(y_te, y_pred)), 3),
        "prec": round(float(precision_score(y_te, y_pred, zero_division=0)), 3),
        "rec": round(float(recall_score(y_te, y_pred, zero_division=0)), 3),
        "f1": round(float(f1_score(y_te, y_pred, zero_division=0)), 3),
    }
    feature_impact_cache[key] = result
    return result


# Pre-warm: train with all features and with subsets
for combo in [
    ALL_FEATURES,
    ['bytes_sent', 'bytes_recv', 'packets', 'duration'],
    ['bytes_sent', 'bytes_recv', 'packets', 'duration', 'bytes_per_second'],
    ['bytes_sent', 'bytes_recv', 'packets', 'duration', 'bytes_per_second', 'port_risk_score'],
    ['bytes_per_second', 'packet_rate', 'bytes_ratio', 'port_risk_score'],
]:
    train_with_features(combo)

# ── Column metadata for templates ─────────────────────────────────────────

COLUMN_META = [
    {"name": "timestamp",    "dtype": "string",  "example": "2024-01-15 08:00:00", "usable": False,
     "transform": "Extract: hour_of_day, is_business_hours"},
    {"name": "src_ip",       "dtype": "string",  "example": "192.168.3.42",        "usable": False,
     "transform": "Extract: is_private, subnet"},
    {"name": "dst_ip",       "dtype": "string",  "example": "185.23.44.102",       "usable": False,
     "transform": "Extract: is_private, known-bad lookup"},
    {"name": "src_port",     "dtype": "int",     "example": "52481",               "usable": True,
     "transform": "Use directly (or drop — ephemeral)"},
    {"name": "dst_port",     "dtype": "int",     "example": "443",                 "usable": True,
     "transform": "Map to port_risk_score"},
    {"name": "protocol",     "dtype": "string",  "example": "TCP",                 "usable": False,
     "transform": "One-hot encode (TCP/UDP/ICMP)"},
    {"name": "bytes_sent",   "dtype": "int",     "example": "3421",                "usable": True,
     "transform": "Use directly"},
    {"name": "bytes_recv",   "dtype": "int",     "example": "15230",               "usable": True,
     "transform": "Use directly"},
    {"name": "packets",      "dtype": "int",     "example": "42",                  "usable": True,
     "transform": "Use directly"},
    {"name": "duration_str", "dtype": "string",  "example": "2.34s",               "usable": False,
     "transform": "Strip 's' suffix → float"},
    {"name": "action",       "dtype": "string",  "example": "ALLOW",               "usable": False,
     "transform": "Drop — this is the label"},
]

# ── Step metadata ─────────────────────────────────────────────────────────

STEPS = [
    {"id": 0, "title": "The Raw Log",           "sub": "What a firewall export looks like"},
    {"id": 1, "title": "Transformation Plan",    "sub": "Which columns need work?"},
    {"id": 2, "title": "Parse Hidden Numbers",   "sub": "Strings that are actually numbers"},
    {"id": 3, "title": "Security Knowledge",     "sub": "Port risk scores from domain expertise"},
    {"id": 4, "title": "Encode Categories",      "sub": "Label vs OneHot encoding"},
    {"id": 5, "title": "The Scaling Problem",    "sub": "StandardScaler vs MinMaxScaler"},
    {"id": 6, "title": "Feature Impact",         "sub": "Which features help the model?"},
    {"id": 7, "title": "The Full Pipeline",      "sub": "Raw log → ML-ready features"},
]

CHALLENGES = {
    0: {
        "q": "Look at the 'duration_str' column. What would happen if you passed '2.34s' to a multiplication operation?",
        "a": "You'd get a <strong>TypeError</strong> — Python can't multiply a string by a number. The 's' suffix makes it a string, not a float. This is why <strong>parsing</strong> is the first step: strip the suffix, convert to float, then you can compute bytes_per_second.",
    },
    1: {
        "q": "Which column should you NEVER use as a feature? Why?",
        "a": "The <strong>action</strong> column (ALLOW/BLOCK). That's the label — what you're trying to predict. Using it as a feature is called <strong>data leakage</strong>: the model gets the answer as input. In production, you wouldn't know the action before the model decides.",
    },
    2: {
        "q": "A connection sends 50,000 bytes in 0.5 seconds. Another sends 50,000 bytes in 50 seconds. Same bytes_sent — but which is suspicious?",
        "a": "The first one: 100,000 bytes/sec is a rapid data transfer, possibly <strong>exfiltration</strong>. The second is 1,000 bytes/sec — normal browsing. Raw bytes_sent can't distinguish them, but <strong>bytes_per_second</strong> immediately flags the anomaly.",
    },
    3: {
        "q": "Why is port 3389 (RDP) scored as risk 5, while port 443 (HTTPS) is risk 1?",
        "a": "RDP provides <strong>full remote desktop access</strong> — attackers who reach it can control the machine. HTTPS is standard encrypted web traffic. The risk score embeds <strong>domain expertise</strong> that the model doesn't need to learn from data.",
    },
    4: {
        "q": "If you label-encode protocols as ICMP=0, TCP=1, UDP=2 — what false relationship does a linear model learn?",
        "a": "It learns that TCP is 'between' ICMP and UDP, and that UDP is 'twice as much as' TCP. A linear model multiplies the feature by a weight — so <code>weight × 2</code> (UDP) is always double <code>weight × 1</code> (TCP). This is <strong>meaningless</strong> for nominal categories.",
    },
    5: {
        "q": "You have one connection that transferred 100,000 bytes/sec while all others are under 5,000. What happens with MinMaxScaler?",
        "a": "MinMaxScaler maps min→0 and max→1. That one outlier becomes 1.0, and all normal traffic gets compressed into 0.00–0.05. The model can barely distinguish normal connections. <strong>StandardScaler</strong> handles this better — the outlier gets a high z-score, but normal data stays spread around 0.",
    },
    6: {
        "q": "Remove all engineered features and train with just raw columns. Then add bytes_per_second. What happens?",
        "a": "Raw columns alone give decent accuracy (they're already numeric), but adding <strong>bytes_per_second</strong> often boosts recall significantly. It captures transfer speed — a <strong>derived signal</strong> that neither bytes_sent nor duration alone express.",
    },
    7: {
        "q": "A SOC analyst says 'just dump the logs into the model.' What would you tell them?",
        "a": "Models can't read IP addresses, protocol names, or timestamps. You need to <strong>engineer features</strong> that encode security knowledge: bytes_per_second for exfil speed, port_risk for attack surface, is_business_hours for anomaly timing. The transformation is where the real intelligence lives.",
    },
}


# ── Course materials mapping ────────────────────────────────────────────────

_base = "stage2_intermediate/01_feature_engineering"

MATERIALS = {
    0: [("lecture", "Why Raw Logs Fail", f"{_base}/1_why_raw_logs_fail/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/1_why_raw_logs_fail/handson.md"),
        ("solution", "Solution", f"{_base}/1_why_raw_logs_fail/solution_why_raw_logs_fail.py")],
    1: [("lecture", "Why Raw Logs Fail", f"{_base}/1_why_raw_logs_fail/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/1_why_raw_logs_fail/handson.md"),
        ("solution", "Solution", f"{_base}/1_why_raw_logs_fail/solution_why_raw_logs_fail.py")],
    2: [("lecture", "Numeric Feature Extraction", f"{_base}/2_numeric_feature_extraction/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/2_numeric_feature_extraction/handson.md"),
        ("solution", "Solution", f"{_base}/2_numeric_feature_extraction/solution_numeric_feature_extraction.py")],
    3: [("lecture", "Numeric Feature Extraction", f"{_base}/2_numeric_feature_extraction/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/2_numeric_feature_extraction/handson.md"),
        ("solution", "Solution", f"{_base}/2_numeric_feature_extraction/solution_numeric_feature_extraction.py")],
    4: [("lecture", "Categorical Encoding", f"{_base}/3_categorical_encoding/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/3_categorical_encoding/handson.md"),
        ("solution", "Solution", f"{_base}/3_categorical_encoding/solution_categorical_encoding.py")],
    5: [("lecture", "Scaling & Validation", f"{_base}/4_scaling_and_validation/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/4_scaling_and_validation/handson.md"),
        ("solution", "Solution", f"{_base}/4_scaling_and_validation/solution_scaling_and_validation.py")],
    6: [("lecture", "Scaling & Validation", f"{_base}/4_scaling_and_validation/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/4_scaling_and_validation/handson.md"),
        ("solution", "Solution", f"{_base}/4_scaling_and_validation/solution_scaling_and_validation.py")],
    7: [("lecture", "Feature Engineering Overview", f"{_base}/README.md")],
}


# ── Helper to build template context ──────────────────────────────────────

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
    return render_template("s2_01/index.html",
                           steps=STEPS, lesson_id=LESSON_ID,
                           lesson_title=LESSON_TITLE,
                           url_prefix=f"/lesson/{LESSON_ID}")


@bp.route("/step/<int:n>")
def step(n):
    if n < 0 or n >= len(STEPS):
        return "Step not found", 404

    ctx = base_ctx(n)

    if n == 0:
        # Raw log preview (first 10 rows)
        preview_cols = ['timestamp', 'src_ip', 'dst_ip', 'src_port', 'dst_port',
                        'protocol', 'bytes_sent', 'bytes_recv', 'packets',
                        'duration_str', 'action']
        rows = []
        for _, r in raw_df[preview_cols].head(10).iterrows():
            rows.append({c: str(r[c]) for c in preview_cols})
        ctx["log_rows"] = rows
        ctx["columns"] = preview_cols
        ctx["column_meta"] = COLUMN_META

    elif n == 1:
        ctx["column_meta"] = COLUMN_META
        numeric_count = sum(1 for c in COLUMN_META if c["usable"])
        string_count = sum(1 for c in COLUMN_META if not c["usable"])
        ctx["numeric_count"] = numeric_count
        ctx["string_count"] = string_count

    elif n == 2:
        # Show duration parsing and bytes_per_second derivation
        samples = []
        for _, r in raw_df.head(20).iterrows():
            samples.append({
                "duration_str": r["duration_str"],
                "duration": round(float(r["duration"]), 2),
                "bytes_sent": int(r["bytes_sent"]),
                "bytes_per_second": round(float(r["bytes_per_second"]), 1),
                "packets": int(r["packets"]),
                "packet_rate": round(float(r["packet_rate"]), 2),
                "bytes_recv": int(r["bytes_recv"]),
                "bytes_ratio": round(float(r["bytes_ratio"]), 3),
            })
        ctx["samples"] = samples
        # Top 5 by bytes_per_second (suspicious)
        top_bps = raw_df.nlargest(5, 'bytes_per_second')
        ctx["top_bps"] = [
            {"idx": int(i), "bps": round(float(r["bytes_per_second"]), 1),
             "bytes_sent": int(r["bytes_sent"]), "duration": round(float(r["duration"]), 2)}
            for i, r in top_bps.iterrows()
        ]

    elif n == 3:
        # Port risk scores
        port_dist = raw_df['dst_port'].value_counts().sort_index()
        ctx["port_risk_map"] = PORT_RISK_MAP
        ctx["port_dist"] = {int(k): int(v) for k, v in port_dist.items()}
        risk_dist = raw_df['port_risk_score'].value_counts().sort_index()
        ctx["risk_dist"] = {int(k): int(v) for k, v in risk_dist.items()}
        risk_labels = {1: 'Standard (HTTP/HTTPS)', 2: 'Watch (DNS)',
                       3: 'Targeted (SSH)', 4: 'Dangerous (FTP)', 5: 'Critical (RDP)'}
        ctx["risk_labels"] = risk_labels

    elif n == 4:
        # Encoding comparison
        ctx["label_mapping"] = label_mapping
        ctx["ohe_names"] = ohe_names
        ctx["ohe_dropped"] = ohe_dropped
        # First 8 rows for display
        enc_rows = []
        for i in range(8):
            enc_rows.append({
                "protocol": raw_df.iloc[i]["protocol"],
                "label_val": int(raw_df.iloc[i]["protocol_label"]),
                "ohe_vals": [int(v) for v in ohe_matrix[i]],
            })
        ctx["enc_rows"] = enc_rows

    elif n == 5:
        ctx["scaling"] = scaling_comparison

    elif n == 6:
        ctx["all_features"] = ALL_FEATURES
        # Pre-compute some combos for instant display
        combos = {
            "raw_only": train_with_features(['bytes_sent', 'bytes_recv', 'packets', 'duration']),
            "plus_bps": train_with_features(['bytes_sent', 'bytes_recv', 'packets', 'duration', 'bytes_per_second']),
            "plus_risk": train_with_features(['bytes_sent', 'bytes_recv', 'packets', 'duration', 'bytes_per_second', 'port_risk_score']),
            "derived_only": train_with_features(['bytes_per_second', 'packet_rate', 'bytes_ratio', 'port_risk_score']),
            "all": train_with_features(ALL_FEATURES),
        }
        ctx["precomputed"] = combos

    elif n == 7:
        ctx["n_raw_cols"] = len(COLUMN_META)
        ctx["n_string_cols"] = sum(1 for c in COLUMN_META if not c["usable"])
        ctx["n_final_features"] = len(ALL_FEATURES) + len(ohe_names)
        ctx["final_metrics"] = train_with_features(ALL_FEATURES)
        ctx["raw_metrics"] = train_with_features(['bytes_sent', 'bytes_recv', 'packets', 'duration'])

    return render_template(f"s2_01/step_{n:02d}.html", **ctx)


# ── API endpoints ─────────────────────────────────────────────────────────

@bp.route("/api/train", methods=["POST"])
def api_train():
    """Train a model with the specified features and return metrics."""
    data = request.get_json(force=True)
    features = data.get("features", [])
    # Validate
    valid = [f for f in features if f in ALL_FEATURES]
    if not valid:
        return jsonify({"error": "No valid features selected"}), 400
    result = train_with_features(valid)
    result["features_used"] = valid
    result["n_features"] = len(valid) + len(ohe_names)  # +OHE columns
    return jsonify(result)


@bp.route("/api/scale-with-outlier")
def api_scale_with_outlier():
    """Scale bytes_per_second with an injected outlier of given magnitude."""
    mult = float(request.args.get("mult", 1))
    values = raw_df['bytes_per_second'].values.copy()
    # Inject outlier: replace the max with max * mult
    if mult > 1:
        values[np.argmax(values)] = values.max() * mult

    vals = values.reshape(-1, 1)
    ss_local = StandardScaler()
    mm_local = MinMaxScaler()
    standard = ss_local.fit_transform(vals).flatten()
    minmax = mm_local.fit_transform(vals).flatten()

    return jsonify({
        "standard": histogram_data(standard),
        "minmax": histogram_data(minmax),
        "stats": {
            "standard": {
                "mean": round(float(standard.mean()), 3),
                "median": round(float(np.median(standard)), 3),
                "min": round(float(standard.min()), 2),
                "max": round(float(standard.max()), 2),
            },
            "minmax": {
                "mean": round(float(minmax.mean()), 3),
                "median": round(float(np.median(minmax)), 3),
                "min": round(float(minmax.min()), 2),
                "max": round(float(minmax.max()), 2),
            },
        }
    })
