# Tokenisation: Text as Token IDs

> Read this guide fully before opening the lab.

---

## What You Will Learn

- Why models cannot process raw text — they process integers
- What tokenisation is and how subword tokenisation works
- How vocabulary size affects what a model can represent
- The concept of Out-Of-Vocabulary (OOV) tokens

---

## Concept: Why Tokens, Not Characters or Words

There are three natural ways to split text:

| Strategy | Example for "unhappy" | Vocabulary size | Problems |
|----------|----------------------|----------------|----------|
| Character-level | u, n, h, a, p, p, y | ~100 | Long sequences, hard to learn semantics |
| Word-level | unhappy | 50,000+ | OOV: "unfamiliar" → unknown |
| Subword (BPE) | un, happy | ~50,000 | Handles new words: "unXYZ" → un + XYZ |

Modern LLMs use **subword tokenisation** (Byte Pair Encoding or similar). Common words get their own token; rare words are split into subword pieces. This balances vocabulary size against sequence length.

<div class="lecture-visual">
  <img src="/static/lecture_assets/gn_subword_split.png" alt="Three rows comparing tokenisation strategies for the word 'unhappiness'. Row 1 'Character-level' (grey) shows eleven small grey boxes one per letter: u, n, h, a, p, p, i, n, e, s, s; subtitle 'vocab ~100; long sequences, no semantic units'. Row 2 'Word-level' (orange) shows one big orange box containing the whole word 'unhappiness'; subtitle 'vocab 50K+; fails on unseen words (→ <UNK>)'. Row 3 'Subword (BPE / GPT-4)' (cyan) shows two cyan boxes: 'un' and 'happiness'; subtitle 'vocab ~100K; compact, handles new words'.">
  <div class="vis-caption">The same word, three tokenisation philosophies. Character-level produces 11 tokens for one word; word-level uses just one token but breaks on any unseen word. Subword tokenisation gets the best of both — common prefixes like "un" become reusable units, but rare combinations like "hap-pi-ness" can be split as needed.</div>
</div>

---

## Concept: Token IDs

A tokeniser converts text to a sequence of integers:

```
"Hello world" → ["Hello", " world"] → [9906, 1917]
```

**Tokenisation Pipeline:**

| Stage | Example | What it is |
|-------|---------|-----------|
| Raw text | `"Hello world"` | String input |
| Tokens | `"Hello"`, `" world"` | Subword pieces |
| Token IDs | `9906`, `1917` | Integers for the model |
| Embedding Layer | vectors per token | Dense representations |

<div class="lecture-visual">
  <img src="/static/lecture_assets/gn_tokenisation_pipeline.png" alt="A vertical four-stage diagram. Stage 1 'Raw text' shows a grey box containing 'Investigate the ransomware payload immediately' as a string. Stage 2 'Tokens (subword pieces)' shows seven coloured rounded rectangles in a row, each containing one token: 'Invest', 'igate', ' the', ' ransom', 'ware', ' payload', ' immediately'. Stage 3 'Token IDs (integers from a 100k vocabulary)' shows seven numbers below the tokens: 34,976, 65,056, 279, 58,686, 1,698, 7,885, 7,214. Stage 4 'Embedding lookup → vectors fed to the transformer' shows seven '[ … ]' placeholders.">
  <div class="vis-caption">Real GPT-4 tokenisation (cl100k_base) of one sentence. Notice <strong>two different kinds of split</strong>: <em>"Investigate"</em> breaks into <em>"Invest" + "igate"</em> — an arbitrary BPE cut from training frequency — while <em>"ransomware"</em> breaks into <em>"ransom" + "ware"</em>, an etymologically meaningful compound. Common words like <em>"the"</em>, <em>"payload"</em>, and <em>"immediately"</em> each get their own token. The seven integers on the third row are the actual values fed into GPT-4's embedding layer.</div>
</div>

Each integer is a **token ID** — an index into the model's vocabulary. The model's embedding layer converts each ID into a high-dimensional vector.

Real GPT-4 vocabulary: ~100,000 tokens.
Real Claude vocabulary: ~100,000 tokens.
Our toy vocabulary: 20 tokens (for clarity).

> **Try it yourself — official OpenAI tokenizer**
>
> OpenAI hosts a free interactive tokenizer at **<https://platform.openai.com/tokenizer>**. Paste any sentence and switch between **GPT-5.x & o1/o3**, **GPT-4 & GPT-3.5**, and **GPT-3** to see how the same text is split into different numbers of tokens by different model families. Toggle between the **Text** view (coloured token chips) and the **Token IDs** view (the raw integer array fed to the model).
>
> Paste in `Investigate the ransomware payload immediately` and you should see the same 7 tokens and the same integer IDs shown in the diagram above.

---

## Concept: Special Tokens

LLMs add special tokens that carry structural meaning:

