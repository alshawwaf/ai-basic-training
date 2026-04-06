"""
Explore 09 — The Model's Eye View
=================================
A model never "sees" an image. It only sees a flat list of 64 numbers.
This is the same kind of input it gets for a network log, a transaction
record, or a system call trace.

This script gives you the raw numbers and asks you to guess the digit.
No image. Just numbers. See how hard the model's job actually is.

After 5 rounds you'll get a score. The point isn't to be perfect — it's
to feel why classifiers need many features and lots of training data.
"""
import random
from sklearn.datasets import load_digits

ROUNDS = 5

digits = load_digits()


def render_text_grid(flat_64):
    """Cheat-sheet view: print the flat 64-vector as 8 rows of 8 numbers."""
    print()
    print("       col: 0  1  2  3  4  5  6  7")
    print("       " + "-" * 26)
    for r in range(8):
        row = flat_64[r * 8:(r + 1) * 8]
        print(f"  row {r}: " + "  ".join(f"{int(v):2d}" for v in row))
    print()


def play_round(round_num):
    print()
    print("=" * 56)
    print(f"  Round {round_num} of {ROUNDS}")
    print("=" * 56)
    idx = random.randint(0, len(digits.data) - 1)
    flat = digits.data[idx]
    truth = digits.target[idx]

    print()
    print("Raw feature vector (64 numbers, brightness 0..16):")
    print(list(int(v) for v in flat))
    print()
    print("This is exactly what the model receives. Nothing else.")
    print("Tip: type 'show' to see the same numbers laid out as a grid.")
    print("     type 'skip' to skip this round.")

    while True:
        guess = input("Your guess (0-9, 'show', or 'skip'): ").strip().lower()
        if guess == "show":
            render_text_grid(flat)
            continue
        if guess == "skip":
            print(f"  Skipped. Real digit was {truth}.")
            return False
        if guess.isdigit() and 0 <= int(guess) <= 9:
            if int(guess) == truth:
                print(f"  Correct! It was a {truth}.")
                return True
            print(f"  Nope, it was a {truth}.")
            return False
        print("  Please type a single digit 0-9, 'show', or 'skip'.")


def main():
    print("Welcome to The Model's Eye View.")
    print()
    print("You will see 64 raw pixel brightnesses and have to guess the digit.")
    print("This is the same kind of feature vector a model gets for any task —")
    print("network packets, login attempts, file metadata, EEG samples, etc.")

    score = 0
    for r in range(1, ROUNDS + 1):
        if play_round(r):
            score += 1

    print()
    print("=" * 56)
    print(f"  Final score: {score} / {ROUNDS}")
    print("=" * 56)
    print()
    if score == ROUNDS:
        print("Astonishing. You're reading raw pixel arrays in your head.")
    elif score >= ROUNDS // 2:
        print("Solid. Notice how much harder it is without seeing the image.")
    else:
        print("Hard, isn't it? A trained model gets this right ~95% of the time")
        print("by spotting tiny statistical patterns across all 64 numbers.")
    print()
    print("Security parallel:")
    print("  Network log row : [1048576, 443, 0.24, 2, 14, ...]")
    print("  Digit pixels    : [   0,    0,    5,  13, 9, ...]")
    print("Same shape. Same algorithms. Different domain.")
    print()
    print("That's the end of the explore-first track. You're ready for the labs.")


if __name__ == "__main__":
    main()
