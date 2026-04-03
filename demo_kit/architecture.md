# RAG Architecture: Security Analyst Assistant

## What is RAG?

Retrieval-Augmented Generation (RAG) is an architecture that grounds LLM responses in retrieved source documents rather than relying solely on the model's training data. It combines the reasoning ability of a large language model with the accuracy of a curated knowledge base.

**Why not just use a raw LLM?** General-purpose LLMs hallucinate. They generate plausible-sounding answers that may contain fabricated event IDs, incorrect MITRE mappings, or outdated remediation steps. In security operations, a wrong answer is worse than no answer.

**Why not just use keyword search?** Search engines return documents, not answers. An analyst searching for "detect lateral movement" gets a list of links — they still have to read, cross-reference, and synthesise. RAG does that synthesis automatically.

## The 4-Stage Pipeline

| Stage | What Happens | Technology |
|-------|-------------|------------|
| 1. Chunk | Source documents are split into overlapping passages (default 500 tokens, 50-token overlap) | Python text splitter |
| 2. Embed | Each chunk is converted to a dense vector (384-dimensional) | `sentence-transformers` (`all-MiniLM-L6-v2`) |
| 3. Retrieve | The user query is embedded and compared against all chunk vectors using cosine similarity; top-k most relevant chunks are returned | `numpy` cosine similarity |
| 4. Generate | Retrieved chunks are injected into the LLM prompt as context; the model generates an answer grounded only in those chunks | Claude, GPT, or Gemini via API |

## Data Flow

```
User query
    |
    v
[Embed query] --> [Cosine similarity search against chunk vectors]
                          |
                          v
                  [Top-k chunks retrieved]
                          |
                          v
              [System prompt + retrieved chunks + user query]
                          |
                          v
                  [LLM generates grounded answer]
                          |
                          v
                  Answer returned to user
```

## Security Considerations

| Concern | How RAG Addresses It |
|---------|---------------------|
| Data residency | All documents stay local. Embeddings are computed on the host machine. No data is sent to third parties for indexing. |
| Model training | Commercial LLM APIs (Claude, GPT, Gemini) do not train on API inputs. Your documents are not absorbed into the model. |
| Air-gapped deployment | Replace the cloud LLM with Ollama running a local model (e.g. Llama 3, Mistral). The entire pipeline runs offline. |
| Access control | The retrieval layer can be extended with document-level permissions so users only retrieve chunks they are authorised to see. |

## Production Scaling Path

| Component | Demo (Current) | Production |
|-----------|---------------|------------|
| Vector store | In-memory numpy array | Chroma, Qdrant, or Weaviate |
| Embedding model | `all-MiniLM-L6-v2` (384-dim) | `bge-large-en-v1.5` (1024-dim) or domain-fine-tuned model |
| Retrieval | Cosine similarity, top-k | Hybrid search (dense + BM25) with cross-encoder reranking |
| Corpus size | 5 documents | Thousands of runbooks, threat reports, and advisories |
| Interface | CLI | Web UI with authentication, audit logging, and citation links |
