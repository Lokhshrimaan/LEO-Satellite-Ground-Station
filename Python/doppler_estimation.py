import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# STEP 16 — DOPPLER ESTIMATION AND COMPENSATION
# ============================================================

np.random.seed(42)


# ------------------------------------------------------------
# 1. SYSTEM PARAMETERS
# ------------------------------------------------------------

NUM_BITS = 1000

SAMPLES_PER_SYMBOL = 100

SYMBOL_RATE = 10_000          # 10 ksym/s

FS = SYMBOL_RATE * SAMPLES_PER_SYMBOL
# FS = 1 MHz

CARRIER_FREQUENCY = 145.8e6   # 145.8 MHz

TRUE_DOPPLER = 2500.0         # Unknown Doppler in simulation

SNR_DB = 15.0


# ------------------------------------------------------------
# 2. GENERATE RANDOM BITS
# ------------------------------------------------------------

bits = np.random.randint(0, 2, NUM_BITS)


# ------------------------------------------------------------
# 3. BPSK MODULATION
# ------------------------------------------------------------

# 0 -> -1
# 1 -> +1

symbols = 2 * bits - 1


# ------------------------------------------------------------
# 4. OVERSAMPLE THE SYMBOLS
# ------------------------------------------------------------

tx_signal = np.repeat(
    symbols,
    SAMPLES_PER_SYMBOL
).astype(float)


# ------------------------------------------------------------
# 5. TIME AXIS
# ------------------------------------------------------------

N = len(tx_signal)

t = np.arange(N) / FS


# ------------------------------------------------------------
# 6. APPLY UNKNOWN DOPPLER
# ------------------------------------------------------------

doppler_rotation = np.exp(
    1j * 2 * np.pi * TRUE_DOPPLER * t
)

received_clean = (
    tx_signal * doppler_rotation
)


# ------------------------------------------------------------
# 7. ADD AWGN
# ------------------------------------------------------------

signal_power = np.mean(
    np.abs(received_clean) ** 2
)

snr_linear = 10 ** (SNR_DB / 10)

noise_power = signal_power / snr_linear

noise = np.sqrt(noise_power / 2) * (
    np.random.randn(N)
    +
    1j * np.random.randn(N)
)

received = received_clean + noise


# ------------------------------------------------------------
# 8. DOPPLER ESTIMATION
# ------------------------------------------------------------

# Square the received BPSK signal.
#
# This removes the BPSK data because:
#
# (+1)^2 = 1
# (-1)^2 = 1
#
# Therefore:
#
# r(t)^2 = exp(j*4*pi*fD*t)
#
# The phase slope is therefore:
#
# d(phi)/dt = 4*pi*fD

squared_signal = received ** 2


# Calculate phase
phase = np.angle(squared_signal)


# Unwrap phase so that it becomes continuous
unwrapped_phase = np.unwrap(phase)


# ------------------------------------------------------------
# 9. LINEAR PHASE FIT
# ------------------------------------------------------------

# Fit:
#
# phase = slope * time + intercept

phase_slope, phase_intercept = np.polyfit(
    t,
    unwrapped_phase,
    1
)


# Convert phase slope to Doppler

estimated_doppler = (
    phase_slope / (4 * np.pi)
)


# ------------------------------------------------------------
# 10. DOPPLER COMPENSATION
# ------------------------------------------------------------

correction = np.exp(
    -1j * 2 * np.pi * estimated_doppler * t
)

compensated = (
    received * correction
)


# ------------------------------------------------------------
# 11. SYMBOL SAMPLING
# ------------------------------------------------------------

sample_indices = (
    np.arange(NUM_BITS) * SAMPLES_PER_SYMBOL
    + SAMPLES_PER_SYMBOL // 2
)


received_symbols_before = (
    received[sample_indices]
)

received_symbols_after = (
    compensated[sample_indices]
)


# ------------------------------------------------------------
# 12. BIT DECISION
# ------------------------------------------------------------

