# Attention: Which Words Matter to Which

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

<div class="lecture-visual">
  <img src="/static/lecture_assets/gn_attention_arrows.png" alt="A row of five word boxes spelling 'the firewall blocked malicious connection'. The middle word 'blocked' is highlighted in orange. Cyan arrows of varying thickness fan down from 'blocked' to each of the other four words. The thickest arrow points to 'firewall' (labelled 0.45), the second thickest to 'malicious' (labelled 0.28), a thinner arrow to 'connection' (labelled 0.24), and very thin lines to 'the' and other small weights. Caption above: 'When the model processes blocked, it asks every other word: how much do you matter to me?'">
  <div class="vis-caption">Attention in one picture. When the transformer is computing the new representation for "blocked", it weighs every other word in the sentence by an attention score. The thickness of each arrow is the score. "firewall" wins (subject doing the blocking) and "malicious" comes second (the thing being blocked) — exactly what a human would consider when interpreting that word.</div>
</div>

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

**Query-Key-Value Flow for "blocked":**

| Step | Operation | Result |
|------|-----------|--------|
| 1 | "blocked" embedding x W_Q | Q — "what am I looking for?" |
| 2 | Q dot K_firewall, Q dot K_malicious, ... | Raw attention scores |
| 3 | Softmax across all positions | 0.45 (firewall), 0.28 (malicious), ... |
| 4 | 0.45 x V_firewall + 0.28 x V_malicious + ... | **Context vector for "blocked"** |

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

**Attention Matrix — reading the "blocked" row:**

| | the | firewall | blocked | malicious | connection | Sum |
|---|-----|----------|---------|-----------|------------|-----|
| **blocked** | 0.03 | **0.45** | 0.00 | **0.28** | 0.24 | 1.0 |

> **firewall** (0.45) = strongest — "who blocked?" **malicious** (0.28) = second — "what was blocked?"

<div class="lecture-visual">
  <img src="/static/lecture_assets/gn_attention_matrix.png" alt="A 5×5 heatmap titled 'Attention matrix — gold row is blocked'. Rows and columns are labelled the, firewall, blocked, malicious, connection. Cells are coloured on a yellow-to-blue gradient with the numerical attention weight written in each cell. The 'blocked' row (third row) is highlighted with a thick gold border. In that row, the cell for 'firewall' (0.45) is the darkest, followed by 'malicious' (0.28) and 'connection' (0.24); the diagonal cell ('blocked' to itself) is 0.00.">
  <div class="vis-caption">The full 5×5 attention matrix. Each row is one word asking "what should I look at?" — and the row's values must sum to 1.0 because they come from a softmax. The gold-highlighted "blocked" row is the same one visualised by the arrow diagram above, but here you can read the exact numerical weights.</div>
</div>

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
