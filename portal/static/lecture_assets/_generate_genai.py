"""
Generate visuals for the 13 GenAI lectures (Stage 4).
    python portal/static/lecture_assets/_generate_genai.py

Uses real data sources where possible:
  - tiktoken (cl100k_base, GPT-4) for actual tokenisation
  - sentence-transformers all-MiniLM-L6-v2 for real sentence embeddings
  - cosine similarity from sklearn

Generates all visuals prefixed gn_*.png across the four sessions:
  4.1 How LLMs Work — tokenisation, embeddings, attention
  4.2 HuggingFace   — zero-shot, sentence embeddings, semantic search
  4.3 LLM API       — first call, system prompts, structured output, conversation
  4.4 RAG           — chunking, retrieval, full pipeline
"""
import os
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")
os.environ.setdefault("TF_ENABLE_ONEDNN_OPTS", "0")
import warnings
warnings.filterwarnings("ignore")

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, FancyArrowPatch

OUT = Path(__file__).resolve().parent

DPI  = 140
SAVE = dict(dpi=DPI, bbox_inches="tight", facecolor="white")
ACCENT = "#0891b2"
VIOLET = "#8b5cf6"
RED    = "#dc2626"
ORANGE = "#f59e0b"
GREEN  = "#16a34a"
GREY   = "#64748b"
LIGHT  = "#e2e8f0"
DARK   = "#0f172a"
GOLD   = "#facc15"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
})


def save(fig, name):
    fig.savefig(OUT / name, **SAVE)
    plt.close(fig)
    print(f"  wrote {name}")


# ============================================================
# 4.1 — How LLMs Work
# ============================================================

# 1. gn_tokenisation_pipeline.png — text → tokens → IDs → embeddings
import tiktoken
enc = tiktoken.get_encoding("cl100k_base")
sentence = "Investigate the ransomware payload immediately"
ids = enc.encode(sentence)
toks = [enc.decode([i]) for i in ids]
print(f"  → real GPT-4 tokeniser: {len(ids)} tokens for {sentence!r}")

fig, ax = plt.subplots(figsize=(12, 4.6))
ax.set_xlim(0, 12); ax.set_ylim(0, 5)
ax.axis('off')

# Stage 1: raw text
ax.text(0.7, 4.4, "1. Raw text", fontsize=11, color=GREY, fontweight='bold')
text_box = FancyBboxPatch((0.5, 3.55), 11, 0.7,
                          boxstyle="round,pad=0.05,rounding_size=0.1",
                          facecolor=LIGHT, edgecolor=GREY, linewidth=1.5)
ax.add_patch(text_box)
ax.text(6, 3.9, f'"{sentence}"', ha='center', va='center', fontsize=12,
        color=DARK, family='monospace')

# Stage 2: tokens (coloured boxes, one per token)
ax.text(0.7, 3.0, "2. Tokens (subword pieces)", fontsize=11, color=ACCENT,
        fontweight='bold')
tok_colours = [ACCENT, ACCENT, VIOLET, ORANGE, GREEN, GREY, RED]
tok_w = 11 / max(len(toks), 1)
for i, t in enumerate(toks):
    x0 = 0.5 + i * tok_w
    box = FancyBboxPatch((x0 + 0.05, 2.15), tok_w - 0.1, 0.7,
                         boxstyle="round,pad=0.02,rounding_size=0.08",
                         facecolor=tok_colours[i % len(tok_colours)],
                         edgecolor='white', linewidth=1.5, alpha=0.85)
    ax.add_patch(box)
    ax.text(x0 + tok_w / 2, 2.5, repr(t).strip("'"), ha='center', va='center',
            fontsize=11, color='white', fontweight='bold', family='monospace')

# Stage 3: IDs
ax.text(0.7, 1.6, "3. Token IDs (integers from a 100k vocabulary)",
        fontsize=11, color=ORANGE, fontweight='bold')
for i, tid in enumerate(ids):
    x0 = 0.5 + i * tok_w
    ax.text(x0 + tok_w / 2, 1.05, f"{tid:,}", ha='center', va='center',
            fontsize=11, color=DARK, family='monospace')

# Stage 4: embedding lookup
ax.text(0.7, 0.55, "4. Embedding lookup → vectors fed to the transformer",
        fontsize=11, color=VIOLET, fontweight='bold')
for i in range(len(ids)):
    x0 = 0.5 + i * tok_w
    ax.text(x0 + tok_w / 2, 0.05, "[ … ]", ha='center', va='center',
            fontsize=10, color=VIOLET, family='monospace')

fig.suptitle(f"Real GPT-4 tokenisation — {len(ids)} tokens for one sentence",
             y=1.02)
save(fig, "gn_tokenisation_pipeline.png")


# 2. gn_subword_split.png — same word split three ways
# Layout:  [strategy name + short caption]   |   [token boxes]
# The left column gets ~5 axis units, the box column starts at px=5.6.
fig, ax = plt.subplots(figsize=(12, 4.6))
ax.set_xlim(0, 12); ax.set_ylim(0, 5)
ax.axis('off')

word = "unhappiness"
strategies = [
    ("Character-level",       list(word),               GREY,
     "vocab ~100; long sequences, no semantic units"),
    ("Word-level",            [word],                   ORANGE,
     "vocab 50K+; fails on unseen words (→ <UNK>)"),
    ("Subword (BPE / GPT-4)", ["un", "happiness"],      ACCENT,
     "vocab ~100K; compact, handles new words"),
]
for si, (name, parts, colour, why) in enumerate(strategies):
    y = 4.2 - si * 1.5
    ax.text(0.3, y + 0.45, name, fontsize=12, color=colour, fontweight='bold')
    ax.text(0.3, y - 0.05, why, fontsize=9, color=GREY, style='italic')
    # part boxes — start well to the right of the caption column
    px = 5.6
    for p in parts:
        w = max(0.6, len(p) * 0.18 + 0.25)
        box = FancyBboxPatch((px, y - 0.05), w, 0.55,
                             boxstyle="round,pad=0.02,rounding_size=0.08",
                             facecolor=colour, edgecolor='white', linewidth=1.5,
                             alpha=0.85)
        ax.add_patch(box)
        ax.text(px + w / 2, y + 0.22, p, ha='center', va='center', fontsize=10,
                color='white', fontweight='bold', family='monospace')
        px += w + 0.08

fig.suptitle('Same word "unhappiness", three tokenisation strategies', y=1.0)
save(fig, "gn_subword_split.png")


# 3. gn_embedding_space.png — REAL sentence embeddings projected to 2D
print("  → loading sentence-transformers model ...")
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

st_model = SentenceTransformer('all-MiniLM-L6-v2')

# Words for embedding visualisation (we'll embed each as its own "sentence")
embed_words = [
    ("malicious", "threat"),
    ("suspicious", "threat"),
    ("attack", "threat"),
    ("breach", "threat"),
    ("exploit", "threat"),
    ("firewall", "network"),
    ("router", "network"),
    ("packet", "network"),
    ("traffic", "network"),
    ("port", "network"),
    ("the", "function"),
    ("a", "function"),
    ("of", "function"),
    ("and", "function"),
    ("apple", "food"),
    ("pizza", "food"),
    ("bread", "food"),
    ("coffee", "food"),
]
words = [w for w, _ in embed_words]
groups = [g for _, g in embed_words]

