# Facilitator Guide — Session 3.3: Convolutional Networks

> **Stage:** 3  |  **Week:** 9  |  **Lecture deck:** `Lecture-12-Convolutional-Networks.pptx`  |  **Total time:** 60 min

---

## Pre-Session Checklist

- [ ] Reviewed the lecture slides and all 4 exercise guides
- [ ] Prepared a whiteboard diagram of the CNN pipeline: Input → Conv → Pool → Conv → Pool → Flatten → Dense → Output
- [ ] Run through the "why dense fails on images" exercise — confirmed the accuracy gap between dense and CNN is clearly visible
- [ ] Reviewed the malware visualisation context exercise — be ready to explain how binary files can be converted to greyscale images

---

## Session Flow

| Time | Section | Activity |
|------|---------|----------|
| 0:00 – 0:05 | Recap | Quick: "Last session we fought overfitting. Today we tackle a new question: what if the data has spatial structure — pixels next to each other, bytes in sequence? Can a flat dense layer capture that?" Let participants think about why position matters. |
| 0:05 – 0:15 | Why dense fails on images | Walk through Exercise 1 concepts. A dense layer treats every pixel independently — it has no concept of "next to." Shuffling pixel order would not change the dense layer's output. Ask: "If I scrambled every pixel in a photo, could you still recognise it? Neither can a dense network." |
| 0:15 – 0:25 | The convolution operation | Draw a 3x3 filter sliding across a small grid on the whiteboard. Show how it computes a weighted sum at each position. Key insight: "The same filter slides everywhere — it detects the same pattern regardless of position. That's translation invariance." Use a simple edge-detection filter as the example. |
| 0:25 – 0:35 | CNN architecture: Conv → Pool → Dense | Walk through the full pipeline on the whiteboard. Conv layers detect local patterns (edges, textures). Pooling layers shrink the spatial dimensions and make the model more robust to small shifts. Dense layers at the end combine the detected patterns into a classification. |
| 0:35 – 0:50 | Hands-on exercises | Participants work through Exercises 2-4: conv and pooling, build and train CNN, malware visualisation context. Exercise 1 (why dense fails) was discussed — participants can revisit. Circulate and help — shape mismatches are the most common error in CNN exercises. |
| 0:50 – 0:55 | Security applications | Facilitate discussion on the malware visualisation angle: "Malware researchers convert binary executables to greyscale images and classify them with CNNs. Why does this work?" Answer: malware families share structural patterns in their binaries — code sections, packing routines, resource layouts — that appear as visual textures. |
| 0:55 – 1:00 | Wrap-up | Summarise: "CNNs exploit spatial structure. That applies to images, but also to any data with local patterns — network packet sequences, binary file layouts, even log entries arranged in time. Next session: how to tune all the knobs we've introduced." |

---

## Key Points to Emphasise

1. **Convolution exploits local spatial structure** — a convolutional filter detects the same pattern at every position in the input. This is fundamentally different from a dense layer, which treats every input element independently. For any data where neighbouring elements are related (pixels, bytes, time steps), convolution is the right inductive bias.
2. **The CNN pipeline follows a clear hierarchy: detect → shrink → classify** — convolutional layers detect local patterns, pooling layers reduce spatial size and add robustness, and dense layers at the end make the final decision. Understanding this pipeline makes it easy to read and modify any CNN architecture.
3. **Malware binary visualisation is a real and active area of security research** — converting executables to greyscale images and classifying them with CNNs is not a toy example. It is used in production by security vendors and has been published in peer-reviewed security conferences. This technique works because malware families share structural byte patterns that manifest as visual textures.

---

## Discussion Prompts

- "A 28x28 image has 784 pixels. A dense layer connecting all 784 to 128 neurons needs 100,352 weights. A 3x3 convolutional filter needs only 9 weights but slides across the entire image. What are the implications for training speed, overfitting, and data efficiency?"
- "You convert a malware binary into a 256x256 greyscale image and feed it to a CNN. A colleague says this is 'throwing away information.' Is that true? What information is preserved and what is lost?"
- "Could you use a CNN on network traffic data? How would you structure the input — what would the 'image' look like?"

---

## Common Questions and Answers

**Q: Why is pooling necessary? Can't I just use more convolutions?**
A: Pooling serves two purposes: it reduces the spatial dimensions (making the network computationally cheaper) and it provides a degree of translation invariance (a pattern detected at position 5 or position 6 produces the same pooled output). You can build architectures without pooling — some modern designs use strided convolutions instead — but pooling remains a simple, effective default.

**Q: How does converting a binary file to an image actually work?**
A: Each byte in the executable (value 0–255) becomes one pixel in a greyscale image (0 = black, 255 = white). You read the raw bytes sequentially and arrange them into rows of a fixed width (commonly 256 or 512 pixels). The resulting image reveals structural patterns: code sections look different from data sections, packed malware looks different from unpacked, and different compiler toolchains produce different visual textures.

**Q: Do I need a GPU to train CNNs?**
A: For the exercises in this session (small images, simple architectures), a CPU is fine — training takes seconds to minutes. For production CNNs on large datasets (thousands of high-resolution images), a GPU accelerates training by 10–50x and becomes practically necessary. Cloud GPU instances are a cost-effective option if local hardware is limited.

---

## Facilitator Notes

- The "why dense fails" exercise (Exercise 1) sets up the entire session. If participants do not understand why a dense layer struggles with spatial data, the motivation for convolution will feel arbitrary. Spend the time to make this clear before moving on.
- Shape errors are the single most common problem in CNN exercises. Participants will see errors like "expected input shape (None, 28, 28, 1) but got (None, 784)." Teach them to read shape errors: "The model expected a 28x28 image with 1 channel, but got a flat vector of 784 numbers. You need to reshape."
- The malware visualisation exercise (Exercise 4) is the security hook that makes CNNs relevant to the audience. Even if time is short, do not skip the discussion. Showing an actual greyscale image of a binary file (if available in the slides) creates a strong visual memory.
- Some participants may ask about colour images and 3-channel inputs (RGB). Briefly explain: "Same idea, but the filter is 3x3x3 instead of 3x3x1 — it slides across all three colour channels simultaneously." Do not go deeper unless the group is advanced.

---

## Connections to Sales Conversations

- **When a customer asks:** "How do you detect malware that has never been seen before — zero-day threats?"
- **You can now say:** "One approach is to analyse the structure of the file itself, not just signatures or hashes. We can convert a binary executable into a visual representation and use convolutional neural networks to classify it based on structural patterns — the layout of code sections, packing characteristics, and byte-level textures. Malware families share these structural fingerprints even when the specific code changes. This means we can detect variants that signature-based tools miss, because we're recognising the structural family, not the exact sample."
