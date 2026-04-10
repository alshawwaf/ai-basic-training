# How LLMs Work

---

## Concept: The Core Idea

An **LLM (Large Language Model)** is, at its core, a very sophisticated **next-token predictor**.

**Step 1 — break the input into tokens:**

| Position | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| Token | `The` | `attacker` | `used` | `a` | `SQL` | `injection` | `to` |

**Step 2 — the model predicts the most probable next token:**

<div class="md-flow">
  <span class="md-flow-chip md-chip-cyan">Input: 7 tokens</span>
  <span class="md-flow-arrow">&rarr;</span>
  <span class="md-flow-chip md-chip-violet">LLM</span>
  <span class="md-flow-arrow">&rarr;</span>
  <span class="md-flow-chip md-chip-amber">"exfiltrate" <small>(top prob.)</small></span>
</div>

**Step 3 — append the new token and feed it back as input. Repeat.**

| Position | 1 | 2 | 3 | 4 | 5 | 6 | 7 | **8** | next |
|---|---|---|---|---|---|---|---|---|---|
| Token | `The` | `attacker` | `used` | `a` | `SQL` | `injection` | `to` | **`exfiltrate`** | `???` |

<div class="md-callout md-callout-red">
  <strong>The loop:</strong> predict &rarr; append &rarr; predict &rarr; append. Run this billions of times on trillions of words and you get reasoning, coding, summarisation &mdash; <strong>all of it emerges from this one task</strong>.
</div>

---

## Tokens

Before any prediction happens, your text is sliced up into **tokens**. A token is **not** always one word — that is the single biggest misconception. Modern tokenizers (used by Claude, ChatGPT, and Gemini) use a scheme called **Byte-Pair Encoding (BPE)** that splits text into the most frequent reusable chunks the model has seen in training.

### Is one token = one word?

**No.** Sometimes yes, often no. Three real examples from the GPT-4 tokenizer (`cl100k_base`):

<div class="tok-example">
  <div class="tok-example-head">
    <div class="tok-example-title">Example 1 — plain English <small>5 words</small></div>
    <span class="tok-verdict tok-verdict-good">6 tokens · efficient</span>
  </div>
  <div class="tok-input">Input: <strong>"The firewall blocked malicious traffic"</strong></div>
  <div class="tok-chips">
    <span class="tok-chip"><span class="tok-chip-text">The</span><span class="tok-chip-id">791</span></span>
    <span class="tok-chip"><span class="tok-chip-text"> firewall</span><span class="tok-chip-id">50450</span></span>
    <span class="tok-chip"><span class="tok-chip-text"> blocked</span><span class="tok-chip-id">19857</span></span>
    <span class="tok-chip"><span class="tok-chip-text"> mal</span><span class="tok-chip-id">8492</span></span>
    <span class="tok-chip"><span class="tok-chip-text">icious</span><span class="tok-chip-id">9824</span></span>
    <span class="tok-chip"><span class="tok-chip-text"> traffic</span><span class="tok-chip-id">9629</span></span>
  </div>
  <div class="tok-takeaway">
    Common words land 1 token each. <strong>"malicious"</strong> is rarer and splits into <code>mal</code> + <code>icious</code>. Notice the <strong>leading space is part of the token</strong> — <code>" firewall"</code> is one token, not two.
  </div>
</div>

