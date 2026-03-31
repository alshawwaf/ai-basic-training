# Exercise 1 — Tokenisation: Text as Token IDs

> **Exercise file:** [exercise1_tokenisation.py](exercise1_tokenisation.py)
> Read this guide fully before opening the exercise file.

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

## Expected Outputs at a Glance

**Task 1**
```
Vocabulary (20 tokens):
  0: <UNK>
  1: the
  2: network
  3: connection
  4: is
  5: suspicious
  6: malicious
  7: benign
  8: port
  9: scan
 10: firewall
 11: blocked
 12: allowed
 13: traffic
 14: alert
 15: endpoint
 16: detected
 17: attack
 18: normal
 19: <EOS>
```

**Task 2**
```
"the network connection is suspicious" → [1, 2, 3, 4, 5, 19]
"port scan detected on endpoint"       → [8, 9, 16, 0, 15, 19]
```

**Task 3**
```
[1, 2, 3, 4, 5, 19] → "the network connection is suspicious <EOS>"
Round-trip successful: True
```

---

## Common Mistakes

**`KeyError` when encoding**
Use `.get(word, 0)` instead of `vocab[word]` — the `.get()` with a default handles unknown words gracefully.

**Decode produces wrong words**
Make sure your reverse vocabulary (ID→word) matches your forward vocabulary exactly. Build it with `{v: k for k, v in vocab.items()}`.

---

## Now Open the Exercise File

[exercise1_tokenisation.py](exercise1_tokenisation.py)

---

## Next

[exercise2_embeddings.md](exercise2_embeddings.md) — how token IDs become high-dimensional vectors and how similarity works.
