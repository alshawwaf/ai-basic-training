# Explore 9 — The Model's Eye View
#
# A model never sees an image. It sees a row of 64 numbers.
# Can YOU identify a digit from just the numbers?
#
#   python explore_09_model_eye_view.py
#
# You'll get 5 rounds. See how many you can guess correctly.

import numpy as np
from sklearn.datasets import load_digits

digits = load_digits()

print("=" * 60)
print("  THE MODEL'S EYE VIEW")
print("=" * 60)
print()
print("A machine learning model never sees images.")
print("It receives a flat row of 64 numbers (0-16).")
print("Can you identify the digit from just the numbers?")
print()

correct = 0
rounds = 5

for r in range(rounds):
    idx = np.random.randint(len(digits.data))
    flat = digits.data[idx].astype(int)
    label = digits.target[idx]
    image = digits.images[idx].astype(int)

    print(f"{'─' * 60}")
    print(f"  Round {r + 1} of {rounds}")
    print(f"{'─' * 60}")
    print()
    print("The model receives this:")
    print(flat)
    print()

    try:
        guess = input("What digit is this? (0-9): ").strip()
        guess = int(guess)
    except (ValueError, EOFError):
        guess = -1

    print(f"\nAnswer: {label}")
    print()
    print("As an 8x8 grid:")
    for row in image:
        print("  " + "  ".join(f"{v:2d}" for v in row))

    if guess == label:
        correct += 1
        print(f"\n  Correct!")
    else:
        print(f"\n  Not quite. The pattern is hard to see in raw numbers.")

    print()

print("=" * 60)
print(f"  Score: {correct}/{rounds}")
print("=" * 60)

if correct >= 4:
    print("\n  Impressive! You're reading numbers like a model.")
elif correct >= 2:
    print("\n  Not bad. With practice, patterns emerge.")
else:
    print("\n  That's the point — raw numbers are hard for humans.")
    print("  But models process them in milliseconds.")

print()
print("Now imagine a network intrusion model.")
print("Instead of pixel values, it receives:")
print()
print("  [1048576, 443, 2.4, 14, 0, 3, 1, 0.87, 2048, ...]")
print()
print("  bytes_sent    = 1048576")
print("  dest_port     = 443")
print("  duration_sec  = 2.4")
print("  packets       = 14")
print("  tcp_flags     = 0")
print("  protocol      = 3 (TCP)")
print("  is_encrypted  = 1")
print("  entropy       = 0.87")
print("  payload_size  = 2048")
print()
print("Same idea. Different domain. Just numbers in a row.")
print("That's what machine learning works with — always.")
print()
print("  You've completed all 10 exploration steps!")
print("  To review the theory behind what you discovered,")
print("  read the lecture.md files in each exercise folder.")
