# Lab — Exercise 3: Structured JSON Output

> Follow each step in order. Copy the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `03_structured_output.py` in this folder.

---

## Step 2: Add the imports and set up the client

`json` is needed to parse the model's response. The `sys.path` fix and `get_client()` pattern is identical to the previous exercises.

```python
import json
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from llm_client import get_client

provider, client = get_client()
if client is None:
    print("No API key found. Set ANTHROPIC_API_KEY, OPENAI_API_KEY, or GOOGLE_API_KEY.")
    exit(1)

print(f"Provider: {provider}\n")
```

---

## Step 3: Define the data, system prompt, and JSON parser

The system prompt tells the model it is a classification API and must return only JSON — no prose. The `parse_json_response` helper strips markdown code fences that some models add around JSON output before parsing.

Add this to your file:

```python
LOGS = [
    "Failed login for root from 45.33.32.156 — 198 attempts in 60 seconds",
    "powershell.exe -EncodedCommand JABjAGwAaQBlAG4AdAAgAD0A... spawned by winword.exe",
    "Scheduled task 'DailyBackup' completed successfully — 0 errors",
    "nmap scan from 10.0.1.200 to 10.0.2.0/24, 65535 ports scanned in 120s",
]

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
```

---

## Step 4: Get structured JSON for one log entry

This confirms the model follows the JSON schema before you loop over all logs. Printing each field individually makes it easy to verify the response is correctly parsed.

Add this to your file:

```python
raw = client.chat(
    system=JSON_SYSTEM,
    messages=[{"role": "user", "content": LOGS[0]}],
    max_tokens=200,
)
data = parse_json_response(raw)

print("--- Log 1 ---")
for key in ["threat_type", "technique_id", "severity", "confidence", "summary"]:
    print(f"  {key:<12} : {data[key]}")
```

Run your file. You should see:
```
--- Log 1 ---
  threat_type  : brute_force
  technique_id : T1110
  severity     : High
  confidence   : 0.95
  summary      : SSH brute-force attack targeting root account from 45.33.32.156
```

---

## Step 5: Process all 4 logs

Looping over all logs with a progress indicator helps track where you are during the API calls, which can take a few seconds each.

Add this to your file:

```python
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
```

Run your file. You should see:
```
Processing log 1/4...
Processing log 2/4...
Processing log 3/4...
Processing log 4/4...
```

---

## Step 6: Print a formatted results table

Aligning columns with f-string format specifiers (`:<10`, `:.2f`) makes the table easy to scan across all four logs at once.

Add this to your file:

```python
print("\nSeverity   | Technique  | Conf | Summary")
print("-----------+------------+------+" + "-" * 58)
for r in results:
    if r is None:
        print("  [parse error]")
        continue
    print(f"  {r['severity']:<10} | {r['technique_id']:<10} | {r['confidence']:.2f} | {r['summary'][:55]}")

print("\n--- Exercise 3 complete. Move to 04_conversation.py ---")
```

Run your file. You should see:
```
Severity   | Technique  | Conf | Summary
-----------+------------+------+----------------------------------------------------------
  High       | T1110      | 0.95 | SSH brute-force attack targeting root account
  Critical   | T1059.001  | 0.92 | Encoded PowerShell execution spawned by Word process
  Low        | none       | 0.45 | Scheduled backup task completed without errors
  High       | T1046      | 0.88 | Network port scan from internal host across /24 subnet

--- Exercise 3 complete. Move to 04_conversation.py ---
```

---

## Your completed script

At this point your file contains all the working code. Compare it against the matching `_solution_` file (`03_solution_structured_output.py`) if anything looks different.
