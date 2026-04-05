# Facilitator Guide — Session 4.1: How LLMs Work

> **Stage:** 4  |  **Week:** 11  |  **Lecture deck:** `Lecture-14-How-LLMs-Work.pptx`  |  **Total time:** 60 min

---

## Pre-Session Checklist

- [ ] Reviewed the lecture slides and all 3 exercise guides
- [ ] Run through the tokenisation exercise — confirmed the vocab lookup and `<UNK>` handling work correctly
- [ ] Run through the embeddings exercise — confirmed cosine similarity output makes intuitive sense (e.g., "malicious" closer to "attack" than to "normal")
- [ ] Prepared a whiteboard-ready comparison table: classic ML (tabular features, explicit training) vs LLMs (text in, text out, pre-trained on internet-scale data)

---

## Session Flow

| Time | Section | Activity |
|------|---------|----------|
| 0:00 – 0:05 | Bridge from Stage 3 | "In neural networks, we designed feature vectors by hand. What if the model could read raw text and figure out the features itself? That's what LLMs do." |
| 0:05 – 0:15 | Next-token prediction | Explain LLMs as sophisticated autocomplete: given a sequence of tokens, predict the next one. Show a simple example: "The firewall blocked the ___." The model assigns probabilities to every token in its vocabulary. Draw the pipeline on the whiteboard: text → tokens → embeddings → transformer → probability distribution → next token. |
| 0:15 – 0:25 | Tokenisation and embeddings | Explain that LLMs don't see words — they see token IDs, which get converted to numerical vectors (embeddings). Tokens can be words, sub-words, or single characters. Embeddings capture meaning: similar words end up as nearby vectors. Use the "map coordinates" analogy — each word gets a location in meaning-space, and words with similar meanings are close together. |
| 0:25 – 0:35 | Attention mechanism | Explain that attention lets each token look at every other token and decide which ones matter most for its meaning. "blocked" attends strongly to "firewall" (what did the blocking?) and "connection" (what was blocked?). This is the key innovation that makes transformers work — context is everything. |
| 0:35 – 0:50 | Hands-on exercises | Participants work through Exercises 1-3: tokenisation (building a vocab and encoding text), embeddings (cosine similarity between security terms), and attention (interpreting an attention matrix). Circulate and help. |
| 0:50 – 0:55 | Classic ML vs LLMs | Draw a comparison table: classic ML needs structured features and labelled data for each task; LLMs are pre-trained once on massive text and then applied to many tasks. Ask: "When would you still choose classic ML over an LLM?" (Structured tabular data, latency constraints, interpretability requirements.) |
| 0:55 – 1:00 | Wrap-up | Preview Session 4.2 (HuggingFace). Key bridge: "Now you know what's happening inside. Next session, we'll use pre-trained models off the shelf — no training required — and apply them to real security text." |

---

## Key Points to Emphasise

1. **LLMs are next-token predictors, not reasoning engines** — understanding this grounds every future discussion. When a vendor says their product "understands" threats, what's actually happening is sophisticated pattern completion based on training data. This framing helps participants evaluate AI claims with clear eyes.
2. **Embeddings turn words into numbers that capture meaning** — this is the bridge between human language and mathematics. Cosine similarity between embedding vectors is the foundation of semantic search, clustering, and retrieval — all techniques participants will use in later sessions.
3. **Attention is what makes context work** — the word "bank" means different things in "river bank" vs "bank vault." Attention lets the model weigh surrounding words to resolve ambiguity. This is why LLMs can handle nuance that keyword-based tools cannot.

---

## Discussion Prompts

- "A vendor says their product uses 'AI-powered threat detection' on log data. Knowing what you now know about tokenisation and next-token prediction — what questions would you ask them about how it actually works?"
- "You see two security sentences: 'Lateral movement via SMB' and 'File sharing across the network.' A human analyst knows these could describe the same activity. How do embeddings help a model see this similarity when the words are completely different?"
- "Attention tells us which words the model focuses on. If you could see the attention weights for an LLM analysing a phishing email, what words would you expect it to attend to most strongly? Why?"

---

## Common Questions and Answers

**Q: How is an LLM different from the neural networks we built in Stage 3?**
A: The Stage 3 networks were small feed-forward networks trained on structured numeric data for a single task. LLMs are transformer-based networks with billions of parameters, pre-trained on massive text corpora. The key architectural difference is the attention mechanism — it lets LLMs handle variable-length text and capture long-range dependencies between words. Think of Stage 3 as learning to recognise single patterns; LLMs learn language itself.

**Q: Do LLMs actually "understand" language?**
A: They are extremely good at predicting what text should come next, based on statistical patterns in their training data. Whether that constitutes "understanding" is debated. What matters practically is that they produce useful output for many tasks — but they can also produce confident nonsense (hallucinations), because the prediction mechanism has no built-in fact-checking. Always verify LLM output against authoritative sources.

**Q: Why do we need to learn the internals if we're just going to use APIs?**
A: Knowing how tokenisation, embeddings, and attention work helps you debug and optimise in practice. For example: if your security logs exceed the token limit, you need to understand tokenisation to chunk them intelligently. If semantic search returns poor results, understanding embeddings helps you diagnose whether the issue is the model, the data, or the query. The internals also help you evaluate vendor claims critically.

---

## Facilitator Notes

- The tokenisation exercise is pure Python with no dependencies — it's a good warm-up that builds confidence before the NumPy-based exercises. Make sure participants understand that real LLM tokenisers (like GPT's BPE) use sub-word tokens, not whole words — the exercise simplifies this deliberately.
- The embeddings exercise produces a cosine similarity matrix. Project it on screen and ask: "Which pair of security terms is most similar? Does that match your intuition?" The moment participants see "malicious" and "attack" are close while "malicious" and "normal" are far apart, the concept clicks.
- The attention exercise uses a hand-crafted 5x5 attention matrix. Emphasise that in real transformers, these weights are learned — not hand-set. The exercise just makes the concept visible and concrete.

---

## Connections to Sales Conversations

- **When a customer asks:** "Every vendor says they use AI. How do I know if it's real or just a buzzword?"
- **You can now say:** "Great question. There are specific things to look for. Ask the vendor whether the model uses embeddings or just keyword matching — that tells you whether it can handle paraphrasing and novel phrasing. Ask whether it uses attention-based architecture or simpler pattern matching — that determines how well it handles context. These aren't just technical details; they directly affect detection quality. I can walk you through what to look for in a vendor evaluation."
