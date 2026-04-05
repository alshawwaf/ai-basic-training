# Demo Script: Security Analyst Assistant (5 minutes)

## The Problem (0:00 - 0:30)

> "A typical SOC analyst spends 30-40% of their shift on enrichment — searching wikis, scrolling through runbooks, cross-referencing MITRE ATT&CK. That's time not spent on actual investigation.
>
> You might think a general-purpose LLM could help, but raw LLMs hallucinate — they'll confidently give you a detection rule that references event IDs that don't exist. And a search engine can find documents, but it can't synthesise an answer across three runbooks and a threat intel report.
>
> We need something that combines the reasoning of an LLM with the accuracy of your own trusted documentation."

## How RAG Solves It (0:30 - 1:30)

> "This is Retrieval-Augmented Generation — RAG. It's a four-step pipeline."

Walk through the pipeline:

| Step | What Happens | Plain Language |
|------|-------------|----------------|
| 1. Chunk | Documents are split into small, overlapping passages | "We break your runbooks into bite-sized pieces" |
| 2. Embed | Each chunk is converted to a numerical vector | "We give each piece a mathematical fingerprint" |
| 3. Retrieve | The user's question is embedded and matched to the closest chunks | "We find the pieces most relevant to the question" |
| 4. Generate | The LLM answers using only the retrieved chunks as context | "The AI writes an answer grounded in your actual docs — not its training data" |

> "The key insight: the LLM never answers from memory. It only uses what we retrieve. That's what eliminates hallucination."

## Live Demo (1:30 - 4:00)

### Query 1: Multi-document retrieval

Type into the assistant:
```
What is credential dumping and how do I detect it?
```

**Talking points:**
- Point out that the answer pulls indicators from the credential dumping guide — LSASS access, SAM export, DCSync.
- Highlight that it includes specific Sysmon event IDs and MITRE technique IDs.
- Note: "Every fact in this answer traces back to a document your team wrote."

### Query 2: Runbook-style response

Type into the assistant:
```
We detected lateral movement via PsExec in our environment. Walk me through the response steps.
```

**Talking points:**
- The assistant returns a structured response action sequence.
- It references specific detection indicators (service name PSEXESVC, Event 7045).
- "This is the kind of answer that would take a junior analyst 15 minutes of searching. The assistant returns it in seconds."

### Query 3: Threat technique lookup

Type into the assistant:
```
What techniques can attackers use to maintain persistence on Windows?
```

**Talking points:**
- The answer covers scheduled tasks, registry Run keys, WMI subscriptions, startup folder, and service creation.
- MITRE ATT&CK IDs are included for each technique.
- "Notice it maps directly to your detection rules — the analyst can go from question to actionable detection in one step."

### Query 4: Out-of-scope handling

Type into the assistant:
```
How do I detect SQL injection attacks?
```

**Talking points:**
- The assistant should indicate it doesn't have enough context to answer confidently (no SQLi document in the corpus).
- "This is a feature, not a bug. The system knows what it knows and what it doesn't. It won't make something up."

## Value and Next Steps (4:00 - 5:00)

> "What you've just seen is a working prototype built on five detection guides. Now imagine this loaded with your full runbook library — hundreds of documents covering every alert type your SOC handles.
>
> To scale this to production, the path looks like this:
> 1. **Expand the corpus** — add your runbooks, threat intel, and compliance docs.
> 2. **Add a vector database** — swap the in-memory search for something like Chroma or Qdrant for persistent, fast retrieval.
> 3. **Deploy internally** — this can run entirely on-premise. No data leaves your network. With Ollama, it can even run air-gapped.
>
> The assistant gets smarter every time your team writes a new runbook. Your documentation becomes a living, queryable knowledge base."
