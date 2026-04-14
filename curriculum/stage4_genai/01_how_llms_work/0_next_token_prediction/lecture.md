# Next-Token Prediction

---

## The Core Idea

An **LLM (Large Language Model)** is, at its core, a very sophisticated **next-token predictor**. That single sentence is the entire trick. Everything you have ever heard about LLMs &mdash; chat, code generation, summarisation, "reasoning" &mdash; is built on top of one mechanical loop:

1. Take the words so far.
2. Predict what word probably comes next.
3. Append that word to the input.
4. Go to step 1.

There is no separate "answer module", no "summariser", no "code generator". The same prediction loop drafts emails, finishes functions, and writes poems.

---

## The Loop in Action

**Step 1 &mdash; break the input into tokens:**

| Position | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| Token | `The` | `attacker` | `used` | `a` | `SQL` | `injection` | `to` |

**Step 2 &mdash; the model predicts the most probable next token:**

<div class="md-flow">
  <span class="md-flow-chip md-chip-cyan">Input: 7 tokens</span>
  <span class="md-flow-arrow">&rarr;</span>
  <span class="md-flow-chip md-chip-violet">LLM</span>
  <span class="md-flow-arrow">&rarr;</span>
  <span class="md-flow-chip md-chip-amber">"exfiltrate" <small>(top prob.)</small></span>
</div>

**Step 3 &mdash; append the new token and feed everything back as input. Repeat.**

| Position | 1 | 2 | 3 | 4 | 5 | 6 | 7 | **8** | next |
|---|---|---|---|---|---|---|---|---|---|
| Token | `The` | `attacker` | `used` | `a` | `SQL` | `injection` | `to` | **`exfiltrate`** | `???` |

The token added on this turn becomes part of the input on the next turn, and the cycle continues until the model emits a special end-of-sequence token.

---

## Why This One Trick Gives You Everything Else

Predicting the next token is a deceptively narrow task. But the model is doing it from billions of examples of real human text &mdash; code, novels, manuals, advisories, research papers. To predict the next token *well* across all of that, the model has to implicitly know who Marie Curie was, what TCP port 443 is for, how a Python `for` loop works, and that a sentence about ransomware is unlikely to end with "and they all lived happily ever after".

None of this is programmed in. None of it is hand-labelled. It is all an emergent side effect of making the prediction more accurate.

<div class="md-callout md-callout-red">
  <strong>The loop:</strong> predict &rarr; append &rarr; predict &rarr; append. During training, this loop runs billions of times across trillions of words scraped from the internet. Each time the model guesses the next token wrong, the error is used to slightly adjust its billions of internal weights &mdash; nudging it toward better predictions. After enough repetitions, reasoning, coding, and summarisation emerge as side effects &mdash; <strong>all from this one task</strong>.
</div>

> **Does bigger always mean better?** More parameters give a model more capacity to learn patterns &mdash; which is why GPT-4 (~1.8 trillion parameters) outperforms GPT-2 (1.5 billion). But size alone is not enough. A huge model trained on too little data will memorise instead of generalise. Research on scaling laws shows diminishing returns: doubling parameters does not double quality. Architecture matters too &mdash; the attention mechanism (Step 7) let transformers outperform much larger older models. And data quality often beats data quantity &mdash; Meta's Llama 3 (70B) matches models 10x its size thanks to better-curated training data. Think of it as a three-legged stool: parameters, data, and architecture. Knock out any leg and the model falls over.

---

## What's Next in This Lesson

The remaining 9 steps zoom into the pieces of this loop:

| Step | What it covers |
|---|---|
| 2 &mdash; Tokenisation | How text gets sliced into tokens before any prediction happens |
| 3 &mdash; Vocabulary Limits | What happens when the tokenizer meets words it has never seen |
| 4 &mdash; Embeddings | How tokens become vectors of numbers ("fingerprints") |
| 5 &mdash; Comparing Embeddings | Similar fingerprints, similar meaning |
| 6 &mdash; Cosine Similarity | Measuring how similar two embeddings are |
| 7 &mdash; Attention | How the model decides which earlier tokens matter most |
| 8 &mdash; Context Vectors | Attention combining many tokens into one weighted answer |
| 9 &mdash; Pretraining | Where the billions of weights come from in the first place |
| 10 &mdash; LLMs vs Classic ML | When to reach for an LLM and when not to |

Click **Next: Reflect** below to think through a few questions, then move to **Step 2** to see tokenisation for yourself.
