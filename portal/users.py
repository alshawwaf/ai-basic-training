"""
Server-side user progress storage.

Each user is identified by a token (UUID stored in their browser's localStorage).
Progress, bookmarks, and last-visited state are stored in SQLite so they survive
browser cache clears and are unique per user.
"""

import json
import os
import sqlite3
import uuid
from contextlib import contextmanager

DB_PATH = os.environ.get(
    "PORTAL_DB_PATH",
    os.path.join(os.path.dirname(__file__), "portal.db"),
)


def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


@contextmanager
def _db():
    conn = _connect()
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with _db() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                token     TEXT PRIMARY KEY,
                name      TEXT NOT NULL UNIQUE COLLATE NOCASE,
                created   TEXT NOT NULL DEFAULT (datetime('now'))
            );
            CREATE TABLE IF NOT EXISTS progress (
                token      TEXT NOT NULL REFERENCES users(token) ON DELETE CASCADE,
                lesson_id  TEXT NOT NULL,
                step       INTEGER NOT NULL,
                visited_at TEXT NOT NULL DEFAULT (datetime('now')),
                PRIMARY KEY (token, lesson_id, step)
            );
            CREATE TABLE IF NOT EXISTS bookmarks (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                token     TEXT NOT NULL REFERENCES users(token) ON DELETE CASCADE,
                lesson_id TEXT NOT NULL,
                step      INTEGER NOT NULL,
                title     TEXT NOT NULL DEFAULT '',
                created   TEXT NOT NULL DEFAULT (datetime('now')),
                UNIQUE(token, lesson_id, step)
            );
            CREATE TABLE IF NOT EXISTS last_visited (
                token      TEXT PRIMARY KEY REFERENCES users(token) ON DELETE CASCADE,
                lesson_id  TEXT NOT NULL,
                step       TEXT NOT NULL,
                title      TEXT NOT NULL DEFAULT '',
                updated_at TEXT NOT NULL DEFAULT (datetime('now'))
            );
            CREATE TABLE IF NOT EXISTS last_step (
                token      TEXT NOT NULL REFERENCES users(token) ON DELETE CASCADE,
                lesson_id  TEXT NOT NULL,
                step       INTEGER NOT NULL,
                PRIMARY KEY (token, lesson_id)
            );
        """)


# ── User management ─────────────────────────────────────────────────────────

def create_user(name: str) -> str:
    token = uuid.uuid4().hex
    with _db() as conn:
        conn.execute(
            "INSERT INTO users (token, name) VALUES (?, ?)",
            (token, name.strip()),
        )
    return token


def name_taken(name: str) -> bool:
    with _db() as conn:
        row = conn.execute(
            "SELECT 1 FROM users WHERE name = ? COLLATE NOCASE", (name.strip(),)
        ).fetchone()
    return row is not None


def get_user(token: str):
    with _db() as conn:
        return conn.execute(
            "SELECT token, name, created FROM users WHERE token = ?", (token,)
        ).fetchone()


# ── Progress ────────────────────────────────────────────────────────────────

def mark_step(token: str, lesson_id: str, step: int):
    with _db() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO progress (token, lesson_id, step) VALUES (?, ?, ?)",
            (token, lesson_id, step),
        )


def get_progress(token: str) -> dict:
    with _db() as conn:
        rows = conn.execute(
            "SELECT lesson_id, step FROM progress WHERE token = ? ORDER BY lesson_id, step",
            (token,),
        ).fetchall()
    out = {}
    for r in rows:
        out.setdefault(r["lesson_id"], []).append(r["step"])
    return out


# ── Bookmarks ───────────────────────────────────────────────────────────────

def add_bookmark(token: str, lesson_id: str, step: int, title: str):
    with _db() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO bookmarks (token, lesson_id, step, title) VALUES (?, ?, ?, ?)",
            (token, lesson_id, step, title),
        )


def remove_bookmark(token: str, lesson_id: str, step: int):
    with _db() as conn:
        conn.execute(
            "DELETE FROM bookmarks WHERE token = ? AND lesson_id = ? AND step = ?",
            (token, lesson_id, step),
        )


def get_bookmarks(token: str) -> list:
    with _db() as conn:
        rows = conn.execute(
            "SELECT lesson_id, step, title, created FROM bookmarks WHERE token = ? ORDER BY created",
            (token,),
        ).fetchall()
    return [dict(r) for r in rows]


# ── Last visited ────────────────────────────────────────────────────────────

def set_last_visited(token: str, lesson_id: str, step, title: str):
    with _db() as conn:
        conn.execute(
            """INSERT INTO last_visited (token, lesson_id, step, title, updated_at)
               VALUES (?, ?, ?, ?, datetime('now'))
               ON CONFLICT(token) DO UPDATE SET
                   lesson_id = excluded.lesson_id,
                   step = excluded.step,
                   title = excluded.title,
                   updated_at = excluded.updated_at""",
            (token, lesson_id, str(step), title),
        )


def get_last_visited(token: str):
    with _db() as conn:
        row = conn.execute(
            "SELECT lesson_id, step, title FROM last_visited WHERE token = ?",
            (token,),
        ).fetchone()
    return dict(row) if row else None


# ── Last step per lesson ────────────────────────────────────────────────────

def set_last_step(token: str, lesson_id: str, step: int):
    with _db() as conn:
        conn.execute(
            """INSERT INTO last_step (token, lesson_id, step) VALUES (?, ?, ?)
               ON CONFLICT(token, lesson_id) DO UPDATE SET step = excluded.step""",
            (token, lesson_id, step),
        )


def get_last_steps(token: str) -> dict:
    with _db() as conn:
        rows = conn.execute(
            "SELECT lesson_id, step FROM last_step WHERE token = ?", (token,)
        ).fetchall()
    return {r["lesson_id"]: r["step"] for r in rows}


# ── Reset ───────────────────────────────────────────────────────────────────

def reset_lesson(token: str, lesson_id: str):
    with _db() as conn:
        conn.execute("DELETE FROM progress WHERE token = ? AND lesson_id = ?", (token, lesson_id))
        conn.execute("DELETE FROM bookmarks WHERE token = ? AND lesson_id = ?", (token, lesson_id))
        conn.execute("DELETE FROM last_step WHERE token = ? AND lesson_id = ?", (token, lesson_id))
        lv = conn.execute("SELECT lesson_id FROM last_visited WHERE token = ?", (token,)).fetchone()
        if lv and lv["lesson_id"] == lesson_id:
            conn.execute("DELETE FROM last_visited WHERE token = ?", (token,))


def reset_stage(token: str, lesson_ids: list):
    with _db() as conn:
        ph = ",".join("?" * len(lesson_ids))
        conn.execute(f"DELETE FROM progress WHERE token = ? AND lesson_id IN ({ph})", [token] + lesson_ids)
        conn.execute(f"DELETE FROM bookmarks WHERE token = ? AND lesson_id IN ({ph})", [token] + lesson_ids)
        conn.execute(f"DELETE FROM last_step WHERE token = ? AND lesson_id IN ({ph})", [token] + lesson_ids)
        lv = conn.execute("SELECT lesson_id FROM last_visited WHERE token = ?", (token,)).fetchone()
        if lv and lv["lesson_id"] in lesson_ids:
            conn.execute("DELETE FROM last_visited WHERE token = ?", (token,))


def reset_all(token: str):
    with _db() as conn:
        conn.execute("DELETE FROM progress WHERE token = ?", (token,))
        conn.execute("DELETE FROM bookmarks WHERE token = ?", (token,))
        conn.execute("DELETE FROM last_step WHERE token = ?", (token,))
        conn.execute("DELETE FROM last_visited WHERE token = ?", (token,))


# ── Full state (single fetch for page load) ─────────────────────────────────

def get_full_state(token: str) -> dict:
    return {
        "progress": get_progress(token),
        "bookmarks": get_bookmarks(token),
        "lastVisited": get_last_visited(token),
        "lastStep": get_last_steps(token),
    }
