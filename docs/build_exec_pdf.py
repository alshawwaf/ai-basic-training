"""Render the AI Ninja Program executive deck as a slide-style PDF.

Uses reportlab directly (no LibreOffice dependency) so the build is reproducible
on any machine with the repo's Python deps. Each "slide" is one landscape 16:9 page.

Output: docs/AI-Ninja-Program-Exec-Deck.pdf
"""

from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "docs" / "AI-Ninja-Program-Exec-Deck.pdf"

# 16:9 landscape, matches the PPTX (13.33 × 7.5 in)
PAGE_W, PAGE_H = 13.333 * inch, 7.5 * inch

# Brand palette (mirrors portal CSS vars)
CYAN   = HexColor("#06d6e0")
VIOLET = HexColor("#a855f7")
ORANGE = HexColor("#f59e0b")
DARK   = HexColor("#0b1120")
INK    = HexColor("#1f2937")
GREY   = HexColor("#475569")
DIM    = HexColor("#94a3b8")
PANEL  = HexColor("#f8fafc")
LINE   = HexColor("#e2e8f0")


# ---------- helpers ----------

def draw_chrome(c, slide_num, total):
    """Top accent bar + slide footer with brand."""
    # Top gradient bar (faked with three solid stripes)
    c.setFillColor(CYAN)
    c.rect(0, PAGE_H - 0.18 * inch, PAGE_W * 0.45, 0.18 * inch, fill=1, stroke=0)
    c.setFillColor(VIOLET)
    c.rect(PAGE_W * 0.45, PAGE_H - 0.18 * inch, PAGE_W * 0.40, 0.18 * inch, fill=1, stroke=0)
    c.setFillColor(ORANGE)
    c.rect(PAGE_W * 0.85, PAGE_H - 0.18 * inch, PAGE_W * 0.15, 0.18 * inch, fill=1, stroke=0)

    # Footer
    c.setFillColor(DIM)
    c.setFont("Helvetica", 8)
    c.drawString(0.6 * inch, 0.35 * inch, "AI Ninja Program  ·  Executive Proposal")
    c.drawRightString(PAGE_W - 0.6 * inch, 0.35 * inch, f"{slide_num} / {total}")


def title_block(c, title, subtitle=None, y=PAGE_H - 1.0 * inch):
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 26)
    c.drawString(0.7 * inch, y, title)
    if subtitle:
        c.setFillColor(GREY)
        c.setFont("Helvetica", 13)
        c.drawString(0.7 * inch, y - 0.32 * inch, subtitle)
    # Underline accent
    c.setStrokeColor(CYAN)
    c.setLineWidth(2)
    c.line(0.7 * inch, y - 0.55 * inch, 2.2 * inch, y - 0.55 * inch)


def bullet_lines(c, items, x=0.8 * inch, y=PAGE_H - 2.2 * inch, line_h=0.42 * inch,
                 max_width=PAGE_W - 1.6 * inch):
    """Draw a list of bullet items. Each item is (text, level, optional_color)."""
    from reportlab.pdfbase.pdfmetrics import stringWidth

    for item in items:
        if isinstance(item, tuple):
            text, level = item[0], item[1]
            color = item[2] if len(item) > 2 else INK
        else:
            text, level, color = item, 0, INK

        if not text:
            y -= line_h * 0.4
            continue

        indent = level * 0.35 * inch
        bullet_x = x + indent
        text_x = bullet_x + 0.22 * inch

        if level == 0:
            c.setFillColor(CYAN)
            c.circle(bullet_x + 0.06 * inch, y + 0.06 * inch, 0.055 * inch, fill=1, stroke=0)
            c.setFont("Helvetica-Bold", 14)
        else:
            c.setFillColor(VIOLET)
            c.rect(bullet_x + 0.02 * inch, y + 0.04 * inch, 0.10 * inch, 0.10 * inch, fill=1, stroke=0)
            c.setFont("Helvetica", 13)

        c.setFillColor(color)
        # Word-wrap manually
        words = text.split()
        current = ""
        first_line = True
        for w in words:
            trial = (current + " " + w).strip()
            if stringWidth(trial, c._fontname, c._fontsize) > max_width - indent - 0.4 * inch:
                c.drawString(text_x if first_line else text_x, y, current)
                first_line = False
                y -= line_h
                current = w
            else:
                current = trial
        if current:
            c.drawString(text_x, y, current)
        y -= line_h
    return y