print(f"  → encoding {len(words)} words for embedding space ...")
W = st_model.encode(words)

# 2D projection via PCA
from sklearn.decomposition import PCA
pca = PCA(n_components=2, random_state=42)
W2 = pca.fit_transform(W)

group_colour = {"threat": RED, "network": ACCENT, "function": GREY, "food": GREEN}
fig, ax = plt.subplots(figsize=(10, 6.5))
for grp in ["threat", "network", "function", "food"]:
    mask = [g == grp for g in groups]
    ax.scatter(W2[mask, 0], W2[mask, 1], s=210, color=group_colour[grp],
               edgecolor='white', linewidth=2, zorder=3, label=grp,
               alpha=0.92)
for (x, y), w in zip(W2, words):
    ax.annotate(w, (x, y), xytext=(8, 5), textcoords='offset points',
                fontsize=10, color=DARK, fontweight='bold')
ax.set_title("Real sentence-transformer embeddings — PCA to 2D\n"
             "semantically related words cluster together")
ax.set_xlabel('PC 1')
ax.set_ylabel('PC 2')
ax.legend(loc='best', framealpha=0.95)
ax.grid(True, alpha=0.3)
save(fig, "gn_embedding_space.png")


# 4. gn_cosine_pairs.png — REAL cosine similarities for security pairs
pair_words_a = ["malicious", "malicious", "firewall", "the",      "phishing"]
pair_words_b = ["suspicious", "benign",   "router",   "malicious", "credential theft"]
print(f"  → computing pairwise cosine for {len(pair_words_a)} pairs ...")
all_words = list(set(pair_words_a + pair_words_b))
emb = st_model.encode(all_words)
sim_lookup = {}
for i, wi in enumerate(all_words):
    for j, wj in enumerate(all_words):
        sim_lookup[(wi, wj)] = float(cosine_similarity([emb[i]], [emb[j]])[0, 0])

scores = [sim_lookup[(a, b)] for a, b in zip(pair_words_a, pair_words_b)]
labels = [f'"{a}"\nvs\n"{b}"' for a, b in zip(pair_words_a, pair_words_b)]

fig, ax = plt.subplots(figsize=(11, 5.2))
colours = [GREEN if s > 0.7 else (ORANGE if s > 0.4 else RED) for s in scores]
bars = ax.bar(range(len(scores)), scores, color=colours, edgecolor='white',
              linewidth=2, width=0.6)
ax.set_xticks(range(len(scores)))
ax.set_xticklabels(labels, fontsize=10)
for bar, s in zip(bars, scores):
    ax.text(bar.get_x() + bar.get_width() / 2, s + 0.01, f'{s:.3f}',
            ha='center', fontsize=11, color=DARK, fontweight='bold')
ax.set_ylabel('cosine similarity')
ax.set_ylim(0, max(scores) * 1.15)
ax.set_title('Real cosine similarities from all-MiniLM-L6-v2 embeddings')
ax.grid(True, alpha=0.3, axis='y')
ax.axhline(0.7, color=GREEN, linestyle='--', alpha=0.5, label='≥ 0.70 strong')
ax.axhline(0.4, color=ORANGE, linestyle='--', alpha=0.5, label='≥ 0.40 weak')
ax.legend(loc='upper right')
fig.tight_layout()
save(fig, "gn_cosine_pairs.png")


# 5. gn_attention_matrix.png — toy attention heatmap with arrows from "blocked"
words_attn = ["the", "firewall", "blocked", "malicious", "connection"]
A = np.array([
    [0.80, 0.10, 0.05, 0.03, 0.02],
    [0.15, 0.65, 0.10, 0.05, 0.05],
    [0.03, 0.45, 0.00, 0.28, 0.24],
    [0.02, 0.08, 0.12, 0.70, 0.08],
    [0.04, 0.12, 0.30, 0.25, 0.29],
])

fig, ax = plt.subplots(figsize=(8.5, 6))
im = ax.imshow(A, cmap='YlGnBu', vmin=0, vmax=1)
ax.set_xticks(range(len(words_attn)))
ax.set_yticks(range(len(words_attn)))
ax.set_xticklabels(words_attn, rotation=30, ha='right')
ax.set_yticklabels(words_attn)
for i in range(len(words_attn)):
    for j in range(len(words_attn)):
        col = 'white' if A[i, j] > 0.4 else DARK
        ax.text(j, i, f'{A[i, j]:.2f}', ha='center', va='center',
                fontsize=11, color=col,
                fontweight='bold' if A[i, j] > 0.4 else 'normal')
# highlight the "blocked" row
ax.add_patch(Rectangle((-0.5, 1.5), 5, 1, fill=False, edgecolor=GOLD,
                       linewidth=3.5))
ax.set_title('Attention matrix — gold row is "blocked"\n'
             'each cell = how much row word attends to column word')
ax.set_xlabel('attended TO →')
ax.set_ylabel('attended FROM ↓')
fig.colorbar(im, ax=ax, label='attention weight')
fig.tight_layout()
save(fig, "gn_attention_matrix.png")


# 6. gn_attention_arrows.png — sentence with arrows from "blocked" to context
fig, ax = plt.subplots(figsize=(11, 4.6))
ax.set_xlim(0, 11); ax.set_ylim(0, 5)
ax.axis('off')

# top row of word boxes
positions = []
xpos = 0.7
for i, w in enumerate(words_attn):
    boxw = 1.6
    is_blocked = (w == "blocked")
    facecol = ORANGE if is_blocked else LIGHT
    edgecol = ORANGE if is_blocked else GREY
    box = FancyBboxPatch((xpos, 3.2), boxw, 0.8,
                         boxstyle="round,pad=0.05,rounding_size=0.1",
                         facecolor=facecol, edgecolor=edgecol, linewidth=2)
    ax.add_patch(box)
    ax.text(xpos + boxw / 2, 3.6, w, ha='center', va='center', fontsize=12,
            color='white' if is_blocked else DARK,
            fontweight='bold' if is_blocked else 'normal')
    positions.append((xpos + boxw / 2, 3.2))
    xpos += boxw + 0.4

# attention weights from "blocked" (index 2)
blocked_idx = 2
weights = A[blocked_idx]
bx, by = positions[blocked_idx]
arrow_y = 1.2

for i, (px, py) in enumerate(positions):
    if i == blocked_idx:
        continue
    w = weights[i]
    if w < 0.05:
        continue
    arrow = FancyArrowPatch((bx, by - 0.05), (px, arrow_y + 0.4),
                            arrowstyle='->', mutation_scale=14,
                            color=ACCENT, linewidth=1 + 6 * w, alpha=0.55 + w)
    ax.add_patch(arrow)
    midx = (bx + px) / 2
    midy = (by + arrow_y + 0.4) / 2
    ax.text(midx + 0.05, midy, f'{w:.2f}', fontsize=10, color=ACCENT,
            fontweight='bold')

