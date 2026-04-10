# Pretraining: How the Weights Get Made

> Read this guide fully — there is no hands-on lab for this section. It is a conceptual deep-dive into how the model you've been using was actually built.

---

## What You Will Learn

- Why "training a Large Language Model" is really *one task repeated trillions of times*
- How **self-supervised learning** turns plain text into free training data
- What the **cross-entropy loss** actually measures, and how a single weight update happens
- How model output evolves from random gibberish → grammar → fact → reasoning as training progresses
- The realistic compute, time, and money cost of a frontier pretraining run
- Why pretraining is the part of the LLM lifecycle you will *never* do yourself — and what you do instead

---

## Concept: The Self-Supervised Loop

Every other ML system you have built so far in this course needed **labelled data** — somebody, somewhere, had to tell the model the right answer. For 1,000 examples, somebody hand-labelled 1,000 rows.

Pretraining sidesteps this entirely with one trick: **the answer to "what comes next?" is already in the sentence.**

Take any sentence from the open internet:

```
"The firewall blocked the malicious traffic on port 443."
```

Cut it at any point, and you have created a training example for free. The text *before* the cut is the input, and the *next token* is the label:

| Input (everything before the cut) | Label (next token) |
|---|---|
| `The` | `firewall` |
| `The firewall` | `blocked` |
| `The firewall blocked` | `the` |
| `The firewall blocked the` | `malicious` |
| `The firewall blocked the malicious` | `traffic` |
| `The firewall blocked the malicious traffic` | `on` |
| `The firewall blocked the malicious traffic on` | `port` |
| `The firewall blocked the malicious traffic on port` | `443` |
| `The firewall blocked the malicious traffic on port 443` | `.` |

**One sentence → 9 free training examples.** Scale this up: a 1 trillion-token corpus produces ~1 trillion training examples without a single human ever touching a label. That is what the word **self-supervised** means — the supervision signal is hidden inside the data itself.

---

## Concept: One Step of Pretraining

Pretraining is just this loop, repeated trillions of times. Each step has six stages:

| Stage | What happens | What changes |
|---|---|---|
| 1. **Sample** | Grab a random chunk of text from the corpus | — |
| 2. **Tokenise** | Convert it to integer token IDs | — |
| 3. **Forward pass** | Run the tokens through the model. The model outputs a probability distribution over its ~100,000 vocabulary entries for the *next* token. | — |
| 4. **Compute loss** | Compare the model's prediction to the actual next token using **cross-entropy loss**. If the right answer was given high probability, loss is low. If it was given near-zero probability, loss is high. | — |
| 5. **Backward pass** | Compute the gradient of the loss with respect to every weight in the model — the direction in which each weight should move to reduce the loss next time. | — |
| 6. **Update** | Nudge every weight by a tiny step in that direction (controlled by the **learning rate**, typically `1e-4`). | **Billions of weights change very slightly.** |

That's it. That's the entire training loop. The "magic" of an LLM is just **stage 6 happening a few billion times.**

### Worked example: cross-entropy in numbers

Suppose the model sees the input `"The firewall blocked the"` and outputs the following probability distribution over the vocabulary (only the top entries shown):

| Candidate next token | Model's probability |
|---|---|
| `door` | 0.40 |
| `connection` | 0.20 |
| `traffic` | 0.05 |
| `malicious` | 0.03 |
| ...everything else... | 0.32 (spread across ~100k tokens) |

The **actual** next token in the source text is `malicious`. The cross-entropy loss for this single example is:

```
loss = -log(probability assigned to the correct token)
     = -log(0.03)
     ≈ 3.51
```

A "perfect" model that gave `malicious` probability 1.0 would have loss `-log(1.0) = 0`. A model that gave it `0.5` would have loss `~0.69`. The number `3.51` is high — the model was wrong, and the gradient computed from this loss will push the weights to make `malicious` slightly more likely *and* `door` slightly less likely the next time it sees a similar context.

After **one** update, this change is invisible. After **a trillion** updates, the weights have absorbed the entire structure of human language.

---

## Concept: Watching the Model Learn

Pretraining starts from **random weights** — literally `numpy.random.randn(...)` (or a smarter init, but conceptually random). The model knows nothing. It does not even know that English exists. Then it sees the first token, then the next, then a billion more.

The same prompt fed in at different points during training produces strikingly different output:

