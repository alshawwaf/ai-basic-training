# Facilitator Guide — Session 4.2: HuggingFace Pre-trained Models

> **Stage:** 4  |  **Week:** 11  |  **Lecture deck:** `Lecture-15-HuggingFace.pptx`  |  **Total time:** 60 min

---

## Pre-Session Checklist

- [ ] Reviewed the lecture slides and all 3 exercise guides
- [ ] Run through the zero-shot classification exercise — confirmed model downloads complete and classification labels return sensible scores for the sample log entries
- [ ] Run through the sentence embeddings exercise — confirmed cosine similarity matrix shows attack logs clustering apart from benign logs
- [ ] Run through the semantic search exercise — confirmed queries like "credential theft" return the Mimikatz knowledge base entry
- [ ] Pre-downloaded model weights to avoid long waits during the session: `all-MiniLM-L6-v2` (~80 MB) and the zero-shot classification model (~550 MB) should be cached at `~/.cache/huggingface/`

---

## Session Flow

| Time | Section | Activity |
|------|---------|----------|
| 0:00 – 0:05 | Recap | "Last session we looked inside an LLM — tokens, embeddings, attention. Today, we skip training entirely and use models that someone else already trained. One line of code, real results." |
| 0:05 – 0:15 | The pipeline API | Explain HuggingFace's `pipeline()` as a single function that wraps model loading, tokenisation, inference, and output formatting. Walk through the available tasks: text-classification, zero-shot-classification, summarisation, question-answering, and more. Emphasise: the model is pre-trained — you provide no training data. |
| 0:15 – 0:25 | Zero-shot classification | Demonstrate classifying a security log entry into categories the model has never been trained on. Explain the trick: the model was trained on natural language inference (NLI), so it can judge whether a text "entails" a label. Draw the flow on the whiteboard: log entry + candidate labels → model → confidence scores. Ask: "Where else could you use this in a SOC?" |
| 0:25 – 0:35 | Sentence embeddings and semantic search | Explain that `SentenceTransformer` converts full sentences into vectors. Show cosine similarity: attack logs cluster together, benign logs cluster together — even though they use completely different words. Then show semantic search: encode a query, compare against a knowledge base of embedded documents, return the closest matches. |
| 0:35 – 0:50 | Hands-on exercises | Participants work through Exercises 1-3: zero-shot classification of security logs, building a cosine similarity matrix of sentence embeddings, and semantic search over a security knowledge base. Circulate and help — watch for slow model downloads on first run. |
| 0:50 – 0:55 | When to use pre-trained models vs training your own | Discuss: pre-trained models work surprisingly well out of the box for general tasks. Fine-tuning is only needed when domain-specific accuracy is critical and you have labelled data. For most security use cases — classification, search, summarisation — pre-trained models are the pragmatic starting point. |
| 0:55 – 1:00 | Wrap-up | Preview Session 4.3 (LLM APIs). Key bridge: "HuggingFace runs models locally on your machine. Next session, we'll call cloud-hosted LLMs via API — much larger models, much more capable, but now your data leaves your network. That trade-off matters in security." |

---

## Key Points to Emphasise

1. **Zero-shot classification requires no training data** — you provide candidate labels at inference time, and the model scores each one. For security teams drowning in uncategorised alerts or threat intel, this is immediately useful: classify without the months-long process of building a labelled dataset.
2. **Sentence embeddings capture semantic meaning, not keywords** — "Outbound connection to C2 server" and "Lateral movement via SMB" are semantically closer (both are attack activity) than either is to "Scheduled backup completed" — even though they share no words. This is the foundation of semantic search and intelligent document retrieval.
3. **Pre-trained models are the 80/20 rule in action** — someone else spent millions training these models on internet-scale data. You download them in one line and apply them to your problem. Fine-tuning is the last 20% — only worth it when the general model measurably falls short for your specific domain.

---

## Discussion Prompts

- "Your threat intel team receives 200 reports per week and currently tags them manually. How would you use zero-shot classification to automate the first pass? What labels would you choose?"
- "A customer asks: 'We already have keyword search — why do we need semantic search?' What's your answer, and what example would you use to demonstrate the difference?"
- "You run a pre-trained sentence embedding model on your internal incident reports and the results are mediocre. What could be going wrong, and what would you try before fine-tuning?"

---

## Common Questions and Answers

**Q: How can zero-shot classification work if the model was never trained on security data?**
A: The model was trained on natural language inference (NLI) — given a premise and a hypothesis, it predicts whether the premise entails, contradicts, or is neutral to the hypothesis. When you pass a log entry and candidate labels, the model treats each label as a hypothesis: "This text is about [label]." Because it understands language broadly, it can generalise to domains it was never explicitly trained on — including security. It won't match a domain-specific model, but it's remarkably effective as a starting point.

**Q: Are these models safe to run on sensitive data since they run locally?**
A: Yes — that's a key advantage. The models run entirely on your machine, and no data is sent to any external service. The model weights are downloaded once from HuggingFace and cached locally. This makes local models suitable for processing sensitive logs, threat intel, and internal documents that you would never want to send to a cloud API.

**Q: How do I know which pre-trained model to use for my task?**
A: HuggingFace has a model hub with thousands of models, filterable by task (text classification, embeddings, summarisation, etc.). For sentence embeddings, `all-MiniLM-L6-v2` is a strong default — fast, small, and effective. For zero-shot classification, models trained on NLI (like `facebook/bart-large-mnli`) are the standard choice. Start with the most popular model for your task, evaluate it on your data, and only switch if results are unsatisfactory.

---

## Facilitator Notes

- Model download times can disrupt the session if participants haven't pre-cached the weights. If bandwidth is limited, consider downloading the models onto a shared drive or USB and distributing them. The exercise guide includes a `pip install` step — confirm everyone has the packages installed before the hands-on block.
- The zero-shot classification exercise classifies security log entries. When results appear, pause and discuss the confidence scores as a group: "The model says this log is 92% 'brute force attack' — is that right? What about the 5% it assigned to 'port scan'?" This grounds the concept in judgement, not just code.
- The semantic search exercise uses a small knowledge base of CVEs and attack techniques. Once participants get results, ask: "If this knowledge base had 10,000 entries instead of 6, what would change?" (Answer: almost nothing in the code — embeddings scale well.) This sets up the RAG discussion in Session 4.4.

---

## Connections to Sales Conversations

- **When a customer asks:** "We have thousands of unclassified alerts. How can AI help without spending months building training data?"
- **You can now say:** "Zero-shot classification lets you define your categories — say phishing, brute force, data exfiltration, lateral movement — and the model scores every alert against those labels immediately, with no training data. It runs locally, so your sensitive alert data never leaves your environment. It's not a replacement for a tuned detection model, but it can cut your triage backlog dramatically while you build your labelled dataset. I can show you a working example in five minutes."
