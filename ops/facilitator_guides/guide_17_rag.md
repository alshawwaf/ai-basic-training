# Facilitator Guide — Session 4.4: RAG (Retrieval-Augmented Generation)

> **Stage:** 4  |  **Week:** 12  |  **Lecture deck:** `Lecture-17-RAG.pptx`  |  **Total time:** 60 min

---

## Pre-Session Checklist

- [ ] Reviewed the lecture slides and all 3 exercise guides
- [ ] Run through the chunking exercise — confirmed all three strategies (fixed-size, overlap, sentence-boundary) produce sensible chunks from the Mimikatz sample document
- [ ] Run through the retrieval exercise — confirmed that queries return relevant chunks from the security knowledge base, and that irrelevant queries rank low
- [ ] Run through the full RAG pipeline exercise — confirmed the LLM generates an answer grounded in the retrieved context, citing specific details from the knowledge base
- [ ] Prepared a whiteboard-ready diagram of the RAG pipeline: Question → Embed → Retrieve top-k chunks → Inject into prompt → LLM generates grounded answer

---

## Session Flow

| Time | Section | Activity |
|------|---------|----------|
| 0:00 – 0:05 | Bridge from LLM APIs | "Last session, we called LLMs via API and got impressive results. But the model only knows what was in its training data. Ask it about your internal CVE database, your runbooks, your incident history — and it guesses. Today, we fix that." |
| 0:05 – 0:15 | With vs without RAG | Show two examples side by side. Without RAG: ask the LLM about a specific internal threat (e.g., "What is our remediation procedure for Log4Shell?") — it gives a generic, possibly wrong answer. With RAG: the same question, but relevant document chunks are injected into the prompt — the answer is specific, accurate, and cites your own sources. Draw this on the whiteboard as two flows: direct question → hallucination vs question → retrieve → grounded answer. |
| 0:15 – 0:25 | The RAG pipeline | Walk through the four stages: (1) Chunk — split documents into digestible pieces; (2) Embed — convert each chunk into a vector using a sentence embedding model; (3) Retrieve — given a query, embed it and find the most similar chunks via cosine similarity; (4) Generate — pass the retrieved chunks as context to the LLM and ask it to answer based only on the provided information. Emphasise that participants already know steps 2 and 3 from the HuggingFace session. |
| 0:25 – 0:30 | Chunking strategies | Explain why chunking matters: too large and the embedding loses specificity, too small and you lose context. Walk through three strategies: fixed-size (simple, fast), overlapping windows (preserves context at boundaries), and sentence-boundary splitting (respects natural breaks). The exercise compares all three. |
| 0:30 – 0:50 | Hands-on exercises | Participants work through Exercises 1-3: document chunking (three strategies on a Mimikatz article), retrieval (embedding and querying a security knowledge base), and the full RAG pipeline (chunk → embed → retrieve → generate). Circulate and help — the final exercise requires both a sentence-transformer model and an LLM API key. |
| 0:50 – 0:55 | Grounding and the capstone | Discuss grounding: RAG doesn't eliminate hallucination, but it dramatically reduces it by giving the model source material to draw from. The model can still misinterpret or over-generalise, so human review remains essential. Then preview the capstone: "The Stage 4 project ties everything together — you'll build a security assistant grounded in your own threat intel. This is the demo kit you can take into customer conversations." |
| 0:55 – 1:00 | Wrap-up and programme reflection | This is the final lecture session. Acknowledge the journey: "In Stage 1, you didn't know what a feature vector was. Now you're building RAG pipelines. That's real, demonstrable expertise." Preview the capstone project and any remaining programme milestones. |

---

## Key Points to Emphasise