| Tokens seen so far | Output for prompt: *"The firewall blocked the"* | What changed |
|---|---|---|
| **0** (random init) | `qz $$ k7 ;; xx vv` | Pure noise — random token IDs from the vocab |
| **1 million** | `the the the the the` | Learned token frequencies — common words dominate |
| **100 million** | `the door and went home` | Learned grammar and word order, but no meaning |
| **1 billion** | `the user from accessing the website` | Plausible English sentences, generic content |
| **100 billion** | `the suspicious connection and logged the event` | Domain coherence — knows what firewalls *do* |
| **1 trillion+** | `the malicious traffic on port 443 and triggered alert ID 1042` | Specific, technical, contextually correct |

**Nothing about the architecture changed between rows.** Same number of layers, same number of parameters, same attention heads. Only the *values* of the weights changed, after billions of "predict, compare, nudge" updates.

This is the source of what people call "emergent abilities." Reasoning, world knowledge, coding ability, the ability to translate between languages — none of these were programmed in. They emerge as side-effects of the model getting good at one thing: **predicting the next token.**

<div class="lecture-visual">
  <img src="/static/lecture_assets/gn_pretraining_loss_curve.png" alt="A loss curve plot. X-axis is 'training tokens seen' on a log scale from 1 million up to 10 trillion. Y-axis is 'cross-entropy loss' from 0 at the bottom to 11 at the top. The curve starts at a loss of about 11 (random initialisation, equivalent to a uniform guess over the 100k vocabulary) and drops sharply over the first billion tokens, then more slowly down to about 1.8 at 10 trillion tokens. Annotations along the curve mark six stages: 'random init' at 0 tokens, 'frequency learned' at 1 million, 'grammar learned' at 100 million, 'plausible sentences' at 1 billion, 'domain coherence' at 100 billion, and 'frontier model' at 10 trillion.">
  <div class="vis-caption">A real pretraining loss curve never goes to zero — it asymptotes around 1.5–2.0 for frontier models, because language is inherently uncertain (there are always multiple reasonable next tokens). The interesting part is the <em>shape</em>: the steepest drop happens in the first billion tokens, where the model picks up grammar and frequencies. Reasoning and knowledge are squeezed out of the long, slow tail — the difference between a 100B-token model and a 10T-token model is not that the loss is dramatically lower, but that the *kinds* of mistakes it makes are different.</div>
</div>

---

## Concept: The Compute Cost

The reason "just train your own LLM" is not advice that anyone seriously gives:

| Resource | Frontier LLM pretraining run (2024–2025) |
|---|---|
| Tokens consumed | 10–20 trillion |
| GPUs | ~10,000–25,000 NVIDIA H100s |
| Wall-clock time | 2–6 months |
| Electricity | ~50 GWh — comparable to a small town for a month |
| **Estimated cost** | **~$50M–$200M** |

To put that in scale:

| Compute step | Cost | How much pretraining that buys |
|---|---|---|
| Training a logistic regression on 10k rows | <$0.01 | n/a |
| Fine-tuning a 7B open-weight model on 50k examples | $50–$500 | ~0.0005% of a frontier run |
| Pretraining a small 1B model from scratch | ~$50k | 0.05% of a frontier run |
| Pretraining LLaMA 3 (Meta, 2024) | ~$100M | 1× |

**You will not pretrain.** Even Fortune-500 companies typically do not pretrain — they fine-tune somebody else's open-weight checkpoint, or just call an API. The economics simply do not work out unless your name is OpenAI, Anthropic, Google, Meta, Mistral, or DeepSeek.

---

## Concept: Pretraining vs Fine-Tuning vs Inference

Three separate phases that often get confused, because "training" is sometimes used to mean any of them:

| Phase | Who does it | When | Cost per run | What it produces |
|---|---|---|---|---|
| **Pretraining** | Big labs only | Once per model generation | $50M–$200M | A "base model" — knows language, knows facts, but is *not* a chatbot. It will happily complete a sentence; it won't follow instructions. |
| **Fine-tuning** | Same labs, or you on a small open-weight model | Per dataset / per task | $1k–$10M | A model specialised for a domain or aligned to instructions. This is where "answer in JSON" or "be a security analyst assistant" gets baked in. |
| **RLHF / RLAIF** | Same labs, sometimes you | Per alignment goal | $100k–$10M | A model that has learned which of *its own* outputs humans (or another AI) prefer. This is how you get a polite, refusal-aware ChatGPT-style assistant from a raw base model. |
| **Inference** | You, every time you call the API | Continuous | Fractions of a cent per query | The actual answer to your prompt. |

