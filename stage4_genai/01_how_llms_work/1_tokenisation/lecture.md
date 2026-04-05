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

---

## Now Open the Lab

[handson.md](handson.md)
## Next

[../2_embeddings/lecture.md](../2_embeddings/lecture.md) — how token IDs become high-dimensional vectors and how similarity works.