ax.text(5.5, 0.6, 'attention weights from "blocked" to every other word',
        ha='center', fontsize=11, color=GREY, style='italic')
ax.text(5.5, 4.6, 'When the model processes "blocked", it asks every other word: '
        '"how much do you matter to me?"',
        ha='center', fontsize=11, color=DARK)
save(fig, "gn_attention_arrows.png")


# 7. gn_pretraining_loss_curve.png — loss vs tokens-seen on log scale
#    Synthetic but realistic shape: high random-init loss, sharp early drop,
#    long slow asymptotic tail toward ~1.7 (typical frontier final loss).
tokens_log = np.linspace(np.log10(1e6), np.log10(1e13), 400)
tokens = 10 ** tokens_log
# Smooth curve from ~11 (random over 100k vocab) down to ~1.7 (frontier).
# Use a shifted log decay that flattens out.
final_loss = 1.7
init_loss  = 10.8
curve = final_loss + (init_loss - final_loss) * np.exp(
    -(tokens_log - np.log10(1e6)) * 0.55
)

fig, ax = plt.subplots(figsize=(11, 5.4))
ax.plot(tokens, curve, color=VIOLET, linewidth=2.8, zorder=3)
ax.fill_between(tokens, curve, final_loss - 0.2, color=VIOLET, alpha=0.10, zorder=1)
ax.set_xscale('log')
ax.set_xlim(1e6, 2e13)
ax.set_ylim(0, 12)
ax.set_xlabel('training tokens seen  (log scale)')
ax.set_ylabel('cross-entropy loss')
ax.set_title('How the loss falls during pretraining\n'
             'one curve = trillions of next-token predictions')
ax.grid(True, which='both', alpha=0.25, linestyle='--')

# Annotated waypoints
waypoints = [
    (1e6,  None,        'frequency learned',   ACCENT),
    (1e8,  None,        'grammar learned',     GREEN),
    (1e9,  None,        'plausible sentences', ORANGE),
    (1e11, None,        'domain coherence',    RED),
    (1e13, None,        'frontier model',      DARK),
]
for x, _, label, colour in waypoints:
    # Find loss at that x
    y = float(np.interp(np.log10(x), tokens_log, curve))
    ax.scatter([x], [y], s=80, color=colour, zorder=5,
               edgecolor='white', linewidth=2)
    # Stagger label vertical offset so they don't collide
    ax.annotate(label, xy=(x, y),
                xytext=(8, 14), textcoords='offset points',
                fontsize=10, color=colour, fontweight='bold',
                arrowprops=dict(arrowstyle='-', color=colour, alpha=0.5, lw=1))

# Random-init reference line (the loss you would get from a uniform
# guess over a 100k vocabulary is -log(1/100000) ≈ 11.5)
ax.axhline(np.log(100000), color=GREY, linestyle=':', alpha=0.7)
ax.text(1.2e6, np.log(100000) + 0.18,
        'random-init loss (uniform over 100k vocab)',
        fontsize=9, color=GREY, style='italic')

# Asymptote line
ax.axhline(final_loss, color=GREEN, linestyle=':', alpha=0.7)
ax.text(1.2e6, final_loss + 0.18,
        'best achievable loss (≈ irreducible language entropy)',
        fontsize=9, color=GREEN, style='italic')

fig.tight_layout()
save(fig, "gn_pretraining_loss_curve.png")


# 8. gn_pretraining_pipeline.png — five-stage horizontal flow:
#    raw text → pretraining → base model → fine-tuning/RLHF → product model
fig, ax = plt.subplots(figsize=(12.5, 4.4))
ax.set_xlim(0, 12.5); ax.set_ylim(0, 4)
ax.axis('off')

stages = [
    # (label_top, label_bottom, sub, colour, x_start, width)
    ("WEB TEXT + BOOKS\n+ CODE",
     "~10 trillion tokens",
     "no labels",
     ACCENT,  0.2, 2.0),
    ("PRETRAINING",
     "predict next token\nbillions of weight updates",
     "$100M  ·  2-6 months",
     VIOLET,  2.6, 2.4),
    ("BASE MODEL",
     "knows language\ncompletes any text",
     "not yet a chatbot",
     ORANGE,  5.4, 2.0),
    ("FINE-TUNING\n+ RLHF",
     "instruction-following\nsafety, persona",
     "$1k - $10M",
     GREEN,   7.8, 2.0),
    ("PRODUCT MODEL",
     "ChatGPT, Claude,\nGemini",
     "what you call from an API",
     DARK,    10.2, 2.1),
]

for i, (top, mid, sub, colour, x0, w) in enumerate(stages):
    # Stage box
    box = FancyBboxPatch((x0, 0.6), w, 2.6,
                         boxstyle="round,pad=0.05,rounding_size=0.18",
                         facecolor=colour, edgecolor='white',
                         linewidth=2, alpha=0.92)
    ax.add_patch(box)
    ax.text(x0 + w / 2, 2.7, top, ha='center', va='center',
            fontsize=11, color='white', fontweight='bold')
    ax.text(x0 + w / 2, 1.9, mid, ha='center', va='center',
            fontsize=9.5, color='white')
    ax.text(x0 + w / 2, 1.0, sub, ha='center', va='center',
            fontsize=8.5, color='white', style='italic')
    # Connector arrow to the next stage
    if i < len(stages) - 1:
        next_x = stages[i + 1][4]
        arrow = FancyArrowPatch((x0 + w + 0.02, 1.9),
                                (next_x - 0.02, 1.9),
                                arrowstyle='->', mutation_scale=18,
                                color=GREY, linewidth=2)
        ax.add_patch(arrow)

ax.text(6.25, 3.7,
        'From raw web text to a model you can call from your code',
        ha='center', fontsize=12, color=DARK, fontweight='bold')
ax.text(6.25, 0.18,
        'pretraining is the most expensive stage by ~100x — '
        'and the only one you will not do yourself',
        ha='center', fontsize=10, color=GREY, style='italic')

save(fig, "gn_pretraining_pipeline.png")


# ============================================================
# 4.2 — HuggingFace
# ============================================================

# 7. gn_zeroshot_pipeline.png — input + labels → NLI scoring → ranked output
fig, ax = plt.subplots(figsize=(12, 5.2))
ax.set_xlim(0, 12); ax.set_ylim(0, 6)
ax.axis('off')

# Input text box
input_box = FancyBboxPatch((0.4, 4.0), 4.5, 1.5,
                           boxstyle="round,pad=0.05,rounding_size=0.12",
                           facecolor=LIGHT, edgecolor=GREY, linewidth=2)
ax.add_patch(input_box)
ax.text(2.65, 5.2, "INPUT TEXT", ha='center', fontsize=10, color=GREY,
        fontweight='bold')
ax.text(2.65, 4.7, '"Outbound connection from\nworkstation to 185.234.219.47\nafter powershell execution"',
        ha='center', va='center', fontsize=9, color=DARK, family='monospace')

