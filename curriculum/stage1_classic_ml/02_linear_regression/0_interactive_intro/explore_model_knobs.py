"""
Explore — What Is a Model?
==========================
A "model" is just a small bag of numbers. For linear regression that
bag has exactly TWO numbers: a weight and a bias. Together they describe
a single straight line:

    response_time = (weight * requests_per_second) + bias

That's it. The model is not an algorithm, it is not code, it is not a
neural network — it is two numbers stored in memory. When you save a
trained model to disk, those two numbers are what gets saved.

In this script YOU are the algorithm. Drag the two sliders to find the
weight and bias that make the red line cut through the data cloud as
neatly as possible. Watch the error metric (RMSE) drop as your line
gets closer to the truth.

Then click "Let the algorithm do it" — sklearn's LinearRegression will
solve the same problem analytically, snap the sliders to its optimal
values, and show you what "trained" really means.

CHALLENGES:
1. Without touching the sliders, what is the RMSE of a random model?
2. How low can YOU push the RMSE by hand? Write your best score down.
3. Click "Let the algorithm do it". By how much did it beat you?
4. The optimal weight is roughly 1.8 and the bias is roughly 30. What
   would those two numbers mean to a SOC analyst monitoring the server?
"""
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from sklearn.linear_model import LinearRegression

if "agg" in plt.get_backend().lower():
    print("ERROR: Non-interactive matplotlib backend detected.")
    print("Run from a normal terminal: python explore_model_knobs.py")
    sys.exit(1)

# Same synthetic dataset as the rest of lesson 1.2
np.random.seed(42)
n = 500
rps = np.random.uniform(5, 200, n)
ms = 1.8 * rps + 30 + np.random.normal(0, 15, n)

print("Dataset: 500 measurements of (requests_per_second, response_time_ms)")
print("True relationship: response_time = 1.8 * rps + 30 + noise")
print()
print("YOUR JOB: drag the two sliders so the red line fits the cloud.")
print("The model is literally those two slider values.")
print()

# ── Layout ──────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(10, 7))
fig.suptitle("What is a Model? — drag the two knobs to BE the algorithm",
             fontsize=13)

ax_plot = fig.add_axes([0.10, 0.34, 0.85, 0.56])
ax_w = fig.add_axes([0.18, 0.20, 0.65, 0.03])
ax_b = fig.add_axes([0.18, 0.14, 0.65, 0.03])
ax_btn_fit = fig.add_axes([0.18, 0.04, 0.30, 0.05])
ax_btn_reset = fig.add_axes([0.53, 0.04, 0.30, 0.05])

# Sliders start at deliberately bad values so the first line is obviously wrong
slider_w = Slider(ax_w, "weight", -2.0, 5.0, valinit=0.5, valstep=0.05)
slider_b = Slider(ax_b, "bias", -100.0, 200.0, valinit=120.0, valstep=1.0)

btn_fit = Button(ax_btn_fit, "Let the algorithm do it")
btn_reset = Button(ax_btn_reset, "Reset to random")

# x values for drawing the line smoothly
x_line = np.linspace(rps.min(), rps.max(), 100)


def redraw(_=None):
    w = slider_w.val
    b = slider_b.val
    y_pred = w * rps + b
    rmse = float(np.sqrt(np.mean((ms - y_pred) ** 2)))

    ax_plot.cla()
    ax_plot.scatter(rps, ms, alpha=0.35, s=18,
                    color="steelblue", label="actual data")
    ax_plot.plot(x_line, w * x_line + b,
                 color="crimson", linewidth=2.5,
                 label=f"model: y = {w:.2f}*x + {b:.1f}")
    ax_plot.set_xlabel("requests per second")
    ax_plot.set_ylabel("response time (ms)")
    ax_plot.set_ylim(-50, 500)
    ax_plot.set_title(
        f"RMSE = {rmse:.1f} ms     "
        f"the model IS those two numbers:  w={w:.2f},  b={b:.1f}"
    )
    ax_plot.legend(loc="upper left")
    ax_plot.grid(True, alpha=0.2)
    fig.canvas.draw_idle()


def on_fit(_event):
    """Fit a real LinearRegression and snap the sliders to its parameters."""
    model = LinearRegression()
    model.fit(rps.reshape(-1, 1), ms)
    optimal_w = float(model.coef_[0])
    optimal_b = float(model.intercept_)
    print(f"Algorithm picked   w = {optimal_w:.4f}   b = {optimal_b:.4f}")
    slider_w.set_val(round(optimal_w, 2))
    slider_b.set_val(round(optimal_b, 1))


def on_reset(_event):
    """Randomise both slider values to give the learner a fresh starting line."""
    new_w = float(np.random.uniform(-2, 5))
    new_b = float(np.random.uniform(-100, 200))
    slider_w.set_val(round(new_w, 2))
    slider_b.set_val(round(new_b, 1))


slider_w.on_changed(redraw)
slider_b.on_changed(redraw)
btn_fit.on_clicked(on_fit)
btn_reset.on_clicked(on_reset)

redraw()
plt.show()

print()
print("Takeaway: a 'trained model' is nothing more than the numeric values")
print("of its parameters. Linear regression: 2 numbers. The digits classifier")
print("you met in lesson 1.1: ~640 numbers. GPT-4: a few hundred billion.")
print("Same idea, different scale.")
print()
print("The algorithm's job is to PICK those numbers. Once it has, the")
print("algorithm is done — you ship the numbers (the model) to production.")
