# Vector Databases: Why They Exist and How They Work


---

## What You Will Learn

- What a vector database is and what problem it solves
- The two-step pattern: **INDEX** once, **SEARCH** many times
- Why semantic search beats keyword search for unstructured text
- When to use a vector database and when not to

---

## Concept: From Embeddings to Search

In **Lesson 4.1** you learned that sentence embeddings place text into a high-dimensional space where similar meaning = nearby coordinates. In **Lesson 4.2** you encoded sentences and measured cosine similarity between them.

That is powerful for comparing a handful of sentences. But what happens when you have **millions** of them and need to ask: *"which ones are nearest to this query?"*

That is what a **vector database** (Pinecone, Weaviate, Qdrant, Chroma, FAISS, pgvector, ...) is for.

---

## Concept: What Is a "Document"?

In vector-DB land, a **document** is just **one piece of text you want to be searchable**. It is not necessarily a Word file or a PDF:

| Real thing | What gets stored as a "document" |
|---|---|
| A 200-page incident response playbook | Each **paragraph** or section becomes one document &mdash; chopping the file up is called *chunking* (next step) |
| A SOC ticket | The ticket **summary + description** as a single document |
| A Slack message | One **message** = one document |
| A firewall log line | One **log entry** = one document |
| A knowledge-base article | The article **title + body** as one document, or each section as its own |

The rule of thumb: a document is *whatever sized chunk of text you want the search to return as a single hit*. Smaller chunks (a paragraph) give precise, focused answers. Larger chunks (a whole page) give more context but noisier matches.

---

## Concept: How Documents Get Placed

An **embedding model** &mdash; a small neural network already trained on billions of sentences &mdash; converts each document into a fixed-length list of numbers. Those numbers **are** the coordinates:

```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

vec = model.encode("Ransomware encrypted the file server")
# array([ 0.0421, -0.0837, 0.1129, ..., -0.0218])   384 numbers
```

Same text in &rarr; same vector out, every time. It is deterministic, one-way, and **already trained** &mdash; you do not train anything yourself, you just call `.encode()`.

The embedding model was trained on billions of sentences from the public internet, so it has learned that words like *malware*, *encrypted*, and *ransom* tend to appear in the same contexts &mdash; and that is why threat-related documents end up clustered together without anyone telling the database what "threat" means.

---

## Concept: Step 1 &mdash; INDEX (done once)

Every document is converted to a vector **once** and stored in the database. Documents that talk about the same thing land near each other **automatically** &mdash; nobody told the database that ransomware and SQL injection are both threats. The clustering is a free side effect of the embedding model.

<div class="lecture-visual">
  <img src="/static/lecture_assets/gn_vector_db_index.png" alt="A 2D scatter plot showing 12 documents as coloured dots. Five red dots labelled with security threat sentences cluster in the upper left. Four cyan dots labelled with network operations sentences cluster in the upper right. Three grey dots labelled with unrelated sentences cluster in the lower middle. Title: STEP 1 INDEX every document becomes a point in space, similar meaning means nearby coordinates.">
  <div class="vis-caption">Every document becomes a point in high-dimensional space. Similar meaning = nearby coordinates. The five threat documents cluster together, the network operations cluster together, and the unrelated sentences sit far away. Nobody labelled any of this &mdash; the structure emerged from the embedding model.</div>
</div>

---

## Concept: Step 2 &mdash; SEARCH (done every query)

At query time the user's question gets encoded with the **same** embedding model and dropped onto the same map. The database returns the **K closest dots** by distance &mdash; those are the most semantically similar documents. **That is the entire algorithm.**

<div class="lecture-visual">
  <img src="/static/lecture_assets/gn_vector_db_search.png" alt="The same scatter plot with all documents dimmed. A violet star labelled 'query: How do I detect ransomware on a host?' is placed inside the threat cluster. Gold rings highlight the three nearest documents and arrows point to them, labelled #1, #2, #3. Title: STEP 2 SEARCH encode the query, return top-K nearest.">
  <div class="vis-caption">The violet star is the user's query, embedded with the same model. The database returns the 3 nearest documents by cosine distance. That is the entire vector-DB lookup.</div>
</div>

---

## Concept: Keyword Search vs Semantic Search

A SQL `WHERE text LIKE '%ransomware%'` only finds documents containing the literal word "ransomware". It would miss every one of these:

| Document text | Contains "ransomware"? | Found by vector search? |
|---|---|---|
| "Files were encrypted and a ransom note appeared" | No | **Yes** &mdash; same semantic region |
| "Encryption malware demanding bitcoin payment" | No | **Yes** &mdash; synonym cluster |
| "Cryptolocker variant detected on host" | No | **Yes** &mdash; specific family name |

A vector database returns all of them because their **embeddings are close to "ransomware"** even though the surface words are different. This is the difference between **keyword search** and **semantic search**.

---

## Concept: When to Use a Vector Database

| You have | Use a vector DB? |
|---|---|
| 50 internal policy PDFs and want a chatbot to answer questions about them | **Yes** &mdash; this is the canonical use case (RAG) |
| 10 million SOC tickets you want to find "things like this one" in | **Yes** &mdash; semantic similarity over a huge corpus |
| A structured table of users with `user_id`, `email`, `last_login` | **No** &mdash; that is a normal SQL query, no embeddings needed |
| Real-time stream of 100k events/sec for exact rule matching | **No** &mdash; use a SIEM / Sigma rules; vector search is too slow |

---

## Concept: The API &mdash; Two Functions

The entire interface is two operations:

```python
# INDEX time -- done once per document
vec = embedding_model.encode("Ransomware encrypted the file server")
vector_db.upsert(id="ticket-4291", vector=vec, metadata={"severity": "high"})

# QUERY time -- done on every user question
query_vec = embedding_model.encode("How do I detect ransomware on a host?")
hits = vector_db.search(vector=query_vec, top_k=3)
# [{"id": "ticket-4291", "score": 0.91, "metadata": {...}}, ...]
```

**upsert** (write a vector) and **search** (find K nearest vectors). Everything else &mdash; RAG, semantic cache, dedup, recommendation &mdash; is built on these two calls.

<div class="md-callout md-callout-red">
  <strong>Mental model:</strong> a vector DB is just <em>"a regular database where the index is the geometry of meaning."</em> The database itself is not smart &mdash; the embedding model is. The DB just stores points and finds the closest ones very fast, even when there are billions of them.
</div>

---

## What's Next

The next three steps build on this foundation:

| Step | What you will build |
|---|---|
| **Document Chunking** | Split long documents into embeddable pieces (the "documents" that get indexed) |
| **Retrieval** | Encode chunks and retrieve top-k for a query &mdash; the SEARCH step in code |
| **Full RAG Pipeline** | Retrieve + augment the LLM prompt + generate a grounded answer |
