# Embeddings: Tokens as Vectors

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

**Token ID → Embedding Lookup** (Embedding Matrix: 20 x 4)

| Token ID | Word | Dim 0 | Dim 1 | Dim 2 | Dim 3 |
|----------|------|-------|-------|-------|-------|
| 1 | "the" | 0.12 | -0.34 | 0.78 | 0.05 |
| 2 | "network" | 0.89 | 0.12 | -0.45 | 0.67 |
| 5 | "suspicious" | 0.91 | 0.08 | -0.50 | 0.71 |
| 6 | "malicious" | 0.88 | 0.15 | -0.42 | 0.69 |

> Notice: "suspicious" and "malicious" have very close vectors — similar meaning produces similar embeddings.

<div class="lecture-visual">
  <img src="/static/lecture_assets/gn_embedding_space.png" alt="A 2D scatter plot titled 'Real sentence-transformer embeddings — PCA to 2D' with 18 word labels coloured by category. Red 'threat' cluster: malicious, suspicious, attack, breach, exploit grouped together in one region. Cyan 'network' cluster: firewall, router, packet, traffic, port grouped in another region. Grey 'function' cluster: the, a, of, and grouped together. Green 'food' cluster: apple, pizza, bread, coffee grouped together far from the others. The four clusters are visibly separated.">
  <div class="vis-caption">Real embeddings from <code>all-MiniLM-L6-v2</code> projected to 2D with PCA. No labels were given to the model — it learned during pre-training that "malicious" and "suspicious" belong together, "firewall" and "router" belong together, and food words live somewhere completely different. This is what "the geometry of meaning" looks like.</div>
</div>

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

**Embedding Space (2-D projection):**

| Cluster | Words | Position |
|---------|-------|----------|
| Threat terms | malicious, suspicious | Close together (cosine ~ 0.95) |
| Network terms | firewall, traffic | Moderate similarity |
| Function words | the, a | Far from security terms |

<div class="lecture-visual">
  <img src="/static/lecture_assets/gn_cosine_pairs.png" alt="A bar chart titled 'Real cosine similarities from all-MiniLM-L6-v2 embeddings' with five bars. From left to right: '\"malicious\" vs \"suspicious\"' high green bar, '\"malicious\" vs \"benign\"' moderate green bar, '\"firewall\" vs \"router\"' green bar, '\"the\" vs \"malicious\"' green bar, '\"phishing\" vs \"credential theft\"' green bar. Each bar shows the exact similarity score above it. Two dashed reference lines: green at 0.70 (strong) and orange at 0.40 (weak).">
  <div class="vis-caption">Real cosine similarities measured by encoding each word individually with the same sentence-transformer model. The numbers come straight from the model — no hand-picked toy values. Word pairs that share security context have higher similarity; unrelated function words have lower scores.</div>
</div>

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
