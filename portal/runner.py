"""
Script runner — executes a .py file in a subprocess, captures stdout/stderr
and any matplotlib figures as base64 PNG images.

Usage (internal — called by app.py's /api/run endpoint):
    result = run_script("stage1_classic_ml/01_what_is_ml/.../solution_loading_data.py")
"""

import base64
import os
import subprocess
import sys
import tempfile
import glob

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Wrapper injected before every script to capture matplotlib figures
_WRAPPER = r'''
import sys, os, warnings
warnings.filterwarnings("ignore")
os.environ["MPLBACKEND"] = "Agg"

# Patch matplotlib.pyplot.show() to save figures instead of displaying
_fig_dir = os.environ.get("_FIG_DIR", "")
_fig_counter = 0

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as _plt

    _original_show = _plt.show

    def _patched_show(*args, **kwargs):
        global _fig_counter
        if _fig_dir:
            for fig_num in _plt.get_fignums():
                fig = _plt.figure(fig_num)
                path = os.path.join(_fig_dir, f"fig_{_fig_counter:03d}.png")
                fig.savefig(path, dpi=100, bbox_inches="tight", facecolor="white")
                _fig_counter += 1
            _plt.close("all")

    _plt.show = _patched_show
except ImportError:
    pass

# ------- user script below -------
'''


MAX_OUTPUT_BYTES = 64 * 1024   # 64 KB max stdout/stderr
MAX_IMAGES = 10                # max matplotlib figures returned
ALLOWED_PREFIX = "curriculum/" # scripts must live under curriculum/

# Minimal env — strip secrets, API keys, etc.
# Keep OS essentials + Python/venv vars, block everything else
_SAFE_ENV_KEYS = {
    # OS essentials
    "PATH", "HOME", "LANG", "LC_ALL", "TMPDIR", "USER", "LOGNAME",
    # Windows essentials (Python crashes without these)
    "SYSTEMROOT", "COMSPEC", "WINDIR", "TEMP", "TMP",
    "HOMEDRIVE", "HOMEPATH", "USERPROFILE", "APPDATA", "LOCALAPPDATA",
    # Python / venv
    "VIRTUAL_ENV", "PYTHONPATH", "PYTHONHOME",
    # Runner-specific
    "MPLBACKEND", "_FIG_DIR", "PYTHONDONTWRITEBYTECODE", "PYTHONUNBUFFERED",
}


def run_script(rel_path: str, timeout: int = 60) -> dict:
    """Execute a Python script and return its output.

    Args:
        rel_path: path relative to REPO_ROOT (e.g. "curriculum/.../solution_x.py")
        timeout:  max seconds before killing the process

    Returns:
        dict with keys: stdout, stderr, images (list of base64 PNGs),
                        exit_code, timed_out
    """
    _err = lambda msg: {"stdout": "", "stderr": msg, "images": [],
                        "exit_code": 1, "timed_out": False}

    # Security: must be under curriculum/
    if not rel_path.startswith(ALLOWED_PREFIX):
        return _err("Access denied: scripts must be in curriculum/")

    full_path = os.path.normpath(os.path.join(REPO_ROOT, rel_path))

    # Security: prevent path traversal
    if not full_path.startswith(REPO_ROOT):
        return _err("Access denied")

    if not os.path.isfile(full_path):
        return _err(f"File not found: {rel_path}")

    if not full_path.endswith(".py"):
        return _err("Only .py files can be executed")

    # Read the script
    with open(full_path, encoding="utf-8") as f:
        user_code = f.read()

    # Create temp dir for figures + combined script
    with tempfile.TemporaryDirectory() as tmp_dir:
        fig_dir = os.path.join(tmp_dir, "figs")
        os.makedirs(fig_dir)

        # Write combined wrapper + user script
        script_path = os.path.join(tmp_dir, "run.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(_WRAPPER)
            f.write(user_code)

        # Build minimal environment (no secrets leak)
        env = {k: v for k, v in os.environ.items() if k in _SAFE_ENV_KEYS}
        env["MPLBACKEND"] = "Agg"
        env["_FIG_DIR"] = fig_dir
        env["PYTHONDONTWRITEBYTECODE"] = "1"

        # Run the script
        timed_out = False
        try:
            proc = subprocess.run(
                [sys.executable, "-u", script_path],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=os.path.dirname(full_path),
                env=env,
            )
            exit_code = proc.returncode
            stdout = proc.stdout[:MAX_OUTPUT_BYTES]
            stderr = proc.stderr[:MAX_OUTPUT_BYTES]
        except subprocess.TimeoutExpired:
            timed_out = True
            exit_code = -1
            stdout = ""
            stderr = f"Script timed out after {timeout} seconds."

        # Collect saved figures (capped)
        images = []
        for png in sorted(glob.glob(os.path.join(fig_dir, "*.png")))[:MAX_IMAGES]:
            with open(png, "rb") as img:
                images.append(base64.b64encode(img.read()).decode("ascii"))

    return {
        "stdout": stdout,
        "stderr": stderr,
        "images": images,
        "exit_code": exit_code,
        "timed_out": timed_out,
    }
