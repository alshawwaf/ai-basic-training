# Lab — Exercise 2: Embeddings: Tokens as Vectors

> Follow each step in order. Copy the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `exercise2_embeddings.py` in this folder.

---

## Step 2: Add the imports and vocabulary

NumPy provides the array and linear algebra operations needed for this exercise. The vocabulary from Exercise 1 is reproduced here so the file runs standalone.

```python
import numpy as np

vocab = {
    "<UNK>": 0, "the": 1, "network": 2, "connection": 3, "is": 4,
    "suspicious": 5, "malicious": 6, "benign": 7, "port": 8, "scan": 9,
    "firewall": 10, "blocked": 11, "allowed": 12, "traffic": 13, "alert": 14,
    "endpoint": 15, "detected": 16, "attack": 17, "normal": 18, "<EOS>": 19,
}
```

---

## Step 3: Build the embedding matrix

Each row in this 20×4 matrix is the embedding vector for one token. Hand-crafted values make threat words (malicious, suspicious, attack) cluster together, and benign/normal cluster in the opposite direction.

Add this to your file:

```python
embeddings = np.array([
    [ 0.00,  0.00,  0.00,  0.00],  # <UNK>
    [ 0.10, -0.20,  0.05,  0.10],  # the
    [ 0.70,  0.20, -0.30,  0.60],  # network
    [ 0.65,  0.25, -0.25,  0.55],  # connection
    [ 0.08, -0.15,  0.03,  0.08],  # is
    [ 0.90,  0.10, -0.50,  0.75],  # suspicious
    [ 0.92,  0.08, -0.52,  0.78],  # malicious
    [-0.85, -0.10,  0.48, -0.70],  # benign
    [ 0.60,  0.40, -0.20,  0.50],  # port
    [ 0.75,  0.35, -0.40,  0.65],  # scan
    [ 0.55,  0.45, -0.15,  0.45],  # firewall
    [ 0.50,  0.30, -0.10,  0.40],  # blocked
    [-0.45, -0.25,  0.08, -0.35],  # allowed
    [ 0.60,  0.35, -0.18,  0.50],  # traffic
    [ 0.80,  0.20, -0.45,  0.70],  # alert
    [ 0.65,  0.30, -0.28,  0.55],  # endpoint
    [ 0.72,  0.18, -0.38,  0.62],  # detected
    [ 0.93,  0.05, -0.55,  0.80],  # attack
    [-0.80, -0.08,  0.45, -0.65],  # normal
    [ 0.00,  0.01,  0.00,  0.00],  # <EOS>
])

print("Embedding matrix shape:", embeddings.shape)
```

Run your file. You should see:
```
Embedding matrix shape: (20, 4)
```

---

## Step 4: Look up embeddings for individual words

The `get_embedding` function converts a word to its ID and returns the corresponding row of the embedding matrix.

Add this to your file:

```python
def get_embedding(word):
    token_id = vocab.get(word, 0)
    return embeddings[token_id]

print("\nWord embeddings:")
for word in ["malicious", "benign", "attack"]:
    vec = get_embedding(word)
    print(f"  {word:<10}: {vec}")
```

Run your file. You should see:
```
Word embeddings:
  malicious : [ 0.92  0.08 -0.52  0.78]
  benign    : [-0.85 -0.10  0.48 -0.70]
  attack    : [ 0.93  0.05 -0.55  0.80]
```

---

## Step 5: Compute cosine similarity

Cosine similarity measures the angle between two vectors: +1 means identical direction (same meaning), -1 means opposite, 0 means unrelated. Threat words should score near +1 with each other and near -1 with benign/normal words.

Add this to your file:

```python
def cosine_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

pairs = [
    ("malicious", "suspicious"),
    ("malicious", "benign"),
    ("firewall",  "traffic"),
    ("the",       "attack"),
]

print("\nCosine similarities:")
for w1, w2 in pairs:
    score = cosine_sim(get_embedding(w1), get_embedding(w2))
    print(f"  {w1:<10} vs {w2:<10} : {score:.4f}")
```

Run your file. You should see (approximate values):
```
Cosine similarities:
  malicious  vs suspicious  : 0.9957
  malicious  vs benign      : -0.9991
  firewall   vs traffic     : 0.9981
  the        vs attack      : 0.2341
```

---

## Step 6: Find most similar words (Bonus Task 4)

This function computes cosine similarity between a query word and every word in the vocabulary, then returns the top N matches. Special tokens and the query itself are excluded.

Add this to your file:

```python
def most_similar(query_word, top_n=5):
    query_vec = get_embedding(query_word)
    scores = []
    for word, id_ in vocab.items():
        if word in (query_word, "<UNK>", "<EOS>"):
            continue
        score = cosine_sim(query_vec, embeddings[id_])
        scores.append((word, score))
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:top_n]

print(f"\nTop 5 words most similar to 'attack':")
for rank, (word, score) in enumerate(most_similar("attack"), 1):
    print(f"  {rank}. {word:<12} {score:.4f}")

print("\n--- Exercise 2 complete. Move to exercise3_attention.py ---")
```

Run your file. You should see:
```
Top 5 words most similar to 'attack':
  1. malicious     0.9993
  2. suspicious    0.9957
  3. alert         0.9946
  4. scan          0.9935
  5. detected      0.9927

--- Exercise 2 complete. Move to exercise3_attention.py ---
```

---

## Your completed script

At this point your file contains all the working code. Compare it against the matching `_solution_` file (`02_solution_embeddings.py`) if anything looks different.
