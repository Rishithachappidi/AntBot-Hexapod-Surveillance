"""
tripod_gait_trajectory.py
--------------------------
Generates the single-leg foot trajectory for one tripod gait cycle
(swing phase + stance phase) and plots it, matching Fig. 3 of the
AntBot paper.

FUNCTION
    tripod_gait_trajectory(step_length, step_height, ground_z, num_points=50)

INPUT
    step_length : float -- forward step length (mm)
    step_height : float -- max foot lift during swing phase (mm)
    ground_z    : float -- z-coordinate of the ground / stance height (mm)
    num_points  : int   -- samples per phase (default 50)

OUTPUT
    x, y, z : numpy arrays of the foot position across one full cycle
              (swing phase followed by stance phase)

Running this file saves a 3D plot to ../images/foot_trajectory.png
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401


def tripod_gait_trajectory(step_length, step_height, ground_z, num_points=50):
    half = step_length / 2

    # Swing phase: semi-elliptical arc
    t = np.linspace(0, np.pi, num_points)
    x_swing = -half + step_length * (t / np.pi)
    y_swing = np.zeros(num_points)
    z_swing = ground_z + step_height * np.sin(t)

    # Stance phase: straight line at ground level
    x_stance = np.linspace(half, -half, num_points)
    y_stance = np.zeros(num_points)
    z_stance = np.full(num_points, ground_z)

    x = np.concatenate([x_swing, x_stance])
    y = np.concatenate([y_swing, y_stance])
    z = np.concatenate([z_swing, z_stance])
    return x, y, z


if __name__ == "__main__":
    step_length = 40   # mm
    step_height = 25   # mm
    ground_z = -90     # mm

    x, y, z = tripod_gait_trajectory(step_length, step_height, ground_z)

    fig = plt.figure(figsize=(7, 6))
    ax = fig.add_subplot(111, projection="3d")

    n = len(x) // 2
    ax.plot(x[:n], y[:n], z[:n], "r--", linewidth=2, label="Swing Phase (ground clearance)")
    ax.plot(x[n:], y[n:], z[n:], "b-", linewidth=2, label="Stance Phase (propulsion)")
    ax.scatter(*[a[0] for a in (x, y, z)], color="green", s=60, label="Start of Swing")
    ax.scatter(*[a[n] for a in (x, y, z)], color="purple", s=60, label="End of Swing / Start of Stance")

    ax.set_xlabel("X-axis (Forward/Backward) [mm]")
    ax.set_ylabel("Y-axis (Sideways) [mm]")
    ax.set_zlabel("Z-axis [mm]")
    ax.set_title("Simulated Foot Trajectory - One Gait Cycle")
    ax.legend(loc="upper left", fontsize=8)

    plt.tight_layout()
    plt.savefig("../images/foot_trajectory.png", dpi=150)
    print("Saved ../images/foot_trajectory.png")
