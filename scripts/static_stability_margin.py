"""
static_stability_margin.py
----------------------------
Computes and visualizes the static stability margin: the distance
from the ground-projected center of mass (CoM) to the nearest edge of
the support polygon formed by the three stance legs in a tripod gait,
matching Fig. 4 of the AntBot paper.

FUNCTION
    static_stability_margin(com_xy, support_polygon)

INPUT
    com_xy          : tuple (x, y)      -- ground projection of CoM (mm)
    support_polygon : list of (x, y)    -- vertices of the stance-leg
                                            support triangle, in order (mm)

OUTPUT
    margin : float -- distance (mm) from CoM to nearest polygon edge.
             Positive = inside polygon (stable).
             Negative = outside polygon (unstable).

Running this file saves a 2D plot to ../images/stability_analysis.png
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.path import Path


def _point_to_segment_distance(p, a, b):
    p, a, b = np.array(p), np.array(a), np.array(b)
    ab = b - a
    ap = p - a
    t = np.dot(ap, ab) / np.dot(ab, ab)
    t = np.clip(t, 0, 1)
    closest = a + t * ab
    return np.linalg.norm(p - closest)


def static_stability_margin(com_xy, support_polygon):
    n = len(support_polygon)
    distances = [
        _point_to_segment_distance(com_xy, support_polygon[i], support_polygon[(i + 1) % n])
        for i in range(n)
    ]
    margin = min(distances)

    inside = Path(support_polygon).contains_point(com_xy)
    return margin if inside else -margin


if __name__ == "__main__":
    # Two alternating tripods (example foot positions, mm)
    tripod_A = [(0, 60), (80, -50), (-80, -50)]   # e.g. Phase 1
    tripod_B = [(0, -60), (80, 50), (-80, 50)]    # e.g. Phase 2
    com = (5, 2)  # CoM projection drifts slightly as the robot walks

    margin_A = static_stability_margin(com, tripod_A)
    margin_B = static_stability_margin(com, tripod_B)
    print(f"Stability margin vs Tripod A: {margin_A:.2f} mm")
    print(f"Stability margin vs Tripod B: {margin_B:.2f} mm")
    print(f"Minimum stability margin: {min(margin_A, margin_B):.2f} mm")

    fig, ax = plt.subplots(figsize=(7, 6))

    ax.add_patch(Polygon(tripod_A, closed=True, fill=True, alpha=0.25,
                          color="tab:green", label="Support Polygon - Tripod A"))
    ax.add_patch(Polygon(tripod_B, closed=True, fill=True, alpha=0.25,
                          color="tab:red", label="Support Polygon - Tripod B"))

    ax.plot(*com, "ko", markersize=8, label="CoM Projection")
    ax.annotate(f"min margin ~ {min(margin_A, margin_B):.1f} mm",
                xy=com, xytext=(com[0] + 15, com[1] + 15),
                fontsize=9)

    ax.set_xlabel("X-axis (Direction of Travel) [mm]")
    ax.set_ylabel("Y-axis [mm]")
    ax.set_title("Static Stability Analysis: CoM vs. Support Polygon")
    ax.legend(loc="upper right", fontsize=8)
    ax.axis("equal")
    ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig("../images/stability_analysis.png", dpi=150)
    print("Saved ../images/stability_analysis.png")
