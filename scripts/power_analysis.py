"""
power_analysis.py
--------------------
Simulates the battery discharge profile and current draw pattern
during tripod-gait operation, matching Fig. 5 (battery voltage) and
Fig. 6 (current draw) of the AntBot paper.

FUNCTIONS
    battery_voltage_profile(capacity_mah, nominal_v, avg_power_w, cutoff_v, duration_ms)
        Simple discharge-curve model (not a real cell datasheet model --
        illustrative only, matching the shape reported in the paper).

    current_draw_profile(avg_current_a, gait_freq_hz, duration_s, num_legs_per_tripod=3)
        Simulates cyclical current peaks corresponding to the tripod
        gait's power stroke (three legs actuating simultaneously).

INPUT / OUTPUT
    See each function's docstring below.

Running this file saves:
    ../images/battery_voltage.png
    ../images/current_draw.png
"""

import numpy as np
import matplotlib.pyplot as plt


def battery_voltage_profile(capacity_mah=1800, nominal_v=11.1, full_v=12.6,
                             cutoff_v=9.9, avg_power_w=6.5, duration_ms=300000):
    """
    INPUT:
        capacity_mah : battery capacity (mAh)
        nominal_v    : nominal pack voltage (V)
        full_v       : fully charged voltage (V)
        cutoff_v     : safe cutoff voltage (V)
        avg_power_w  : average power draw under load (W)
        duration_ms  : simulated duration (ms)
    OUTPUT:
        t_ms, voltage : numpy arrays of time (ms) and voltage (V)
    """
    t_ms = np.linspace(0, duration_ms, 500)
    frac = t_ms / duration_ms
    # simple smooth decay: fast tail-off near cutoff, matching the
    # discharge curve shape reported in the paper
    voltage = full_v - (full_v - cutoff_v) * (frac ** 1.6)
    return t_ms, voltage


def current_draw_profile(avg_current_a=0.55, gait_freq_hz=1.2, duration_s=5, peak_factor=0.45):
    """
    INPUT:
        avg_current_a : baseline average current draw (A)
        gait_freq_hz  : tripod gait step frequency (Hz)
        duration_s    : simulated duration (s)
        peak_factor   : amplitude of cyclical peaks relative to baseline
    OUTPUT:
        t_s, current : numpy arrays of time (s) and current (A)
    """
    t_s = np.linspace(0, duration_s, 1000)
    current = avg_current_a + peak_factor * np.abs(np.sin(np.pi * gait_freq_hz * t_s))
    current += np.random.normal(0, 0.02, size=t_s.shape)  # small sensor-like noise
    return t_s, current


if __name__ == "__main__":
    # --- Battery voltage profile ---
    t_ms, voltage = battery_voltage_profile()

    plt.figure(figsize=(7, 5))
    plt.plot(t_ms, voltage, color="tab:blue", linewidth=2, label="Simulated Voltage Under Load")
    plt.axhline(12.6, color="green", linestyle="--", linewidth=1, label="Fully Charged (12.6V)")
    plt.axhline(11.1, color="orange", linestyle="--", linewidth=1, label="Nominal Voltage (11.1V)")
    plt.axhline(9.9, color="red", linestyle="--", linewidth=1, label="Safe Cut-off (9.9V)")
    plt.xlabel("Time (milliseconds)")
    plt.ylabel("Voltage (V)")
    plt.title("Simulated Battery Voltage Profile Over Time")
    plt.legend(fontsize=8)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("../images/battery_voltage.png", dpi=150)
    print("Saved ../images/battery_voltage.png")

    # --- Current draw profile ---
    t_s, current = current_draw_profile()

    plt.figure(figsize=(7, 5))
    plt.plot(t_s, current, color="tab:red", linewidth=1.2, label="Total System Current")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Current Draw (Amps)")
    plt.title("Simulated Current Draw Profile (Tripod Gait)")
    plt.legend(fontsize=8)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("../images/current_draw.png", dpi=150)
    print("Saved ../images/current_draw.png")
