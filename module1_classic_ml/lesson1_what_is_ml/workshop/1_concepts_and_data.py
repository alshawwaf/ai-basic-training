# =============================================================================
# LESSON 1.1 - REFERENCE SOLUTION
# =============================================================================
#
# This is the complete reference solution for Lesson 1.1.
#
# BEFORE YOU LOOK AT THIS:
# ------------------------
# Follow the step-by-step walkthrough in 1_what_is_ml.md and build your own
# version in a file called my_lab_1_1.py. Only open this file to compare your
# solution once you have finished, or if you get stuck.
#
# WHAT THIS SCRIPT DOES:
# ----------------------
# Loads the digits dataset (1,797 handwritten digit images 0-9), inspects it
# from every angle, and builds intuition for what an ML model actually "sees":
# rows of numbers, not pictures.
#
# RUN IT:
# -------
#   python module1_classic_ml/lesson1_what_is_ml/workshop/1_concepts_and_data.py
# =============================================================================


# ── Imports ───────────────────────────────────────────────────────────────────
#
# numpy  - fast numerical arrays. "np" is the universal alias.
import numpy as np
#
# pandas - DataFrames (tabular data, like a spreadsheet in Python).
#          "pd" is the universal alias.
#          Key methods: .shape, .head(), .describe(), .value_counts(), .isnull()
import pandas as pd
#
# matplotlib.pyplot - plotting library. "plt" is the universal alias.
#          plt.subplots() creates a grid of panels.
#          plt.imshow()   displays a 2D array as a greyscale image.
#          plt.show()     opens the plot window.
#          plt.savefig()  saves to disk.
import matplotlib.pyplot as plt
#
# load_digits - loads the bundled digits dataset from scikit-learn.
#               No internet needed. The data is a file inside the package.
from sklearn.datasets import load_digits


# =============================================================================
# STEP 1 - Load the Dataset
# =============================================================================

digits = load_digits()
# load_digits() returns a "Bunch" object - a container with named fields:
#
#   digits.data         shape (1797, 64)     1797 images, 64 pixel values each
#   digits.target       shape (1797,)        correct label for each image (0-9)
#   digits.images       shape (1797, 8, 8)   same pixels as 8x8 grids (for plotting)
#   digits.target_names array([0,1,...,9])   the list of class labels

# Wrap the raw data in a DataFrame so we can inspect it easily.
df = pd.DataFrame(
    digits.data,                               # the 1797 x 64 array of pixel values
    columns=[f"pixel_{i}" for i in range(64)]  # name each column pixel_0, pixel_1 ...
)
# f"pixel_{i}" is an f-string - Python embeds the variable i into the string.
# For i=0 it gives "pixel_0", for i=1 "pixel_1", and so on.

df["target"] = digits.target
# Add a "target" column with the correct digit label (0-9) for each row.
# Now each row has 64 pixel features + 1 label.


# =============================================================================
# STEP 2 - Check Shape and Basic Statistics
# =============================================================================
#
# Always do this first. It confirms the data loaded correctly and tells you
# immediately how much you have to work with.

print("=" * 60)
print("STEP 2 - Shape and Basic Statistics")
print("=" * 60)

print(f"\nRows    : {digits.data.shape[0]}  (each row = one image)")
print(f"Columns : {digits.data.shape[1]}  (each column = one pixel feature)")
# .shape returns a tuple: (rows, columns)
# shape[0] = number of rows    = number of images
# shape[1] = number of columns = number of features per image

print(f"Classes : {list(digits.target_names)}")
# target_names is the list of all possible labels

print(f"\nPixel value range: min={digits.data.min():.0f}, max={digits.data.max():.0f}")
print("(0 = white background, 16 = black ink)")
# .min() and .max() scan the entire array and return the extreme values


# =============================================================================
# STEP 3 - Check Class Balance
# =============================================================================
#
# Class balance answers: do we have roughly equal examples of each class?
# In security this is critical - heavily imbalanced data produces misleading models.

print("\n" + "=" * 60)
print("STEP 3 - Class Balance")
print("=" * 60)

print("\nSamples per digit:")
print(df["target"].value_counts().sort_index().to_string())
# value_counts()  - counts how many rows have each unique value in the column
# sort_index()    - sorts by label (0,1,2...) rather than by count
# to_string()     - prints the full result (prevents pandas truncating output)

print("\nThis dataset is well-balanced (~178 per class).")
print("Compare: a real network dataset might have 950,000 normal vs 50,000 attacks.")
print("A model that always predicts 'normal' gets 95% accuracy - but catches ZERO attacks.")


# =============================================================================
# STEP 4 - Visualise Sample Images
# =============================================================================
#
# Before training anything, visually sanity-check your data.
# Ask: "Do these look like what I'd expect?"

print("\n" + "=" * 60)
print("STEP 4 - Sample Images (see plot window)")
print("=" * 60)

fig, axes = plt.subplots(2, 10, figsize=(18, 4))
# subplots(2, 10) creates a 2-row, 10-column grid of plot panels.
# figsize=(18, 4) = 18 inches wide, 4 inches tall.
# Returns: fig (the whole figure), axes (a 2x10 array of individual panels).

fig.suptitle("Two examples of each digit class (0-9)", fontsize=12)
# suptitle() adds a title above the whole figure.