# Candidate labels
labels_box = FancyBboxPatch((0.4, 1.2), 4.5, 2.4,
                            boxstyle="round,pad=0.05,rounding_size=0.12",
                            facecolor="#fff7ed", edgecolor=ORANGE, linewidth=2)
ax.add_patch(labels_box)
ax.text(2.65, 3.3, "CANDIDATE LABELS", ha='center', fontsize=10, color=ORANGE,
        fontweight='bold')
ax.text(2.65, 2.7, '• "malicious activity"', ha='center', fontsize=10,
        color=DARK, family='monospace')
ax.text(2.65, 2.3, '• "normal traffic"', ha='center', fontsize=10,
        color=DARK, family='monospace')
ax.text(2.65, 1.9, '• "configuration change"', ha='center', fontsize=10,
        color=DARK, family='monospace')
ax.text(2.65, 1.45, '(invented at inference time)', ha='center', fontsize=9,
        color=GREY, style='italic')

# NLI scoring box
nli_box = FancyBboxPatch((5.5, 2.0), 2.6, 2.8,
                         boxstyle="round,pad=0.05,rounding_size=0.12",
                         facecolor="#ecfeff", edgecolor=ACCENT, linewidth=2.5)
ax.add_patch(nli_box)
ax.text(6.8, 4.5, "BART-large\nMNLI", ha='center', fontsize=11, color=ACCENT,
        fontweight='bold')
ax.text(6.8, 3.6, "for each label,\nask: does the\ntext entail it?",
        ha='center', fontsize=9, color=DARK, family='monospace')
ax.text(6.8, 2.4, "(NLI model)", ha='center', fontsize=9, color=GREY,
        style='italic')

# Arrow from input/labels to NLI
arrow1 = FancyArrowPatch((4.95, 4.7), (5.55, 3.7),
                         arrowstyle='->', mutation_scale=18, color=GREY,
                         linewidth=2)
ax.add_patch(arrow1)
arrow2 = FancyArrowPatch((4.95, 2.4), (5.55, 3.3),
                         arrowstyle='->', mutation_scale=18, color=GREY,
                         linewidth=2)
ax.add_patch(arrow2)

# Output ranked labels
out_box = FancyBboxPatch((8.7, 1.5), 3.1, 3.6,
                         boxstyle="round,pad=0.05,rounding_size=0.12",
                         facecolor="#f0fdf4", edgecolor=GREEN, linewidth=2.5)
ax.add_patch(out_box)
ax.text(10.25, 4.8, "RANKED RESULT", ha='center', fontsize=10, color=GREEN,
        fontweight='bold')
results = [("malicious activity", 0.87, GREEN),
           ("normal traffic",     0.09, GREY),
           ("configuration change", 0.04, GREY)]
for i, (lbl, score, col) in enumerate(results):
    y = 4.2 - i * 0.7
    ax.text(8.95, y, lbl, fontsize=10, color=col,
            fontweight='bold' if i == 0 else 'normal')
    ax.text(11.55, y, f'{score:.2f}', ha='right', fontsize=10, color=col,
            fontweight='bold' if i == 0 else 'normal', family='monospace')

# Arrow from NLI to output
arrow3 = FancyArrowPatch((8.15, 3.4), (8.65, 3.4),
                         arrowstyle='->', mutation_scale=18, color=GREY,
                         linewidth=2)
ax.add_patch(arrow3)

ax.text(6, 0.6, 'no training required — labels are invented at inference time',
        ha='center', fontsize=11, color=GREY, style='italic')
fig.suptitle('Zero-shot classification pipeline', y=1.02)
save(fig, "gn_zeroshot_pipeline.png")


# 8. gn_sentence_similarity.png — REAL similarity matrix on 6 security sentences
sec_sentences = [
    "Outbound connection to suspicious IP after powershell",
    "Powershell launched with encoded command from word.exe",
    "User logged in from new location",
    "DNS query to known C2 domain detected",
    "Multiple failed login attempts in 60 seconds",
    "Order shipped via FedEx to your address",
]
print("  → encoding 6 security sentences ...")
sent_emb = st_model.encode(sec_sentences)
sim_matrix = cosine_similarity(sent_emb)

fig, ax = plt.subplots(figsize=(9, 7.2))
im = ax.imshow(sim_matrix, cmap='YlGnBu', vmin=0, vmax=1)
short = [s if len(s) < 38 else s[:36] + "…" for s in sec_sentences]
ax.set_xticks(range(len(sec_sentences)))
ax.set_yticks(range(len(sec_sentences)))
ax.set_xticklabels([f'#{i+1}' for i in range(len(sec_sentences))])
ax.set_yticklabels([f'#{i+1}: {s}' for i, s in enumerate(short)], fontsize=9)
for i in range(len(sec_sentences)):
    for j in range(len(sec_sentences)):
        col = 'white' if sim_matrix[i, j] > 0.5 else DARK
        ax.text(j, i, f'{sim_matrix[i, j]:.2f}', ha='center', va='center',
                fontsize=10, color=col)
ax.set_title('Real cosine similarity matrix from all-MiniLM-L6-v2\n'
             '6 security sentences encoded as 384-dim vectors')
fig.colorbar(im, ax=ax, label='cosine similarity', fraction=0.04)
fig.tight_layout()
save(fig, "gn_sentence_similarity.png")


# 9. gn_search_two_phase.png — indexing vs query phase
fig, ax = plt.subplots(figsize=(12, 5))
ax.set_xlim(0, 12); ax.set_ylim(0, 5)
ax.axis('off')

# Phase 1 — Indexing (top)
ax.text(6, 4.65, "PHASE 1 — Indexing  (offline, once per corpus update)",
        ha='center', fontsize=11, color=ACCENT, fontweight='bold')

p1_docs = FancyBboxPatch((0.4, 3.2), 2.4, 1.0,
                         boxstyle="round,pad=0.05,rounding_size=0.1",
                         facecolor=LIGHT, edgecolor=GREY, linewidth=2)
ax.add_patch(p1_docs)
ax.text(1.6, 3.7, "Doc 1 … Doc N", ha='center', fontsize=11, color=DARK,
        family='monospace')

p1_enc = FancyBboxPatch((4.0, 3.2), 3.2, 1.0,
                        boxstyle="round,pad=0.05,rounding_size=0.1",
                        facecolor="#ecfeff", edgecolor=ACCENT, linewidth=2)
ax.add_patch(p1_enc)
ax.text(5.6, 3.7, "model.encode(docs)", ha='center', fontsize=11,
        color=ACCENT, family='monospace', fontweight='bold')

p1_idx = FancyBboxPatch((8.4, 3.2), 3.2, 1.0,
                        boxstyle="round,pad=0.05,rounding_size=0.1",
                        facecolor="#f0fdf4", edgecolor=GREEN, linewidth=2)
ax.add_patch(p1_idx)
ax.text(10.0, 3.85, "Embedding matrix", ha='center', fontsize=10, color=GREEN,
        fontweight='bold')
