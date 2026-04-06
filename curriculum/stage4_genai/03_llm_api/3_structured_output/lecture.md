# Exercise 3 — Structured JSON Output

> Read this guide fully before opening the lab.

---

## What You Will Learn

- How to instruct an LLM to return JSON instead of prose
- How to parse and validate the JSON response
- How to handle malformed output gracefully
- Why structured output is essential for pipeline integration

---

## Concept: LLMs as Classification APIs

When you need ML output to feed into another system, you need structured, parseable output — not prose. Compare:

**Prose response (hard to parse automatically):**
```
The log entry indicates a brute-force attack. The severity is high because there were
198 failed attempts in 60 seconds. I recommend blocking the IP immediately.
```

**JSON response (machine-readable):**
```json
{
  "threat_type": "brute_force",
  "technique_id": "T1110",
  "severity": "High",
  "confidence": 0.92,
  "recommended_actions": [
    "Block IP 45.33.32.156 at firewall",
    "Audit successful logins from this IP in past 24h"
  ]
}
```

The JSON version can be consumed directly by a SIEM, ticketing system, or automated response playbook.

**Structured output — log entry to actionable record**

| Stage | What it does | Example |
|---|---|---|
| 1. Log entry | raw text input | `"198 failed logins in 60s from 45.33.32.156"` |
| 2. LLM call | runs the model with a JSON-only system prompt | model returns a JSON string |
| 3. `json.loads()` | parses to a Python dict | `{"threat_type": "brute_force", "severity": "High", ...}` |
| 4. Downstream system | consumes the dict directly | SIEM / SOAR / ticket system / response playbook |

The whole point: every step after the LLM is just normal Python code working on a dict — no scraping, no regex on prose.

---

## Concept: How to Request JSON Output

The most reliable technique is to tell the model in the system prompt:

```python
SYSTEM = """You are a log classification API.
Respond ONLY with valid JSON. No prose, no markdown code blocks, no explanation.
The JSON must have exactly these fields:
  threat_type: string
  technique_id: string (MITRE T-number or "none")
  severity: "Critical" | "High" | "Medium" | "Low"
  confidence: number between 0 and 1
  summary: string (one sentence)
"""
```

Then parse with:
```python
import json
data = json.loads(response)
```

**From prompt to Python dict**

| Step | What you have | Type |
|---|---|---|
| 1. Prompt | system prompt + user log entry | strings |
| 2. Model output | `'{"threat_type": "brute_force", "severity": "High", "confidence": 0.92, ...}'` | str (JSON text) |
| 3. `json.loads(response)` | `{"threat_type": "brute_force", "severity": "High", "confidence": 0.92, ...}` | dict |
| 4. Field access | `data["severity"]` → `"High"`, `data["confidence"]` → `0.92` | normal Python values |

---

## Concept: Handling Malformed Output

LLMs sometimes wrap JSON in markdown:
````
```json
{"key": "value"}
```
````

Strip the fencing before parsing:
```python
text = response.strip()
if text.startswith("```"):
    text = text.split("```")[1]
    if text.startswith("json"):
        text = text[4:]
data = json.loads(text.strip())
```

---

## What Each Task Asks You to Do

### Task 1 — Get JSON for one log entry
Request structured JSON output for one log entry. Parse it. Print each field.

### Task 2 — Process multiple log entries
Loop over 4 log entries. For each, get JSON output, parse it, and build a summary table.

### Task 3 — Print a formatted results table
Print all results as an aligned table: `severity | technique_id | confidence | summary`.

### Task 4 — Error handling (Bonus)
Wrap the JSON parsing in a try/except. If parsing fails, print the raw response and a warning. Test with a deliberately malformed request.

---

## Now Open the Lab

[handson.md](handson.md)
## Next

[../4_conversation/lecture.md](../4_conversation/lecture.md) — maintain context across multiple turns.