<div class="tok-example">
  <div class="tok-example-head">
    <div class="tok-example-title">Example 2 — security identifier <small>looks like 1 word</small></div>
    <span class="tok-verdict tok-verdict-bad">7 tokens · expensive</span>
  </div>
  <div class="tok-input">Input: <strong>"CVE-2024-1234"</strong></div>
  <div class="tok-chips">
    <span class="tok-chip"><span class="tok-chip-text">CVE</span><span class="tok-chip-id">36849</span></span>
    <span class="tok-chip"><span class="tok-chip-text">-</span><span class="tok-chip-id">12</span></span>
    <span class="tok-chip"><span class="tok-chip-text">202</span><span class="tok-chip-id">2366</span></span>
    <span class="tok-chip"><span class="tok-chip-text">4</span><span class="tok-chip-id">19</span></span>
    <span class="tok-chip"><span class="tok-chip-text">-</span><span class="tok-chip-id">12</span></span>
    <span class="tok-chip"><span class="tok-chip-text">123</span><span class="tok-chip-id">4513</span></span>
    <span class="tok-chip"><span class="tok-chip-text">4</span><span class="tok-chip-id">19</span></span>
  </div>
  <div class="tok-takeaway">
    <strong>7 tokens for what looks like 1 "word"</strong> to a human. The tokenizer has never seen this exact CVE ID, so it falls back to subword chunks. CVEs, hashes, IPs, and registry paths all behave this way.
  </div>
</div>

<div class="tok-example">
  <div class="tok-example-head">
    <div class="tok-example-title">Example 3 — uncommon compound word <small>1 word</small></div>
    <span class="tok-verdict tok-verdict-warn">2 tokens · split</span>
  </div>
  <div class="tok-input">Input: <strong>"Cybersecurity"</strong></div>
  <div class="tok-chips">
    <span class="tok-chip"><span class="tok-chip-text">Cyber</span><span class="tok-chip-id">56541</span></span>
    <span class="tok-chip"><span class="tok-chip-text">security</span><span class="tok-chip-id">17672</span></span>
  </div>
  <div class="tok-takeaway">
    The model sees it as the concept of <strong>"cyber"</strong> combined with <strong>"security"</strong> — actually a useful side effect: it can generalise from related compounds it <em>has</em> seen.
  </div>
</div>

<div class="md-callout md-callout-red">
  <strong>Rule of thumb:</strong> 1 token &approx; 4 characters of English &approx; <strong>0.75 words</strong>. So 1,000 words &approx; 1,300 tokens. Security text (CVEs, IPs, hashes, registry paths) is <strong>much heavier</strong> — often 2&ndash;3&times; more tokens than the same word count of plain English.
</div>

---

## The Context Window

Once your text is tokens, the model can only "see" a fixed number of them at once. That maximum is the **context window**. Anything beyond it is invisible to the model — as if it never existed.