ax.text(10.0, 3.5, "(N, 384) on disk", ha='center', fontsize=9, color=DARK,
        family='monospace')

ax.add_patch(FancyArrowPatch((2.85, 3.7), (3.95, 3.7), arrowstyle='->',
                             mutation_scale=18, color=GREY, linewidth=2))
ax.add_patch(FancyArrowPatch((7.25, 3.7), (8.35, 3.7), arrowstyle='->',
                             mutation_scale=18, color=GREY, linewidth=2))

# Divider
ax.axhline(2.85, color=LIGHT, linewidth=1.5)

# Phase 2 — Query (bottom)
ax.text(6, 2.55, "PHASE 2 — Query  (real-time, every search)",
        ha='center', fontsize=11, color=ORANGE, fontweight='bold')

p2_q = FancyBboxPatch((0.2, 1.0), 2.6, 1.1,
                      boxstyle="round,pad=0.05,rounding_size=0.1",
                      facecolor=LIGHT, edgecolor=GREY, linewidth=2)
ax.add_patch(p2_q)
ax.text(1.5, 1.7, '"how to stop\ncredential theft"', ha='center', va='center',
        fontsize=9, color=DARK, family='monospace')

p2_enc = FancyBboxPatch((3.6, 1.0), 3.0, 1.1,
                        boxstyle="round,pad=0.05,rounding_size=0.1",
                        facecolor="#ecfeff", edgecolor=ACCENT, linewidth=2)
ax.add_patch(p2_enc)
ax.text(5.1, 1.7, "encode(query)", ha='center', va='center', fontsize=10,
        color=ACCENT, family='monospace', fontweight='bold')
ax.text(5.1, 1.3, "(1, 384)", ha='center', va='center', fontsize=9,
        color=DARK, family='monospace')

p2_sim = FancyBboxPatch((7.4, 1.0), 2.0, 1.1,
                        boxstyle="round,pad=0.05,rounding_size=0.1",
                        facecolor="#fff7ed", edgecolor=ORANGE, linewidth=2)
ax.add_patch(p2_sim)
ax.text(8.4, 1.7, "cosine\nvs index", ha='center', va='center', fontsize=10,
        color=ORANGE, fontweight='bold')

p2_top = FancyBboxPatch((10.0, 1.0), 1.8, 1.1,
                        boxstyle="round,pad=0.05,rounding_size=0.1",
                        facecolor="#f0fdf4", edgecolor=GREEN, linewidth=2)
ax.add_patch(p2_top)
ax.text(10.9, 1.7, "top-k\nresults", ha='center', va='center', fontsize=10,
        color=GREEN, fontweight='bold')

for x0, x1 in [(2.85, 3.55), (6.65, 7.35), (9.45, 9.95)]:
    ax.add_patch(FancyArrowPatch((x0, 1.55), (x1, 1.55), arrowstyle='->',
                                 mutation_scale=18, color=GREY, linewidth=2))

ax.text(6, 0.3, 'phase 1 is the slow step — phase 2 only encodes the query',
        ha='center', fontsize=10, color=GREY, style='italic')
fig.suptitle('Semantic search — two-phase architecture', y=1.02)
save(fig, "gn_search_two_phase.png")


# 10. gn_keyword_vs_semantic.png — same query, two retrieval styles
fig, ax = plt.subplots(figsize=(11, 5.2))
ax.set_xlim(0, 11); ax.set_ylim(0, 6)
ax.axis('off')

ax.text(5.5, 5.5, 'Query: "how to stop credential theft"',
        ha='center', fontsize=12, color=DARK, fontweight='bold',
        family='monospace')

# Left — Keyword
left_box = FancyBboxPatch((0.3, 0.4), 5.0, 4.5,
                          boxstyle="round,pad=0.05,rounding_size=0.12",
                          facecolor='#fff7ed', edgecolor=RED, linewidth=2.5)
ax.add_patch(left_box)
ax.text(2.8, 4.55, "Keyword search", ha='center', fontsize=12, color=RED,
        fontweight='bold')
ax.text(2.8, 4.15, '(matches exact tokens)', ha='center', fontsize=9, color=GREY,
        style='italic')
keyword_hits = [
    "✓ contains 'credential'",
    "✓ contains 'theft'",
    "✗ Mimikatz writeup (no match)",
    "✗ DCSync defence (no match)",
    "✗ LSASS dumping (no match)",
    "✗ Pass-the-Hash (no match)",
]
for i, h in enumerate(keyword_hits):
    col = GREEN if h.startswith("✓") else RED
    ax.text(0.6, 3.65 - i * 0.5, h, fontsize=10, color=col, family='monospace')

# Right — Semantic
right_box = FancyBboxPatch((5.7, 0.4), 5.0, 4.5,
                           boxstyle="round,pad=0.05,rounding_size=0.12",
                           facecolor='#f0fdf4', edgecolor=GREEN, linewidth=2.5)
ax.add_patch(right_box)
ax.text(8.2, 4.55, "Semantic search", ha='center', fontsize=12, color=GREEN,
        fontweight='bold')
ax.text(8.2, 4.15, '(matches meaning)', ha='center', fontsize=9, color=GREY,
        style='italic')
semantic_hits = [
    "✓ Mimikatz detection",
    "✓ DCSync defence",
    "✓ LSASS memory dumping",
    "✓ Pass-the-Hash mitigation",
    "✓ Credential Guard",
    "✓ Sysmon Event ID 10",
]
for i, h in enumerate(semantic_hits):
    ax.text(6.0, 3.65 - i * 0.5, h, fontsize=10, color=GREEN, family='monospace')

fig.suptitle('Same query, two retrieval philosophies', y=1.02)
save(fig, "gn_keyword_vs_semantic.png")


# ============================================================
# 4.3 — LLM API
# ============================================================

# 11. gn_api_anatomy.png — request/response anatomy
fig, ax = plt.subplots(figsize=(11, 5.4))
ax.set_xlim(0, 11); ax.set_ylim(0, 6)
ax.axis('off')

# Client side
client_box = FancyBboxPatch((0.3, 0.5), 4.0, 5.0,
                            boxstyle="round,pad=0.05,rounding_size=0.12",
                            facecolor="#ecfeff", edgecolor=ACCENT, linewidth=2.5)
ax.add_patch(client_box)
ax.text(2.3, 5.1, "YOUR PYTHON CODE", ha='center', fontsize=11, color=ACCENT,
        fontweight='bold')
client_lines = [
    "client.chat(",
    "  system=\"You are...\",",
    "  messages=[",
    "    {role: \"user\",",
    "     content: \"...\"}",
    "  ],",
    "  max_tokens=200",
    ")",
]
for i, line in enumerate(client_lines):
    ax.text(0.55, 4.5 - i * 0.42, line, fontsize=10, color=DARK,
            family='monospace')
ax.text(2.3, 0.85, "→ str (the reply)", ha='center', fontsize=10, color=GREEN,
        fontweight='bold', family='monospace')

