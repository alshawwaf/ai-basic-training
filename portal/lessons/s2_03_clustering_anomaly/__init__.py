"""
Lesson 2.3 — Clustering & Anomaly Detection
Flask Blueprint for the network anomaly detection with K-Means workshop.
"""

from flask import Blueprint, render_template

bp = Blueprint(
    "s2_03",
    __name__,
    template_folder="templates",
)

LESSON_ID = "s2_03"
LESSON_TITLE = "k-Means Clustering"

# ── Step metadata ───────────────────────────────────────────────────────────

STEPS = [
    {"id": 0, "title": "Unsupervised Framing",
     "sub": "Why labels are unavailable and what clustering finds",
     "icon": "unlabeled-cloud"},
    {"id": 1, "title": "K-Means and Visualisation",
     "sub": "Cluster assignment, PCA to 2D, colour-coded plots",
     "icon": "kmeans-cluster"},
    {"id": 2, "title": "Choosing K",
     "sub": "Elbow method, silhouette score, picking the right K",
     "icon": "elbow-curve"},
    {"id": 3, "title": "Anomaly Scoring",
     "sub": "Distance from centroid as an anomaly score",
     "icon": "anomaly-outlier"},
]

# ── Quiz ────────────────────────────────────────────────────────────────────

QUIZ = [
    {
        "q": "Your team has 2 million network connection logs but <strong>zero labelled attacks</strong>. Can you still build a detection system?",
        "options": [
            "No &mdash; you must collect labels first",
            "Yes &mdash; cluster the connections, learn what normal looks like, and flag anything that falls far from every cluster centre",
            "Yes &mdash; just use a supervised model with no labels",
            "No &mdash; ML requires labelled data by definition",
        ],
        "answer": 1,
        "explanation": "This is exactly what <strong>unsupervised anomaly detection</strong> is for. K-Means learns the shape of normal traffic from the data alone &mdash; new connections far from every centroid get flagged. You never needed labels. This is how baseline behavioural detection works in production SOCs.",
    },
    {
        "q": "What is the fundamental task of K-Means clustering?",
        "options": [
            "Predict labels for unseen data",
            "Group samples into <em>K</em> clusters by similarity, with each sample assigned to its nearest centroid",
            "Reduce feature dimensions",
            "Train a deep neural network",
        ],
        "answer": 1,
        "explanation": "K-Means iteratively (1) assigns each point to its nearest centroid, then (2) recomputes each centroid as the mean of its assigned points. The result: <em>K</em> groups of similar samples. No labels needed.",
    },
    {
        "q": "The elbow method suggests <strong>K=3</strong> but the silhouette score peaks at <strong>K=4</strong>. Which should you trust more?",
        "options": [
            "Always pick K=3 &mdash; the elbow rule is sacred",
            "Pick K=4 &mdash; silhouette directly measures cluster quality (separation + cohesion); the elbow only measures decreasing inertia",
            "Pick K=10 to be safe",
            "It doesn't matter",
        ],
        "answer": 1,
        "explanation": "<strong>Silhouette score</strong> measures how well-separated and cohesive each cluster is &mdash; it's a much more direct quality measure than inertia. The elbow plot always slopes downward as K grows, so the 'elbow' is sometimes ambiguous. Trust silhouette when they disagree.",
    },
    {
        "q": "How does an anomaly score work in K-Means-based detection?",
        "options": [
            "It uses the cluster ID directly",
            "It uses the distance from the sample to its nearest centroid &mdash; large distance means the sample doesn't fit any normal pattern",
            "It uses the number of clusters",
            "It compares against a fixed threshold of 0.5",
        ],
        "answer": 1,
        "explanation": "Normal traffic clusters tightly around centroids. An anomalous connection lands <strong>far</strong> from every centroid &mdash; that distance is its anomaly score. Set a percentile threshold (e.g. 95th percentile of distances) and alert on anything above it.",
    },
    {
        "q": "You set your anomaly threshold at the 95th percentile and a week later <strong>20%</strong> of connections are being flagged. What likely happened?",
        "options": [
            "The model is broken",
            "Concept drift &mdash; the network's normal behaviour has changed (new app deployed, traffic shifted, seasonal change), so the baseline is stale",
            "Attackers found a 0-day",
            "scikit-learn has a bug",
        ],
        "answer": 1,
        "explanation": "Your K-Means baseline was trained on <em>last month's</em> normal. Networks evolve &mdash; new services, new patterns, new applications. This is <strong>concept drift</strong>. The fix: <em>retrain</em> the baseline on a recent window of data so the centroids reflect current normal.",
    },
]


