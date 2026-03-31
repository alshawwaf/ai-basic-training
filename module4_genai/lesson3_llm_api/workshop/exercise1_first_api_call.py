# =============================================================================
# LESSON 4.3 | WORKSHOP | Exercise 1 of 4
# Your First LLM API Call
# =============================================================================
# WHAT YOU WILL LEARN
# -------------------
# - The structure of an LLM API request: system, messages, max_tokens
# - How to read and print the model's response
# - How token limits affect response completeness
#
# RUN THIS FILE
# -------------
#   python module4_genai/lesson3_llm_api/workshop/exercise1_first_api_call.py
#
# REQUIRES: at least one API key set in environment:
#   set ANTHROPIC_API_KEY=...   (Claude — recommended)
#   set OPENAI_API_KEY=...      (OpenAI)
#   set GOOGLE_API_KEY=...      (Gemini)
# =============================================================================

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from llm_client import get_client

# =============================================================================
# BACKGROUND
# =============================================================================
# Every LLM chat API call has the same shape:
#
#   client.chat(
#       system   = "You are ...",           # sets persona — not shown to user
#       messages = [{"role": "user",        # conversation history
#                    "content": "..."}],
#       max_tokens = 200,                   # hard cap on output length
#   )
#
# The return value is a plain string: the model's reply.
# 100 tokens ≈ 75 words.

# =============================================================================
# TASK 1 — Load the client
# =============================================================================
# Call get_client() and store the result in (provider, client).
# If client is None (no API key found), exit with:
#   print("No API key found. Set ANTHROPIC_API_KEY, OPENAI_API_KEY, or GOOGLE_API_KEY.")
#   exit(1)
#
# Print:
#   "Provider: [provider name]"
#   "Client loaded successfully."
#
# EXPECTED OUTPUT:
#   Provider: claude
#   Client loaded successfully.

# >>> YOUR CODE HERE


# =============================================================================
# TASK 2 — First call: ask about a security concept
# =============================================================================
# Call client.chat() with:
#   system   = "You are a concise cybersecurity instructor."
#   messages = [{"role": "user", "content": "What is lateral movement? Explain in 2 sentences."}]
#   max_tokens = 150
#
# Print the question and the response:
#   "Q: What is lateral movement? Explain in 2 sentences."
#   "A: [response]"
#
# EXPECTED OUTPUT (will vary):
#   Q: What is lateral movement? Explain in 2 sentences.
#   A: Lateral movement refers to techniques attackers use to progressively move
#      through a network after gaining initial access...

# >>> YOUR CODE HERE


# =============================================================================
# TASK 3 — Analyse a security log entry
# =============================================================================
# Send this log entry to the model and ask for a threat analysis:

LOG_ENTRY = "Failed login for root from 45.33.32.156 (198 attempts in 60 seconds)"

# Call client.chat() with:
#   system   = "You are a SOC analyst. When given a log entry, identify the threat
#               type, severity (Critical/High/Medium/Low), and one recommended action.
#               Be concise — 3 bullet points maximum."
#   messages = [{"role": "user", "content": f"Analyse this log entry:\n{LOG_ENTRY}"}]
#   max_tokens = 200
#
# Print the log and the analysis.
#
# EXPECTED OUTPUT (will vary):
#   Log: Failed login for root from 45.33.32.156 (198 attempts in 60 seconds)
#   Analysis:
#   • Threat: SSH brute-force attack (MITRE T1110)
#   • Severity: High
#   • Action: Block IP 45.33.32.156 at firewall; review successful logins from this IP

# >>> YOUR CODE HERE


# =============================================================================
# TASK 4 — Token limit experiment (BONUS)
# =============================================================================
# Make the same log analysis request twice:
#   - Once with max_tokens=50
#   - Once with max_tokens=400
#
# Print both responses side by side.
# Observe: at 50 tokens the response is cut mid-sentence.
# At 400 tokens it is complete with room to spare.

# >>> YOUR CODE HERE


print("\n--- Exercise 1 complete. Move to exercise2_system_prompts.py ---")