def draw_table(c, headers, rows, x, y, col_widths, header_color=VIOLET,
               header_text=white, body_text=INK, row_h=0.5 * inch, header_h=0.45 * inch):
    """Manual brand-styled table."""
    total_w = sum(col_widths)

    # Header row
    c.setFillColor(header_color)
    c.rect(x, y - header_h, total_w, header_h, fill=1, stroke=0)
    c.setFillColor(header_text)
    c.setFont("Helvetica-Bold", 12)
    cx = x
    for h, w in zip(headers, col_widths):
        c.drawString(cx + 0.12 * inch, y - header_h + 0.14 * inch, h)
        cx += w

    # Body rows
    cy = y - header_h
    for r_idx, row in enumerate(rows):
        cy_top = cy
        cy -= row_h
        if r_idx % 2 == 0:
            c.setFillColor(PANEL)
            c.rect(x, cy, total_w, row_h, fill=1, stroke=0)
        c.setStrokeColor(LINE)
        c.setLineWidth(0.5)
        c.line(x, cy, x + total_w, cy)

        c.setFillColor(body_text)
        cx = x
        for col_idx, (val, w) in enumerate(zip(row, col_widths)):
            font = "Helvetica-Bold" if col_idx == 0 else "Helvetica"
            c.setFont(font, 11)
            # Wrap text within cell
            from reportlab.pdfbase.pdfmetrics import stringWidth
            words = val.split()
            line = ""
            text_y = cy + row_h - 0.22 * inch
            for w_word in words:
                trial = (line + " " + w_word).strip()
                if stringWidth(trial, font, 11) > w - 0.24 * inch:
                    c.drawString(cx + 0.12 * inch, text_y, line)
                    line = w_word
                    text_y -= 0.18 * inch
                else:
                    line = trial
            if line:
                c.drawString(cx + 0.12 * inch, text_y, line)
            cx += w

    # Outer border
    c.setStrokeColor(LINE)
    c.setLineWidth(0.7)
    c.rect(x, cy, total_w, y - cy, fill=0, stroke=1)
    return cy


# ---------- slides ----------

def slide_title(c, total):
    # Big centered title slide with brand background tint
    c.setFillColor(DARK)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    # Cyan→violet stripe behind title
    c.setFillColor(CYAN)
    c.rect(0.7 * inch, PAGE_H * 0.55, 0.12 * inch, PAGE_H * 0.25, fill=1, stroke=0)

    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 48)
    c.drawString(1.0 * inch, PAGE_H * 0.62, "AI Ninja Program")

    c.setFillColor(CYAN)
    c.setFont("Helvetica", 20)
    c.drawString(1.0 * inch, PAGE_H * 0.55, "Building deep AI/ML capability across our Security Engineering team")

    c.setFillColor(DIM)
    c.setFont("Helvetica", 13)
    c.drawString(1.0 * inch, PAGE_H * 0.35, "Presented by  Khalid Alshawwaf")
    c.drawString(1.0 * inch, PAGE_H * 0.30, "For  Head of Security Engineering")
    c.drawString(1.0 * inch, PAGE_H * 0.25, "Duration  ~7 minutes + Q&A")

    # Bottom accent line
    c.setStrokeColor(VIOLET)
    c.setLineWidth(3)
    c.line(0.7 * inch, 0.9 * inch, 4.0 * inch, 0.9 * inch)

    # Footer (light variant for dark slide)
    c.setFillColor(DIM)
    c.setFont("Helvetica", 8)
    c.drawString(0.7 * inch, 0.45 * inch, "AI Ninja Program  ·  Executive Proposal")
    c.drawRightString(PAGE_W - 0.7 * inch, 0.45 * inch, f"1 / {total}")
    c.showPage()


