# Gate 4 Assessment — Capstone Demo Day

> **Week:** 13  |  **Duration:** 10 min per participant (5 min demo + 5 min Q&A)  |  **Format:** Live presentation  |  **Passing:** Average score of 3.0/5.0 across all criteria

---

## Overview

Each participant presents their Security Analyst Assistant (the Stage 4 capstone project) to a review panel. This is the final gate — it simulates presenting AI capabilities to a customer. You must demonstrate both technical depth and the ability to communicate AI value clearly.

---

## What to Prepare

### Your Demo

Build and customise the Stage 4 Security Analyst Assistant. At minimum, your assistant must:

1. **Load a document corpus** — at least 5 documents (CVE advisories, threat reports, runbooks, or your own security content)
2. **Chunk and embed** the documents using a sentence transformer model
3. **Retrieve** relevant chunks for a user question using cosine similarity
4. **Generate** a grounded answer using an LLM API (Claude, OpenAI, Gemini, or Ollama)
5. **Demonstrate grounding** — the answer should clearly reference the retrieved context, not hallucinate

### Your Presentation (5 minutes)

Structure your demo as a customer-facing narrative:

| Time | Section | What to Cover |
|------|---------|---------------|
| 0:00 - 0:30 | **The Problem** | What problem does this solve? Why can't a search engine or a raw LLM do it? |
| 0:30 - 1:30 | **How It Works** | Explain the RAG pipeline in plain language: chunking, embedding, retrieval, generation. Use terms from the program. |
| 1:30 - 4:00 | **Live Demo** | Run 2-3 pre-selected queries. Show the retrieved context alongside the generated answer. Show at least one query where the system correctly says "I don't have enough context to answer." |
| 4:00 - 5:00 | **Value and Next Steps** | What value does this deliver? How would you extend this for a real customer deployment? |

### Q&A Preparation (5 minutes)

The review panel will ask questions. Prepare for these common ones:

- "What happens if the answer isn't in the documents?"
- "How do you know the retrieval is returning the right chunks?"
- "What's the chunk size, and why did you choose it?"
- "Could an attacker poison the document corpus to manipulate answers?"
- "How would this scale to 10,000 documents?"
- "What's the latency? Is it fast enough for a SOC analyst in the middle of an incident?"
- "How is this different from just pasting documents into ChatGPT?"

---

## Evaluation Rubric

The review panel scores each criterion on a 1-5 scale.

### Criterion 1: Technical Depth

| Score | Description |
|-------|-------------|
| **1** | Cannot explain how RAG works. Reads from notes. Confuses components. |
| **2** | Explains RAG at a high level but cannot describe chunking, embedding, or retrieval specifically. |
| **3** | Clearly explains all 4 RAG stages (chunk, embed, retrieve, generate). Uses correct terminology. |
| **4** | Explains trade-offs: chunk size vs context quality, embedding model choice, retrieval accuracy. |
| **5** | Discusses advanced considerations: overlap strategies, reranking, hybrid search, embedding model benchmarks. |

### Criterion 2: Demo Quality

| Score | Description |
|-------|-------------|
| **1** | Demo fails to run, or produces irrelevant/hallucinated answers. |
| **2** | Demo runs but answers are generic or not clearly grounded in retrieved documents. |
| **3** | Demo runs, answers are clearly grounded. Shows retrieved context alongside the answer. |
| **4** | Pre-built queries showcase impressive, accurate results. Includes a "no context" example. |
| **5** | Demo handles edge cases gracefully. Shows comparison between with-context and without-context answers. |

### Criterion 3: Customer Readiness

| Score | Description |
|-------|-------------|
| **1** | Presentation is disorganised. Uses excessive jargon. No clear problem statement. |
| **2** | Has a structure but struggles to connect technical details to business value. |
| **3** | Clear narrative: problem, how it works, demo, value. Accessible to a non-technical stakeholder. |
| **4** | Handles Q&A confidently. Ties answers to business outcomes (time saved, accuracy improved, risk reduced). |
| **5** | Could deliver this demo to a real customer today. Reframes technical questions into business impact. Acknowledges limitations honestly. |

### Criterion 4: Code Quality and Customisation

| Score | Description |
|-------|-------------|
| **1** | Solution is an unmodified copy of the provided template. |
| **2** | Minor modifications to the template (changed a few document paths). |
| **3** | Loaded custom documents relevant to their domain. Adjusted chunk size or retrieval parameters. |
| **4** | Extended with additional features: better error handling, formatted output, source citations in answers. |
| **5** | Significant extensions: multi-document comparison, follow-up questions, evaluation metrics on retrieval accuracy, custom UI. |

---

## Scoring

| Total Score (sum of 4 criteria) | Average | Result |
|--------------------------------|---------|--------|
| 18-20 | 4.5-5.0 | Exceptional — invite to co-facilitate future cohorts |
| 14-17 | 3.5-4.25 | Strong pass |
| 12-13 | 3.0-3.25 | Pass |
| 8-11 | 2.0-2.75 | Fail — provide specific feedback, allow retake in 2 weeks |
| 4-7 | 1.0-1.75 | Fail — requires additional Stage 4 study before retake |

**Pass (average 3.0+) → Tier 3: AI Ninja**

---

## Panel Composition

| Role | Count | Responsibility |
|------|-------|---------------|
| Program tech lead | 1 | Primary evaluator, leads Q&A |
| Engineering manager or sales leader | 1-2 | Evaluates customer readiness and business relevance |
| Tier 3 graduate (optional, from prior cohort) | 1 | Evaluates technical depth from peer perspective |

---

## Logistics

| Item | Details |
|------|---------|
| **Schedule** | Each participant gets a 10-min slot (5 demo + 5 Q&A). With 12-16 participants, plan 3-4 hours with breaks. |
| **Setup** | Participants share their screen. Have a backup plan (pre-recorded demo) in case of connectivity issues. |
| **Scoring** | Each panelist scores independently on the rubric. Final score is the average across panelists. |
| **Feedback** | Each participant receives written feedback within 48 hours: scores per criterion + 2 strengths + 2 areas for improvement. |
| **Retake** | One retake allowed within 2 weeks. Participant must address the specific feedback from the first attempt. |

---

## What Exceptional Looks Like

The strongest capstone demos in previous programs shared these qualities:

- **Custom corpus that matters** — loaded their own team's runbooks, threat reports, or incident post-mortems, not generic Wikipedia articles
- **Showed the failure mode** — demonstrated a query the system can't answer and explained why (context not in corpus), proving they understand grounding
- **Compared with vs without RAG** — showed the same question answered by a raw LLM (hallucinated) vs with RAG (grounded), making the value undeniable
- **Connected to a real customer need** — "In my last engagement, the customer's SOC analysts spent 2 hours per incident on enrichment. This assistant reduces that to 30 seconds."
- **Honest about limitations** — "This prototype uses a local embedding model with 384 dimensions. Production would need a larger model and a vector database like Pinecone or Weaviate for scale."

---

## After Passing

Tier 3: AI Ninja graduates receive:

- **AI Ninja certification** recognised across the organisation
- **Customer demo kit** — their capstone project, polished and packaged for customer meetings
- **Invitation to co-facilitate** future Ninja Program cohorts
- **Alumni network access** — ongoing channel for knowledge sharing and AI developments
- **Priority access** to advanced AI training and conference opportunities