CHALLENGES = {
    0: {
        "q": "Your network has 2 million connection logs from the past month but zero labelled attacks. Can you still build a detection system? How?",
        "a": "Yes -- use <strong>unsupervised learning</strong>. Cluster the 2 million connections by behaviour (bytes, duration, port, rate). Normal traffic forms dense, predictable clusters. Any new connection that falls <strong>far from all cluster centres</strong> is flagged as anomalous. You never needed a single label. This is exactly how baseline anomaly detection works in production SOCs -- learn what 'normal' looks like, then alert on deviations.",
    },
    1: {
        "q": "After running K-Means with K=4, you project to 2D with PCA and see that two clusters overlap heavily. What does this mean?",
        "a": "It could mean two things. First, the clusters may genuinely overlap in the <strong>two principal components</strong> but be well-separated in the full 6D space -- PCA only shows a projection, not the full picture. Second, K may be <strong>too large</strong> and those two clusters should actually be one. Check the silhouette score for those clusters -- if samples in the overlapping region have low or negative silhouette scores, the split is not justified.",
    },
    2: {
        "q": "The elbow method suggests K=3 but the silhouette score peaks at K=4. Which do you choose and why?",
        "a": "In security, prefer <strong>K=4</strong>. The silhouette score directly measures cluster quality (how well-separated and cohesive each cluster is). The elbow method only measures total inertia, which always decreases with more K. A higher silhouette at K=4 means there is a <strong>genuine fourth behavioural group</strong> in the traffic. In a SOC context, that fourth cluster might separate DNS traffic from ICMP, giving you finer-grained baseline profiles for anomaly detection.",
    },
    3: {
        "q": "You set your anomaly threshold at the 95th percentile of centroid distances. A week later, 20% of connections are flagged. What happened?",
        "a": "The network behaviour has <strong>drifted</strong>. The baseline clusters were learned on old traffic patterns, but the network has changed -- perhaps a new application was deployed, a server moved, or traffic patterns shifted seasonally. This is <strong>concept drift</strong>. The fix: periodically <strong>retrain the K-Means model</strong> on recent baseline data so the centroids reflect current normal behaviour, not last month's normal.",
    },
}

# ── Course materials mapping ────────────────────────────────────────────────

_base = "curriculum/stage2_intermediate/03_clustering_anomaly"

MATERIALS = {
    0: [("lecture", "Lecture", f"{_base}/1_unsupervised_framing/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/1_unsupervised_framing/handson.md"),
        ("solution", "Solution", f"{_base}/1_unsupervised_framing/solution_unsupervised_framing.py")],
    1: [("lecture", "Lecture", f"{_base}/2_kmeans_and_visualisation/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/2_kmeans_and_visualisation/handson.md"),
        ("solution", "Solution", f"{_base}/2_kmeans_and_visualisation/solution_kmeans_and_visualisation.py")],
    2: [("lecture", "Lecture", f"{_base}/3_choosing_k/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/3_choosing_k/handson.md"),
        ("solution", "Solution", f"{_base}/3_choosing_k/solution_choosing_k.py")],
    3: [("lecture", "Lecture", f"{_base}/4_anomaly_scoring/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/4_anomaly_scoring/handson.md"),
        ("solution", "Solution", f"{_base}/4_anomaly_scoring/solution_anomaly_scoring.py")],
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
    return render_template("s2_03/index.html",
                           steps=STEPS, lesson_id=LESSON_ID,
                           lesson_title=LESSON_TITLE,
                           url_prefix=f"/lesson/{LESSON_ID}")


@bp.route("/step/<int:n>")
def step(n):
    if n < 0 or n >= len(STEPS):
        return "Step not found", 404
    return render_template(f"s2_03/step_{n:02d}.html", **base_ctx(n))


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
