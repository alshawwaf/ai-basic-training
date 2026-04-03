# Facilitator Guide — Session 4.3: Working with LLM APIs

> **Stage:** 4  |  **Week:** 12  |  **Lecture deck:** `Lecture-16-LLM-API.pptx`  |  **Total time:** 60 min

---

## Pre-Session Checklist

- [ ] Reviewed the lecture slides and all 4 exercise guides
- [ ] Confirmed at least one API key is working: `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, or `GOOGLE_API_KEY` — the exercises use `llm_client.py` which auto-detects whichever key is set
- [ ] Run through all 4 exercises end-to-end — confirmed API calls return valid responses, structured JSON output parses correctly, and multi-turn conversation maintains context
- [ ] Prepared a whiteboard-ready diagram of the messages array pattern: `[{role: system, content: ...}, {role: user, content: ...}, {role: assistant, content: ...}]`

---

## Session Flow

| Time | Section | Activity |
|------|---------|----------|
| 0:00 – 0:05 | Bridge from HuggingFace | "Last session, we ran models locally — small, fast, and private. Today, we call much larger models via API. Billions of parameters, hosted in the cloud. More capable, but now your data travels over the wire. Let's understand the trade-off and the pattern." |
| 0:05 – 0:15 | The API pattern: messages array | Draw the messages array on the whiteboard. Every LLM API uses the same core pattern: a list of message objects with `role` (system/user/assistant) and `content`. The system message sets behaviour, user messages are your input, assistant messages are the model's replies. Walk through a concrete example: analysing a log entry. |
| 0:15 – 0:20 | System prompts | Explain that the system prompt is the most powerful lever you have. It defines the model's persona, constraints, and output format. Show two examples side by side: the same log entry analysed with a generic system prompt vs a security-analyst system prompt. The difference in output quality is dramatic. |
| 0:20 – 0:25 | Structured JSON output | Explain the challenge: LLMs return free text by default. For integration into pipelines (SIEMs, ticketing systems, dashboards), you need structured data. Show how a well-crafted system prompt plus explicit JSON schema instructions reliably produce parseable output. Mention `json.loads()` as the validation step. |
| 0:25 – 0:30 | Multi-turn conversations | Explain how conversation history works: you send the entire message history with each API call. The model itself is stateless — context comes from the growing messages array. This enables progressive analysis: first message provides a log, second asks for IOCs, third asks for recommended actions. |
| 0:30 – 0:50 | Hands-on exercises | Participants work through Exercises 1-4: first API call, system prompt design, structured JSON output, and multi-turn conversation. Circulate and help — watch for API key issues. If a participant has no API key, they can pair with a neighbour or use Ollama locally. |
| 0:50 – 0:55 | Provider comparison and data sensitivity | Briefly compare providers: Claude (Anthropic), GPT (OpenAI), Gemini (Google), Ollama (local). Key decision factors: capability, cost, data residency, and compliance. Ask: "If you're analysing customer incident data, which provider option matters most?" (Data residency and terms of service.) |
| 0:55 – 1:00 | Wrap-up | Preview Session 4.4 (RAG). Key bridge: "LLMs are powerful but they only know what was in their training data. What if you need answers grounded in your own threat intel, your CVE database, your runbooks? That's RAG — and it brings everything together." |

---

## Key Points to Emphasise

1. **The messages array is the universal API pattern** — whether you use Claude, GPT, Gemini, or a local model via Ollama, the structure is the same: a list of role/content message objects. Learn this pattern once and you can switch providers with minimal code changes. This is the single most practical skill in the GenAI toolkit.
2. **System prompts are your primary control mechanism** — the system message defines the model's expertise, tone, constraints, and output format. A well-designed system prompt is the difference between a generic chatbot and a useful security analysis tool. Treat prompt design as engineering, not guesswork.
3. **Structured output makes LLMs pipeline-ready** — free-text responses are useful for humans but useless for automation. By instructing the model to return JSON with a specific schema, you can feed LLM output directly into SIEMs, ticketing systems, or dashboards. The structured output exercise demonstrates this end-to-end.

---

## Discussion Prompts

- "You're building an internal tool that analyses firewall logs with an LLM. Your CISO asks: 'Where does our data go when you make an API call?' Walk through the data flow and the controls you'd put in place."
- "You write a system prompt that says 'You are a senior SOC analyst.' Your colleague writes one that says 'You are a helpful assistant.' You both send the same log entry. How would the outputs differ, and why does this matter for production tools?"
- "Your structured JSON output exercise returns valid JSON 95% of the time but fails 5% of the time. What do you do? How do you make this robust enough for a production pipeline?"

---

## Common Questions and Answers

**Q: Which LLM provider should I use for security work?**
A: It depends on your constraints. For the highest capability, Claude (Anthropic) and GPT-4 (OpenAI) are the current leaders. For data sovereignty — when logs and incident data must not leave your environment — Ollama lets you run open-source models locally with no external API calls. For cost-sensitive batch processing, smaller models or Gemini may be more economical. Start by clarifying your data sensitivity and compliance requirements; that narrows the field immediately.

**Q: Is it safe to send security logs to an LLM API?**
A: Treat LLM API calls like any third-party data transfer. Read the provider's data usage policy: does the provider train on your data? (Most enterprise tiers do not, but verify.) Use TLS for transit encryption. Redact sensitive fields (credentials, PII, customer identifiers) before sending. For highly sensitive data, use a locally hosted model via Ollama — no data leaves your network. Document your data handling in your security policy.

**Q: Why do I need to send the full conversation history every time? Doesn't the model remember?**
A: LLM APIs are stateless — each request is independent. The model has no memory between calls. To maintain a conversation, you append each new exchange (user message + assistant response) to the messages array and send the full array with every request. This is why token limits matter: a long conversation eventually exceeds the model's context window. For long analyses, you may need to summarise earlier turns to stay within limits.

---

## Facilitator Notes

- API key setup is the most common friction point. Have participants verify their key works before the hands-on block. If anyone is stuck, pair them with a neighbour who has a working key. The `llm_client.py` helper auto-detects keys, which reduces setup complexity.
- The system prompt exercise (Exercise 2) is the most eye-opening for participants. When they see the same log entry produce dramatically different analyses depending on the system prompt, the concept of prompt engineering clicks. Project two outputs side by side and discuss as a group.
- The structured output exercise (Exercise 3) often generates discussion about reliability. When `json.loads()` fails on a response, use it as a teaching moment: "This is why production systems need validation, retry logic, and fallback handling. The model is probabilistic, not deterministic."
- The multi-turn conversation exercise (Exercise 4) builds a progressive incident analysis. Walk through the first two turns as a group, then let participants continue independently. The growing context window is visible — participants see the messages array getting longer with each turn.

---

## Connections to Sales Conversations

- **When a customer asks:** "We want to use AI for threat analysis, but we can't send our data to the cloud."
- **You can now say:** "That's a common and valid concern. There are multiple deployment options. For the most sensitive data, you can run open-source models locally — same API pattern, zero data exfiltration risk. For less sensitive workloads, enterprise API tiers from providers like Anthropic and OpenAI include contractual guarantees that your data is not used for training. The key is matching the deployment model to your data classification. I can walk you through the options and help you design an architecture that satisfies your compliance requirements."
