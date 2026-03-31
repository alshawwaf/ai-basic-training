# Lesson 4.3 — Working with LLM APIs
#
# Demonstrates calling an LLM provider to build a threat intelligence assistant.
# Works with Claude, OpenAI, or Gemini — whichever key you have set.
#
# Set ONE of:
#   set ANTHROPIC_API_KEY=...    (Claude  — recommended)
#   set OPENAI_API_KEY=...       (OpenAI)
#   set GOOGLE_API_KEY=...       (Gemini)

import json
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from llm_client import get_client

provider, client = get_client()
if client is None:
    exit(1)

print("=" * 60)
print(f"  LESSON 4.3: LLM API — THREAT INTEL ASSISTANT ({provider.upper()})")
print("=" * 60)

SECURITY_ANALYST_SYSTEM = """You are a senior cybersecurity analyst and threat hunter.
When given log entries, alerts, or IOCs:
- Identify the attack technique and MITRE ATT&CK tactic/technique if applicable
- Assess the severity (Critical / High / Medium / Low)
- Explain what the attacker was likely trying to do
- Give 2-3 immediate response actions
Keep responses concise and technical. Use bullet points."""

# ── 1. Basic call: analyse a log entry ────────────────────────────────────────
print("\n── 1. Basic API Call ──")

log_entry = """
2024-01-15 03:47:22 | WORKSTATION-042 | Event ID 4688
Process: cmd.exe → powershell.exe -EncodedCommand JABjAGwAaQBlAG4AdAAgAD0AIABOAGUAdwAtAE8AYgBqAGUAYwB0...
Parent: winword.exe
User: jsmith (standard user)
Network: Outbound connection to 185.234.219.47:443 immediately after
"""

response = client.chat(
    system=SECURITY_ANALYST_SYSTEM,
    messages=[{"role": "user", "content": f"Analyse this log entry:\n{log_entry}"}],
    max_tokens=600,
)
print(response)

# ── 2. Multi-turn conversation ────────────────────────────────────────────────
print("\n\n── 2. Multi-turn Conversation ──")

conversation = []

def chat(user_message):
    conversation.append({"role": "user", "content": user_message})
    reply = client.chat(system=SECURITY_ANALYST_SYSTEM, messages=conversation, max_tokens=400)
    conversation.append({"role": "assistant", "content": reply})
    print(f"\nUser: {user_message}")
    print(f"\n{provider.capitalize()}: {reply}")
    print("-" * 40)
    return reply

chat("We've detected lateral movement from WORKSTATION-042 to 5 servers in the last 10 minutes. What's the likely objective?")
chat("The affected servers are our Active Directory domain controllers. How does this change the threat assessment?")
chat("We've isolated the workstation. What are the next 3 steps in our incident response?")

print(f"\nConversation maintained {len(conversation)} turns of context.")

# ── 3. Structured JSON output ─────────────────────────────────────────────────
print("\n── 3. Structured JSON Output (for pipeline integration) ──")

JSON_SYSTEM = """You are a security classification API.
Respond ONLY with valid JSON. No prose, no markdown, no code blocks.
The JSON must have exactly these fields:
  tactic: string (MITRE ATT&CK tactic name)
  technique_id: string (e.g. "T1059.001")
  technique_name: string
  severity: "Critical" | "High" | "Medium" | "Low"
  confidence: number between 0 and 1
  iocs: array of strings
  recommended_actions: array of strings (max 3)"""

alerts = [
    "Mimikatz-style LSASS memory access detected on DC01 at 2am by service account",
    "DNS queries to randomised subdomains of .ru TLD at 500 queries/minute from multiple hosts",
    "Scheduled task created to run Base64-encoded PowerShell at system startup",
]

for alert in alerts:
    response = client.chat(
        system=JSON_SYSTEM,
        messages=[{"role": "user", "content": alert}],
        max_tokens=300,
    )
    try:
        data = json.loads(response)
        print(f"\n  Alert: {alert[:60]}...")
        print(f"  Tactic    : {data.get('tactic')}")
        print(f"  Technique : {data.get('technique_id')} — {data.get('technique_name')}")
        print(f"  Severity  : {data.get('severity')} (confidence: {data.get('confidence', 0):.0%})")
        print(f"  Actions   : {data.get('recommended_actions', [])}")
    except json.JSONDecodeError:
        print(f"  Raw: {response[:200]}")

# ── 4. Streaming ───────────────────────────────────────────────────────────────
print("\n\n── 4. Streaming Response ──\n")
print(f"{provider.capitalize()}: ", end="", flush=True)
for chunk in client.stream(
    system="You are a concise threat intelligence writer.",
    messages=[{
        "role": "user",
        "content": "Write a 3-sentence executive summary of Log4Shell (CVE-2021-44228) for a non-technical board."
    }],
    max_tokens=300,
):
    print(chunk, end="", flush=True)
print("\n")

print("=" * 60)
print("Next: Lesson 4.4 — RAG to ground answers in your own documents.")
