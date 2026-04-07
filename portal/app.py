"""
AI Ninja Program — Training Portal

Run:   python portal/app.py
Open:  http://localhost:5000
"""

import importlib
import json
import os
import secrets
import warnings
from hmac import compare_digest

import markdown
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    abort,
    redirect,
    url_for,
    session,
    Response,
    stream_with_context,
    send_from_directory,
)
from config import STAGES, get_all_lessons, get_lesson
from runner import run_script, run_script_stream

warnings.filterwarnings("ignore")

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024  # 1 MB max request size

# Session signing key. Use PORTAL_SECRET_KEY if set so /admin sessions
# survive a restart; otherwise mint a per-process random key (logs you
# out on every restart, but the portal still works without configuration).
app.secret_key = os.environ.get("PORTAL_SECRET_KEY") or secrets.token_hex(32)
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"


@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdn.jsdelivr.net; "
        "font-src 'self' https://fonts.gstatic.com; "
        "img-src 'self' data:; "
        "connect-src 'self'"
    )
    return response

# ── Auto-discover and register lesson Blueprints ────────────────────────────

registered_lessons = []

for stage in STAGES:
    for lesson in stage["lessons"]:
        if not lesson.get("has_app"):
            continue
        folder = lesson["folder"]
        try:
            mod = importlib.import_module(f"lessons.{folder}")
            bp = getattr(mod, "bp", None)
            if bp:
                app.register_blueprint(bp, url_prefix=f"/lesson/{lesson['id']}")
                registered_lessons.append(lesson["id"])
        except Exception as e:
            print(f"  [!] Could not load lesson {folder}: {e}")


# ── Portal routes ───────────────────────────────────────────────────────────

@app.route("/")
def home():
    return render_template("home.html", stages=STAGES, registered=registered_lessons)


@app.route("/lesson/<lesson_id>/")
def lesson_placeholder(lesson_id):
    """Placeholder page for lessons not yet built (demo mode)."""
    if lesson_id in registered_lessons:
        # Blueprint handles this — redirect just in case
        return render_template("home.html", stages=STAGES, registered=registered_lessons)
    lesson = get_lesson(lesson_id)
    if not lesson:
        return "Not found", 404
    return render_template("lesson_placeholder.html", lesson=lesson)


@app.route("/stage/<stage_id>")
def stage_view(stage_id):
    stage = next((s for s in STAGES if s["id"] == stage_id), None)
    if not stage:
        return "Stage not found", 404
    return render_template("stage.html", stage=stage, stages=STAGES, registered=registered_lessons)


# ── Admin console (login-gated) ─────────────────────────────────────────────

DOCS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docs"))
PROPOSAL_FILES = {
    "pdf":  ("AI-Ninja-Program-Exec-Deck.pdf",  "application/pdf"),
    "pptx": ("AI-Ninja-Program-Exec-Deck.pptx",
             "application/vnd.openxmlformats-officedocument.presentationml.presentation"),
}

# Admin password. Set PORTAL_ADMIN_PASSWORD in your environment for a real
# secret; falls back to a known default so the portal still works out of
# the box on a fresh checkout.
ADMIN_PASSWORD = os.environ.get("PORTAL_ADMIN_PASSWORD", "ninja")
if ADMIN_PASSWORD == "ninja":
    print(
        "  [admin] Using default admin password 'ninja'. "
        "Set PORTAL_ADMIN_PASSWORD env var to override."
    )


def _is_admin():
    """True iff the current session has been authenticated as admin."""
    return bool(session.get("is_admin"))


def _require_admin():
    """Redirect to the admin login page if the session isn't authenticated."""
    if not _is_admin():
        # Remember where the user was trying to go so we can bounce them
        # back after a successful login.
        return redirect(url_for("admin_login", next=request.path))
    return None


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    """Single-password login form for the admin console."""
    error = None
    if request.method == "POST":
        password = request.form.get("password", "")
        # compare_digest avoids leaking length / first-mismatch timing.
        if compare_digest(password, ADMIN_PASSWORD):
            session["is_admin"] = True
            session.permanent = False
            target = request.form.get("next") or url_for("admin_console")
            # Refuse open redirects — only allow same-site relative paths.
            if not target.startswith("/") or target.startswith("//"):
                target = url_for("admin_console")
            return redirect(target)
        error = "Incorrect password."
    next_url = request.args.get("next", "")
    return render_template("admin_login.html", error=error, next_url=next_url)


@app.route("/admin/logout", methods=["POST", "GET"])
def admin_logout():
    """Drop the admin session and bounce back to the public home."""
    session.pop("is_admin", None)
    return redirect(url_for("home"))


@app.route("/admin")
def admin_console():
    """Instructor-only console. Login-gated via session cookie."""
    redirect_response = _require_admin()
    if redirect_response is not None:
        return redirect_response
    return render_template("admin.html")


