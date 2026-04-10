# LLMs vs Classic ML

---

## The Side-by-Side

You spent Stages 1&ndash;3 building classic ML systems &mdash; logistic regression, random forests, gradient boosting. LLMs sit in a different part of the toolbox. Same goal (turn input into output), wildly different mechanics, and very different costs.

| Classic ML (Stages 1&ndash;3) | LLMs (Stage 4) |
|---|---|
| Trained from scratch on your data | **Pre-trained on ~1 trillion tokens** before you ever touch it |
| Needs labelled data | No labels needed for pre-training |
| Solves one specific task | General purpose &mdash; one model, many tasks |
| Hundreds to millions of parameters | **Billions** of parameters |
| Inference: microseconds | **Inference: seconds** |
| Runs on a laptop | Usually requires a GPU or an API call |

Two of those rows deserve unpacking &mdash; they are the rows that *change how you architect a system around an LLM*.

---

## ① Pre-trained on ~1 trillion tokens

**What "pre-trained" means.** The model has *already* learned general language patterns from a massive text corpus **before you ever touch it**. You don't train it from scratch like a logistic regression &mdash; you download the finished weights and just *use* them.

**What "1 trillion tokens" means.** Tokens, not words &mdash; recall ~1 token &asymp; 0.75 words from the tokenisation step. So 1T tokens &asymp; **750 billion words**. To put that in scale:

| Corpus | Approximate token count |
|---|---|
| All of English Wikipedia | ~4 billion |
| Every book on Project Gutenberg | ~10 billion |
| GPT-3 training set (2020) | ~300 billion |
| **A "1 trillion token" round number** | **1,000 billion** |
| LLaMA 3 (2024) | ~15 trillion |
| Modern frontier models (2025) | 10&ndash;20 trillion |

That is more text than any human could read in a thousand lifetimes. *That* is where reasoning, world knowledge, and coding ability come from &mdash; emergent side-effects of compressing this much language into the weights.

<div class="md-callout md-callout-violet">
  <strong>Why this matters for you.</strong> You will never reproduce this. Pre-training a frontier LLM costs ~$50M&ndash;$200M of GPU compute and weeks on thousands of H100s. In practice, you consume pre-trained models via API (Claude, GPT-4, Gemini) or by downloading open-weight checkpoints (LLaMA, Mistral, Qwen).
</div>

---

## ② Inference: seconds

**What "inference" means.** Running the model forward to get an answer &mdash; predicting the next token, then the next, then the next. This is what happens **every time** you send a prompt.

**Why classic ML inference is microseconds.** A logistic regression on the 64-pixel digit dataset is one matrix multiply on a 64-element vector &mdash; about 64 multiplications. A modern CPU does that in **under 10 microseconds**, faster than the network round-trip to even ask for it.

**Why LLM inference is seconds.** Three compounding reasons:

| Reason | Impact |
|---|---|
| **Model size** | A 70B-parameter model holds ~140&nbsp;GB in memory. Every token prediction touches a large fraction of those weights &mdash; gigabytes of memory bandwidth per token. |
| **Autoregressive generation** | The model produces **one token at a time**, then re-runs the whole forward pass to get the next one. A 200-token answer = 200 forward passes. |
| **Full transformer stack per token** | Each forward pass walks through dozens of attention layers, then scores all ~100,000 vocabulary tokens via softmax to pick the next one. |

**What this looks like in practice:**

| Model class | Tokens per second | A 200-token answer |
|---|---|---|
| Logistic regression (digits) | n/a &mdash; single shot | ~0.00001&nbsp;s |
| Local 7B model on a good GPU | 30&ndash;80 | 3&ndash;7&nbsp;s |
| Local 70B model on a good GPU | 5&ndash;15 | 13&ndash;40&nbsp;s |
| GPT-4o / Claude Sonnet via API | 50&ndash;100 | 2&ndash;4&nbsp;s |

<div class="md-callout md-callout-red">
  <strong>Why this matters in practice.</strong> A ~10<sup>6</sup>&times; slowdown vs. classic ML changes how systems are architected around LLMs:
  <ul>
    <li>You <strong>cannot</strong> put an LLM in the hot path of every log line, every email, every packet. Too slow, too expensive.</li>
    <li>LLMs belong on the <strong>triage / analysis / summarisation / report-writing</strong> side of a pipeline, not the real-time blocking side.</li>
    <li>High-volume pipelines use a <strong>cheap classifier in front of an expensive LLM</strong> &mdash; the classifier filters 99% of traffic, the LLM only sees the suspicious 1%.</li>
    <li>Latency budget is the single biggest constraint when wiring an LLM into a production workflow.</li>
  </ul>
</div>

---

## Picking the Right Tool

A simple rule of thumb that will keep you out of trouble:

| You have | Reach for |
|---|---|
| Structured tabular data with labels (CSV of firewall logs, user records, transaction history) | **Classic ML** &mdash; faster, cheaper, more interpretable, usually more accurate |
| Unstructured text where you need *understanding* (incident reports, threat intel articles, free-form Q&amp;A) | **LLM** &mdash; this is exactly what it was built for |
| Real-time blocking / filtering at high volume (every packet, every log line) | **Classic ML or rules** &mdash; latency rules out LLMs in the hot path |
| Triage, summarisation, report drafting on already-filtered events | **LLM** &mdash; the slow, expensive path is fine here |
| A mix: high volume in, low volume needs deep analysis | **Both** &mdash; cheap classifier filters, LLM handles the survivors |

The mistake to avoid is using GPT-4 to classify CSV rows. It is technically possible, absurdly expensive, and a Random Forest would beat it on accuracy. Right tool, right job.

---

## End of Lesson 4.1

You have now seen the entire next-token loop end to end: tokens &rarr; embeddings &rarr; attention &rarr; pretraining &rarr; the architectural consequences. The next lesson, **4.2 HuggingFace**, gets you running real pre-trained models locally without writing any training code.
