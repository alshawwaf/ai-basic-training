"""
Lesson 3.3 — Convolutional Neural Networks
Flask Blueprint for the CNN workshop — from Dense failures to malware visualisation.
"""

from flask import Blueprint, render_template

bp = Blueprint(
    "s3_03",
    __name__,
    template_folder="templates",
)

LESSON_ID = "s3_03"
LESSON_TITLE = "Convolutional Networks"

STEPS = [
    {"id": 0, "title": "Why Dense Fails on Images",       "sub": "Flattening destroys spatial structure",  "icon": "flatten-fail"},
    {"id": 1, "title": "Conv2D & MaxPooling",             "sub": "Sliding filters and downsampling",       "icon": "conv-filter"},
    {"id": 2, "title": "Build & Train a CNN",             "sub": "Full CNN on MNIST digit classification", "icon": "cnn-stack"},
    {"id": 3, "title": "Malware Visualisation Context",   "sub": "Binary-to-image for malware families",   "icon": "binary-image"},
]

# ── Quiz ────────────────────────────────────────────────────────────────────

QUIZ = [
    {
        "q": "Why does a Dense (fully-connected) network struggle with images compared to a CNN?",
        "options": [
            "Dense networks can't handle large datasets",
            "Dense flattens images into a 1D vector and treats every pixel as independent &mdash; it has no concept of spatial structure (which pixels are next to which)",
            "Dense doesn't support GPUs",
            "Dense networks always overfit",
        ],
        "answer": 1,
        "explanation": "Flattening a 28&times;28 image gives 784 numbers with no preserved geometry. The Dense layer treats them as 784 independent features. <strong>CNNs use small filters that look at local pixel neighbourhoods</strong>, learning edges, curves, and textures that depend on adjacency.",
    },
    {
        "q": "If you randomly shuffle every pixel in an MNIST image, Dense accuracy barely changes. What does that prove?",
        "options": [
            "Dense is robust to noise",
            "Dense has zero spatial awareness &mdash; it sees the same statistical distribution regardless of pixel positions; a CNN would collapse to random because its filters depend on adjacency",
            "Pixel shuffling is a security feature",
            "MNIST is too easy",
        ],
        "answer": 1,
        "explanation": "If shuffling pixels doesn't break a model, that model never used spatial structure to begin with. CNNs <em>would</em> collapse on shuffled inputs because their 3&times;3 filters need adjacent pixels to detect edges. This is why CNNs win on images.",
    },
    {
        "q": "A <code>Conv2D(32, (3,3))</code> layer on a 28&times;28&times;1 input has only ~320 parameters, while a Dense(676) layer on the same input has ~530,000. Why so few?",
        "options": [
            "Conv layers are slower so they need fewer params",
            "<strong>Weight sharing</strong> &mdash; each filter (3&times;3 = 9 weights + 1 bias) is reused at every position in the image instead of having unique weights per pixel",
            "Conv layers have a bug",
            "Conv layers can only have 32 parameters",
        ],
        "answer": 1,
        "explanation": "A CNN learns one small filter and slides it across the entire image. This <strong>weight sharing</strong> is why CNNs have far fewer parameters than Dense networks &mdash; and why they generalise so well to images: a 'curve detector' is useful no matter where in the image the curve appears.",
    },
    {
        "q": "A malware analyst asks: <em>'Why not just use file hashes?'</em> What's the fundamental advantage of CNN-based malware visualisation?",
        "options": [
            "Hashes are too slow to compute",
            "Hashes are exact-match only &mdash; change one byte and the hash changes completely; CNNs detect <em>structural similarity</em> between malware family variants",
            "CNNs are easier to compute",
            "Hashes can't be stored",
        ],
        "answer": 1,
        "explanation": "Malware authors evade hash detection by recompiling, packing, or flipping a single byte. A CNN trained on byte-as-image representations learns the <strong>visual signature</strong> of a malware family &mdash; code section layouts, data patterns &mdash; which survives minor mutations.",
    },
    {
        "q": "What does a <strong>MaxPooling</strong> layer do, and why is it useful?",
        "options": [
            "It adds more parameters to the network",
            "It downsamples the feature maps by keeping only the maximum value in each small window &mdash; reducing spatial size, computation, and overfitting while keeping the strongest signals",
            "It encrypts the feature maps",
            "It adds randomness to the model",
        ],
        "answer": 1,
        "explanation": "MaxPooling shrinks the feature maps (e.g. 26&times;26 &rarr; 13&times;13 with 2&times;2 pooling), keeping only the strongest activation per window. This <strong>cuts computation</strong>, gives the network a small amount of <em>translation invariance</em>, and reduces the parameter count of subsequent layers.",
    },
]


