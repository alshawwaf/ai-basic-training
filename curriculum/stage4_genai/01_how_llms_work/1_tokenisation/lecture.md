# Exercise 1 — Tokenisation: Text as Token IDs

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
  <img src="/static/lecture_assets/gn_subword_split.png" alt="Three rows comparing tokenisation strategies for the word 'unhappiness'. Row 1 'Character-level' (grey) shows eleven small grey boxes one per letter: u, n, h, a, p, p, i, n, e, s, s; subtitle 'vocab ~100, sequence too long, no semantic units'. Row 2 'Word-level' (orange) shows one big orange box containing the whole word 'unhappiness'; subtitle 'vocab 50,000+, fails on any unseen word'. Row 3 'Subword (BPE / GPT-4)' (cyan) shows two cyan boxes: 'un' and 'happiness'; subtitle 'vocab ~100,000, handles new words, compact sequences'.">
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
  <img src="/static/lecture_assets/gn_tokenisation_pipeline.png" alt="A vertical four-stage diagram. Stage 1 'Raw text' shows a grey box containing 'Analyse this log entry for threats' as a string. Stage 2 'Tokens (subword pieces)' shows seven coloured rounded rectangles in a row, each containing one token: 'Analy', 'se', ' this', ' log', ' entry', ' for', ' threats'. Stage 3 'Token IDs (integers from a 100k vocabulary)' shows seven numbers below the tokens: 74,407, 325, 420, 1,515, 4,441, 369, 18,208. Stage 4 'Embedding lookup → vectors fed to the transformer' shows seven '[ … ]' placeholders.">
  <div class="vis-caption">Real GPT-4 tokenisation (cl100k_base) of one sentence. Notice how "Analyse" splits into two pieces ("Analy" + "se") because it's less common than "Analyze", while "this", "log", "entry", "for", and "threats" each get their own token. The seven integers on the third row are the actual values fed into GPT-4's embedding layer.</div>
</div>

Each integer is a **token ID** — an index into the model's vocabulary. The model's embedding layer converts each ID into a high-dimensional vector.

Real GPT-4 vocabulary: ~100,000 tokens.
Real Claude vocabulary: ~100,000 tokens.
Our toy vocabulary: 20 tokens (for clarity).

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
