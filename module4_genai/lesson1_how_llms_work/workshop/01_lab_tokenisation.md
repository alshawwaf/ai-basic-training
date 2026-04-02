# Lab — Exercise 1: Tokenisation: Text as Token IDs

> Follow each step in order. Copy the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `01_tokenisation.py` in this folder.

---

## Step 2: Add the imports

No external libraries are needed. Add this comment to the top of your file so it is clear this is pure Python:

```python
# No external libraries needed — this is pure Python
```

---

## Step 3: Build the vocabulary

A vocabulary maps every word the model knows to an integer ID. `<UNK>` (ID 0) handles any word not in the vocabulary, and `<EOS>` (ID 19) signals the end of a sequence.

Add this to your file:

```python
vocab = {
    "<UNK>": 0,
    "the": 1, "network": 2, "connection": 3, "is": 4,
    "suspicious": 5, "malicious": 6, "benign": 7,
    "port": 8, "scan": 9, "firewall": 10, "blocked": 11,
    "allowed": 12, "traffic": 13, "alert": 14,
    "endpoint": 15, "detected": 16, "attack": 17, "normal": 18,
    "<EOS>": 19,
}

print("Vocabulary (20 tokens):")
for word, id_ in vocab.items():
    print(f"  {id_:2d}: {word}")
```

Run your file. You should see:
```
Vocabulary (20 tokens):
   0: <UNK>
   1: the
   2: network
   3: connection
   4: is
   5: suspicious
   6: malicious
   7: benign
   8: port
   9: scan
  10: firewall
  11: blocked
  12: allowed
  13: traffic
  14: alert
  15: endpoint
  16: detected
  17: attack
  18: normal
  19: <EOS>
```

---

## Step 4: Encode sentences to token IDs

The `encode` function splits text on spaces, maps each word to its ID (using 0 for unknowns), and appends the end-of-sequence token.

Add this to your file:

```python
def encode(text):
    ids = [vocab.get(word, 0) for word in text.split()]
    ids.append(vocab["<EOS>"])
    return ids

sentence1 = "the network connection is suspicious"
sentence2 = "port scan detected on endpoint"

print(f'"{sentence1}" → {encode(sentence1)}')
print(f'"{sentence2}" → {encode(sentence2)}')
```

Run your file. You should see:
```
"the network connection is suspicious" → [1, 2, 3, 4, 5, 19]
"port scan detected on endpoint"       → [8, 9, 16, 0, 15, 19]
```

Note: "on" is not in the vocabulary, so it maps to 0 (`<UNK>`).

---

## Step 5: Decode token IDs back to text

The reverse vocabulary maps IDs back to words. The `decode` function reconstructs the sentence from a list of IDs.

Add this to your file:

```python
id_to_word = {id_: word for word, id_ in vocab.items()}

def decode(ids):
    return " ".join(id_to_word[i] for i in ids)

encoded = encode(sentence1)
decoded = decode(encoded)
print(f"{encoded} → \"{decoded}\"")
print(f"Round-trip successful: {decoded == sentence1 + ' <EOS>'}")
```

Run your file. You should see:
```
[1, 2, 3, 4, 5, 19] → "the network connection is suspicious <EOS>"
Round-trip successful: True
```

---

## Step 6: Observe OOV handling (Bonus Task 4)

Words not in the vocabulary all collapse to the same `<UNK>` token — the model cannot distinguish between them. This is the OOV (out-of-vocabulary) problem.

Add this to your file:

```python
oov_sentence = "the ransomware encrypted all files on the endpoint"
oov_encoded = encode(oov_sentence)
oov_decoded = decode(oov_encoded)
print(f"\nOriginal : {oov_sentence}")
print(f"Encoded  : {oov_encoded}")
print(f"Decoded  : {oov_decoded}")
print("Note: ransomware, encrypted, all, files, on → all become <UNK> (ID 0). "
      "The model cannot distinguish between these unknown words.")

print("\n--- Exercise 1 complete. Move to 02_embeddings.py ---")
```

Run your file. You should see:
```
Original : the ransomware encrypted all files on the endpoint
Encoded  : [1, 0, 0, 0, 0, 0, 1, 15, 19]
Decoded  : the <UNK> <UNK> <UNK> <UNK> <UNK> the endpoint <EOS>
Note: ransomware, encrypted, all, files, on → all become <UNK> (ID 0). The model cannot distinguish between these unknown words.

--- Exercise 1 complete. Move to 02_embeddings.py ---
```

---

## Your completed script

At this point your file contains all the working code. Compare it against the matching `_solution_` file (`01_solution_tokenisation.py`) if anything looks different.