detected_bits = (
    np.real(received_symbols_after) >= 0
).astype(int)


# ------------------------------------------------------------
# 13. BER
# ------------------------------------------------------------

bit_errors = np.sum(
    bits != detected_bits
)

ber = bit_errors / NUM_BITS


# ------------------------------------------------------------
# 14. ESTIMATION ERROR
# ------------------------------------------------------------

estimation_error = (
    estimated_doppler - TRUE_DOPPLER
)


# ------------------------------------------------------------
# 15. RESULTS
# ------------------------------------------------------------

print("=" * 70)
print("DOPPLER ESTIMATION AND COMPENSATION")
print("=" * 70)

print()
print("SYSTEM")
print("-" * 70)

print(
    f"Carrier frequency:       "
    f"{CARRIER_FREQUENCY / 1e6:.3f} MHz"
)

print(
    f"Number of bits:          "
    f"{NUM_BITS}"
)

print(
    f"Symbol rate:             "
    f"{SYMBOL_RATE / 1e3:.1f} ksym/s"
)

print(
    f"Sampling frequency:      "
    f"{FS / 1e6:.2f} MHz"
)

print(
    f"Samples per symbol:      "
    f"{SAMPLES_PER_SYMBOL}"
)

print(
    f"SNR:                     "
    f"{SNR_DB:.1f} dB"
)

print()
print("DOPPLER ESTIMATION")
print("-" * 70)

print(
    f"True Doppler:            "
    f"{TRUE_DOPPLER:+.2f} Hz"
)

print(
    f"Estimated Doppler:       "
    f"{estimated_doppler:+.2f} Hz"
)

print(
    f"Estimation error:        "
    f"{estimation_error:+.2f} Hz"
)

print()
print("BER PERFORMANCE")
print("-" * 70)

print(
    f"Bit errors:              "
    f"{bit_errors}"
)

print(
    f"BER:                     "
    f"{ber:.6f}"
)

print()
print("=" * 70)
print("MODEL COMPLETE")
print("=" * 70)


# ============================================================
# PLOT 1 — BEFORE COMPENSATION
# ============================================================

plt.figure(figsize=(8, 6))

plt.scatter(
    np.real(received_symbols_before),
    np.imag(received_symbols_before),
    s=8
)

plt.axhline(0, linestyle="--")
plt.axvline(0, linestyle="--")

plt.xlabel("In-phase (I)")
plt.ylabel("Quadrature (Q)")

plt.title(
    "BPSK Before Doppler Compensation"
)

plt.grid(True)

plt.show()


# ============================================================
# PLOT 2 — AFTER COMPENSATION
# ============================================================

plt.figure(figsize=(8, 6))

plt.scatter(
    np.real(received_symbols_after),
    np.imag(received_symbols_after),
    s=8
)

plt.axhline(0, linestyle="--")
plt.axvline(0, linestyle="--")

plt.xlabel("In-phase (I)")
plt.ylabel("Quadrature (Q)")

plt.title(
    "BPSK After Doppler Compensation"
)

plt.grid(True)

plt.show()


# ============================================================
# PLOT 3 — PHASE USED FOR DOPPLER ESTIMATION
# ============================================================

plt.figure(figsize=(9, 5))

plt.plot(
    t,
    unwrapped_phase
)

plt.xlabel("Time (s)")
plt.ylabel("Unwrapped Phase (rad)")

plt.title(
    "Unwrapped Squared-Signal Phase"
)

plt.grid(True)

plt.show()


# ============================================================
# PLOT 4 — TRUE VS ESTIMATED DOPPLER
# ============================================================

plt.figure(figsize=(8, 5))

plt.bar(
    ["True Doppler", "Estimated Doppler"],
    [
        TRUE_DOPPLER,
        estimated_doppler
    ]
)

plt.ylabel("Frequency Offset (Hz)")

plt.title(
    "Doppler Estimation"
)

plt.grid(axis="y")

plt.show()