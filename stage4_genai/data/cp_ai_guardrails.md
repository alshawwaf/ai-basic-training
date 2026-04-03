# Check Point AI Guardrails

## Overview

AI Guardrails defends LLM-powered applications against prompt injection, jailbreaks, sensitive data extraction, and toxic or harmful content generation. As organisations deploy customer-facing chatbots, internal knowledge assistants, and AI-powered workflows, the LLMs behind these applications become attack targets. AI Guardrails provides a real-time scanning layer that inspects both inbound prompts and outbound responses to enforce application-level security policies.

## Architecture

AI Guardrails operates as a bidirectional inspection layer integrated into the LLM application pipeline:

- **Inbound scanning (user to LLM):** Analyses user prompts before they reach the model, detecting prompt injection attempts, jailbreak patterns, and requests designed to extract training data or system prompts
- **Outbound scanning (LLM to user):** Inspects model responses before delivery, catching sensitive data leakage, toxic content, policy violations, and hallucinated outputs that could cause harm

This dual-direction architecture ensures that both the input and output of the LLM are subject to security controls, with end-to-end scanning latency of approximately 20-50 milliseconds.

## Detection Methods

| Method | Description |
|--------|-------------|
| Pattern Matching | Identifies known prompt injection templates, jailbreak phrases, and common bypass techniques using signature-based rules |
| NLP Classification | ML classifiers trained on labelled datasets of malicious and benign prompts to detect novel attack variants |
| Semantic Analysis | Embedding-based comparison that detects prompts with similar intent to known attacks, even when phrasing is significantly altered |
| Contextual Analysis | Evaluates the full conversation context — not just individual messages — to detect multi-turn attacks that gradually escalate toward a policy violation |

## Threat Categories

- **Prompt injection:** Attacker-crafted input that overrides the application's system prompt or instructions
- **Jailbreaks:** Techniques that bypass the model's safety alignment to produce restricted content
- **Data extraction:** Prompts designed to leak the system prompt, training data, or retrieval-augmented context
- **Toxic content generation:** Manipulation of the model into producing harmful, biased, or offensive output

## Deployment

AI Guardrails integrates via API into existing LLM application architectures — no changes to the underlying model are required. It supports major LLM providers and self-hosted models, inserting as a middleware layer between the application and the model endpoint.