# Server side
server_box = FancyBboxPatch((6.7, 0.5), 4.0, 5.0,
                            boxstyle="round,pad=0.05,rounding_size=0.12",
                            facecolor="#fff7ed", edgecolor=ORANGE, linewidth=2.5)
ax.add_patch(server_box)
ax.text(8.7, 5.1, "LLM PROVIDER", ha='center', fontsize=11, color=ORANGE,
        fontweight='bold')
ax.text(8.7, 4.4, "Receives JSON payload", ha='center', fontsize=10, color=DARK)
ax.text(8.7, 3.95, "Runs the model", ha='center', fontsize=10, color=DARK)
ax.text(8.7, 3.5, "Generates tokens one\nat a time until <eos>\nor max_tokens",
        ha='center', fontsize=10, color=DARK)
ax.text(8.7, 2.4, "Bills you per token", ha='center', fontsize=10, color=DARK)
ax.text(8.7, 1.7, "Returns JSON response", ha='center', fontsize=10, color=DARK)
ax.text(8.7, 0.85, "stateless — no memory\nof previous calls",
        ha='center', fontsize=9, color=GREY, style='italic')

# HTTPS arrows
arrow_req = FancyArrowPatch((4.4, 3.5), (6.6, 3.5),
                            arrowstyle='->', mutation_scale=22, color=GREY,
                            linewidth=2.4)
ax.add_patch(arrow_req)
ax.text(5.5, 3.8, "HTTPS request", ha='center', fontsize=9, color=GREY,
        fontweight='bold')

arrow_resp = FancyArrowPatch((6.6, 2.5), (4.4, 2.5),
                             arrowstyle='->', mutation_scale=22, color=GREY,
                             linewidth=2.4)
ax.add_patch(arrow_resp)
ax.text(5.5, 2.8, "HTTPS response", ha='center', fontsize=9, color=GREY,
        fontweight='bold')

fig.suptitle('Anatomy of one chat API call — request goes out, reply comes back',
             y=1.0)
save(fig, "gn_api_anatomy.png")


# 12. gn_system_user_assistant.png — three message stack
fig, ax = plt.subplots(figsize=(11, 5))
ax.set_xlim(0, 11); ax.set_ylim(0, 5)
ax.axis('off')

roles = [
    ("SYSTEM",    "You are a senior SOC analyst. Be concise.",
     ACCENT, "no — invisible to end user"),
    ("USER",      '"Analyse this log entry: ..."',
     ORANGE, "yes"),
    ("ASSISTANT", "model's reply, shaped by the system prompt above",
     GREEN, "yes"),
]
for i, (role, content, colour, visible) in enumerate(roles):
    y = 4.2 - i * 1.4
    box = FancyBboxPatch((0.5, y - 0.05), 9.0, 1.05,
                         boxstyle="round,pad=0.05,rounding_size=0.1",
                         facecolor=colour, edgecolor='white', linewidth=2,
                         alpha=0.18)
    ax.add_patch(box)
    label_box = FancyBboxPatch((0.55, y + 0.1), 1.7, 0.8,
                               boxstyle="round,pad=0.02,rounding_size=0.08",
                               facecolor=colour, edgecolor='white', linewidth=1.5)
    ax.add_patch(label_box)
    ax.text(1.4, y + 0.5, role, ha='center', va='center', fontsize=11,
            color='white', fontweight='bold')
    ax.text(2.4, y + 0.62, content, fontsize=11, color=DARK, family='monospace')
    ax.text(2.4, y + 0.22, f'visible to user: {visible}', fontsize=9,
            color=GREY, style='italic')
    if i < len(roles) - 1:
        ax.add_patch(FancyArrowPatch((5.0, y - 0.05), (5.0, y - 0.4),
                                     arrowstyle='->', mutation_scale=16,
                                     color=GREY, linewidth=2))

fig.suptitle('How system, user, and assistant messages stack inside one call',
             y=1.0)
save(fig, "gn_system_user_assistant.png")


# 13. gn_json_pipeline.png — log → LLM → JSON → SIEM
fig, ax = plt.subplots(figsize=(12, 4.4))
ax.set_xlim(0, 12); ax.set_ylim(0, 5)
ax.axis('off')

stages = [
    ("Log entry",       '"198 failed logins\nin 60s from\n45.33.32.156"',
     LIGHT, GREY),
    ("LLM call",        "system: JSON\nonly\n+ user log",
     "#ecfeff", ACCENT),
    ("json.loads()",    'dict with\nthreat_type,\nseverity, ...',
     "#fff7ed", ORANGE),
    ("Downstream",      "SIEM /\nticket / SOAR\nplaybook",
     "#f0fdf4", GREEN),
]
xpos = 0.4
boxw = 2.6
for i, (title, body, fill, edge) in enumerate(stages):
    box = FancyBboxPatch((xpos, 1.2), boxw, 2.6,
                         boxstyle="round,pad=0.05,rounding_size=0.12",
                         facecolor=fill, edgecolor=edge, linewidth=2.5)
    ax.add_patch(box)
    ax.text(xpos + boxw / 2, 3.5, title, ha='center', fontsize=11,
            color=edge if edge != LIGHT else GREY, fontweight='bold')
    ax.text(xpos + boxw / 2, 2.3, body, ha='center', va='center', fontsize=9,
            color=DARK, family='monospace')
    if i < len(stages) - 1:
        ax.add_patch(FancyArrowPatch((xpos + boxw + 0.05, 2.5),
                                     (xpos + boxw + 0.4, 2.5),
                                     arrowstyle='->', mutation_scale=18,
                                     color=GREY, linewidth=2))
    xpos += boxw + 0.45

ax.text(6, 0.55, 'every step after the LLM is normal Python on a dict — no scraping prose',
        ha='center', fontsize=10, color=GREY, style='italic')
fig.suptitle('Structured output pipeline — log entry to actionable record', y=1.0)
save(fig, "gn_json_pipeline.png")


# 14. gn_conversation_growth.png — message list grows on every turn
fig, axes = plt.subplots(1, 2, figsize=(12, 4.6))

# Left: bar chart of messages per turn
turns = [1, 2, 3, 4, 5]
msg_count = [2 * t - 1 for t in turns]
axes[0].bar(turns, msg_count, color=ACCENT, edgecolor='white', linewidth=2,
            width=0.55)
for t, c in zip(turns, msg_count):
    axes[0].text(t, c + 0.15, f'{c}', ha='center', fontsize=11, color=DARK,
                 fontweight='bold')
axes[0].set_xlabel('turn number')
axes[0].set_ylabel('messages in the list you send')
axes[0].set_title('Conversation length grows linearly\n(2N − 1 messages on turn N)')
axes[0].set_xticks(turns)
axes[0].set_ylim(0, max(msg_count) + 2)
axes[0].grid(True, alpha=0.3, axis='y')

