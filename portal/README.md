# AI Ninja Program — Training Portal

Interactive training portal for the AI Ninja Program.

## Quick start

```bash
cd portal
pip install -r requirements.txt
python app.py
```

Open http://localhost:5000

## Structure

```
portal/
  app.py              Main Flask app (auto-discovers lesson Blueprints)
  config.py           Curriculum structure (stages, lessons, metadata)
  requirements.txt
  static/             Shared CSS, JS
  templates/           Portal-level templates (home, stage, lesson base)
  lessons/
    s1_01_what_is_ml/  Lesson 1.1 Blueprint (routes, data, templates)
    ...                Future lessons plug in here
```

## Adding a new interactive lesson

1. Create `portal/lessons/<folder>/` with `__init__.py`
2. Define a Flask `Blueprint` named `bp`
3. Add step templates under `templates/<lesson_id>/`
4. Set `has_app: True` in `config.py` for that lesson
5. The portal auto-registers it on startup
