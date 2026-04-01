# Lesson 4.1 — How LLMs Work

---

## Concept: The Core Idea

An LLM (Large Language Model) is, at its core, a very sophisticated **next-token predictor**:

```
Input:  "The attacker used a SQL injection to"
         |       |      |   |   |         |
       token1  token2 ...                token7

                     LLM predicts next token
                              |
                              v
Output: "exfiltrate"   (highest probability next token)

Then feeds output back as new input and repeats...

"The attacker used a SQL injection to exfiltrate the ..."
                                                    ^
                                               next token
```

That's all it's doing. Everything — reasoning, coding, summarisation — emerges from predicting the next token, trained on trillions of tokens of text.

---

## Tokens

Text is split into **tokens** before being processed. A token is roughly:
- 1 word (common words like "the", "attack")
- Part of a word ("injection" → "inject" + "ion")
- A character for rare words

```python
"Cybersecurity" → ["Cyber", "security"]     # 2 tokens
"Hello world"   → ["Hello", " world"]        # 2 tokens
"CVE-2024-1234" → ["CVE", "-", "2024", "-", "1234"]  # 5 tokens
```

**Why tokens matter for you:**
- API pricing is per-token
- Context windows are measured in tokens (e.g. Claude: 200,000 tokens)
- Long documents need chunking to fit in context

---

## Embeddings

Before tokens are processed by the model, each is converted to an **embedding** — a dense vector of hundreds of numbers that captures the token's meaning:

```
"malware"    → [0.23, -0.41, 0.88, ...]   # 768 numbers
"ransomware" → [0.25, -0.38, 0.91, ...]   # similar! (same semantic space)
"pizza"      → [-0.51, 0.12, -0.33, ...]  # very different
```

**Semantic similarity** = similar vectors. This is how the model knows "virus" and "malware" are related without being told:

```
         "malware" [0.23, -0.41, 0.88]
         "ransomware" [0.25, -0.38, 0.91]   <-- close together
         "virus" [0.21, -0.44, 0.85]        <-- (related meaning)

         "pizza" [-0.51, 0.12, -0.33]       <-- far away
         "guitar" [-0.48, 0.09, -0.29]      <-- (unrelated meaning)
```

---

## The Transformer Architecture

The breakthrough behind all modern LLMs is the **attention mechanism**:

```
Input: "The malware connects to the C2 server"

When processing "C2":
- Attends strongly to "malware" (it's related)
- Attends strongly to "connects" (it's the action)
- Attends weakly to "The", "to", "server"
```

The model learns which tokens to "pay attention to" when predicting each next token. This allows it to capture long-range dependencies that RNNs couldn't.

---

## Why LLMs Are Different from Classifiers

| Classic ML (Stages 1–3) | LLMs (Stage 4) |
|------------------------|----------------|
| Train from scratch | Pre-trained on ~1 trillion tokens |
| Needs labelled data | No labels needed for pre-training |
| Single specific task | General purpose |
| Hundreds of parameters | Billions of parameters |
| Inference: microseconds | Inference: seconds |
| Runs on laptop | Usually requires GPU or API |

---

## What to Notice When You Run It

1. How text gets tokenised — compare a clean sentence vs a CVE ID
2. How similar security terms are in embedding space (cosine similarity)
3. The token count for different types of security text

---

## Next Lesson

**[Lesson 4.2 — HuggingFace](2_huggingface_pretrained_models.md):** Use pre-trained transformer models without training anything — just load and run.

---

## Ready for the Workshop?

You have covered the concepts. Now build it yourself.

**[Open workshop/1_lab_guide.md](workshop/1_lab_guide.md)**
