# AI Ninja Program — Training Portal

Interactive training portal for the AI Ninja Program. All 21 lessons across 5 stages are fully built with step-through content pages, materials drawers, challenge questions, and progress tracking.

## Quick start

```bash
cd portal
pip install -r requirements.txt
python app.py
```

Open http://localhost:5000 (this is the direct `python app.py` port; via `docker-compose up` from the repo root the portal is published on **http://localhost:5545**).

## What's included

- **21 interactive lessons** across 5 stages (Classic ML, Intermediate ML, Neural Networks, Generative AI, CP AI Security)
- **110 step routes** with concept cards, code patterns, info tables, and security callouts
- **Materials drawer** on each step linking to the curriculum's lecture notes, lab guides, and solution files
- **Challenge questions** with expandable answers on every step, plus a per-lesson multiple-choice **quiz**
- **Progress tracking** stored server-side in SQLite, keyed by a per-browser token (visited steps, bookmarks, and last-visited state survive cache clears)
- **Admin console** at `/admin` — login-gated (`PORTAL_ADMIN_PASSWORD`, default `ninja`) with analytics and a home-layout toggle
- **Dark/light theme** toggle
- **Brand identity** — Twin Scan ninja logo (favicon + navbar), 5 unique stage icons (belt, kunai, mask, scroll, shield)

## Structure

```
portal/
  app.py              Main Flask app (auto-discovers lesson Blueprints, admin console, content + run APIs)
  config.py           Curriculum structure (stages, lessons, metadata)
  runner.py            Script executor (subprocess + matplotlib capture)
  users.py             Server-side progress store (SQLite, per-browser token)
  site_settings.py     Per-deployment settings (e.g. home-page layout), JSON-backed
  requirements.txt
  static/
    style.css          Portal styles (dark/light themes, responsive)
    app.js             Theme toggle, grid rendering, progress tracking
    favicon.svg        Twin Scan ninja favicon
    lecture_assets/    Pre-rendered matplotlib figures for lecture panels
  templates/
    portal_base.html   Shared layout (navbar, theme toggle)
    home.html          Homepage with roadmap and stage cards
    stage.html         Individual stage view
    lesson_base.html   Step page layout (sidebar, drawer, modals)
    quiz.html          Per-lesson multiple-choice quiz
    admin.html / admin_login.html / admin_analytics.html   Login-gated admin console
    choose_logo.html   Logo picker
    icons.html         SVG icon library (brand logo + 5 stage icons)
  lessons/
    s1_01_what_is_ml/  ... through s5_04_positioning_cp_ai/
    (21 lesson Blueprints, each with __init__.py + templates/)
```

## Adding a new interactive lesson

1. Create `portal/lessons/<folder>/` with `__init__.py`
2. Define a Flask `Blueprint` named `bp`
3. Add step templates under `templates/<lesson_id>/`
4. Set `has_app: True` in `config.py` for that lesson
5. The portal auto-registers it on startup