for digit in range(10):
    samples = digits.images[digits.target == digit]
    # digits.target == digit  creates a True/False mask - True where label matches.
    # Applying it filters to only the 8x8 images of this digit.

    for row, sample in zip(axes, samples[:2]):
        # zip() pairs axes rows with the first 2 sample images.
        # axes[0] gets sample 0, axes[1] gets sample 1.
        row[digit].imshow(sample, cmap="gray_r")
        # imshow() renders the 8x8 number grid as a greyscale picture.
        # cmap="gray_r" = reversed greyscale: high values (ink) appear dark.
        row[digit].set_title(str(digit))
        row[digit].axis("off")  # hide axis ticks and labels

plt.tight_layout()
# tight_layout() adjusts spacing so panels don't overlap.

plt.savefig("module1_classic_ml/lesson1_what_is_ml/workshop/sample_digits.png")
plt.show()
print("What to look for: are the digits recognisable? Any that look ambiguous?")
print("Ambiguous samples = harder for the model. That's expected and normal.")


# =============================================================================
# STEP 5 - What the Model Actually Sees (Numbers, Not Images)
# =============================================================================
#
# This is the most important step for building correct intuition.
# The model NEVER sees a picture. It sees a flat row of 64 numbers.
# In security: instead of pixel values, those numbers would be
# bytes_per_second, unique_ports, entropy, protocol_flags - same structure.

print("\n" + "=" * 60)
print("STEP 5 - One Image as Raw Numbers")
print("=" * 60)

print("\nThe first image in the dataset, printed as its 8x8 pixel grid:")
print("(0 = white background, 16 = black ink)\n")

sample_image = digits.images[0]
# digits.images[0] = the first image, as an 8x8 NumPy array.

for row in sample_image.astype(int):
    # .astype(int) converts floats to integers (cleaner to print).
    # We loop over each of the 8 rows and print it as a line of numbers.
    print("  " + "  ".join(f"{v:2d}" for v in row))
    # f"{v:2d}" formats each number as 2 characters wide so columns align.

print(f"\n  ^ This is the digit '{digits.target[0]}'")
print("\nThis row of 64 numbers is exactly what the model will receive as input.")


# =============================================================================
# STEP 6 - Average Image per Class
# =============================================================================
#
# Averaging all images of each digit gives the "prototype" for that class.
# If two prototypes look very similar, the model will struggle to tell them apart.
# This is a quick way to spot which classification problems are harder.

print("\n" + "=" * 60)
print("STEP 6 - Average Images per Class (see plot window)")
print("=" * 60)

fig, axes = plt.subplots(1, 10, figsize=(18, 2))
fig.suptitle("Average pixel pattern per digit class", fontsize=12)

for digit, ax in enumerate(axes):
    # enumerate() gives both the index (digit) and the panel (ax) together.
    mean_image = digits.images[digits.target == digit].mean(axis=0)
    # .mean(axis=0) averages across all images of this digit, pixel by pixel.
    # Result: one 8x8 array showing the average brightness at each position.
    ax.imshow(mean_image, cmap="gray_r")
    ax.set_title(str(digit))
    ax.axis("off")

plt.tight_layout()
plt.savefig("module1_classic_ml/lesson1_what_is_ml/workshop/average_digits.png")
plt.show()
print("What to look for: which digits have the most similar average shapes?")
print("Hint: look at 1 vs 7, and 3 vs 8. Those pairs will have higher confusion rates.")


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print("""
What you explored in this lab:
  - 1,797 images, 64 features each, 10 balanced classes
  - The model sees rows of numbers - not pictures
  - Class balance matters: imbalanced data produces misleading models
  - Average images reveal which classes are hardest to separate

Next: open 2_linear_regression.md and run 2_linear_regression.py
""")


# =============================================================================
# EXERCISES - Uncomment and run each block one at a time
# =============================================================================
#
# These exercises build deeper intuition. Work through them after the main
# script runs cleanly. Uncomment one block, run the script, observe, re-comment,
# move to the next.

# ── Exercise 1 ────────────────────────────────────────────────────────────────
# Which pixels differ most between digit 0 and digit 1?
# Bright pixels in the output = most informative features for separating these classes.
#
# mean_0 = digits.data[digits.target == 0].mean(axis=0)
# mean_1 = digits.data[digits.target == 1].mean(axis=0)
# diff = abs(mean_0 - mean_1).reshape(8, 8)
# plt.imshow(diff, cmap="hot")
# plt.title("Pixel differences: digit 0 vs digit 1")
# plt.colorbar()
# plt.show()

# ── Exercise 2 ────────────────────────────────────────────────────────────────
# Are there any missing values in this dataset?
# In real security data there almost always are. Get used to checking.
#
# print(df.isnull().sum())
# print(f"\nTotal missing values: {df.isnull().sum().sum()}")

# ── Exercise 3 ────────────────────────────────────────────────────────────────
# What does the distribution of a single pixel look like across all images?
# pixel_32 is roughly the centre of the 8x8 grid.
#
# plt.hist(df["pixel_32"], bins=17, color="steelblue", edgecolor="white")
# plt.title("Distribution of pixel_32 (centre pixel) across all 1,797 images")
# plt.xlabel("Pixel brightness (0-16)")
# plt.ylabel("Count")
# plt.show()
# print(df["pixel_32"].describe().round(2))

# ── Exercise 4 ────────────────────────────────────────────────────────────────
# Which pixel features are most correlated with the target label?
# High correlation = potentially useful feature for the model.
#
# correlations = df.corr()["target"].abs().sort_values(ascending=False)
# print("Top 10 most correlated pixels with the digit label:")
# print(correlations.head(11).to_string())  # head(11) because "target" itself is first
