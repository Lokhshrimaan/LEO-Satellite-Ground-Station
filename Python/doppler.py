import math

# ============================================================
# CONSTANTS
# ============================================================

c = 299_792_458
mu = 3.986004418e14

earth_radius_km = 6371.0

# ============================================================
# SATELLITE
# ============================================================

altitude_km = 500.0

orbital_radius_m = (
    earth_radius_km + altitude_km
) * 1000

velocity_mps = math.sqrt(
    mu / orbital_radius_m
)

# ============================================================
# COMMUNICATION
# ============================================================

carrier_frequency_hz = 145.8e6

# ============================================================
# DOPPLER MODEL
# ============================================================

print("========== DOPPLER MODEL ==========")
print()

print(
    "Time(s) | Range(km) | "
    "Radial velocity(m/s) | Doppler(Hz) | Received freq(MHz)"
)

for t in range(-300, 301, 30):

    # Horizontal displacement
    x_m = velocity_mps * t

    # Slant range
    distance_m = math.sqrt(
        (altitude_km * 1000)**2 + x_m**2
    )

    # Radial velocity = rate of change of range
    radial_velocity_mps = (
        velocity_mps**2 * t
    ) / distance_m

    # Doppler shift
    doppler_hz = (
        -radial_velocity_mps
        / c
        * carrier_frequency_hz
    )

    # Received carrier
    received_frequency_hz = (
        carrier_frequency_hz + doppler_hz
    )

    print(
        f"{t:>+6d} | "
        f"{distance_m/1000:>9.1f} | "
        f"{radial_velocity_mps:>19.1f} | "
        f"{doppler_hz:>11.1f} | "
        f"{received_frequency_hz/1e6:>16.6f}"
    )