| Token | Purpose |
|-------|---------|
| `<BOS>` (Begin Of Sequence) | Marks the start of a prompt |
| `<EOS>` (End Of Sequence) | Tells the model to stop generating |
| `<PAD>` | Fills shorter sequences in a batch to equal length |
| `<UNK>` | Replaces unknown tokens not in vocabulary |

**Sequence with special tokens:**

| Position | Token | Role |
|----------|-------|------|
| 1 | `<BOS>` | Start of sequence |
| 2 | `Hello` | Actual content |
| 3 | `world` | Actual content |
| 4 | `<EOS>` | End of sequence |
| 5 | `<PAD>` | Padding (batch alignment) |
| 6 | `<PAD>` | Padding (batch alignment) |

---

## Concept: Token Economics

Once text is tokens, two practical numbers start to matter:

- **API pricing is per token** &mdash; input and output, with output usually more expensive. A 2,000-token prompt that produces a 200-token reply is billed as `2000 × input_price + 200 × output_price`.
- **Context windows are measured in tokens** &mdash; the model can only "see" a fixed number at once (more on this in the next section).

A useful rule of thumb for English:

> **1 token &asymp; 4 characters &asymp; 0.75 words.** So 1,000 words &asymp; 1,300 tokens.

But security text is **much heavier**. CVEs, IPs, hashes, registry paths, and base64 blobs all sit outside the tokenizer's high-frequency vocabulary, so they get split into many short pieces. Three worked examples from the GPT-4 (`cl100k_base`) tokenizer:

| Input | Tokens | Notes |
|---|---:|---|
| `The firewall blocked malicious traffic` <small>(5 words)</small> | **6** | Common words land 1 token each; only `malicious` splits into `mal` + `icious`. Efficient. |
| `CVE-2024-1234` <small>(looks like 1 word)</small> | **7** | The tokenizer has never seen this exact ID, so it falls back to subword chunks: `CVE` + `-` + `202` + `4` + `-` + `123` + `4`. |
| `Cybersecurity` <small>(1 word)</small> | **2** | Splits into `Cyber` + `security` &mdash; a meaningful compound the model can generalise from. |

The takeaway: **plain English is cheap, security identifiers are expensive.** A page of incident-response prose tokenises near the 0.75-word rule, but a page of CVE IDs, SHA-256 hashes, and Windows registry paths can run **2&ndash;3&times; heavier**. Budget for it when you push logs through an API.

---

## Concept: The Context Window

Once your text is tokens, the model can only "see" a fixed number of them at once. That maximum is the **context window**. Anything beyond it is invisible to the model &mdash; as if it never existed.

| Model | Context window | Roughly equals |
|---|---|---|
| GPT-3.5 | 16,000 tokens | ~12,000 words / ~25 pages |
| GPT-4 Turbo | 128,000 tokens | ~96,000 words / ~200 pages |
| **Claude Opus / Sonnet** | **200,000 tokens** | ~150,000 words / ~500 pages |
| Gemini 1.5 Pro | 128,000 tokens | ~96,000 words / ~200 pages |

Every token in the request *and* the model's reply counts against the budget:

```
system prompt + conversation history + your new message + model's reply  ≤  context limit
```

Once you hit the limit, the oldest tokens are silently dropped, or the API rejects the call.

**Why this matters in practice:**

- Pasting a 10&nbsp;MB log file? Won't fit. You need to **chunk** it or filter first (Lesson 4.4).
- Long incident reports may exceed the window &mdash; summarise sections before passing them in.
- A model that "forgets" what you told it 50 messages ago hasn't malfunctioned &mdash; it has scrolled out of the window.

<div class="md-callout md-callout-red">
  <strong>The illusion of memory.</strong> LLMs have <strong>no persistent memory</strong> between API calls. Every conversation rebuilds the entire history from scratch and feeds it back in as input tokens. The "memory" you experience in ChatGPT or Claude is the chat client re-sending the transcript every turn. When the transcript exceeds the context window, the start gets cut.
</div>

---

## What Each Task Asks You to Do

### Task 1 — Build a toy vocabulary
Create a word-to-ID mapping from a list of 18 words. Add `<UNK>` (ID=0) and `<EOS>` (ID=19).

### Task 2 — Encode a sentence
Write an `encode(text)` function that splits on spaces and maps each word to its ID (or 0 for unknown). Print the token IDs for two example sentences.

### Task 3 — Decode back to text
Write a `decode(ids)` function that maps IDs back to words. Confirm you can round-trip: `decode(encode(text)) == text`.

### Task 4 — Observe OOV handling (Bonus)
Encode a sentence containing words not in your vocabulary. How does the model's view of the text change when words become `<UNK>`?

---

## Common Mistakes

**`KeyError` when encoding**
Use `.get(word, 0)` instead of `vocab[word]` — the `.get()` with a default handles unknown words gracefully.

**Decode produces wrong words**
Make sure your reverse vocabulary (ID→word) matches your forward vocabulary exactly. Build it with `{v: k for k, v in vocab.items()}`.