@app.route("/proposal.<fmt>")
def download_proposal(fmt):
    """Serve the AI Ninja Program executive proposal as PDF or PPTX.

    Login-gated — only reachable once you've authenticated at /admin/login.
    """
    redirect_response = _require_admin()
    if redirect_response is not None:
        return redirect_response
    fmt = fmt.lower()
    if fmt not in PROPOSAL_FILES:
        abort(404)
    filename, mimetype = PROPOSAL_FILES[fmt]
    if not os.path.exists(os.path.join(DOCS_DIR, filename)):
        abort(404)
    return send_from_directory(
        DOCS_DIR, filename,
        mimetype=mimetype,
        as_attachment=True,
        download_name=filename,
    )


# ── Content API (serve markdown / Python files) ────────────────────────────

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

MD_EXTENSIONS = ["fenced_code", "tables", "toc", "nl2br", "sane_lists"]


@app.route("/api/content")
def api_content():
    """Return rendered markdown or raw source for a file in the repo."""
    rel_path = request.args.get("path", "")
    if not rel_path:
        abort(400, "Missing path parameter")

    # Security: prevent path traversal
    full = os.path.normpath(os.path.join(REPO_ROOT, rel_path))
    if not full.startswith(REPO_ROOT):
        abort(403, "Access denied")

    if not os.path.isfile(full):
        abort(404, "File not found")

    ext = os.path.splitext(full)[1].lower()
    if ext not in (".md", ".py"):
        abort(403, "Only .md and .py files are served")

    with open(full, encoding="utf-8") as f:
        raw = f.read()

    if ext == ".md":
        html = markdown.markdown(raw, extensions=MD_EXTENSIONS)
        return jsonify({"type": "markdown", "html": html, "raw": raw, "path": rel_path})
    else:
        return jsonify({"type": "python", "raw": raw, "path": rel_path})


# ── PDF generation API ──────────────────────────────────────────────────────

# Pure-Python PDF generator. Doesn't need GTK/Pango/Cairo system libs the way
# WeasyPrint does, so it works on Windows out of a plain `pip install`.
# Trade-off: less complete CSS support (no flexbox, no gradients) — fine for
# rendered markdown which is mostly headings, paragraphs, tables, code blocks.
try:
    from xhtml2pdf import pisa
    _PDF_AVAILABLE = True
except Exception:
    _PDF_AVAILABLE = False


PDF_STYLE = """
<style>
    @page { size: A4; margin: 18mm 16mm; }
    body { font-family: Helvetica, Arial, sans-serif; color: #1a1a2e; font-size: 11pt; line-height: 1.5; }
    h1 { font-size: 20pt; color: #06b6d4; margin: 0 0 8pt; -pdf-keep-with-next: true; }
    h2 { font-size: 15pt; color: #0e7490; margin: 14pt 0 6pt; border-bottom: 1pt solid #e2e8f0; padding-bottom: 3pt; -pdf-keep-with-next: true; }
    h3 { font-size: 12pt; color: #334155; margin: 10pt 0 4pt; -pdf-keep-with-next: true; }
    h4 { font-size: 11pt; color: #475569; margin: 8pt 0 3pt; -pdf-keep-with-next: true; }
    p { margin: 6pt 0; }
    ul, ol { margin: 6pt 0 6pt 18pt; }
    li { margin: 2pt 0; }
    a { color: #0891b2; text-decoration: none; }
    code { background: #f1f5f9; font-family: Courier, monospace; font-size: 9.5pt; padding: 1pt 3pt; }
    pre { background: #f1f5f9; padding: 8pt 10pt; font-family: Courier, monospace; font-size: 9pt; -pdf-keep-in-frame-mode: shrink; }
    pre code { background: transparent; padding: 0; }
    table { border-collapse: collapse; width: 100%; margin: 8pt 0; -pdf-keep-in-frame-mode: shrink; }
    th { background: #e2e8f0; font-weight: bold; border: 1pt solid #94a3b8; padding: 4pt 6pt; text-align: left; }
    td { border: 1pt solid #cbd5e1; padding: 4pt 6pt; vertical-align: top; }
    blockquote { margin: 8pt 0 8pt 12pt; padding-left: 10pt; border-left: 3pt solid #06b6d4; color: #475569; }
    hr { border: 0; border-top: 1pt solid #e2e8f0; margin: 12pt 0; }
    .pdf-header { border-bottom: 2pt solid #06b6d4; padding-bottom: 6pt; margin-bottom: 12pt; }
    .pdf-header .pdf-title { font-size: 18pt; font-weight: bold; color: #0e7490; }
    .pdf-header .pdf-subtitle { font-size: 9pt; color: #64748b; margin-top: 2pt; }
    .pdf-footer { font-size: 8pt; color: #94a3b8; text-align: center; margin-top: 14pt; padding-top: 6pt; border-top: 1pt solid #e2e8f0; }
</style>
"""


