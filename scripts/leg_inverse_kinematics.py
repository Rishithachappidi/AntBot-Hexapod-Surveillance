"""
leg_inverse_kinematics.py
--------------------------
Geometric inverse kinematics (IK) for one 3-DoF hexapod leg
(coxa -> femur -> tibia), matching Section III-A / Eqs. 1-8 of the
AntBot paper.

FUNCTION
    leg_inverse_kinematics(target, L1, L2, L3)

INPUT
    target : tuple (x, y, z)  -- desired foot position in mm,
                                  in the leg's local coordinate frame
    L1     : float            -- coxa link length (mm)
    L2     : float            -- femur link length (mm)
    L3     : float            -- tibia link length (mm)

OUTPUT
    (theta1, theta2, theta3) : joint angles in degrees
        theta1 -> coxa  (yaw)
        theta2 -> femur (pitch)
        theta3 -> tibia (pitch)
    Returns (nan, nan, nan) if the target is outside the leg's
    reachable workspace.

Run this file directly to see a sample computation printed to the
console and saved to outputs/ik_sample_output.txt.
"""

import math


def leg_inverse_kinematics(target, L1, L2, L3):
    x, y, z = target

    # Eq. 1 -- coxa angle
    theta1 = math.atan2(y, x)

    # Eq. 2, 3 -- reduce to a 2D planar problem
    d = math.sqrt(x**2 + y**2) - L1
    D = math.sqrt(d**2 + z**2)

    # Reachability check
    if D > (L2 + L3) or D < abs(L2 - L3):
        return (float("nan"), float("nan"), float("nan"))

    # Eq. 4, 5 -- law of cosines
    alpha = math.acos((L2**2 + D**2 - L3**2) / (2 * L2 * D))
    beta = math.acos((L2**2 + L3**2 - D**2) / (2 * L2 * L3))

    # Eq. 6 -- elevation angle
    gamma = math.atan2(z, d)

    # Eq. 7, 8 -- final joint angles
    theta2 = gamma + alpha
    theta3 = beta - math.pi / 2

    return tuple(math.degrees(a) for a in (theta1, theta2, theta3))


if __name__ == "__main__":
    # Example link lengths (mm) -- replace with your own measured values
    L1, L2, L3 = 30, 60, 90

    # Example target foot positions
    samples = [
        (120, 20, -90),
        (140, 0, -95),
        (100, -15, -80),
    ]

    lines = ["Leg Inverse Kinematics -- sample output", "=" * 40]
    for target in samples:
        angles = leg_inverse_kinematics(target, L1, L2, L3)
        line = (
            f"target(x,y,z)={target} mm  ->  "
            f"coxa={angles[0]:.2f} deg, femur={angles[1]:.2f} deg, tibia={angles[2]:.2f} deg"
        )
        print(line)
        lines.append(line)

    with open("../outputs/ik_sample_output.txt", "w") as f:
        f.write("\n".join(lines) + "\n")