1. **RAG grounds LLM answers in your own data** — instead of relying on the model's training data (which may be outdated, generic, or wrong for your domain), RAG retrieves relevant chunks from your knowledge base and injects them into the prompt. The model's job becomes summarising and reasoning over your data, not recalling from memory. This is the single most practical pattern for enterprise AI.
2. **Chunking is where most RAG pipelines succeed or fail** — if chunks are too large, embeddings become vague and retrieval returns irrelevant results. If chunks are too small, the LLM lacks enough context to produce a useful answer. Overlapping windows and sentence-boundary splitting are practical defaults, but the right strategy depends on your document structure.
3. **RAG reduces hallucination but does not eliminate it** — the model can still misinterpret retrieved text, combine chunks incorrectly, or fill gaps with invented details. Always include source references in the prompt template so the model cites its sources. Human review of LLM-generated answers remains essential, especially for security-critical decisions.

---

## Discussion Prompts

- "Your SOC has 500 runbook documents. An analyst types 'How do we respond to a ransomware incident?' into your RAG-powered assistant. Walk through exactly what happens — from the query to the answer — at each stage of the pipeline."
- "You build a RAG system over your CVE database. It works well for Log4Shell and Mimikatz but returns poor results for a brand-new zero-day. Why? What are the limitations of RAG when the knowledge base doesn't contain the answer?"
- "A manager asks: 'Why can't we just give the LLM all our documents in one big prompt instead of building this retrieval pipeline?' What's your answer?"

---

## Common Questions and Answers

**Q: How is RAG different from just pasting documents into the prompt?**
A: Token limits are the practical constraint. LLMs have a maximum context window — even the largest models cap out at tens of thousands of tokens. A real knowledge base might contain millions of tokens across hundreds of documents. RAG solves this by retrieving only the most relevant chunks for each query, keeping the prompt within the model's context window while ensuring the answer draws from the right source material.

**Q: How many chunks should I retrieve (what is the right top-k)?**
A: There is no universal answer — it depends on chunk size, context window, and how much redundancy exists in your knowledge base. A common starting point is 3-5 chunks. Too few and you risk missing relevant information; too many and you dilute the context with noise (and consume token budget). The retrieval exercise lets participants experiment with different values and see the impact on answer quality.

**Q: Can I use RAG with a local model instead of a cloud API?**
A: Absolutely. The embedding step (chunking + cosine similarity search) already runs locally using `SentenceTransformer`. For the generation step, you can replace the cloud API call with a locally hosted model via Ollama. The entire pipeline — embedding, retrieval, and generation — can run on-premises with no data leaving your network. This is the architecture many security teams choose for sensitive data.

---

## Facilitator Notes

- The chunking exercise (Exercise 1) is pure Python with no API key required. It's a good warm-up that builds intuition before the heavier exercises. Have participants compare the three chunking strategies on the same document and discuss which produces the most useful chunks for retrieval.
- The retrieval exercise (Exercise 2) connects directly to the semantic search exercise from Session 4.2 (HuggingFace). Call back to that experience: "You've already done the hard part — embedding and cosine similarity. RAG retrieval is just semantic search with a purpose."
- The full RAG pipeline exercise (Exercise 3) is the climax of Stage 4. It requires both a sentence-transformer model and an LLM API key. If any participant lacks an API key, pair them with a neighbour. When the pipeline produces a grounded answer with citations, pause and compare it to a direct LLM response without retrieval — the difference is the "aha moment."
- This is the last lecture session in the programme. Take a moment at the end to acknowledge progress and build confidence. Participants have gone from zero ML knowledge to building a RAG pipeline — that's a significant achievement.

---

## Connections to Sales Conversations

- **When a customer asks:** "How can AI help our SOC without replacing our analysts or sending our data to the cloud?"
- **You can now say:** "RAG is the answer to that exact question. It lets you build an assistant that's grounded in your own runbooks, CVE database, and threat intelligence — so analysts get relevant, cited answers instead of generic guesses. The entire pipeline can run on-premises: the embedding model and the LLM both run locally, so no data leaves your network. It doesn't replace your analysts — it gives them instant access to your collective knowledge base. I can demo a working prototype that does exactly this."
