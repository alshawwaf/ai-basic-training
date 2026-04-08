"""
Generate visuals for the four Feature Engineering lectures (Stage 2.1).
    python portal/static/lecture_assets/_generate_feature_engineering.py

Reproduces the lab dataset (200 raw firewall events) and the derived features
exactly as the four solution_*.py files do.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

OUT = Path(__file__).resolve().parent

DPI = 140
SAVE = dict(dpi=DPI, bbox_inches="tight", facecolor="white")
ACCENT = "#0891b2"
VIOLET = "#8b5cf6"
RED    = "#dc2626"
ORANGE = "#f59e0b"
GREEN  = "#16a34a"
GREY   = "#64748b"
LIGHT  = "#e2e8f0"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
})

# ── Reproduce the lab raw log (matches every Stage 2.1 solution file) ──────────
np.random.seed(42)
n = 200
raw_df = pd.DataFrame({
    'timestamp':    pd.date_range('2024-01-15 08:00', periods=n, freq='2min'),
    'src_ip':       [f"192.168.{np.random.randint(0,10)}.{np.random.randint(1,255)}"
                     for _ in range(n)],
    'dst_ip':       [f"{np.random.randint(1,223)}.{np.random.randint(0,255)}."
                     f"{np.random.randint(0,255)}.{np.random.randint(1,255)}"
                     for _ in range(n)],
    'src_port':     np.random.randint(49152, 65535, n),
    'dst_port':     np.random.choice([80, 443, 22, 53, 3389, 21, 8080], n,
                                     p=[0.30, 0.30, 0.10, 0.10, 0.05, 0.05, 0.10]),
    'protocol':     np.random.choice(['TCP', 'UDP', 'ICMP'], n, p=[0.7, 0.25, 0.05]),
    'bytes_sent':   np.random.lognormal(7, 1.2, n).astype(int).clip(100, 100000),
    'bytes_recv':   np.random.lognormal(8, 1.5, n).astype(int).clip(100, 500000),
    'packets':      np.random.poisson(40, n).clip(1, 200),
    'duration_str': [f"{d:.2f}s" for d in np.random.exponential(15, n).clip(0.05, 300)],
    'action':       np.random.choice(['ALLOW', 'BLOCK'], n, p=[0.85, 0.15]),
})
raw_df['duration'] = raw_df['duration_str'].str.rstrip('s').astype(float)
raw_df['bytes_per_second'] = np.where(raw_df['duration'] > 0,
                                      raw_df['bytes_sent'] / raw_df['duration'], 0)
raw_df['packet_rate'] = np.where(raw_df['duration'] > 0,
                                 raw_df['packets'] / raw_df['duration'], 0)
raw_df['bytes_ratio'] = raw_df['bytes_sent'] / (raw_df['bytes_recv'] + 1)
raw_df['hour_of_day'] = raw_df['timestamp'].dt.hour
raw_df['day_of_week'] = raw_df['timestamp'].dt.dayofweek
raw_df['is_business_hours'] = ((raw_df['hour_of_day'] >= 9) &
                               (raw_df['hour_of_day'] <= 17) &
                               (raw_df['day_of_week'] < 5)).astype(int)


def card(ax, x, y, w, h, label, value=None, fill=LIGHT, edge=GREY, fc_label="#0f172a"):
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.06",
                         linewidth=1.4, edgecolor=edge, facecolor=fill)
    ax.add_patch(box)
    if value is None:
        ax.text(x + w/2, y + h/2, label, ha="center", va="center",
                fontsize=10, color=fc_label)
    else:
        ax.text(x + w/2, y + h*0.65, label, ha="center", va="center",
                fontsize=9, color="#475569")
        ax.text(x + w/2, y + h*0.30, value, ha="center", va="center",
                fontsize=11, color=fc_label, fontweight="bold")


# ══════════════════════════════════════════════════════════════════════════════
# 1. fe_raw_log_dtypes — sample raw log with column dtype colour coding
# ══════════════════════════════════════════════════════════════════════════════
def viz_raw_log_dtypes():
    sample = raw_df.head(4)[['timestamp', 'src_ip', 'dst_port', 'protocol',
                             'bytes_sent', 'duration_str']]
    col_kind = {
        'timestamp':    ('string', RED),
        'src_ip':       ('string', RED),
        'dst_port':     ('int',    ACCENT),
        'protocol':     ('string', RED),
        'bytes_sent':   ('int',    ACCENT),
        'duration_str': ('string', ORANGE),
    }
    fig, ax = plt.subplots(figsize=(10.4, 4.0))
    ax.set_xlim(0, 12); ax.set_ylim(0, 7)
    ax.axis("off")

    headers = list(sample.columns)
    col_w   = 12 / len(headers)
    # header row with kind tag
    for i, h in enumerate(headers):
        kind, colour = col_kind[h]
        ax.add_patch(Rectangle((i*col_w, 5.4), col_w-0.05, 1.2,
                               facecolor=colour, edgecolor="white", linewidth=2))
        ax.text(i*col_w + col_w/2, 6.15, h, ha="center", va="center",
                color="white", fontsize=10, fontweight="bold")
        ax.text(i*col_w + col_w/2, 5.70, f"({kind})", ha="center", va="center",
                color="white", fontsize=8.5, style="italic")
    # data rows
    for r, (_, row) in enumerate(sample.iterrows()):
        y_top = 5.3 - r*1.10
        for i, h in enumerate(headers):
            val = str(row[h])
            if len(val) > 14:
                val = val[:13] + "…"
            ax.add_patch(Rectangle((i*col_w, y_top-1.05), col_w-0.05, 1.0,
                                   facecolor="white", edgecolor=LIGHT, linewidth=1))
            ax.text(i*col_w + col_w/2, y_top-0.55, val, ha="center", va="center",
                    fontsize=8.8, color="#0f172a", family="monospace")
    # legend strip
    legends = [(ACCENT, "numeric — sklearn accepts"),
               (ORANGE, "string but parseable (strip 's', cast)"),
               (RED,    "string — sklearn rejects (needs encoding)")]
    for i, (c, label) in enumerate(legends):
        x0 = 0.2 + i*4.0
        ax.add_patch(Rectangle((x0, -0.5), 0.35, 0.35, facecolor=c, edgecolor="none"))
        ax.text(x0+0.5, -0.32, label, fontsize=9, va="center", color="#0f172a")
    plt.savefig(OUT / "fe_raw_log_dtypes.png", **SAVE); plt.close(fig)


# ══════════════════════════════════════════════════════════════════════════════
# 2. fe_sklearn_rejects — flow showing the ValueError on protocol column
# ══════════════════════════════════════════════════════════════════════════════
def viz_sklearn_rejects():
    fig, ax = plt.subplots(figsize=(10.0, 4.2))
    ax.set_xlim(0, 12); ax.set_ylim(0, 6); ax.axis("off")

    # raw frame box
    card(ax, 0.3, 1.3, 3.4, 3.4, "raw_df\n[bytes_sent, bytes_recv,\nprotocol, packets]",
         fill="#f8fafc", edge=GREY)
    # arrow → model
    arrow = FancyArrowPatch((3.8, 3.0), (5.2, 3.0), arrowstyle="-|>",
                            mutation_scale=18, linewidth=2, color=GREY)
    ax.add_patch(arrow)
    ax.text(4.5, 3.45, ".fit(X, y)", ha="center", fontsize=10,
            color="#475569", family="monospace")
    # sklearn box
    card(ax, 5.3, 1.7, 3.0, 2.6, "LogisticRegression",
         fill="#ecfeff", edge=ACCENT, fc_label=ACCENT)
    # arrow → error
    arrow2 = FancyArrowPatch((8.4, 3.0), (9.6, 3.0), arrowstyle="-|>",
                             mutation_scale=18, linewidth=2, color=RED)
    ax.add_patch(arrow2)
    # ValueError box
    card(ax, 9.7, 1.5, 2.2, 3.0, "ValueError\ncould not convert\nstring to float:\n'TCP'",
         fill="#fee2e2", edge=RED, fc_label=RED)
    # caption strip
    ax.text(6.0, 0.6,
            "sklearn fit() requires every column to be numeric. One string column "
            "is enough to halt the entire pipeline.",
            ha="center", fontsize=10, color="#475569", style="italic")
    plt.savefig(OUT / "fe_sklearn_rejects.png", **SAVE); plt.close(fig)


# ══════════════════════════════════════════════════════════════════════════════
# 3. fe_transformation_plan — raw column → action map
# ══════════════════════════════════════════════════════════════════════════════
def viz_transformation_plan():
    plan = [
        ('timestamp',   'extract hour / day / business_hours',  ORANGE),
        ('src_ip',      'is_private flag (RFC1918 lookup)',     ORANGE),
        ('dst_ip',      'is_private + reputation lookup',       ORANGE),
        ('dst_port',    'port_risk_score lookup table',         VIOLET),
        ('protocol',    'one-hot encode (TCP / UDP / ICMP)',    VIOLET),
        ('bytes_sent',  'use directly (numeric)',               ACCENT),
        ('bytes_recv',  'use directly (numeric)',               ACCENT),
        ('packets',     'use directly (numeric)',               ACCENT),
        ('duration_str','strip "s", cast to float',             ORANGE),
        ('action',      'drop — this is the LABEL, not a feature', RED),
    ]
    fig, ax = plt.subplots(figsize=(10.4, 6.6))
    ax.set_xlim(0, 12); ax.set_ylim(0, len(plan)*0.85 + 0.6); ax.axis("off")
    for i, (col, action, c) in enumerate(reversed(plan)):
        y = 0.4 + i*0.85
        ax.add_patch(FancyBboxPatch((0.2, y), 3.4, 0.65,
                                    boxstyle="round,pad=0.02,rounding_size=0.08",
                                    facecolor="#f8fafc", edgecolor=GREY, linewidth=1.2))
        ax.text(1.9, y+0.32, col, ha="center", va="center", fontsize=10.5,
                family="monospace", color="#0f172a")
        arrow = FancyArrowPatch((3.7, y+0.32), (4.6, y+0.32), arrowstyle="-|>",
                                mutation_scale=14, color=c, linewidth=1.8)
        ax.add_patch(arrow)
        ax.add_patch(FancyBboxPatch((4.7, y), 7.1, 0.65,
                                    boxstyle="round,pad=0.02,rounding_size=0.08",
                                    facecolor=c, edgecolor=c, linewidth=1.2, alpha=0.18))
        ax.text(4.9, y+0.32, action, ha="left", va="center", fontsize=10,
                color="#0f172a")
    # title row
    ax.text(1.9, len(plan)*0.85 + 0.2, "raw column",
            ha="center", fontsize=11, color="#475569", fontweight="bold")
    ax.text(8.25, len(plan)*0.85 + 0.2, "transformation",
            ha="center", fontsize=11, color="#475569", fontweight="bold")
    plt.savefig(OUT / "fe_transformation_plan.png", **SAVE); plt.close(fig)


# ══════════════════════════════════════════════════════════════════════════════
# 4. fe_derived_features — three formula cards with worked example
# ══════════════════════════════════════════════════════════════════════════════
def viz_derived_features():
    row = raw_df.iloc[0]
    bs   = int(row['bytes_sent']);   br = int(row['bytes_recv'])
    pkts = int(row['packets']);      dur = float(row['duration'])
    bps  = bs / dur
    pr   = pkts / dur
    bratio = bs / (br + 1)

    fig, ax = plt.subplots(figsize=(10.6, 4.6))
    ax.set_xlim(0, 12); ax.set_ylim(0, 6); ax.axis("off")
    cards = [
        ("bytes_per_second",  f"= bytes_sent / duration",
         f"{bs} / {dur:.2f}  =  {bps:,.0f} B/s",
         "huge spikes flag exfil bursts", ACCENT),
        ("packet_rate",       f"= packets / duration",
         f"{pkts} / {dur:.2f}  =  {pr:.2f} pkt/s",
         "very high → SYN flood / scan", VIOLET),
        ("bytes_ratio",       f"= bytes_sent / (bytes_recv + 1)",
         f"{bs} / ({br} + 1)  =  {bratio:.2f}",
         ">>1 means more upload than download", ORANGE),
    ]
    w = 3.6
    for i, (name, formula, worked, intuition, colour) in enumerate(cards):
        x0 = 0.3 + i*3.9
        ax.add_patch(FancyBboxPatch((x0, 0.5), w, 5.0,
                                    boxstyle="round,pad=0.05,rounding_size=0.12",
                                    facecolor=colour, edgecolor=colour,
                                    linewidth=1.5, alpha=0.13))
        ax.text(x0 + w/2, 4.85, name, ha="center", fontsize=12,
                fontweight="bold", color=colour, family="monospace")
        ax.text(x0 + w/2, 4.1, formula, ha="center", fontsize=10,
                color="#475569", family="monospace")
        ax.add_patch(Rectangle((x0+0.25, 2.55), w-0.5, 0.95,
                               facecolor="white", edgecolor=colour, linewidth=1.2))
        ax.text(x0 + w/2, 3.02, worked, ha="center", va="center", fontsize=10,
                color="#0f172a", family="monospace")
        ax.text(x0 + w/2, 1.3, intuition, ha="center", fontsize=9.2,
                color="#475569", style="italic", wrap=True)
    plt.savefig(OUT / "fe_derived_features.png", **SAVE); plt.close(fig)


# ══════════════════════════════════════════════════════════════════════════════
# 5. fe_port_risk_table — coloured port → risk lookup
# ══════════════════════════════════════════════════════════════════════════════
def viz_port_risk_table():
    rows = [
        ("80",   "HTTP",        1, "standard web",                ACCENT),
        ("443",  "HTTPS",       1, "standard encrypted web",      ACCENT),
        ("53",   "DNS",         2, "watch for DNS tunnelling",    "#06b6d4"),
        ("22",   "SSH",         3, "legitimate but targeted",     ORANGE),
        ("21",   "FTP",         4, "credentials in clear text",   "#f97316"),
        ("3389", "RDP",         5, "frequently exploited",        RED),
    ]
    fig, ax = plt.subplots(figsize=(10.0, 4.6))
    ax.set_xlim(0, 12); ax.set_ylim(0, 7.6); ax.axis("off")
    headers = ["dst_port", "service", "risk score", "why"]
    col_x   = [0.5, 2.6, 4.8, 7.4]
    col_w   = [2.0, 2.0, 2.4, 4.4]
    for i, h in enumerate(headers):
        ax.add_patch(Rectangle((col_x[i], 6.6), col_w[i]-0.05, 0.8,
                               facecolor="#1e293b", edgecolor="white", linewidth=2))
        ax.text(col_x[i] + col_w[i]/2, 7.0, h, ha="center", va="center",
                color="white", fontsize=10.5, fontweight="bold")
    for r, (port, svc, score, why, c) in enumerate(rows):
        y = 5.6 - r*0.95
        for i in range(4):
            ax.add_patch(Rectangle((col_x[i], y), col_w[i]-0.05, 0.85,
                                   facecolor="white", edgecolor=LIGHT, linewidth=1))
        ax.text(col_x[0] + col_w[0]/2, y+0.42, port, ha="center", va="center",
                fontsize=11, family="monospace", color="#0f172a")
        ax.text(col_x[1] + col_w[1]/2, y+0.42, svc, ha="center", va="center",
                fontsize=11, color="#0f172a")
        # score badge
        ax.add_patch(FancyBboxPatch((col_x[2]+0.7, y+0.18), 1.0, 0.50,
                                    boxstyle="round,pad=0.02,rounding_size=0.10",
                                    facecolor=c, edgecolor=c, linewidth=1))
        ax.text(col_x[2] + col_w[2]/2 - 0.15, y+0.42, str(score),
                ha="center", va="center", fontsize=12, color="white",
                fontweight="bold")
        ax.text(col_x[3] + 0.15, y+0.42, why, ha="left", va="center",
                fontsize=10, color="#0f172a", style="italic")
    plt.savefig(OUT / "fe_port_risk_table.png", **SAVE); plt.close(fig)


# ══════════════════════════════════════════════════════════════════════════════
# 6. fe_business_hours — bytes_per_second business vs off-hours bar chart
# ══════════════════════════════════════════════════════════════════════════════
def viz_business_hours():
    biz = raw_df[raw_df['is_business_hours'] == 1]['bytes_per_second']
    off = raw_df[raw_df['is_business_hours'] == 0]['bytes_per_second']
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.4, 4.0),
                                   gridspec_kw=dict(width_ratios=[1.05, 1.5]))
    # left: counts
    ax1.bar(["Business hours\n(Mon–Fri 9–17)", "Off hours"],
            [len(biz), len(off)], color=[ACCENT, ORANGE],
            edgecolor="white", linewidth=2)
    ax1.set_ylabel("# connections")
    ax1.set_title("How many events fall in each window")
    for i, v in enumerate([len(biz), len(off)]):
        ax1.text(i, v + 1, str(v), ha="center", fontsize=11, fontweight="bold")
    ax1.spines["top"].set_visible(False); ax1.spines["right"].set_visible(False)
    # right: mean bytes/sec
    ax2.bar(["Business hours", "Off hours"], [biz.mean(), off.mean()],
            color=[ACCENT, ORANGE], edgecolor="white", linewidth=2)
    ax2.set_ylabel("mean bytes_per_second")
    ax2.set_title("Average traffic intensity per window")
    for i, v in enumerate([biz.mean(), off.mean()]):
        ax2.text(i, v + 30, f"{v:,.0f}", ha="center", fontsize=11, fontweight="bold")
    ax2.spines["top"].set_visible(False); ax2.spines["right"].set_visible(False)
    plt.tight_layout()
    plt.savefig(OUT / "fe_business_hours.png", **SAVE); plt.close(fig)


# ══════════════════════════════════════════════════════════════════════════════
# 7. fe_label_vs_onehot — side-by-side encoding comparison
# ══════════════════════════════════════════════════════════════════════════════
def viz_label_vs_onehot():
    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.6))
    samples = ["TCP", "UDP", "ICMP", "TCP", "UDP"]

    # ── LabelEncoder panel
    ax = axes[0]
    ax.set_xlim(0, 6); ax.set_ylim(0, 7.5); ax.axis("off")
    ax.text(3.0, 7.0, "LabelEncoder", ha="center", fontsize=13,
            color=RED, fontweight="bold")
    ax.text(3.0, 6.5, "(implies a fake ordering)", ha="center", fontsize=9.5,
            color="#475569", style="italic")
    # header
    ax.add_patch(Rectangle((0.4, 5.5), 2.4, 0.6, facecolor="#1e293b"))
    ax.add_patch(Rectangle((3.0, 5.5), 2.4, 0.6, facecolor="#1e293b"))
    ax.text(1.6, 5.8, "protocol", ha="center", color="white", fontsize=10, fontweight="bold")
    ax.text(4.2, 5.8, "protocol_label", ha="center", color="white", fontsize=10, fontweight="bold")
    label_map = {"ICMP": 0, "TCP": 1, "UDP": 2}
    for i, s in enumerate(samples):
        y = 4.8 - i*0.75
        ax.add_patch(Rectangle((0.4, y), 2.4, 0.65, facecolor="white", edgecolor=LIGHT))
        ax.add_patch(Rectangle((3.0, y), 2.4, 0.65, facecolor="white", edgecolor=LIGHT))
        ax.text(1.6, y+0.32, s, ha="center", va="center", fontsize=11, family="monospace")
        ax.text(4.2, y+0.32, str(label_map[s]), ha="center", va="center", fontsize=11,
                family="monospace", color=RED, fontweight="bold")
    ax.text(3.0, 0.4, "model thinks: TCP is halfway between ICMP and UDP",
            ha="center", fontsize=9.5, color=RED, style="italic")

    # ── OneHotEncoder panel
    ax = axes[1]
    ax.set_xlim(0, 8); ax.set_ylim(0, 7.5); ax.axis("off")
    ax.text(4.0, 7.0, "OneHotEncoder", ha="center", fontsize=13,
            color=GREEN, fontweight="bold")
    ax.text(4.0, 6.5, "(no false ordering — independent flags)", ha="center",
            fontsize=9.5, color="#475569", style="italic")
    headers = ["protocol", "proto_ICMP", "proto_TCP", "proto_UDP"]
    col_x   = [0.2, 2.4, 4.3, 6.2]
    for i, h in enumerate(headers):
        ax.add_patch(Rectangle((col_x[i], 5.5), 1.8, 0.6, facecolor="#1e293b"))
        ax.text(col_x[i]+0.9, 5.8, h, ha="center", color="white", fontsize=9.5, fontweight="bold")
    flag = {"ICMP":(1,0,0), "TCP":(0,1,0), "UDP":(0,0,1)}
    for i, s in enumerate(samples):
        y = 4.8 - i*0.75
        ax.add_patch(Rectangle((col_x[0], y), 1.8, 0.65, facecolor="white", edgecolor=LIGHT))
        ax.text(col_x[0]+0.9, y+0.32, s, ha="center", va="center", fontsize=11, family="monospace")
        for j, v in enumerate(flag[s]):
            cell_color = "#dcfce7" if v == 1 else "white"
            ax.add_patch(Rectangle((col_x[j+1], y), 1.8, 0.65,
                                   facecolor=cell_color, edgecolor=LIGHT))
            ax.text(col_x[j+1]+0.9, y+0.32, str(v), ha="center", va="center",
                    fontsize=11, family="monospace",
                    color=GREEN if v == 1 else "#94a3b8",
                    fontweight="bold" if v == 1 else "normal")
    ax.text(4.0, 0.4, "each protocol gets its own flag column — no implied distance",
            ha="center", fontsize=9.5, color=GREEN, style="italic")
    plt.tight_layout()
    plt.savefig(OUT / "fe_label_vs_onehot.png", **SAVE); plt.close(fig)


# ══════════════════════════════════════════════════════════════════════════════
# 8. fe_dummy_trap — drop=first explained
# ══════════════════════════════════════════════════════════════════════════════
def viz_dummy_trap():
    fig, ax = plt.subplots(figsize=(10.4, 4.6))
    ax.set_xlim(0, 12); ax.set_ylim(0, 7); ax.axis("off")
    ax.text(2.5, 6.5, "Naive one-hot (3 columns)", ha="center", fontsize=11.5,
            fontweight="bold", color="#0f172a")
    ax.text(9.5, 6.5, "drop='first' (2 columns)", ha="center", fontsize=11.5,
            fontweight="bold", color=GREEN)
    cols_full = ["proto_ICMP", "proto_TCP", "proto_UDP"]
    cols_drop = ["proto_TCP", "proto_UDP"]
    rows = [("TCP", (0,1,0)), ("UDP", (0,0,1)), ("ICMP", (1,0,0))]

    # left table
    for i, h in enumerate(cols_full):
        ax.add_patch(Rectangle((0.4 + i*1.6, 5.4), 1.5, 0.55, facecolor="#1e293b"))
        ax.text(0.4 + i*1.6 + 0.75, 5.67, h, ha="center", color="white", fontsize=8.6)
    for r, (label, vals) in enumerate(rows):
        y = 4.7 - r*0.7
        for i, v in enumerate(vals):
            cell_color = "#fee2e2" if (r == 2 and i == 0) else ("#dcfce7" if v == 1 else "white")
            ax.add_patch(Rectangle((0.4 + i*1.6, y), 1.5, 0.6,
                                   facecolor=cell_color, edgecolor=LIGHT))
            ax.text(0.4 + i*1.6 + 0.75, y+0.30, str(v), ha="center", va="center",
                    fontsize=11, family="monospace",
                    color="#0f172a", fontweight="bold")

    # right table (drop ICMP)
    for i, h in enumerate(cols_drop):
        ax.add_patch(Rectangle((7.6 + i*1.6, 5.4), 1.5, 0.55, facecolor="#1e293b"))
        ax.text(7.6 + i*1.6 + 0.75, 5.67, h, ha="center", color="white", fontsize=8.6)
    drop_rows = [("TCP", (1,0)), ("UDP", (0,1)), ("ICMP", (0,0))]
    for r, (label, vals) in enumerate(drop_rows):
        y = 4.7 - r*0.7
        for i, v in enumerate(vals):
            cell_color = "#dcfce7" if v == 1 else "white"
            ax.add_patch(Rectangle((7.6 + i*1.6, y), 1.5, 0.6,
                                   facecolor=cell_color, edgecolor=LIGHT))
            ax.text(7.6 + i*1.6 + 0.75, y+0.30, str(v), ha="center", va="center",
                    fontsize=11, family="monospace", color="#0f172a", fontweight="bold")
    # arrow
    arrow = FancyArrowPatch((5.4, 4.0), (7.3, 4.0), arrowstyle="-|>",
                            mutation_scale=20, linewidth=2.4, color=GREEN)
    ax.add_patch(arrow)
    ax.text(6.35, 4.4, "drop\nreference", ha="center", fontsize=9.2,
            color=GREEN, fontweight="bold")
    # caption
    ax.text(6.0, 1.0,
            "If proto_TCP=0 AND proto_UDP=0, the row must be ICMP — the third column "
            "carried no new information.\nKeeping all three causes perfect collinearity "
            "(the dummy variable trap).",
            ha="center", fontsize=10, color="#475569", style="italic")
    plt.savefig(OUT / "fe_dummy_trap.png", **SAVE); plt.close(fig)


# ══════════════════════════════════════════════════════════════════════════════
# 9. fe_encoding_accuracy — TASK 4 model comparison bar chart
# ══════════════════════════════════════════════════════════════════════════════
def viz_encoding_accuracy():
    # Reproduce the TASK 4 comparison from solution_categorical_encoding.py
    np.random.seed(42)
    nn = 200
    df = pd.DataFrame({
        'dst_port':   np.random.choice([80, 443, 22, 53, 3389], nn,
                                       p=[0.30, 0.30, 0.15, 0.15, 0.10]),
        'protocol':   np.random.choice(['TCP', 'UDP', 'ICMP'], nn, p=[0.7, 0.25, 0.05]),
        'bytes_sent': np.random.lognormal(7, 1.2, nn).astype(int).clip(100, 100000),
        'bytes_recv': np.random.lognormal(8, 1.5, nn).astype(int).clip(100, 500000),
        'packets':    np.random.poisson(40, nn).clip(1, 200),
        'duration':   np.random.exponential(15, nn).clip(0.05, 300),
    })
    df['label'] = ((df['bytes_sent'] > df['bytes_sent'].quantile(0.85)) &
                   (df['duration']   < df['duration'].quantile(0.30))).astype(int)
    le = LabelEncoder(); df['protocol_label'] = le.fit_transform(df['protocol'])
    ohe = OneHotEncoder(sparse_output=False, drop='first')
    enc = ohe.fit_transform(df[['protocol']])
    enc_df = pd.DataFrame(enc, columns=ohe.get_feature_names_out(['protocol']))
    base = ['bytes_sent', 'bytes_recv', 'packets', 'duration']
    yy = df['label']
    accs = {}
    for name, X in [('LabelEncoded', df[base + ['protocol_label']]),
                    ('OneHotEncoded', pd.concat([df[base], enc_df], axis=1))]:
        Xtr, Xte, ytr, yte = train_test_split(X, yy, test_size=0.2,
                                              random_state=42, stratify=yy)
        m = LogisticRegression(max_iter=500, random_state=42).fit(Xtr, ytr)
        accs[name] = accuracy_score(yte, m.predict(Xte))

    fig, ax = plt.subplots(figsize=(8.4, 4.2))
    names = list(accs.keys())
    vals  = [accs[k] for k in names]
    colours = [RED, GREEN]
    bars = ax.bar(names, vals, color=colours, edgecolor="white", linewidth=2)
    ax.set_ylim(0, 1.05); ax.set_ylabel("test-set accuracy")
    ax.set_title("Same model, same features, only the encoding differs")
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width()/2, v + 0.02, f"{v:.3f}",
                ha="center", fontsize=12, fontweight="bold")
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    diff = accs['OneHotEncoded'] - accs['LabelEncoded']
    ax.text(0.5, -0.18, f"Δ accuracy = {diff:+.3f}  (one-hot wins for linear models)",
            ha="center", transform=ax.transAxes, fontsize=10.5,
            color=GREEN if diff > 0 else RED, fontweight="bold")
    plt.savefig(OUT / "fe_encoding_accuracy.png", **SAVE); plt.close(fig)
    return accs


# ══════════════════════════════════════════════════════════════════════════════
# 10. fe_scaler_compare — StandardScaler vs MinMaxScaler with outlier
# ══════════════════════════════════════════════════════════════════════════════
def viz_scaler_compare():
    bps = raw_df[['bytes_per_second']].values
    ss = StandardScaler();  bps_s = ss.fit_transform(bps).flatten()
    mm = MinMaxScaler();    bps_m = mm.fit_transform(bps).flatten()

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12.0, 4.0))
    ax1.hist(bps.flatten(), bins=30, color=GREY, edgecolor="white")
    ax1.set_title("Raw bytes_per_second")
    ax1.set_xlabel("B/s")
    ax1.spines["top"].set_visible(False); ax1.spines["right"].set_visible(False)
    ax1.text(0.95, 0.95,
             f"max = {bps.max():,.0f}\n(extreme outlier)",
             transform=ax1.transAxes, ha="right", va="top",
             fontsize=9, color=RED, family="monospace",
             bbox=dict(facecolor="white", edgecolor=RED, boxstyle="round,pad=0.3"))

    ax2.hist(bps_s, bins=30, color=ACCENT, edgecolor="white")
    ax2.set_title("StandardScaler  (x − μ)/σ")
    ax2.set_xlabel("z-score")
    ax2.axvline(0, linestyle="--", color=GREY, linewidth=1)
    ax2.spines["top"].set_visible(False); ax2.spines["right"].set_visible(False)
    ax2.text(0.95, 0.95,
             f"range\n[{bps_s.min():.1f}, {bps_s.max():.1f}]\nmedian {np.median(bps_s):+.2f}",
             transform=ax2.transAxes, ha="right", va="top",
             fontsize=9, color=ACCENT, family="monospace",
             bbox=dict(facecolor="white", edgecolor=ACCENT, boxstyle="round,pad=0.3"))

    ax3.hist(bps_m, bins=30, color=ORANGE, edgecolor="white")
    ax3.set_title("MinMaxScaler  (x − min)/(max − min)")
    ax3.set_xlabel("scaled to [0, 1]")
    ax3.spines["top"].set_visible(False); ax3.spines["right"].set_visible(False)
    ax3.text(0.95, 0.95,
             f"range\n[{bps_m.min():.2f}, {bps_m.max():.2f}]\nmedian {np.median(bps_m):.3f}\n← squashed!",
             transform=ax3.transAxes, ha="right", va="top",
             fontsize=9, color=ORANGE, family="monospace",
             bbox=dict(facecolor="white", edgecolor=ORANGE, boxstyle="round,pad=0.3"))
    plt.tight_layout()
    plt.savefig(OUT / "fe_scaler_compare.png", **SAVE); plt.close(fig)
    return float(np.median(bps_m)), float(bps_m.max())


# ══════════════════════════════════════════════════════════════════════════════
# 11. fe_scaler_leakage — fit-on-train vs fit-on-all
# ══════════════════════════════════════════════════════════════════════════════
def viz_scaler_leakage():
    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.6))

    # ── Correct flow
    ax = axes[0]
    ax.set_xlim(0, 10); ax.set_ylim(0, 7); ax.axis("off")
    ax.text(5, 6.5, "Correct: fit on TRAIN, transform BOTH",
            ha="center", fontsize=12, fontweight="bold", color=GREEN)
    card(ax, 0.4, 4.0, 2.2, 1.4, "X_train", fill="#dcfce7", edge=GREEN)
    card(ax, 0.4, 1.6, 2.2, 1.4, "X_test",  fill="#fef3c7", edge=ORANGE)
    card(ax, 4.0, 2.8, 2.4, 1.6, "scaler.fit\n(learns μ, σ)",
         fill="white", edge=ACCENT, fc_label=ACCENT)
    card(ax, 7.5, 4.0, 2.2, 1.4, "scaled train", fill="#dcfce7", edge=GREEN)
    card(ax, 7.5, 1.6, 2.2, 1.4, "scaled test",  fill="#fef3c7", edge=ORANGE)
    for x0, x1, y0, y1, c in [(2.6, 4.0, 4.7, 3.6, GREEN),
                              (2.6, 4.0, 2.3, 3.6, ORANGE),
                              (6.4, 7.5, 3.6, 4.7, GREEN),
                              (6.4, 7.5, 3.6, 2.3, ORANGE)]:
        ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>",
                                     mutation_scale=14, color=c, linewidth=1.6))
    ax.text(5, 0.6, "test stats stay hidden until prediction time",
            ha="center", fontsize=9.5, color="#475569", style="italic")

    # ── Wrong flow
    ax = axes[1]
    ax.set_xlim(0, 10); ax.set_ylim(0, 7); ax.axis("off")
    ax.text(5, 6.5, "Wrong: fit on EVERYTHING (data leakage)",
            ha="center", fontsize=12, fontweight="bold", color=RED)
    card(ax, 0.4, 4.0, 2.2, 1.4, "X_train", fill="#dcfce7", edge=GREEN)
    card(ax, 0.4, 1.6, 2.2, 1.4, "X_test",  fill="#fef3c7", edge=ORANGE)
    card(ax, 4.0, 2.8, 2.4, 1.6, "scaler.fit\non train+test",
         fill="#fee2e2", edge=RED, fc_label=RED)
    card(ax, 7.5, 4.0, 2.2, 1.4, "scaled train", fill="#dcfce7", edge=GREEN)
    card(ax, 7.5, 1.6, 2.2, 1.4, "scaled test",  fill="#fef3c7", edge=ORANGE)
    for x0, x1, y0, y1 in [(2.6, 4.0, 4.7, 3.6), (2.6, 4.0, 2.3, 3.6),
                            (6.4, 7.5, 3.6, 4.7), (6.4, 7.5, 3.6, 2.3)]:
        ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>",
                                     mutation_scale=14, color=RED, linewidth=1.6))
    ax.text(5, 0.6, "test set leaks its mean/std into the scaler — optimistic scores",
            ha="center", fontsize=9.5, color=RED, style="italic")
    plt.tight_layout()
    plt.savefig(OUT / "fe_scaler_leakage.png", **SAVE); plt.close(fig)


# ══════════════════════════════════════════════════════════════════════════════
# 12. fe_pipeline_flow — sklearn Pipeline diagram
# ══════════════════════════════════════════════════════════════════════════════
def viz_pipeline_flow():
    fig, ax = plt.subplots(figsize=(10.6, 3.6))
    ax.set_xlim(0, 12); ax.set_ylim(0, 5); ax.axis("off")
    # title
    ax.text(6, 4.5, "Pipeline([('scaler', StandardScaler()), ('model', LogisticRegression())])",
            ha="center", fontsize=10.5, family="monospace", color="#0f172a")
    # boxes
    card(ax, 0.4, 1.4, 2.4, 1.8, "raw X_train", fill="#dcfce7", edge=GREEN)
    card(ax, 3.4, 1.4, 2.6, 1.8, "scaler.fit\n_transform",
         fill="#ecfeff", edge=ACCENT, fc_label=ACCENT)
    card(ax, 6.6, 1.4, 2.6, 1.8, "model.fit",
         fill="#f3e8ff", edge=VIOLET, fc_label=VIOLET)
    card(ax, 9.8, 1.4, 1.8, 1.8, "trained\npipeline",
         fill="#0f172a", edge="#0f172a", fc_label="white")
    for x0, x1 in [(2.8, 3.4), (6.0, 6.6), (9.2, 9.8)]:
        ax.add_patch(FancyArrowPatch((x0, 2.3), (x1, 2.3), arrowstyle="-|>",
                                     mutation_scale=18, color=GREY, linewidth=1.8))
    ax.text(6, 0.3,
            ".fit() automatically learns the scaler from train, then "
            ".predict() applies transform-only to new data — leakage impossible.",
            ha="center", fontsize=10, color="#475569", style="italic")
    plt.savefig(OUT / "fe_pipeline_flow.png", **SAVE); plt.close(fig)


# ── Run everything ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Generating Stage 2.1 Feature Engineering visuals...")
    viz_raw_log_dtypes();      print("  ✓ fe_raw_log_dtypes.png")
    viz_sklearn_rejects();     print("  ✓ fe_sklearn_rejects.png")
    viz_transformation_plan(); print("  ✓ fe_transformation_plan.png")
    viz_derived_features();    print("  ✓ fe_derived_features.png")
    viz_port_risk_table();     print("  ✓ fe_port_risk_table.png")
    viz_business_hours();      print("  ✓ fe_business_hours.png")
    viz_label_vs_onehot();     print("  ✓ fe_label_vs_onehot.png")
    viz_dummy_trap();          print("  ✓ fe_dummy_trap.png")
    accs = viz_encoding_accuracy(); print(f"  ✓ fe_encoding_accuracy.png  {accs}")
    sm = viz_scaler_compare(); print(f"  ✓ fe_scaler_compare.png  median/MM={sm}")
    viz_scaler_leakage();      print("  ✓ fe_scaler_leakage.png")
    viz_pipeline_flow();       print("  ✓ fe_pipeline_flow.png")
    print("Done.")