The model you call from an API — `claude-opus-4-6`, `gpt-4o`, `gemini-1.5-pro` — is **pretrained + fine-tuned + RLHFed**. Three separate training runs stacked on top of each other. Pretraining is by far the largest and most expensive of the three; fine-tuning and RLHF are surface polish.

<div class="lecture-visual">
  <img src="/static/lecture_assets/gn_pretraining_pipeline.png" alt="A horizontal pipeline diagram with five stacked stages from left to right. Stage 1, in cyan, is labelled 'Web text + books + code, ~10 trillion tokens, no labels'. Stage 2, in violet, is labelled 'PRETRAINING, predict next token, billions of weight updates, ~$100 million, 2 to 6 months'. Stage 3, in orange, is labelled 'BASE MODEL, knows language, completes any text, not yet a chatbot'. Stage 4, in green, is labelled 'FINE-TUNING and RLHF, instruction-following, safety, persona, $1k to $10 million'. Stage 5, on the right, is labelled 'PRODUCT MODEL, ChatGPT, Claude, Gemini, what you call from an API'. Arrows connect each stage left to right.">
  <div class="vis-caption">The full pipeline from raw web text to a usable product model. The orange "base model" in the middle is the rarely-discussed intermediate step — it knows language but does not know it is supposed to be helpful, polite, or refuse harmful requests. All of that is added in the green stage on the right. When you fine-tune your own model, you start from the orange box; when you call an API, you are talking to the blue box on the far right.</div>
</div>

---

## What This Means for You In Practice

When you call an LLM API, you are renting the output of a $100M training run that someone else paid for. Three practical consequences fall out of that:

1. **You cannot change the weights** — the only levers you have are the *tokens you put in front of the model*. That is why prompt engineering, system prompts, and retrieval (RAG) get so much attention in later lessons. They are the only tools you actually control.
2. **Knowledge has a cutoff date** — pretraining happened *before* you sent your prompt. The model does not know about a CVE published yesterday, the patch your team shipped this morning, or the policy your CISO updated last week. RAG (Lesson 4.4) exists specifically to inject fresh knowledge at inference time without retraining anything.
3. **Fine-tuning is rarely the right answer** — most people who think they need to fine-tune actually need a better prompt, a better retrieval pipeline, or a different model. Fine-tuning is expensive, freezes the model at a point in time, and is hard to update. Reach for it only after you have exhausted prompting and retrieval.

---

## Common Mistakes

**"Pretraining and fine-tuning are the same thing"**
No. Pretraining starts from random weights and learns language from scratch on a giant unlabeled corpus. Fine-tuning starts from a finished pretrained model and nudges its weights on a much smaller, often labelled, task-specific dataset. The compute difference is roughly 10,000×.

**"The model 'remembers' things from training"**
The model has no episodic memory — it does not recall *that* it saw a specific Wikipedia article. What survives training is a statistical compression of patterns across the entire corpus. If a fact appeared often enough, it shapes the weights; if it appeared once, it almost certainly does not.

**"More tokens always means a smarter model"**
Not for free. Doubling the training tokens roughly halves the loss *delta* for a fixed model size — diminishing returns kick in fast. Frontier labs scale tokens, model size, and compute *together* (the so-called "Chinchilla scaling laws") to get the most capability per dollar. Just throwing more data at a fixed model eventually stops helping.

**"Fine-tuning teaches the model new facts"**
Mostly no. Fine-tuning is much better at teaching the model a new *style* or *output format* than at teaching it new facts. If you need the model to know facts that were not in pretraining, retrieve them at inference time (RAG) — do not try to bake them in via fine-tuning.

---

## Where This Fits in the Course

You have now seen all four ingredients of how an LLM works:

1. **Tokenisation** — text becomes integers
2. **Embeddings** — integers become vectors
3. **Attention** — vectors interact across positions
4. **Pretraining** — the weights that drive all of the above are shaped by trillions of next-token predictions

The next three lessons build *on top* of this foundation:

- **4.2 HuggingFace** — how to download and use somebody else's pretrained model in three lines of Python
- **4.3 LLM API** — how to call a hosted pretrained model over HTTP
- **4.4 RAG** — how to give a frozen pretrained model access to fresh information without retraining it

All of them assume the work in this lesson has already been done by someone else. You will spend the rest of your career *consuming* pretrained models, not *building* them.
