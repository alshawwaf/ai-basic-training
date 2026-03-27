# Lesson 4.3 — The Claude API
#
# Build a threat intelligence assistant using Claude.
# Demonstrates:
#   - Basic API call
#   - System prompt design
#   - Multi-turn conversation
#   - Structured JSON output
#   - Streaming responses
#
# Setup:
#   pip install anthropic
#   set ANTHROPIC_API_KEY=your-key-here

import os
import json
import anthropic

# ── Check for API key ──────────────────────────────────────────────────────────
api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    print("ERROR: ANTHROPIC_API_KEY environment variable not set.")
    print("\nTo get a key:")
    print("  1. Go to https://console.anthropic.com")
    print("  2. Create an account and generate an API key")
    print("  3. Run: set ANTHROPIC_API_KEY=your-key-here")
    exit(1)

client = anthropic.Anthropic(api_key=api_key)
MODEL  = "claude-sonnet-4-6"

print("=" * 60)
print("  LESSON 4.3: CLAUDE API — THREAT INTEL ASSISTANT")
print("=" * 60)

# ── 1. Basic call: analyse a log entry ────────────────────────────────────────
print("\n── 1. Basic API Call ──")

SECURITY_ANALYST_SYSTEM = """You are a senior cybersecurity analyst and threat hunter.
When given log entries, alerts, or IOCs:
- Identify the attack technique and MITRE ATT&CK tactic/technique if applicable
- Assess the severity (Critical / High / Medium / Low)
- Explain what the attacker was likely trying to do
- Give 2-3 immediate response actions
Keep responses concise and technical. Use bullet points."""

log_entry = """
2024-01-15 03:47:22 | WORKSTATION-042 | Event ID 4688
Process: cmd.exe → powershell.exe -EncodedCommand JABjAGwAaQBlAG4AdAAgAD0AIABOAGUAdwAtAE8AYgBqAGUAYwB0...
Parent: winword.exe
User: jsmith (standard user)
Network: Outbound connection to 185.234.219.47:443 immediately after
"""

response = client.messages.create(
    model=MODEL,
    max_tokens=600,
    system=SECURITY_ANALYST_SYSTEM,
    messages=[{"role": "user", "content": f"Analyse this log entry:\n{log_entry}"}]
)

print(f"Response (used {response.usage.input_tokens} input + {response.usage.output_tokens} output tokens):\n")
print(response.content[0].text)

# ── 2. Multi-turn conversation ────────────────────────────────────────────────
print("\n\n── 2. Multi-turn Conversation ──")

conversation = []

def chat(user_message, verbose=True):
    """Add a message, get a response, maintain history."""
    conversation.append({"role": "user", "content": user_message})
    response = client.messages.create(
        model=MODEL,
        max_tokens=400,
        system=SECURITY_ANALYST_SYSTEM,
        messages=conversation
    )
    reply = response.content[0].text
    conversation.append({"role": "assistant", "content": reply})
    if verbose:
        print(f"\nUser: {user_message[:80]}")
        print(f"\nClaude: {reply}\n")
        print("-" * 40)
    return reply

# Simulate a security investigation
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

alerts_to_classify = [
    "Mimikatz-style LSASS memory access detected on DC01 at 2am by service account",
    "DNS queries to randomised subdomains of .ru TLD at 500 queries/minute from multiple hosts",
    "Scheduled task created to run Base64-encoded PowerShell at system startup",
]

print("\nClassifying alerts as structured JSON:")
for alert in alerts_to_classify:
    response = client.messages.create(
        model=MODEL,
        max_tokens=300,
        system=JSON_SYSTEM,
        messages=[{"role": "user", "content": alert}]
    )
    try:
        data = json.loads(response.content[0].text)
        print(f"\n  Alert: {alert[:60]}...")
        print(f"  Tactic     : {data.get('tactic', 'N/A')}")
        print(f"  Technique  : {data.get('technique_id')} — {data.get('technique_name')}")
        print(f"  Severity   : {data.get('severity')} (confidence: {data.get('confidence', 0):.0%})")
        print(f"  IOCs       : {data.get('iocs', [])}")
        print(f"  Actions    : {data.get('recommended_actions', [])}")
    except json.JSONDecodeError:
        print(f"  Raw response: {response.content[0].text[:200]}")

# ── 4. Streaming (for long responses) ─────────────────────────────────────────
print("\n\n── 4. Streaming Response ──")
print("(useful when generating long reports — prints as tokens arrive)\n")

print("Claude: ", end="", flush=True)
with client.messages.stream(
    model=MODEL,
    max_tokens=400,
    system="You are a concise threat intelligence writer.",
    messages=[{
        "role": "user",
        "content": "Write a 3-sentence executive summary of the Log4Shell vulnerability (CVE-2021-44228) for a non-technical board."
    }]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
print("\n")

print("=" * 60)
print("API lesson complete.")
print("Next: Lesson 4.4 — RAG to ground Claude's answers in your own documents.")
