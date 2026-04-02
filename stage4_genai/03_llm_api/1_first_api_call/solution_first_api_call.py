# Exercise 1 — Your First LLM API Call
#
# Demonstrates the chat API structure: system prompt, messages, max_tokens.
# Works with Claude, OpenAI, Gemini, or Ollama -- whichever you have configured.
#
# Set ONE of:
#   set ANTHROPIC_API_KEY=...
#   set OPENAI_API_KEY=...
#   set GOOGLE_API_KEY=...
#   set OLLAMA_MODEL=huihui_ai/qwen3.5-abliterated:2B

import sys
import os

# Import the shared LLM client (one directory up from )
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from llm_client import get_client

# ============================================================
#   TASK 1: Load the client
# ============================================================
print("=" * 60)
print("  TASK 1: Load the LLM Client")
print("=" * 60)

# get_client() auto-detects which API key is set and returns
# a (provider_name, client) tuple with a unified .chat() interface
provider, client = get_client()
if client is None:
    print("No API key configured. See instructions above.")
    exit(1)

print(f"\nProvider: {provider}")
print("Client loaded successfully.")


# ============================================================
#   TASK 2: First call — ask about a security concept
# ============================================================
print("\n" + "=" * 60)
print("  TASK 2: First API Call")
print("=" * 60)

# Every LLM API call has three key parameters:
#   system     — sets the model's role/persona (invisible to the user)
#   messages   — the conversation history as a list of role/content dicts
#   max_tokens — hard cap on response length (100 tokens ~ 75 words)
response = client.chat(
    system="You are a concise cybersecurity instructor.",
    messages=[{
        "role": "user",
        "content": "What is lateral movement in cybersecurity? Explain in 2 sentences.",
    }],
    max_tokens=200,
)

print(f"\nQ: What is lateral movement in 2 sentences?")
print(f"A: {response}")


# ============================================================
#   TASK 3: Analyse a log entry
# ============================================================
print("\n" + "=" * 60)
print("  TASK 3: Analyse a Log Entry")
print("=" * 60)

log_entry = "Failed login for root from 45.33.32.156 (198 attempts in 60 seconds)"

response = client.chat(
    system="You are a senior SOC analyst. Identify threats concisely.",
    messages=[{
        "role": "user",
        "content": f"Analyse this log entry and identify the threat:\n{log_entry}",
    }],
    max_tokens=300,
)

print(f"\nLog: {log_entry}")
print(f"\nAnalysis:\n{response}")


# ============================================================
#   TASK 4 (Bonus): Token limit experiment
# ============================================================
print("\n" + "=" * 60)
print("  TASK 4 (Bonus): Token Limit Experiment")
print("=" * 60)

# The same question with two different max_tokens values.
# A low limit forces the model to truncate mid-sentence.
question = "Explain the MITRE ATT&CK framework and list 5 tactics with descriptions."

for limit in [50, 400]:
    response = client.chat(
        system="You are a cybersecurity instructor.",
        messages=[{"role": "user", "content": question}],
        max_tokens=limit,
    )
    # Show response length and whether it looks complete
    word_count = len(response.split())
    truncated = "likely truncated" if limit <= 50 else "likely complete"
    print(f"\n  max_tokens={limit:>3}  |  {word_count} words  |  {truncated}")
    print(f"  Response: {response[:200]}{'...' if len(response) > 200 else ''}")

print("\nKey takeaway: max_tokens controls the hard upper limit on output length.")
print("Too low and the response is cut off mid-sentence. Too high and you pay")
print("for unused capacity. 200-600 is a good default for most security analysis.")

print("\n--- Exercise 1 complete. Move to ../2_system_prompts/solution.py ---")
