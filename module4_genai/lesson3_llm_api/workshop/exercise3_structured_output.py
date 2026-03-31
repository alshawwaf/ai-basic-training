# =============================================================================
# LESSON 4.3 | WORKSHOP | Exercise 3 of 4
# Structured JSON Output
# =============================================================================
# WHAT YOU WILL LEARN
# -------------------
# - How to instruct an LLM to return valid JSON for pipeline integration
# - How to parse and validate JSON responses
# - How to handle formatting edge cases in LLM output
#
# RUN THIS FILE
# -------------
#   python module4_genai/lesson3_llm_api/workshop/exercise3_structured_output.py
# =============================================================================

import json
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from llm_client import get_client

provider, client = get_client()
if client is None:
    print("No API key found. Set ANTHROPIC_API_KEY, OPENAI_API_KEY, or GOOGLE_API_KEY.")
    exit(1)

print(f"Provider: {provider}\n")

# Four log entries to classify
LOGS = [
    "Failed login for root from 45.33.32.156 — 198 attempts in 60 seconds",
    "powershell.exe -EncodedCommand JABjAGwAaQBlAG4AdAAgAD0A... spawned by winword.exe",
    "Scheduled task 'DailyBackup' completed successfully — 0 errors",
    "nmap scan from 10.0.1.200 to 10.0.2.0/24, 65535 ports scanned in 120s",
]

# =============================================================================
# BACKGROUND
# =============================================================================
# Structured output turns the LLM into a classification API.
# Key: tell the model in the system prompt to respond with ONLY JSON, no prose.
#
# JSON fields to request:
#   threat_type : short string (e.g. "brute_force", "encoded_powershell", "port_scan")
#   technique_id: MITRE ATT&CK ID (e.g. "T1110") or "none"
#   severity    : "Critical" | "High" | "Medium" | "Low"
#   confidence  : float 0.0–1.0
#   summary     : one sentence

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

# =============================================================================
# TASK 1 — Get structured JSON for one log entry
# =============================================================================
# Call client.chat() with JSON_SYSTEM and LOGS[0].
# Parse the response with parse_json_response().
# Print each field on its own line:
#   threat_type  : brute_force
#   technique_id : T1110
#   severity     : High
#   confidence   : 0.95
#   summary      : SSH brute-force attack targeting root account from external IP
#
# EXPECTED OUTPUT (approximate):
#   --- Log 1 ---
#   threat_type  : brute_force
#   technique_id : T1110
#   severity     : High
#   confidence   : 0.95
#   summary      : SSH brute-force attack targeting root account from 45.33.32.156

# >>> YOUR CODE HERE


# =============================================================================
# TASK 2 — Process all 4 logs
# =============================================================================
# Loop over all LOGS. For each:
#   1. Call client.chat() with JSON_SYSTEM
#   2. Parse with parse_json_response()
#   3. Append the result dict (+ add "log" key with first 50 chars) to a `results` list
#
# Print a progress indicator per log: "Processing log 1/4..."

# >>> YOUR CODE HERE


# =============================================================================
# TASK 3 — Print a formatted results table
# =============================================================================
# Print the results as an aligned table with columns:
#   Severity | Technique | Conf | Summary
#
# Format: f"{r['severity']:<10} | {r['technique_id']:<10} | {r['confidence']:.2f} | {r['summary'][:55]}"
#
# EXPECTED OUTPUT (approximate):
#   Severity   | Technique  | Conf | Summary
#   -----------+------------+------+----------------------------------------------------------
#   High       | T1110      | 0.95 | SSH brute-force attack targeting root account
#   Critical   | T1059.001  | 0.92 | Encoded PowerShell execution spawned by Word process
#   Low        | none       | 0.45 | Scheduled backup task completed without errors
#   High       | T1046      | 0.88 | Network port scan from internal host across /24 subnet

# >>> YOUR CODE HERE


# =============================================================================
# TASK 4 — Error handling (BONUS)
# =============================================================================
# Wrap your JSON parsing in try/except json.JSONDecodeError.
# If parsing fails:
#   - Print "WARNING: Could not parse JSON response"
#   - Print the raw response
#   - Append None to results for that log
#
# To test this: modify parse_json_response to intentionally raise JSONDecodeError
# on the first call, then verify the fallback works.

# >>> YOUR CODE HERE


print("\n--- Exercise 3 complete. Move to exercise4_conversation.py ---")
