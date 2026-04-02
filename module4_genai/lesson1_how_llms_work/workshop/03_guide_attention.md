# Exercise 3 — Attention: Which Words Matter to Which

> Read this guide fully before opening the lab.

---

## What You Will Learn

- What the attention mechanism does conceptually
- How attention weights are computed (Q, K, V intuition)
- Why attention is the key innovation that makes transformers powerful
- How to interpret an attention matrix

---

## Concept: The Problem Attention Solves

Before attention, RNNs processed sequences word by word. By the time the model reached the end of a long sentence, the beginning was "forgotten" — compressed into a single vector.

Attention solves this by letting every position look at every other position simultaneously:

```
"The firewall blocked the malicious connection from the suspicious endpoint"

When processing "blocked", attention weights might be:
  the(1):        0.03
  firewall:      0.45  ← high — "firewall" is the subject doing the blocking
  blocked:       0.00  ← skip self
  the(2):        0.02
  malicious:     0.28  ← high — describes the thing being blocked
  connection:    0.15
  from:          0.02
  the(3):        0.01
  suspicious:    0.03
  endpoint:      0.01
```

The model learns which words are relevant to each word's meaning in context.

---

## Concept: Query, Key, Value

Attention uses three learned matrices to compute weights:

```
For each position i:
  Q_i = embedding_i × W_Q    ← "what am I looking for?"
  K_j = embedding_j × W_K    ← "what do I contain?"
  V_j = embedding_j × W_V    ← "what will I contribute if selected?"

Attention score(i→j) = softmax( Q_i · K_j / sqrt(d_k) )

Output_i = sum over j of: score(i→j) × V_j
```

Think of it as a search engine:
- **Query**: the word asking "what context do I need?"
- **Key**: each word advertising "here is what I'm about"
- **Value**: what each word actually contributes to the output

---

## Concept: The Attention Matrix

For a sequence of n tokens, the attention matrix has shape (n, n). Entry [i][j] is how much position i attends to position j.

```
          the   firewall  blocked  malicious  connection
the     [ 0.80   0.10     0.05     0.03       0.02  ]
firewall[ 0.15   0.65     0.10     0.05       0.05  ]
blocked [ 0.03   0.45     0.00     0.28       0.24  ]  ← row shows what "blocked" attends to
malicious[0.02   0.08     0.12     0.70       0.08  ]
connection[0.04  0.12     0.30     0.25       0.29  ]
```

Rows sum to 1.0 (softmax output).

---

## What Each Task Asks You to Do

### Task 1 — Build a toy attention matrix
Given a 5-word sentence, create a 5×5 attention weight matrix using the values provided. Confirm each row sums to 1.0.

### Task 2 — Interpret attention
For each word, print which word it attends to most. This reveals which words the model considers most relevant to each position.

### Task 3 — Compute a weighted context vector
For word index 2 ("blocked"), compute its context vector: the weighted sum of value vectors. This is the output of the attention layer for that position.

### Task 4 — Visualise as a grid (Bonus)
Print the attention matrix as a formatted number grid with word labels on both axes.

---

## Common Mistakes

**Row doesn't sum to 1.0**
Manually verify your values sum to 1.0 per row. If you compute from raw scores, apply `np.exp(row) / np.exp(row).sum()`.

**Context vector shape wrong**
Value vectors have shape `(embedding_dim,)`. Use `attention[2] @ values` for the weighted sum — this is the cleanest NumPy idiom.

---

## Now Open the Lab

[03_lab_attention.md](03_lab_attention.md)
## Workshop Complete

Compare your code against the matching `_solution_` files, then move to:

**[Lesson 4.2 — HuggingFace Pre-trained Models](../../lesson2_huggingface/workshop/00_overview.md)**