def slide_problem(c, total):
    draw_chrome(c, 2, total)
    title_block(c, "Every customer conversation now has AI in it",
                "The gap is not awareness — it's technical depth.")
    bullet_lines(c, [
        "Vendors pitching \"AI-powered EDR\" and \"ML-driven threat detection\"",
        "CISOs asking us to evaluate their LLM and RAG use cases",
        "Competitors claiming their anomaly detection is \"machine learning\"",
        "Customers expecting us to engage on AI as peers, not observers",
        "",
        ("Our engineers are world-class at firewalls, SIEM, and EDR.", 0, INK),
        ("The AI layer is increasingly the part that decides who wins the deal.", 0, VIOLET),
    ])
    c.showPage()


def slide_proposal(c, total):
    draw_chrome(c, 3, total)
    title_block(c, "A 15-week internal training program",
                "Takes a security engineer with zero ML background to fluent practitioner")
    bullet_lines(c, [
        ("Explain  AI/ML to a customer in plain language", 0),
        ("Evaluate  vendor AI claims with technical credibility", 0),
        ("Build  working ML classifiers for security use cases", 0),
        ("Critique  neural network architectures", 0),
        ("Demo  a live AI-powered security assistant", 0),
        ("Position  Check Point AI Security products with technical authority", 0),
        "",
        ("Operating principle: people learn AI by manipulating it, not reading about it.", 0, VIOLET),
    ], y=PAGE_H - 2.0 * inch, line_h=0.45 * inch)
    c.showPage()


def slide_structure(c, total):
    draw_chrome(c, 4, total)
    title_block(c, "21 lessons  ·  5 stages  ·  3 progressive certification tiers")

    headers = ["Tier", "Weeks", "What graduates can do"]
    rows = [
        ("Tier 1 — AI Foundations", "1–7",
         "Hold credible AI conversations with customers; evaluate vendor claims"),
        ("Tier 2 — AI Practitioner", "8–10",
         "Prototype neural networks; assess AI solution architectures"),
        ("Tier 3 — AI Ninja", "11–15",
         "Build AI-powered security tools; lead AI engagements end-to-end"),
    ]
    col_widths = [3.0 * inch, 1.2 * inch, 7.9 * inch]
    end_y = draw_table(c, headers, rows, 0.7 * inch, PAGE_H - 2.1 * inch, col_widths,
                       row_h=0.65 * inch)

    # Stage progression footer
    c.setFillColor(GREY)
    c.setFont("Helvetica-Oblique", 12)
    c.drawString(0.7 * inch, end_y - 0.5 * inch,
                 "5 stages: AI Positioning  →  Classic ML  →  Intermediate ML  →  "
                 "Neural Networks  →  Generative AI / RAG  →  Applied Check Point AI")
    c.showPage()


def slide_why(c, total):
    draw_chrome(c, 5, total)
    title_block(c, "Three things that separate this from a Coursera playlist")
    bullet_lines(c, [
        ("1. Graded assessment gates between stages", 0),
        ("Quiz · mini-project · architecture review · live capstone demo", 1),
        ("People can't just run solution files and graduate — they have to demonstrate understanding", 1),
        ("2. Real security data, not toy datasets", 0),
        ("Real CVEs · real phishing URLs · MITRE ATT&CK · packet captures", 1),
        ("Capstones use data graduates could demo to a customer the next day", 1),
        ("3. Every Ninja graduate ships a portable demo", 0),
        ("Laptop-ready RAG security assistant + 5-minute customer-facing script", 1),
        ("The deliverable is not a certificate — it's a sales tool", 1),
    ], y=PAGE_H - 1.9 * inch, line_h=0.38 * inch)
    c.showPage()


