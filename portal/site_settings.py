"""Per-deployment portal settings persisted to a JSON file.

Currently the only setting is `home_view`, which controls whether the
public home page is rendered as the default `cards` layout (zigzag stage
cards with a neural-network mesh overlay) or as the opt-in `neuron`
layout (glowing soma cores with lesson satellites). The admin console
flips this in /admin under "Display Settings".

The store is a small JSON file living next to this module. We re-read
on every access — the portal traffic is tiny, this avoids any cache
invalidation across processes, and it lets the admin toggle take effect
on the very next request without restarting the server.
"""

import json
import os
from threading import Lock

_SETTINGS_PATH = os.environ.get(
    "PORTAL_SETTINGS_PATH",
    os.path.join(os.path.dirname(__file__), "site_settings.json"),
)
_LOCK = Lock()

ALLOWED_HOME_VIEWS = ("cards", "neuron")
DEFAULT_SETTINGS = {"home_view": "cards"}


def _read() -> dict:
    """Load the settings JSON; return defaults on any error or missing file."""
    if not os.path.exists(_SETTINGS_PATH):
        return dict(DEFAULT_SETTINGS)
    try:
        with open(_SETTINGS_PATH, encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return dict(DEFAULT_SETTINGS)
        # Backfill any missing keys with defaults so callers don't need
        # to handle KeyError on every access.
        merged = dict(DEFAULT_SETTINGS)
        merged.update({k: v for k, v in data.items() if k in DEFAULT_SETTINGS})
        return merged
    except (json.JSONDecodeError, OSError):
        return dict(DEFAULT_SETTINGS)


def _write(data: dict) -> None:
    """Atomically replace the settings JSON file."""
    tmp = _SETTINGS_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp, _SETTINGS_PATH)


def get_home_view() -> str:
    """Return the currently selected home view ('cards' or 'neuron')."""
    with _LOCK:
        view = _read().get("home_view", "cards")
    return view if view in ALLOWED_HOME_VIEWS else "cards"


def set_home_view(view: str) -> str:
    """Persist a new home view choice; reject anything outside the allowlist."""
    if view not in ALLOWED_HOME_VIEWS:
        raise ValueError(f"home_view must be one of {ALLOWED_HOME_VIEWS}")
    with _LOCK:
        data = _read()
        data["home_view"] = view
        _write(data)
    return view
