# Exercise 2 — Embeddings: Tokens as Vectors

> Read this guide fully before opening the lab.

---

## What You Will Learn

- How token IDs are converted to dense vectors (embeddings)
- Why similar words have similar vectors in a trained model
- How cosine similarity measures semantic distance
- How embeddings represent meaning geometrically

---

## Concept: The Embedding Matrix

An LLM's first layer is an embedding matrix of shape `(vocab_size, embedding_dim)`. Each row is the embedding vector for one token:

```
vocab_size = 20
embedding_dim = 4    ← real models use 768, 1024, 4096, etc.

Embedding matrix (20 × 4):
token 0 (<UNK>):    [0.00,  0.00,  0.00,  0.00]
token 1 (the):      [0.12, -0.34,  0.78,  0.05]
token 2 (network):  [0.89,  0.12, -0.45,  0.67]
token 5 (suspicious): [0.91, 0.08, -0.50, 0.71]  ← similar to "malicious"
token 6 (malicious):  [0.88, 0.15, -0.42, 0.69]  ← close to "suspicious"
```

Words that appear in similar contexts get similar vectors after training. This is the **distributional hypothesis** — meaning is defined by context.

---

## Concept: Cosine Similarity

To measure how similar two vectors are, use cosine similarity:

```
cosine_similarity(A, B) = (A · B) / (|A| × |B|)

Range: -1 (opposite) → 0 (unrelated) → +1 (identical direction)
```

```python
def cosine_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
```

In a well-trained embedding space:
- `cosine_sim(embedding("malicious"), embedding("suspicious"))` ≈ 0.95
- `cosine_sim(embedding("malicious"), embedding("the"))` ≈ 0.05

---

## Concept: Why This Matters for Security ML

In security NLP tasks (log classification, phishing detection, threat intel):
- A model sees `"detected"` and `"identified"` as different tokens
- But their embeddings are close → the model generalises across synonyms
- Fine-tuning on domain-specific text (CVE descriptions, log formats) adjusts the embeddings for security vocabulary

---

## What Each Task Asks You to Do

### Task 1 — Build a toy embedding matrix
Create a NumPy array of shape `(20, 4)` with pre-defined values provided in the exercise. This represents a "pre-trained" embedding for our toy vocabulary.

### Task 2 — Look up embeddings
Write `get_embedding(word)` that converts a word to its ID, then returns the row of the embedding matrix.

### Task 3 — Compute cosine similarity
Implement `cosine_sim(a, b)` and use it to compare:
- malicious vs suspicious (should be high)
- malicious vs benign (should be low or negative)
- firewall vs traffic (moderate)

### Task 4 — Find the most similar word (Bonus)
For a given query word, compute cosine similarity against all vocabulary words and print the top 5 most similar.

---

## Now Open the Lab

[02_lab_embeddings.md](02_lab_embeddings.md)
## Next

[03_guide_attention.md](03_guide_attention.md) — the attention mechanism: which words matter to which.
