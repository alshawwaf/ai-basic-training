# AI Ninja Program — Training Portal

Interactive training portal for the AI Ninja Program. All 21 lessons across 5 stages are fully built with step-through content pages, materials drawers, challenge questions, and progress tracking.

## Quick start

```bash
cd portal
pip install -r requirements.txt
python app.py
```

Open http://localhost:5000

## What's included

- **21 interactive lessons** across 5 stages (Classic ML, Intermediate ML, Neural Networks, Generative AI, CP AI Security)
- **101 step routes** with concept cards, code patterns, info tables, and security callouts
- **Materials drawer** on each step linking to the curriculum's lecture notes, lab guides, and solution files
- **Challenge questions** with expandable answers on every step
- **Progress tracking** via localStorage (per-lesson visited steps, completion badges)
- **Dark/light theme** toggle
- **Brand identity** — Twin Scan ninja logo (favicon + navbar), 5 unique stage icons (belt, kunai, mask, scroll, shield)

## Structure

```
portal/
  app.py              Main Flask app (auto-discovers lesson Blueprints)
  config.py           Curriculum structure (stages, lessons, metadata)
  runner.py            Script executor (subprocess + matplotlib capture)
  requirements.txt
  static/
    style.css          Portal styles (dark/light themes, responsive)
    app.js             Theme toggle, grid rendering, progress tracking
    favicon.svg        Twin Scan ninja favicon
  templates/
    portal_base.html   Shared layout (navbar, theme toggle)
    home.html          Homepage with roadmap and stage cards
    stage.html         Individual stage view
    lesson_base.html   Step page layout (sidebar, drawer, modals)
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
