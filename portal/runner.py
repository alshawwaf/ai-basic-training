"""
Script runner — executes a .py file in a subprocess, captures stdout/stderr
and any matplotlib figures as base64 PNG images.

Usage (internal — called by app.py's /api/run endpoint):
    result = run_script("stage1_classic_ml/01_what_is_ml/.../solution_loading_data.py")
"""

import base64
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
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
                print(f"##FIGURE:{_fig_counter}##")
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
        # Force UTF-8 stdout/stderr in the child so unicode glyphs
        # (em-dash, arrows, block chars) survive the cp1252 default on Windows.
        env["PYTHONIOENCODING"] = "utf-8"

        # Run the script
        timed_out = False
        try:
            proc = subprocess.run(
                [sys.executable, "-u", script_path],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
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

    # Parse sections if markers are present
    sections = _parse_sections(stdout, images)

    result = {
        "stderr": stderr,
        "exit_code": exit_code,
        "timed_out": timed_out,
    }

    if sections is not None:
        result["sections"] = sections
        # Strip markers from flat stdout (fallback display)
        result["stdout"] = re.sub(r'##(?:SECTION:.+?|FIGURE:\d+)##\n?', '', stdout).strip()
        result["images"] = images
    else:
        result["stdout"] = stdout
        result["images"] = images

    return result


def run_script_stream(rel_path: str, timeout: int = 60):
    """Execute a Python script, yielding NDJSON events as output is produced.

    Yields dicts with 'type' key:
        section  – new section started (title)
        output   – a line of stdout
        figure   – base64 PNG image
        stderr   – collected stderr (sent after process exits)
        done     – execution finished (exit_code)
        error    – something went wrong (text)
    """
    def _err(msg):
        yield {'type': 'error', 'text': msg}

    if not rel_path.startswith(ALLOWED_PREFIX):
        yield from _err("Access denied: scripts must be in curriculum/")
        return

    full_path = os.path.normpath(os.path.join(REPO_ROOT, rel_path))
    if not full_path.startswith(REPO_ROOT):
        yield from _err("Access denied")
        return
    if not os.path.isfile(full_path):
        yield from _err(f"File not found: {rel_path}")
        return
    if not full_path.endswith(".py"):
        yield from _err("Only .py files can be executed")
        return

    with open(full_path, encoding="utf-8") as f:
        user_code = f.read()

    tmp_dir = tempfile.mkdtemp()
    fig_dir = os.path.join(tmp_dir, "figs")
    os.makedirs(fig_dir)

    script_path = os.path.join(tmp_dir, "run.py")
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(_WRAPPER)
        f.write(user_code)

    env = {k: v for k, v in os.environ.items() if k in _SAFE_ENV_KEYS}
    env["MPLBACKEND"] = "Agg"
    env["_FIG_DIR"] = fig_dir
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    # Force the child interpreter to write UTF-8 to stdout/stderr regardless
    # of the host locale. Without this, em-dashes / arrows / block glyphs
    # from print() come out as mojibake on Windows (cp1252) and we render
    # them as the U+FFFD replacement character.
    env["PYTHONIOENCODING"] = "utf-8"

    proc = subprocess.Popen(
        [sys.executable, "-u", script_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=os.path.dirname(full_path),
        env=env,
    )

    timed_out = [False]

    def _kill_on_timeout():
        timed_out[0] = True
        proc.kill()

    timer = threading.Timer(timeout, _kill_on_timeout)
    timer.start()

    try:
        for raw_line in iter(proc.stdout.readline, b''):
            line = raw_line.decode('utf-8', errors='replace').rstrip('\n\r')

            if line.startswith('##SECTION:') and line.endswith('##'):
                yield {'type': 'section', 'title': line[10:-2]}

            elif line.startswith('##FIGURE:') and line.endswith('##'):
                fig_num = int(line[9:-2])
                fig_path = os.path.join(fig_dir, f"fig_{fig_num:03d}.png")
                if os.path.isfile(fig_path):
                    with open(fig_path, "rb") as img:
                        b64 = base64.b64encode(img.read()).decode("ascii")
                    yield {'type': 'figure', 'data': b64}

            else:
                yield {'type': 'output', 'text': line}

        proc.wait()
        timer.cancel()

        stderr = proc.stderr.read()
        if stderr:
            stderr_text = stderr.decode('utf-8', errors='replace')[:MAX_OUTPUT_BYTES]
            if stderr_text.strip():
                yield {'type': 'stderr', 'text': stderr_text}

        if timed_out[0]:
            yield {'type': 'error', 'text': f'Script timed out after {timeout}s'}

        yield {'type': 'done', 'exit_code': proc.returncode}

    except Exception as e:
        timer.cancel()
        proc.kill()
        yield {'type': 'error', 'text': str(e)}

    finally:
        timer.cancel()
        shutil.rmtree(tmp_dir, ignore_errors=True)


def _parse_sections(stdout: str, images: list) -> list | None:
    """Split stdout by ##SECTION:Title## markers, associate figures.

    Returns None if no section markers found (use flat rendering).
    Returns list of {title, stdout, images[]} dicts otherwise.
    """
    if '##SECTION:' not in stdout:
        return None

    parts = re.split(r'##SECTION:(.+?)##\n?', stdout)

    sections = []

    # parts[0] = text before first marker (preamble — usually empty)
    # parts[1] = first section title, parts[2] = first section body, etc.
    preamble = parts[0].strip()
    if preamble:
        clean = re.sub(r'##FIGURE:\d+##\n?', '', preamble).strip()
        fig_ids = [int(m) for m in re.findall(r'##FIGURE:(\d+)##', preamble)]
        if clean or fig_ids:
            sections.append({
                'title': 'Setup',
                'stdout': clean,
                'images': [images[i] for i in fig_ids if i < len(images)],
            })

    for i in range(1, len(parts), 2):
        title = parts[i].strip()
        body = parts[i + 1] if i + 1 < len(parts) else ''
        fig_ids = [int(m) for m in re.findall(r'##FIGURE:(\d+)##', body)]
        clean = re.sub(r'##FIGURE:\d+##\n?', '', body).strip()

        sections.append({
            'title': title,
            'stdout': clean,
            'images': [images[idx] for idx in fig_ids if idx < len(images)],
        })

    return sections