def slide_ask(c, total):
    draw_chrome(c, 6, total)
    title_block(c, "Four things I'm asking for")

    headers = ["#", "Ask", "What it costs"]
    rows = [
        ("1", "Endorsement to recruit a pilot cohort",
              "Your name on the program announcement"),
        ("2", "Time allocation: 5–8 hrs/week per participant for 15 weeks",
              "~12–16 engineers across the Americas"),
        ("3", "Sponsorship so participation reads as career investment",
              "One internal email + visible support"),
        ("4", "Review panel seat for the final capstone presentations",
              "~2 hours at week 15, you + 2–3 stakeholders"),
    ]
    col_widths = [0.6 * inch, 6.5 * inch, 5.0 * inch]
    end_y = draw_table(c, headers, rows, 0.7 * inch, PAGE_H - 2.0 * inch, col_widths,
                       header_color=CYAN, header_text=DARK, row_h=0.75 * inch)

    c.setFillColor(VIOLET)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(0.7 * inch, end_y - 0.5 * inch,
                 "No external budget required. Curriculum is built. Portal is built. Materials are tested.")
    c.showPage()


def slide_success(c, total):
    draw_chrome(c, 7, total)
    title_block(c, "What success looks like in 15 weeks")
    bullet_lines(c, [
        "12–16 certified engineers who can hold technical AI conversations with any customer in the Americas",
        "Each graduate carries a working AI security demo on their laptop, ready for customer meetings",
        "A repeatable curriculum ready for the next cohort with minimal setup",
        "Clear visibility into Tier 1 (sales-ready), Tier 2 (architecture-ready), Tier 3 (build-ready) capability",
    ], y=PAGE_H - 2.0 * inch, line_h=0.55 * inch)

    # Bottom callout
    c.setFillColor(PANEL)
    c.rect(0.7 * inch, 1.0 * inch, PAGE_W - 1.4 * inch, 1.4 * inch, fill=1, stroke=0)
    c.setStrokeColor(CYAN)
    c.setLineWidth(3)
    c.line(0.7 * inch, 2.4 * inch, PAGE_W - 0.7 * inch, 2.4 * inch)

    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(0.95 * inch, 2.0 * inch, "The customers we sell to are judging us on AI fluency.")
    c.setFillColor(GREY)
    c.setFont("Helvetica", 12)
    c.drawString(0.95 * inch, 1.65 * inch,
                 "This is the lowest-risk, highest-leverage way to build that fluency across the team —")
    c.drawString(0.95 * inch, 1.42 * inch,
                 "using internal time, internal expertise, and a curriculum that's already built.")
    c.showPage()


def slide_close(c, total):
    c.setFillColor(DARK)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 38)
    c.drawString(1.0 * inch, PAGE_H * 0.58, "Want to see the portal?")

    c.setFillColor(CYAN)
    c.setFont("Helvetica", 18)
    c.drawString(1.0 * inch, PAGE_H * 0.48, "20 minutes, in person.")
    c.setFillColor(DIM)
    c.setFont("Helvetica", 14)
    c.drawString(1.0 * inch, PAGE_H * 0.41,
                 "I'll walk you through the labs, the interactive lessons, and one capstone deliverable.")

    c.setStrokeColor(VIOLET)
    c.setLineWidth(3)
    c.line(1.0 * inch, PAGE_H * 0.35, 4.5 * inch, PAGE_H * 0.35)

    c.setFillColor(DIM)
    c.setFont("Helvetica", 11)
    c.drawString(1.0 * inch, PAGE_H * 0.18, "Khalid Alshawwaf  ·  AI Ninja Program")

    c.setFillColor(DIM)
    c.setFont("Helvetica", 8)
    c.drawString(0.7 * inch, 0.45 * inch, "AI Ninja Program  ·  Executive Proposal")
    c.drawRightString(PAGE_W - 0.7 * inch, 0.45 * inch, f"{total} / {total}")
    c.showPage()


# ---------- entry ----------

def build():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUTPUT), pagesize=(PAGE_W, PAGE_H))
    c.setTitle("AI Ninja Program — Executive Proposal")
    c.setAuthor("Khalid Alshawwaf")
    c.setSubject("Internal training program proposal")

    total = 8
    slide_title(c, total)
    slide_problem(c, total)
    slide_proposal(c, total)
    slide_structure(c, total)
    slide_why(c, total)
    slide_ask(c, total)
    slide_success(c, total)
    slide_close(c, total)

    c.save()
    print(f"Wrote {OUTPUT}")
    print(f"Pages: {total}")


if __name__ == "__main__":
    build()