# Right: stacked timeline of evidence accumulation
evidence = [
    "WORKSTATION-042 unusual outbound",
    "+ powershell.exe spawned by winword.exe",
    "+ connected to 185.219.47.33:443",
]
verdicts = [
    "traffic anomaly\nno attribution",
    "macro-doc execution\n→ likely spear-phishing",
    "phishing → execution → C2\nfull kill chain",
]
ax2 = axes[1]
ax2.set_xlim(0, 10); ax2.set_ylim(0, 5)
ax2.axis('off')
ax2.set_title('Incident investigation — context builds')
for i in range(3):
    y = 4.0 - i * 1.4
    ev_box = FancyBboxPatch((0.2, y), 4.5, 1.0,
                            boxstyle="round,pad=0.02,rounding_size=0.08",
                            facecolor=LIGHT, edgecolor=GREY, linewidth=1.5)
    ax2.add_patch(ev_box)
    ax2.text(0.35, y + 0.55, f"turn {i+1}", fontsize=9, color=GREY,
             fontweight='bold')
    ax2.text(0.35, y + 0.2, evidence[i], fontsize=9, color=DARK,
             family='monospace')

    ax2.add_patch(FancyArrowPatch((4.75, y + 0.5), (5.25, y + 0.5),
                                  arrowstyle='->', mutation_scale=14,
                                  color=ACCENT, linewidth=1.8))

    vbox = FancyBboxPatch((5.3, y), 4.5, 1.0,
                          boxstyle="round,pad=0.02,rounding_size=0.08",
                          facecolor="#f0fdf4", edgecolor=GREEN, linewidth=1.5)
    ax2.add_patch(vbox)
    ax2.text(7.55, y + 0.5, verdicts[i], ha='center', va='center', fontsize=9,
             color=DARK)

fig.tight_layout()
save(fig, "gn_conversation_growth.png")


# ============================================================
# 4.4 — RAG
# ============================================================

# 15. gn_chunking_strategies.png — three chunk strategies on the same paragraph
fig, ax = plt.subplots(figsize=(12, 5.4))
ax.set_xlim(0, 12); ax.set_ylim(0, 6)
ax.axis('off')

# Source paragraph (top)
ax.text(6, 5.6, "Source: 800-word security article", ha='center', fontsize=11,
        color=GREY, fontweight='bold')
ax.add_patch(Rectangle((0.5, 4.85), 11, 0.5, facecolor=LIGHT, edgecolor=GREY,
                       linewidth=1.2))
for i in range(20):
    ax.add_patch(Rectangle((0.5 + i * 0.55, 4.85), 0.55, 0.5,
                           facecolor=LIGHT, edgecolor='white', linewidth=0.5))

# Strategy 1 — fixed-size, no overlap
ax.text(6, 4.4, "Fixed-size (chunk_size=100, no overlap)", ha='center',
        fontsize=10, color=ORANGE, fontweight='bold')
chunk_w = 11 / 8
for i in range(8):
    x0 = 0.5 + i * chunk_w
    box = FancyBboxPatch((x0 + 0.04, 3.5), chunk_w - 0.08, 0.55,
                         boxstyle="round,pad=0.01,rounding_size=0.05",
                         facecolor=ORANGE, edgecolor='white', linewidth=1.2,
                         alpha=0.85)
    ax.add_patch(box)
    ax.text(x0 + chunk_w / 2, 3.78, f'C{i+1}', ha='center', va='center',
            fontsize=9, color='white', fontweight='bold')

# Strategy 2 — overlap
ax.text(6, 3.0, "Overlap (chunk_size=100, overlap=20)", ha='center', fontsize=10,
        color=ACCENT, fontweight='bold')
overlap_w = chunk_w * 1.25
shift = chunk_w * 0.8
for i in range(9):
    x0 = 0.5 + i * shift
    if x0 + overlap_w > 11.5:
        break
    box = FancyBboxPatch((x0 + 0.04, 2.05 + 0.04 * (i % 2)),
                         overlap_w - 0.08, 0.5,
                         boxstyle="round,pad=0.01,rounding_size=0.05",
                         facecolor=ACCENT, edgecolor='white', linewidth=1.2,
                         alpha=0.6 if i % 2 else 0.85)
    ax.add_patch(box)
    ax.text(x0 + overlap_w / 2, 2.3 + 0.04 * (i % 2), f'C{i+1}', ha='center',
            va='center', fontsize=9, color='white', fontweight='bold')

# Strategy 3 — sentence-based (variable widths)
ax.text(6, 1.5, "Sentence-based (~3 sentences per chunk, variable size)",
        ha='center', fontsize=10, color=VIOLET, fontweight='bold')
sentence_widths = [1.6, 0.9, 1.4, 1.1, 1.7, 0.8, 1.3, 1.5, 1.0]
xpos = 0.5
for i, w in enumerate(sentence_widths):
    if xpos + w > 11.5:
        break
    box = FancyBboxPatch((xpos + 0.04, 0.55), w - 0.08, 0.5,
                         boxstyle="round,pad=0.01,rounding_size=0.05",
                         facecolor=VIOLET, edgecolor='white', linewidth=1.2,
                         alpha=0.85)
    ax.add_patch(box)
    ax.text(xpos + w / 2, 0.8, f'C{i+1}', ha='center', va='center', fontsize=9,
            color='white', fontweight='bold')
    xpos += w + 0.04

fig.suptitle('Three chunking strategies on the same document', y=1.02)
save(fig, "gn_chunking_strategies.png")


# 16. gn_chunk_overlap_detail.png — close-up of two overlapping chunks
fig, ax = plt.subplots(figsize=(11, 4.2))
ax.set_xlim(0, 11); ax.set_ylim(0, 4.5)
ax.axis('off')

# Chunk 1: words 1-100
c1 = FancyBboxPatch((0.4, 2.5), 6.0, 1.2,
                    boxstyle="round,pad=0.05,rounding_size=0.1",
                    facecolor=ACCENT, edgecolor='white', linewidth=2, alpha=0.8)
ax.add_patch(c1)
ax.text(0.6, 3.4, "Chunk 1  (words 1 – 100)", fontsize=10, color='white',
        fontweight='bold')
ax.text(3.4, 2.85, "... detection of LSASS access ...", ha='center',
        fontsize=10, color='white', family='monospace')

# Chunk 2: words 81-180
c2 = FancyBboxPatch((4.6, 0.8), 6.0, 1.2,
                    boxstyle="round,pad=0.05,rounding_size=0.1",
                    facecolor=ORANGE, edgecolor='white', linewidth=2, alpha=0.8)
ax.add_patch(c2)
ax.text(4.8, 1.7, "Chunk 2  (words 81 – 180)", fontsize=10, color='white',
        fontweight='bold')
ax.text(7.6, 1.15, "... relies on Sysmon Event ID 10 ...", ha='center',
        fontsize=10, color='white', family='monospace')

# Highlight the overlap zone (words 81-100)
overlap_zone = Rectangle((4.6, 2.5), 1.8, 1.2, facecolor=GOLD, alpha=0.55,
                         edgecolor=GOLD, linewidth=2)
ax.add_patch(overlap_zone)
ax.text(5.5, 4.0, "shared words 81–100", ha='center', fontsize=10, color=DARK,
        fontweight='bold')