@app.route("/api/pdf")
def api_pdf():
    """Render a markdown file in the repo to a PDF and return it as a download."""
    if not _PDF_AVAILABLE:
        return jsonify({
            "error": "PDF generator not installed. Run: pip install xhtml2pdf"
        }), 503

    rel_path = request.args.get("path", "")
    title = request.args.get("title", "")
    if not rel_path:
        return jsonify({"error": "Missing path parameter"}), 400

    # Security: prevent path traversal — same model as /api/content
    full = os.path.normpath(os.path.join(REPO_ROOT, rel_path))
    if not full.startswith(REPO_ROOT):
        return jsonify({"error": "Access denied"}), 403
    if not os.path.isfile(full):
        return jsonify({"error": "File not found"}), 404
    if not full.lower().endswith(".md"):
        return jsonify({"error": "Only .md files can be exported to PDF"}), 403

    with open(full, encoding="utf-8") as f:
        raw = f.read()

    # xhtml2pdf's default fonts (Helvetica/Times) don't carry the typographic
    # punctuation that markdown source files use heavily, so we normalize a
    # small set of common code-points to ASCII equivalents before rendering.
    # The text reads identically; we just lose decorative glyphs.
    _PDF_CHAR_MAP = {
        "\u2014": "--",   # em-dash
        "\u2013": "-",    # en-dash
        "\u2018": "'",    # left single quote
        "\u2019": "'",    # right single quote
        "\u201c": '"',    # left double quote
        "\u201d": '"',    # right double quote
        "\u2026": "...",  # ellipsis
        "\u2192": "->",   # rightwards arrow
        "\u2190": "<-",   # leftwards arrow
        "\u2022": "*",    # bullet
        "\u00a0": " ",    # non-breaking space
        "\u00d7": "x",    # multiplication sign
        "\u2248": "~=",   # almost equal
        "\u2265": ">=",   # >=
        "\u2264": "<=",   # <=
    }
    for src, dst in _PDF_CHAR_MAP.items():
        raw = raw.replace(src, dst)

    body_html = markdown.markdown(raw, extensions=MD_EXTENSIONS)
    display_title = title or os.path.basename(full)
    for src, dst in _PDF_CHAR_MAP.items():
        display_title = display_title.replace(src, dst)

    full_html = (
        '<!DOCTYPE html><html><head><meta charset="UTF-8">'
        f'<title>{display_title}</title>'
        f'{PDF_STYLE}</head><body>'
        f'<div class="pdf-header"><div class="pdf-title">{display_title}</div>'
        f'<div class="pdf-subtitle">AI Ninja Program -- {rel_path}</div></div>'
        f'{body_html}'
        '<div class="pdf-footer">Generated by AI Ninja Program</div>'
        '</body></html>'
    )

    import io
    buf = io.BytesIO()
    result = pisa.CreatePDF(src=full_html, dest=buf, encoding="utf-8")
    if result.err:
        return jsonify({"error": "PDF rendering failed"}), 500

    pdf_bytes = buf.getvalue()
    download_name = os.path.splitext(os.path.basename(full))[0] + ".pdf"
    return Response(
        pdf_bytes,
        mimetype="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{download_name}"',
            "Content-Length": str(len(pdf_bytes)),
        },
    )


# ── Script execution API ─────────────────────────────────────────────────────

@app.route("/api/run", methods=["POST"])
def api_run():
    """Execute a Python script and return stdout + matplotlib figures."""
    data = request.get_json(silent=True) or {}
    rel_path = data.get("path", "")
    if not rel_path:
        return jsonify({"error": "Missing path"}), 400

    # Only allow solution_*.py files under curriculum/
    filename = os.path.basename(rel_path)
    if not filename.startswith("solution_") or not filename.endswith(".py"):
        return jsonify({"error": "Only solution_*.py files can be executed"}), 403
    if not rel_path.startswith("curriculum/"):
        return jsonify({"error": "Scripts must be in curriculum/"}), 403

    result = run_script(rel_path, timeout=120)
    return jsonify(result)


@app.route("/api/run-stream", methods=["POST"])
def api_run_stream():
    """Execute a Python script and stream output line-by-line as NDJSON."""
    data = request.get_json(silent=True) or {}
    rel_path = data.get("path", "")
    if not rel_path:
        return jsonify({"error": "Missing path"}), 400

    filename = os.path.basename(rel_path)
    if not filename.startswith("solution_") or not filename.endswith(".py"):
        return jsonify({"error": "Only solution_*.py files can be executed"}), 403
    if not rel_path.startswith("curriculum/"):
        return jsonify({"error": "Scripts must be in curriculum/"}), 403

    def generate():
        for event in run_script_stream(rel_path, timeout=120):
            yield json.dumps(event) + "\n"

    return Response(
        stream_with_context(generate()),
        mimetype="application/x-ndjson",
        headers={"X-Accel-Buffering": "no", "Cache-Control": "no-cache"},
    )


# ── Main ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print()
    print("  AI Ninja Program — Training Portal")
    print(f"  {len(registered_lessons)} interactive lesson(s) loaded")
    print("  Open http://localhost:5000 in your browser")
    print()
    app.run(debug=True, port=5000)
