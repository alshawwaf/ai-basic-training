# Exercise 3 — Structured JSON Output
#
# Instructs the LLM to return machine-readable JSON instead of prose,
# parses the response, and prints a formatted results table.
# Works with Claude, OpenAI, Gemini, or Ollama -- whichever you have configured.
#
# Set ONE of:
#   set ANTHROPIC_API_KEY=...
#   set OPENAI_API_KEY=...
#   set GOOGLE_API_KEY=...
#   set OLLAMA_MODEL=huihui_ai/qwen3.5-abliterated:2B

import json
import sys
import os

# Import the shared LLM client (one directory up from )
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from llm_client import get_client

provider, client = get_client()
if client is None:
    print("No API key found. Set ANTHROPIC_API_KEY, OPENAI_API_KEY, or GOOGLE_API_KEY.")
    exit(1)

print(f"Provider: {provider}\n")


# ============================================================
#   Data and System Prompt
# ============================================================

# Four log entries ranging from clearly malicious to benign
LOGS = [
    "Failed login for root from 45.33.32.156 — 198 attempts in 60 seconds",
    "powershell.exe -EncodedCommand JABjAGwAaQBlAG4AdAAgAD0A... spawned by winword.exe",
    "Scheduled task 'DailyBackup' completed successfully — 0 errors",
    "nmap scan from 10.0.1.200 to 10.0.2.0/24, 65535 ports scanned in 120s",
]

# The system prompt tells the model it is a classification API
# and must return ONLY JSON — no prose, no markdown
JSON_SYSTEM = """You are a log classification API.
Respond ONLY with valid JSON. No prose, no markdown code blocks, no explanation outside JSON.
Return exactly these fields:
  threat_type: string (short identifier, e.g. "brute_force")
  technique_id: string (MITRE ATT&CK ID like "T1110", or "none" if not applicable)
  severity: one of "Critical", "High", "Medium", "Low"
  confidence: number between 0.0 and 1.0
  summary: string (one sentence describing the finding)"""


def parse_json_response(text):
    """Parse JSON from model response, stripping markdown code fences if present."""
    text = text.strip()
    if text.startswith("```"):
        parts = text.split("```")
        for part in parts:
            part = part.strip()
            if part.startswith("json"):
                part = part[4:].strip()
            if part.startswith("{"):
                text = part
                break
    return json.loads(text)


# ============================================================
#   TASK 1: Get structured JSON for one log entry
# ============================================================
print("=" * 60)
print("  TASK 1: Structured JSON for One Log Entry")
print("=" * 60)

# Send a single log entry and parse the JSON response
raw = client.chat(
    system=JSON_SYSTEM,
    messages=[{"role": "user", "content": LOGS[0]}],
    max_tokens=200,
)
data = parse_json_response(raw)

print("\n--- Log 1 ---")
for key in ["threat_type", "technique_id", "severity", "confidence", "summary"]:
    print(f"  {key:<12} : {data[key]}")


# ============================================================
#   TASK 2: Process all 4 log entries
# ============================================================
print("\n" + "=" * 60)
print("  TASK 2: Process All Log Entries")
print("=" * 60)

# Loop over every log, call the API, parse JSON, collect results
results = []
for i, log in enumerate(LOGS, 1):
    print(f"Processing log {i}/{len(LOGS)}...")
    try:
        raw = client.chat(
            system=JSON_SYSTEM,
            messages=[{"role": "user", "content": log}],
            max_tokens=200,
        )
        parsed = parse_json_response(raw)
        parsed["log"] = log[:50]
        results.append(parsed)
    except json.JSONDecodeError:
        print(f"WARNING: Could not parse JSON response for log {i}")
        print(f"Raw response: {raw}")
        results.append(None)


# ============================================================
#   TASK 3: Print a formatted results table
# ============================================================
print("\n" + "=" * 60)
print("  TASK 3: Formatted Results Table")
print("=" * 60)

# Aligned table with severity, technique, confidence, and summary
print("\nSeverity   | Technique  | Conf | Summary")
print("-----------+------------+------+" + "-" * 58)
for r in results:
    if r is None:
        print("  [parse error]")
        continue
    print(f"  {r['severity']:<10} | {r['technique_id']:<10} | {r['confidence']:.2f} | {r['summary'][:55]}")

print("\n--- Exercise 3 complete. Move to ../4_conversation/solution.py ---")