ax.add_patch(FancyArrowPatch((5.5, 3.85), (5.5, 3.7), arrowstyle='->',
                             mutation_scale=14, color=DARK, linewidth=1.5))

ax.text(5.5, 0.25,
        'the boundary sentence "detection of LSASS access relies on Sysmon Event ID 10"\n'
        'now lives intact inside Chunk 2 — retrieval can find the whole answer',
        ha='center', fontsize=9.5, color=GREY, style='italic')
fig.suptitle('Overlap chunking — boundary facts preserved', y=1.0)
save(fig, "gn_chunk_overlap_detail.png")


# 17. gn_rag_pipeline.png — full 3-stage RAG pipeline
fig, ax = plt.subplots(figsize=(12.5, 5.6))
ax.set_xlim(0, 12.5); ax.set_ylim(0, 6)
ax.axis('off')

# User query (top left)
q_box = FancyBboxPatch((0.3, 4.6), 3.0, 1.0,
                       boxstyle="round,pad=0.05,rounding_size=0.1",
                       facecolor=LIGHT, edgecolor=GREY, linewidth=2)
ax.add_patch(q_box)
ax.text(1.8, 5.3, "User question", ha='center', fontsize=10, color=GREY,
        fontweight='bold')
ax.text(1.8, 4.85, '"How do I detect\nMimikatz?"', ha='center', va='center',
        fontsize=9, color=DARK, family='monospace')

# Stage 1 — Retrieve
r_box = FancyBboxPatch((4.0, 4.5), 3.5, 1.2,
                       boxstyle="round,pad=0.05,rounding_size=0.1",
                       facecolor="#ecfeff", edgecolor=ACCENT, linewidth=2.5)
ax.add_patch(r_box)
ax.text(5.75, 5.45, "1. RETRIEVE", ha='center', fontsize=11, color=ACCENT,
        fontweight='bold')
ax.text(5.75, 4.95, "encode(query) →\ncosine vs index", ha='center', va='center',
        fontsize=9, color=DARK, family='monospace')

# Vector index (bottom left of retrieve)
idx_box = FancyBboxPatch((4.0, 2.7), 3.5, 1.4,
                         boxstyle="round,pad=0.05,rounding_size=0.1",
                         facecolor=LIGHT, edgecolor=GREY, linewidth=1.5)
ax.add_patch(idx_box)
ax.text(5.75, 3.85, "Vector index", ha='center', fontsize=9, color=GREY,
        fontweight='bold')
for i in range(3):
    ax.text(5.75, 3.45 - i * 0.3, f'chunk {i+1}: [...] vector', ha='center',
            fontsize=8, color=DARK, family='monospace')
ax.add_patch(FancyArrowPatch((5.75, 4.45), (5.75, 4.15), arrowstyle='->',
                             mutation_scale=14, color=GREY, linewidth=1.5))

# Stage 2 — Augment
a_box = FancyBboxPatch((8.0, 4.5), 4.2, 1.2,
                       boxstyle="round,pad=0.05,rounding_size=0.1",
                       facecolor="#fff7ed", edgecolor=ORANGE, linewidth=2.5)
ax.add_patch(a_box)
ax.text(10.1, 5.45, "2. AUGMENT", ha='center', fontsize=11, color=ORANGE,
        fontweight='bold')
ax.text(10.1, 4.95, "inject top-k chunks into\nsystem prompt CONTEXT:",
        ha='center', va='center', fontsize=9, color=DARK, family='monospace')

# Stage 3 — Generate
g_box = FancyBboxPatch((4.0, 1.0), 8.2, 1.4,
                       boxstyle="round,pad=0.05,rounding_size=0.12",
                       facecolor="#f0fdf4", edgecolor=GREEN, linewidth=2.5)
ax.add_patch(g_box)
ax.text(8.1, 2.15, "3. GENERATE", ha='center', fontsize=11, color=GREEN,
        fontweight='bold')
ax.text(8.1, 1.55, "LLM answers using ONLY the injected context — grounded answer",
        ha='center', va='center', fontsize=10, color=DARK)

# Arrows: query → retrieve, retrieve → augment, augment → generate
ax.add_patch(FancyArrowPatch((3.35, 5.1), (3.95, 5.1), arrowstyle='->',
                             mutation_scale=18, color=GREY, linewidth=2))
ax.add_patch(FancyArrowPatch((7.55, 5.1), (7.95, 5.1), arrowstyle='->',
                             mutation_scale=18, color=GREY, linewidth=2))
ax.add_patch(FancyArrowPatch((10.1, 4.45), (10.1, 2.45), arrowstyle='->',
                             mutation_scale=18, color=GREY, linewidth=2.2))

# Final answer (bottom)
ans_box = FancyBboxPatch((4.0, 0.05), 8.2, 0.7,
                         boxstyle="round,pad=0.03,rounding_size=0.08",
                         facecolor='white', edgecolor=GREEN, linewidth=1.5,
                         linestyle='--')
ax.add_patch(ans_box)
ax.text(8.1, 0.4, '"To detect Mimikatz, monitor LSASS memory access via Sysmon Event ID 10..."',
        ha='center', va='center', fontsize=9, color=DARK, style='italic')

fig.suptitle('Full RAG pipeline — retrieve, augment, generate', y=1.0)
save(fig, "gn_rag_pipeline.png")


# 18. gn_rag_vs_llm.png — ranked comparison table
fig, ax = plt.subplots(figsize=(11, 5))
ax.set_xlim(0, 11); ax.set_ylim(0, 6)
ax.axis('off')

headers = ["", "Pure LLM", "RAG"]
rows = [
    ("Knowledge source",     "training data (frozen)", "your KB (updateable)"),
    ("Hallucination risk",   "higher",                  "lower (grounded)"),
    ("Cites sources",        "no",                      "can be instructed to"),
    ("Answers about new events", "no (cutoff date)",    "yes (if KB current)"),
    ("Domain specificity",   "general",                 "as specific as KB"),
]
col_x = [0.4, 4.5, 8.0]
ax.text(col_x[0], 5.4, headers[0], fontsize=11, color=DARK)
ax.text(col_x[1], 5.4, headers[1], fontsize=11, color=GREY, fontweight='bold')
ax.text(col_x[2], 5.4, headers[2], fontsize=11, color=GREEN, fontweight='bold')
ax.plot([0.3, 10.7], [5.15, 5.15], color=GREY, linewidth=1.2)
for i, (label, llm, rag) in enumerate(rows):
    y = 4.5 - i * 0.85
    ax.text(col_x[0], y, label, fontsize=10.5, color=DARK)
    ax.text(col_x[1], y, llm, fontsize=10.5, color=GREY)
    ax.text(col_x[2], y, rag, fontsize=10.5, color=GREEN, fontweight='bold')

fig.suptitle('RAG vs Pure LLM — when retrieval changes the answer', y=1.0)
save(fig, "gn_rag_vs_llm.png")


print(f"\n18 GenAI visuals written to {OUT}")