| Model | Context window | Roughly equals | Source |
|---|---|---|---|
| GPT-3.5 | 16,000 tokens | ~12,000 words / ~25 pages | [OpenAI docs](https://platform.openai.com/docs/models) |
| GPT-4 Turbo | 128,000 tokens | ~96,000 words / ~200 pages | [OpenAI docs](https://platform.openai.com/docs/models) |
| **Claude Opus / Sonnet** | **200,000 tokens** | ~150,000 words / ~500 pages | [Anthropic docs](https://docs.anthropic.com/en/docs/about-claude/models) |
| Gemini 1.5 Pro | 128,000 tokens | ~96,000 words / ~200 pages | [Google AI docs](https://ai.google.dev/gemini-api/docs/models) |

**What fits in the context window?**

<div class="md-flow">
  <span class="md-flow-chip md-chip-cyan">System prompt</span>
  <span class="md-flow-arrow">+</span>
  <span class="md-flow-chip md-chip-cyan">Conversation history</span>
  <span class="md-flow-arrow">+</span>
  <span class="md-flow-chip md-chip-cyan">Your new message</span>
  <span class="md-flow-arrow">+</span>
  <span class="md-flow-chip md-chip-amber">Model's reply</span>
  <span class="md-flow-arrow">&le;</span>
  <span class="md-flow-chip md-chip-violet">Context limit</span>
</div>

Every token counts against the budget — including the model's own response. Once you hit the limit, the oldest tokens are silently dropped (or the API rejects the call).

**Why this matters for security work:**
- Pasting a 10MB log file? Won't fit. You need to **chunk** it or filter first.
- Long incident reports may exceed the window — summarise sections before passing them in.
- API pricing is **per token in + per token out**, so context window directly drives cost.
- A model that "forgets" what you told it 50 messages ago hasn't malfunctioned — it has scrolled out of the window.

<div class="md-callout md-callout-red">
  <strong>The illusion of memory:</strong> LLMs have <strong>no persistent memory</strong> between API calls. Every conversation rebuilds the entire history from scratch and feeds it back in as input tokens. The "memory" you experience in ChatGPT or Claude is the chat client re-sending the transcript every turn. When the transcript exceeds the context window, the start gets cut.
</div>

---

## Embeddings

Before tokens are processed by the model, each is converted to an **embedding** — a dense vector of hundreds of numbers that captures the token's meaning:

| Token | Vector (first 3 of 768 dims) | Notes |
|---|---|---|
| `malware` | `[0.23, -0.41, 0.88, ...]` | 768 numbers |
| `ransomware` | `[0.25, -0.38, 0.91, ...]` | similar to `malware` |
| `pizza` | `[-0.51, 0.12, -0.33, ...]` | very different |

**Semantic similarity = similar vectors.** Tokens close together in vector space share meaning. The model knows `virus` and `malware` are related without being told — it learned from context.

<div class="md-cluster-grid">
  <div class="md-cluster md-cluster-cyan">
    <div class="md-cluster-title">Security cluster <small>(close together)</small></div>
    <div><code>malware</code> <span class="md-vec">[0.23, -0.41, 0.88]</span></div>
    <div><code>ransomware</code> <span class="md-vec">[0.25, -0.38, 0.91]</span></div>
    <div><code>virus</code> <span class="md-vec">[0.21, -0.44, 0.85]</span></div>
  </div>
  <div class="md-cluster md-cluster-amber">
    <div class="md-cluster-title">Unrelated cluster <small>(far away)</small></div>
    <div><code>pizza</code> <span class="md-vec">[-0.51, 0.12, -0.33]</span></div>
    <div><code>guitar</code> <span class="md-vec">[-0.48, 0.09, -0.29]</span></div>
  </div>
</div>

---

## Vector Databases — Why They Exist and How They Work

Embeddings on their own are just numbers. The interesting thing is what happens when you put **millions** of them next to each other and ask: *"which ones are nearest to this query?"* That is what a **vector database** (Pinecone, Weaviate, Qdrant, Chroma, FAISS, pgvector, …) is for.

### First, what is a "document"?

In vector-DB land, a **document** is just **one piece of text you want to be searchable**. It is not necessarily a Word file or a PDF. It can be any of these:

| Real thing | What gets stored as a "document" |
|---|---|
| A 200-page incident response playbook | Each **paragraph** (or each section) becomes one document — chopping the file up is called *chunking* |
| A SOC ticket | The ticket **summary + description** as a single document |
| A Slack message | One **message** = one document |
| A firewall log line | One **log entry** = one document |
| A knowledge-base article | The article **title + body** as one document, OR each section as its own document |

The rule of thumb: a document is *whatever sized chunk of text you want the search to return as a single hit*. Smaller chunks (a paragraph) give precise, focused answers. Larger chunks (a whole page) give more context but noisier matches. In the diagram below each red/cyan/grey dot is one short example sentence — pretend each one is a SOC ticket title.

### How does the algorithm decide where to place a document?

The "place each document somewhere on the map" step is done by an **embedding model** — a small neural network trained on billions of sentences. You feed it text, it spits out a fixed-length list of numbers, and **those numbers ARE the coordinates**. Same text in → same vector out, every time. It's deterministic, one-way (you can't reverse the vector back into text), and **already trained** — you don't train anything yourself, you just call it.

```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

vec = model.encode("Ransomware encrypted the file server")
# → array([ 0.0421, -0.0837, 0.1129, ..., -0.0218])  ← 384 numbers
```

That array of numbers is the position of the document on the map. Every other document gets placed by running it through the same model.

**How many coordinates?** It depends on which embedding model you pick. The numbers below are the **real production values** for popular models:

| Embedding model | Dimensions (= coordinates) | Notes |
|---|---|---|
| `all-MiniLM-L6-v2` (free, runs locally) | **384** | Small, fast, good enough for most internal tools |
| OpenAI `text-embedding-3-small` | **1,536** | Cheap API, the default for most RAG apps |
| Cohere `embed-english-v3.0` | **1,024** | Strong on English |
| OpenAI `text-embedding-3-large` | **3,072** | Highest quality, more expensive |
| Llama-3 hidden state | **4,096** | What an LLM uses internally |

<div class="md-callout md-callout-red">
  <strong>The diagram below is a lie for teaching purposes.</strong> The real ransomware document doesn't live at <em>(x = &minus;3.4, y = 2.2)</em> — it lives at <strong>1,536 coordinates</strong> (or 384, or 3,072, depending on the model). We squash that high-dimensional point down to 2D using a projection technique like <strong>PCA</strong> or <strong>t-SNE</strong> just so a human can see the clusters on a flat screen. The clustering you see is real; the exact coordinates are not.
</div>

The embedding model is **also already trained** on billions of sentences from the public internet, so it has learned that words like *malware*, *encrypted*, and *ransom* tend to appear in the same contexts — and that's why the threat documents end up clustered together without anyone telling the database what "threat" means. **You don't train it. You just load it and call `.encode()`.**

### Step 1 — INDEX (done once, when you load your documents)

<p align="center">
  <img src="/static/lecture_assets/gn_vector_db_index.png" alt="A 2D scatter plot showing 12 documents as coloured dots. Five red dots labelled with security threat sentences (Ransomware encrypted file server, Phishing email, SQL injection in login form, Suspicious PowerShell process, Credential dump on a leak site) cluster in the upper left. Four cyan dots labelled with network operations sentences (Firewall rule allows port 443, Router BGP session reconverged, VPN tunnel renegotiated keys, Switch spanning-tree change) cluster in the upper right. Three grey dots labelled with unrelated sentences (Recipe for chocolate cake, Football match results, Coffee shop opening hours) cluster in the lower middle. Title: STEP 1 INDEX every document becomes a point in space, similar meaning means nearby coordinates.">
</p>

Every document is converted to a vector **once** and "drawn" onto the map. Documents that talk about the same thing land near each other **automatically** — nobody told the database that ransomware and SQL injection are both threats. The clustering is a free side effect of the embedding model. Add a new document later? Just embed it and drop a new dot on the map.

### Step 2 — SEARCH (done every time the user asks a question)

<p align="center">
  <img src="/static/lecture_assets/gn_vector_db_search.png" alt="The same scatter plot from step 1, but with all documents dimmed. A violet star labelled 'query: How do I detect ransomware on a host?' is placed inside the threat cluster. Gold rings highlight the three nearest red threat documents and gold arrows point from the query star to each of the three nearest neighbours, labelled #1 d=0.94, #2 d=1.00, #3 d=1.08. Title: STEP 2 SEARCH encode the query, return top-K nearest, this is the entire vector-DB lookup.">
</p>

At query time the user's question gets encoded with the **same** embedding model and dropped onto the same map (the violet star). The database returns the **K closest dots** by distance — those are the most semantically similar documents. **That is the entire algorithm.** The gold rings show the top-3 hits and the arrows show which dots the database returned, ordered by distance.

### Why a vector DB instead of a regular database?

A SQL `WHERE text LIKE '%ransomware%'` only finds documents that contain the literal word "ransomware". It would miss every one of these:

- *"Files were encrypted and a ransom note appeared"* (the actual incident description, no "ransomware" word)
- *"Encryption malware demanding bitcoin payment"* (synonym)
- *"Cryptolocker variant detected on host"* (specific family name)

A vector DB would return all of them, because their **embeddings are close to "ransomware"** even though the surface words are different. This is the difference between **keyword search** and **semantic search**.

### When you actually need one

| You have | Use a vector DB? |
|---|---|
| 50 internal policy PDFs and want a chatbot to answer questions about them | **Yes** — this is the canonical use case (RAG) |
| 10 million SOC tickets you want to find "things like this one" in | **Yes** — semantic similarity over a huge corpus |
| A structured table of users with `user_id`, `email`, `last_login` | **No** — that's a normal SQL query, no embeddings needed |
| Real-time stream of 100k events/sec for exact rule matching | **No** — use a SIEM / Sigma rules, vector search is too slow |

### What the API actually looks like

```python
# Index time — done once per document
vec = embedding_model.encode("Ransomware encrypted the file server")
vector_db.upsert(id="ticket-4291", vector=vec, metadata={"severity": "high"})

# Query time — done on every user question
query_vec = embedding_model.encode("How do I detect ransomware on a host?")
hits = vector_db.search(vector=query_vec, top_k=3)
# → [{"id": "ticket-4291", "score": 0.91, "metadata": {...}}, ...]
```

That's the whole interface. Two functions: **upsert** (write a vector) and **search** (find K nearest vectors). Everything else — RAG, semantic cache, dedup, recommendation — is built on those two calls.

<div class="md-callout md-callout-red">
  <strong>Mental model:</strong> a vector DB is just <em>"a regular database where the index is the geometry of meaning"</em>. The database itself isn't smart — the embedding model is. The DB just stores points and finds the closest ones, very fast, even when there are billions of them.
</div>

---

## The Transformer Architecture

Remember the next-token loop from Step 1 — *"given the words so far, predict what comes next."* The breakthrough that made modern LLMs work is the **attention mechanism**: a way for the model to decide **which earlier tokens matter most** when guessing the next one.

**Sentence so far:**

<div class="md-callout md-callout-cyan">
  <em>"The attacker exfiltrated the database to a remote&nbsp;&nbsp;___"</em>
</div>

**Step ① — The model looks at each existing token and assigns it a weight.** High-weight tokens drive the prediction; low-weight tokens are mostly ignored. *(These are the tokens that already exist in the sentence — none of them is the answer.)*

| Existing token | Attention weight | Why it matters here |
|---|---|---|
| `exfiltrated` | <span class="md-bar md-bar-cyan" style="width:90%">0.32</span> | the action — strongly implies *data going somewhere* |
| `remote` | <span class="md-bar md-bar-cyan" style="width:84%">0.30</span> | sits right before the gap — strong local cue |
| `database` | <span class="md-bar md-bar-cyan" style="width:67%">0.24</span> | the *thing* being moved — narrows the destination type |
| `attacker` | <span class="md-bar md-bar-amber" style="width:28%">0.10</span> | sets the malicious context |
| `the` / `a` / `to` | <span class="md-bar md-bar-amber" style="width:11%">0.04</span> | grammar glue, very low signal |

<div class="md-callout md-callout-violet">
  <strong>Step ② — The model fuses these weighted signals and scores <em>every word in its ~100,000-token vocabulary</em></strong> to decide what fills the blank. The answer is a brand-new token — it does <em>not</em> have to appear in the table above.
</div>

**Top candidates for the&nbsp;&nbsp;___&nbsp;&nbsp;blank:**

<div class="tok-chips">
  <span class="tok-chip"><span class="tok-chip-text">server</span><span class="tok-chip-id">62%</span></span>
  <span class="tok-chip"><span class="tok-chip-text">host</span><span class="tok-chip-id">18%</span></span>
  <span class="tok-chip"><span class="tok-chip-text">location</span><span class="tok-chip-id">12%</span></span>
  <span class="tok-chip"><span class="tok-chip-text">system</span><span class="tok-chip-id">8%</span></span>
</div>

The high-weight tokens `exfiltrated` + `database` + `remote` together make `server` the overwhelmingly likely fill — but `server` itself was pulled from the model's full vocabulary, not from the sentence. **Attention is what lets the model fuse evidence from words that may be far apart in the sentence**, so the right next-token candidate floats to the top — something the older RNN models that came before transformers could not do well.

---

## Pretraining — How the Weights Get Made

So far we have talked about the model as a finished product: tokens go in, attention runs, the next token pops out. But **where do the billions of weights come from**? Nobody types them in by hand. They are *learned* during a phase called **pretraining** — and the trick that makes it work is that pretraining needs **zero human-labelled data**.

### The self-supervised setup

The genius of pretraining is that the next-token prediction task **labels itself**. Take any sentence from the internet:

<div class="md-callout md-callout-cyan">
  <em>"The firewall blocked the malicious traffic on port 443."</em>
</div>

Hide one word, ask the model to guess it, then reveal the answer:

| Step | What happens |
|------|--------------|
| 1 | Pick a random cut point: `"The firewall blocked the malicious traffic on port ___"` |
| 2 | Ask the model: *"what comes next?"* Model outputs a probability over all ~100,000 vocabulary tokens. |
| 3 | The **actual** next token in the source text is `443`. That is the label — and it was free, because it was already in the sentence. |
| 4 | Compare prediction to truth using **cross-entropy loss**. If the model gave `443` only 0.01% probability, the loss is very high. If it gave it 60%, the loss is low. |
| 5 | Run **backpropagation** — nudge every weight in the model slightly in the direction that would have made `443` more likely next time. |
| 6 | Slide the cut point one token forward and repeat. Then move to the next sentence. Then the next document. Then the next *trillion* tokens. |

Because every position in every sentence becomes a free training example, **a 1 trillion-token corpus produces ~1 trillion training examples** — without a single human ever writing a label. This is why it is called **self-supervised** learning: the supervision signal is hidden inside the data itself.

### What the model looks like at different points in training

The same weights get nudged a little after every example. At the start, the weights are pure random noise — the model has no idea English even exists. Watch what happens to its output for the same prompt as training progresses:

| Tokens seen | Prompt: *"The firewall blocked the"* | What the model has figured out |
|---|---|---|
| **0** (random init) | `qz $$ k7 ;; xx vv` | Nothing. Output is random token IDs. |
| **1 million** | `the the the the the` | Some tokens are more frequent than others. |
| **100 million** | `the door and went home` | English-shaped noise — grammar is roughly right, content is nonsense. |
| **1 billion** | `the user from accessing the website` | Plausible English sentences, but no domain knowledge. |
| **100 billion** | `the suspicious connection and logged the event` | Domain coherence — knows what firewalls do. |
| **1 trillion+** | `the malicious traffic on port 443 and triggered alert ID 1042` | Specific, technical, contextually correct. |

Nothing changed about the architecture between rows — only the values of the billions of weights, after billions of "predict-and-correct" updates. **Reasoning, world knowledge, and coding ability are emergent side-effects of compressing this much language into the weights.**

<div class="md-callout md-callout-violet">
  <strong>Key insight.</strong> Pretraining does <em>not</em> teach the model facts directly. It teaches the model to <em>predict the next token</em>, and the facts get absorbed as a free side-effect — because to predict the next token well, the model has to implicitly know who Marie Curie was, what TCP port 443 is for, and how a SQL injection works.
</div>

### The compute cost — why nobody pretrains from scratch

The reason "just pretrain your own LLM" is not advice anyone gives you:

| Resource | Frontier LLM pretraining run (2024–2025) |
|---|---|
| Tokens consumed | 10–20 trillion |
| GPUs | ~10,000–25,000 H100s |
| Wall-clock time | 2–6 months |
| Electricity | ~50 GWh — small town for a month |
| **Estimated cost** | **~$50M–$200M** |

In practice, you consume pretrained models via API (Claude, GPT-4, Gemini) or by downloading **open-weight checkpoints** (LLaMA, Mistral, Qwen, DeepSeek). **You do not pretrain — you start from someone else's pretrained checkpoint**, optionally fine-tune on your own data (orders of magnitude cheaper), and use it.

### Pretraining vs fine-tuning vs inference

Three phases that often get confused — they happen at very different scales:

| Phase | Who does it | Cost | Frequency | What it produces |
|---|---|---|---|---|
| **Pretraining** | Big labs (OpenAI, Anthropic, Google, Meta) | $50M–$200M | Once per model generation | A "base model" that knows language |
| **Fine-tuning / RLHF** | The same labs, or you on a small open-weight model | $1k–$10M | Per dataset / per task | A model aligned to instructions or your domain |
| **Inference** | You, every time you call the API | Fractions of a cent per query | Continuous | The actual answer to your prompt |

The "ChatGPT" or "Claude" you use is a **pretrained base model + fine-tuning + RLHF** — three separate training runs stacked on top of each other. Pretraining is by far the largest and most expensive of the three.

<div class="md-callout md-callout-red">
  <strong>Why this matters in practice.</strong> When wiring an LLM into a workflow, you are <em>renting</em> the output of a $100M training run. That is also why <strong>prompts</strong> and <strong>retrieval</strong> matter so much: you can't change the weights, so the only levers you have are the tokens you put in front of the model. Every other lesson in this stage (HuggingFace, LLM APIs, RAG) is downstream of this one fact.
</div>

---

## Why LLMs Are Different from Classifiers

| Classic ML (Stages 1–3) | LLMs (Stage 4) |
|------------------------|----------------|
| Train from scratch | **Pre-trained on ~1 trillion tokens** |
| Needs labelled data | No labels needed for pre-training |
| Single specific task | General purpose |
| Hundreds of parameters | Billions of parameters |
| Inference: microseconds | **Inference: seconds** |
| Runs on laptop | Usually requires GPU or API |

Two of those rows deserve unpacking — they are the rows that *change how you architect a system around an LLM*.

### ① Pre-trained on ~1 trillion tokens

**What "pre-trained" means.** The model has *already* learned general language patterns from a massive text corpus **before you ever touch it**. You don't train it from scratch like a logistic regression — you download the finished weights and just *use* them. (You can optionally fine-tune for a specific domain, but that is a tiny fraction of the total compute.)

**What "1 trillion tokens" means.** Tokens, not words — recall ~1 token ≈ 0.75 words from the tokeniser section. So 1T tokens ≈ **750 billion words**. To put that in scale:

| Corpus | Approximate token count |
|---|---|
| All of English Wikipedia | ~4 billion |
| Every book on Project Gutenberg | ~10 billion |
| GPT-3 training set (2020) | ~300 billion |
| **A "1 trillion token" round number** | **1,000 billion** |
| LLaMA 3 (2024) | ~15 trillion |
| Modern frontier models (2025) | 10–20 trillion |

So `~1 trillion` in the table is a conservative round number — modern frontier LLMs are now trained on **10–20 trillion** tokens. The point isn't the exact figure, it's the **order of magnitude**: more text than any human could read in a thousand lifetimes. *That* is where reasoning, world knowledge, and coding ability come from — they are emergent side-effects of compressing this much language into the weights.

<div class="md-callout md-callout-violet">
  <strong>Why this matters for you.</strong> You will never reproduce this. Pre-training a frontier LLM costs ~$50M–$200M of GPU compute and weeks on thousands of H100s. In practice, you consume pre-trained models via API or by downloading open-weight checkpoints (LLaMA, Mistral, Qwen).
</div>

### ② Inference: seconds

**What "inference" means.** Running the model forward to get an answer — i.e. predicting the next token, then the next, then the next. This is distinct from *training* (learning the weights, done once) and is what happens **every time** you send a prompt.

**Why classic ML inference is microseconds.** A logistic regression on the 64-pixel digit dataset is one matrix multiply on a 64-element vector — about 64 multiplications. A modern CPU does that in **under 10 microseconds**, faster than the network round-trip to even ask for it.

**Why LLM inference is seconds.** Three compounding reasons:

| Reason | Impact |
|---|---|
| **Model size** | A 70B-parameter model holds ~140 GB in memory. Every token prediction touches a large fraction of those weights — gigabytes of memory bandwidth per token. |
| **Autoregressive generation** | The model produces **one token at a time**, then re-runs the whole forward pass to get the next one. A 200-token answer = 200 forward passes. At 50 tokens/sec that is ~4 seconds. |
| **Full transformer stack per token** | Each forward pass walks through dozens of attention layers, then scores all ~100,000 vocabulary tokens via softmax to pick the next one. |

**What this looks like in practice:**

| Model class | Tokens per second | A 200-token answer |
|---|---|---|
| Logistic regression (digits) | n/a — single shot | ~0.00001 s |
| Local 7B model on a good GPU | 30–80 | 3–7 s |
| Local 70B model on a good GPU | 5–15 | 13–40 s |
| GPT-4o / Claude Sonnet via API | 50–100 | 2–4 s |

<div class="md-callout md-callout-red">
  <strong>Why this matters in practice.</strong> A ~10⁶× slowdown vs. classic ML changes how systems are architected around LLMs:
  <ul>
    <li>You <strong>cannot</strong> put an LLM in the hot path of every log line, every email, every packet. Too slow, too expensive.</li>
    <li>LLMs belong on the <strong>triage / analysis / summarisation / report-writing</strong> side of a pipeline, not the real-time blocking side.</li>
    <li>High-volume pipelines use a <strong>cheap classifier in front of an expensive LLM</strong> — the classifier filters 99% of traffic, the LLM only sees the suspicious 1%.</li>
    <li>Latency budget is the single biggest constraint when wiring an LLM into any production workflow.</li>
  </ul>
</div>

---

## What to Notice When You Run It

1. How text gets tokenised — compare a clean sentence vs a CVE ID
2. How similar security terms are in embedding space (cosine similarity)
3. The token count for different types of security text

---

## Next Lesson

**[Lesson 4.2 — HuggingFace](../02_huggingface/README.md):** Use pre-trained transformer models without training anything — just load and run.

---

## Ready for the Workshop?

You have covered the concepts. Now build it yourself.

**[Open README.md](README.md)**

---

## What This Workshop Covers

This workshop demystifies Large Language Models from the ground up — no API key required. You will manipulate tokens, vectors, and attention weights directly in NumPy and Python to build genuine intuition for what happens inside a model.

Work through them in order — each exercise builds on the previous.

---

## Exercise Overview

| # | Guide | Lab | Topic |
|---|-------|---------------|-------|
| 1 | [lecture.md](1_tokenisation/lecture.md) | [handson.md](1_tokenisation/handson.md) | Text → tokens → token IDs; vocabulary and OOV handling |
| 2 | [lecture.md](2_embeddings/lecture.md) | [handson.md](2_embeddings/handson.md) | Tokens → vectors; cosine similarity; semantic distance |
| 3 | [lecture.md](3_attention/lecture.md) | [handson.md](3_attention/handson.md) | Attention weights as "which words matter to which"; Q/K/V intuition |
| 4 | [lecture.md](4_pretraining/lecture.md) | — | Pretraining: self-supervised next-token prediction, cross-entropy loss, why training scales to trillions of tokens |

**For each exercise:** read the guide first, then open the matching `_handson.md` file and follow the steps.

## Running an Exercise

```bash
cd "C:/Users/admin/Desktop/AI Basic Training"
python stage4_genai/01_how_llms_work/1_tokenisation/solution_how_llms_work.py
```

## Tips

- No GPU or internet connection required — all exercises run on NumPy alone
- The numbers you see are simplified toy examples, not real LLM weights
- The goal is intuition, not production-grade code
