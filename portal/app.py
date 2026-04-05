"""
AI Ninja Program — Training Portal

Run:   python portal/app.py
Open:  http://localhost:5000
"""

import importlib
import os
import warnings
import markdown
from flask import Flask, render_template, jsonify, request, abort
from config import STAGES, get_all_lessons, get_lesson
from runner import run_script

warnings.filterwarnings("ignore")

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024  # 1 MB max request size


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


# ── Main ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print()
    print("  AI Ninja Program — Training Portal")
    print(f"  {len(registered_lessons)} interactive lesson(s) loaded")
    print("  Open http://localhost:5000 in your browser")
    print()
    app.run(debug=True, port=5000)
