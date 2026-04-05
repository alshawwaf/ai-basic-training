"""
AI Ninja Program — Training Portal

Run:   python portal/app.py
Open:  http://localhost:5000
"""

import importlib
import warnings
from flask import Flask, render_template
from config import STAGES, get_all_lessons, get_lesson

warnings.filterwarnings("ignore")

app = Flask(__name__)

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


# ── Main ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print()
    print("  AI Ninja Program — Training Portal")
    print(f"  {len(registered_lessons)} interactive lesson(s) loaded")
    print("  Open http://localhost:5000 in your browser")
    print()
    app.run(debug=True, port=5000)