CHALLENGES = {
    0: {
        "q": "You shuffle every pixel in an MNIST image randomly. Dense accuracy barely changes. Why does this prove Dense ignores spatial structure?",
        "a": "Dense treats the image as a <strong>flat vector of 784 independent numbers</strong>. Shuffling changes pixel positions but not the statistical distribution of values — Dense still sees the same correlations. A CNN would <strong>collapse to random chance</strong> because its 3x3 filters rely on adjacent pixels forming local patterns (edges, curves). This proves Dense has <strong>zero spatial awareness</strong>.",
    },
    1: {
        "q": "A Conv2D(32, (3,3)) on a 28x28 input creates 32 feature maps of size 26x26. How many parameters does this layer have compared to a Dense(676) layer on the same flattened input?",
        "a": "Conv2D: each filter has 3x3x1 = 9 weights + 1 bias = 10 params, times 32 filters = <strong>320 parameters</strong>. Dense(676) on 784 inputs: 784 x 676 + 676 = <strong>530,260 parameters</strong>. The Conv layer achieves similar expressive power with <strong>1,657x fewer parameters</strong> through weight sharing — the same 3x3 filter is reused at every position.",
    },
    2: {
        "q": "Your CNN hits 99.2% on MNIST but your Dense baseline hits 97.8%. Is the 1.4% gap worth the added complexity? When would it be?",
        "a": "For MNIST digits, probably not — 97.8% is already excellent. But in security, that 1.4% gap could mean <strong>hundreds of missed detections</strong> at scale. If your NIDS processes 1 million events/day, 1.4% fewer false negatives = <strong>14,000 more correctly caught threats</strong>. The gap matters when the cost of misclassification is high.",
    },
    3: {
        "q": "A malware analyst asks: 'Can we just use file hashes instead of this image stuff?' What is the fundamental limitation of hash-based detection that CNN-based visualisation addresses?",
        "a": "Hashes are <strong>exact-match only</strong> — change one byte and the hash is completely different. Malware authors trivially evade hash detection by recompiling or packing. CNN-based visualisation detects <strong>structural similarity</strong>: variants of the same malware family produce visually similar images because they share code sections, data layouts, and execution patterns. The CNN learns these <strong>family-level patterns</strong> that survive minor modifications.",
    },
}

_base = "curriculum/stage3_neural_networks/03_convolutional_networks"

MATERIALS = {
    0: [("lecture", "Why Dense Fails on Images", f"{_base}/1_why_dense_fails_on_images/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/1_why_dense_fails_on_images/handson.md"),
        ("solution", "Solution", f"{_base}/1_why_dense_fails_on_images/solution_why_dense_fails_on_images.py")],
    1: [("lecture", "Conv2D and MaxPooling", f"{_base}/2_conv_and_pooling/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/2_conv_and_pooling/handson.md"),
        ("solution", "Solution", f"{_base}/2_conv_and_pooling/solution_conv_and_pooling.py")],
    2: [("lecture", "Build and Train a CNN", f"{_base}/3_build_and_train_cnn/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/3_build_and_train_cnn/handson.md"),
        ("solution", "Solution", f"{_base}/3_build_and_train_cnn/solution_build_and_train_cnn.py")],
    3: [("lecture", "Malware Visualisation", f"{_base}/4_malware_visualisation_context/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/4_malware_visualisation_context/handson.md"),
        ("solution", "Solution", f"{_base}/4_malware_visualisation_context/solution_malware_visualisation_context.py")],
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
    return render_template("s3_03/index.html",
                           steps=STEPS, lesson_id=LESSON_ID,
                           lesson_title=LESSON_TITLE,
                           url_prefix=f"/lesson/{LESSON_ID}")


@bp.route("/step/<int:n>")
def step(n):
    if n < 0 or n >= len(STEPS):
        return "Step not found", 404
    return render_template(f"s3_03/step_{n:02d}.html", **base_ctx(n))


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
