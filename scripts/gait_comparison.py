"""
gait_comparison.py
--------------------
Reproduces the tripod / ripple / wave gait comparison (Table II & III
of the AntBot paper) as bar charts.

FUNCTION
    None (this script directly tabulates and plots fixed comparison
    data reported in the paper -- use as a template to plug in your
    own measured/simulated values).

INPUT
    gait_names, avg_speed, body_tilt, avg_power, energy_per_m
    (hard-coded arrays below, taken from the paper's Tables II & III)

OUTPUT
    Bar chart figure saved to ../images/gait_comparison.png
"""

import matplotlib.pyplot as plt
import numpy as np

gait_names = ["Tripod", "Ripple", "Wave"]
avg_speed = [7.1, 5.9, 4.7]        # cm/s
body_tilt = [2.0, 1.4, 1.0]        # deg
avg_power = [6.5, 5.4, 5.0]        # W
energy_per_m = [0.90, 0.75, 0.83]  # Wh/m

if __name__ == "__main__":
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.2))
    colors = ["#4C72B0", "#DD8452", "#55A868"]

    axes[0].bar(gait_names, avg_speed, color=colors)
    axes[0].set_title("Average Speed")
    axes[0].set_ylabel("cm/s")

    axes[1].bar(gait_names, body_tilt, color=colors)
    axes[1].set_title("Expected Body Tilt\n(lower = more stable)")
    axes[1].set_ylabel("deg")

    axes[2].bar(gait_names, energy_per_m, color=colors)
    axes[2].set_title("Energy Efficiency")
    axes[2].set_ylabel("Wh/m")

    for ax in axes:
        ax.grid(axis="y", alpha=0.3)

    fig.suptitle("Tripod vs. Ripple vs. Wave Gait Comparison", fontsize=13)
    plt.tight_layout()
    plt.savefig("../images/gait_comparison.png", dpi=150)
    print("Saved ../images/gait_comparison.png")
