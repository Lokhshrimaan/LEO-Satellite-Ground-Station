import math

# ============================================================
# CONSTANTS
# ============================================================

earth_radius_km = 6371.0
earth_mu = 3.986004418e14       # Earth's gravitational parameter (m^3/s^2)

# ============================================================
# SATELLITE PARAMETERS
# ============================================================

altitude_km = 500.0

# Satellite orbital radius
orbital_radius_m = (
    earth_radius_km + altitude_km
) * 1000

# ============================================================
# ORBITAL VELOCITY
# ============================================================

velocity_mps = math.sqrt(
    earth_mu / orbital_radius_m
)

velocity_kmps = velocity_mps / 1000

# ============================================================
# DISPLAY
# ============================================================

print("========== SIMPLIFIED LEO GEOMETRY ==========")
print()

print(f"Earth radius:       {earth_radius_km:.1f} km")
print(f"Satellite altitude: {altitude_km:.1f} km")
print(f"Orbital radius:     {orbital_radius_m/1000:.1f} km")
print(f"Orbital velocity:   {velocity_kmps:.3f} km/s")
print(f"Orbital velocity:   {velocity_mps:.1f} m/s")

# ============================================================
# SIMPLIFIED PASS
# ============================================================

time_values = [-600, -450, -300, -150, 0, 150, 300, 450, 600]

print()
print("Time from closest approach | Slant range")

for t in time_values:

    # Horizontal displacement from closest approach
    x_km = velocity_kmps * t

    # Simplified slant range
    slant_range_km = math.sqrt(
        altitude_km**2 + x_km**2
    )

    print(
        f"{t:>+8.0f} s"
        f"                     | "
        f"{slant_range_km:8.2f} km"
    )