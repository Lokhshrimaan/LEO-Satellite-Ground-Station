import math

# -----------------------------
# Physical constants
# -----------------------------

k = 1.380649e-23       # Boltzmann constant (J/K)
T = 290                # System temperature (K)

# -----------------------------
# Receiver bandwidths
# -----------------------------

bandwidths_hz = [
    10e3,       # 10 kHz
    100e3,      # 100 kHz
    1e6         # 1 MHz
]

print(f"Temperature: {T} K")
print()

for B in bandwidths_hz:

    # Thermal noise power in watts
    noise_w = k * T * B

    # Convert watts to dBm
    noise_dbm = 10 * math.log10(noise_w / 1e-3)

    print(
        f"Bandwidth: {B/1e3:7.0f} kHz | "
        f"Noise: {noise_w:.3e} W | "
        f"Noise: {noise_dbm:.2f} dBm"
    )