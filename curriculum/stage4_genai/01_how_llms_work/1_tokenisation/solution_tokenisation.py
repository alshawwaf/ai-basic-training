# Exercise 1 — Tokenisation: Text as Token IDs
#
# Demonstrates how LLMs convert raw text into sequences of integer IDs.
# Real models use subword tokenisation (BPE); here we use a toy word-level
# vocabulary of 20 tokens to build intuition.
#
# No dependencies required — pure Python.

# ============================================================
#   TASK 1: Build a toy vocabulary
# ============================================================
print("=" * 60)
print("  TASK 1: Build a Toy Vocabulary")
print("=" * 60)

# 18 security-themed words plus two special tokens:
#   <UNK> (ID 0) — placeholder for any word not in the vocabulary
#   <EOS> (ID 19) — marks the end of a sequence
words = [
    "the", "network", "connection", "is", "suspicious",
    "malicious", "benign", "port", "scan", "firewall",
    "blocked", "allowed", "traffic", "alert", "endpoint",
    "detected", "attack", "normal",
]

# Word-to-ID mapping (forward vocabulary)
vocab = {"<UNK>": 0}
for idx, w in enumerate(words, start=1):
    vocab[w] = idx
vocab["<EOS>"] = 19

print(f"\nVocabulary ({len(vocab)} tokens):")
for word, token_id in vocab.items():
    print(f"  {token_id:>3}: {word}")


# ============================================================
#   TASK 2: Encode a sentence into token IDs
# ============================================================
print("\n" + "=" * 60)
print("  TASK 2: Encode Sentences")
print("=" * 60)


def encode(text):
    """Convert a sentence to a list of token IDs.

    Each word is looked up in the vocabulary; unknown words map to 0 (<UNK>).
    An <EOS> token (ID 19) is appended to mark the end of the sequence.
    """
    ids = [vocab.get(word, 0) for word in text.split()]
    ids.append(vocab["<EOS>"])  # every sequence ends with <EOS>
    return ids


# Two example sentences — the second contains a word ("on") not in our vocab
test_sentences = [
    "the network connection is suspicious",
    "port scan detected on endpoint",
]

for sentence in test_sentences:
    ids = encode(sentence)
    print(f'\n  "{sentence}"')
    print(f"  -> {ids}")


# ============================================================
#   TASK 3: Decode token IDs back to text
# ============================================================
print("\n" + "=" * 60)
print("  TASK 3: Decode Back to Text")
print("=" * 60)

# Reverse vocabulary: ID -> word
id_to_word = {v: k for k, v in vocab.items()}


def decode(ids):
    """Convert a list of token IDs back to a readable string."""
    return " ".join(id_to_word.get(i, "<UNK>") for i in ids)


# Round-trip test: encode then decode should recover the original words
# (unknown words will appear as <UNK> in both directions)
for sentence in test_sentences:
    ids = encode(sentence)
    reconstructed = decode(ids)
    print(f"\n  {ids}")
    print(f'  -> "{reconstructed}"')

# Verify round-trip on a sentence with no unknown words
clean = "the network connection is suspicious"
round_trip_ok = decode(encode(clean)) == clean + " <EOS>"
print(f"\n  Round-trip successful (no OOV words): {round_trip_ok}")


# ============================================================
#   TASK 4 (Bonus): Observe OOV handling
# ============================================================
print("\n" + "=" * 60)
print("  TASK 4 (Bonus): Out-Of-Vocabulary Handling")
print("=" * 60)

# This sentence uses several words not in our 20-token vocabulary.
# Each unknown word becomes <UNK> (ID 0), destroying information.
oov_sentence = "the ransomware encrypted all files on the endpoint"
oov_ids = encode(oov_sentence)
oov_decoded = decode(oov_ids)

print(f'\n  Original : "{oov_sentence}"')
print(f"  Encoded  : {oov_ids}")
print(f'  Decoded  : "{oov_decoded}"')
print("\n  Key insight: with a tiny vocabulary, most meaning is lost.")
print("  Real LLMs use ~100,000 subword tokens to avoid this problem.")
print("  Subword tokenisation (BPE) splits rare words into known pieces,")
print('  e.g. "ransomware" -> ["ran", "som", "ware"].')

print("\n--- Exercise 1 complete. Move to ../2_embeddings/solution.py ---")
