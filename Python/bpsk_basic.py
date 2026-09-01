from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent


# ============================================================
# BPSK PARAMETERS
# ============================================================

# Number of information bits
NUM_BITS = 20

# Samples used to represent each symbol
SAMPLES_PER_SYMBOL = 100

# Carrier frequency used only for visualization
CARRIER_FREQUENCY_HZ = 10_000

# Sampling frequency
SAMPLE_RATE_HZ = (
    CARRIER_FREQUENCY_HZ * SAMPLES_PER_SYMBOL
)


# ============================================================
# RANDOM BIT GENERATION
# ============================================================

rng = np.random.default_rng(42)

bits = rng.integers(
    0,
    2,
    NUM_BITS
)


# ============================================================
# BPSK SYMBOL MAPPING
# ============================================================

# 0 → -1
# 1 → +1

symbols = 2 * bits - 1


# ============================================================
# UPSAMPLE SYMBOLS
# ============================================================

baseband = np.repeat(
    symbols,
    SAMPLES_PER_SYMBOL
)


# ============================================================
# TIME AXIS
# ============================================================

num_samples = len(baseband)

time = (
    np.arange(num_samples)
    / SAMPLE_RATE_HZ
)


# ============================================================
# BPSK PASSBAND WAVEFORM
# ============================================================

carrier = np.cos(
    2 * np.pi
    * CARRIER_FREQUENCY_HZ
    * time
)


bpsk_signal = (
    baseband
    * carrier
)


# ============================================================
# IDEAL CHANNEL
# ============================================================

# At Step 10 we deliberately introduce
# NO noise and NO Doppler.

received_signal = bpsk_signal.copy()


# ============================================================
# COHERENT DEMODULATION
# ============================================================

# Multiply the received signal by the
# locally generated carrier.

mixed_signal = (
    received_signal
    * carrier
)


# ============================================================
# INTEGRATE EACH SYMBOL
# ============================================================

demodulated_symbols = np.zeros(
    NUM_BITS
)


for i in range(NUM_BITS):

    start = (
        i
        * SAMPLES_PER_SYMBOL
    )

    end = (
        start
        + SAMPLES_PER_SYMBOL
    )

    symbol_samples = mixed_signal[
        start:end
    ]

    demodulated_symbols[i] = np.sum(
        symbol_samples
    )


# ============================================================
# BIT DECISION
# ============================================================

recovered_bits = (
    demodulated_symbols >= 0
).astype(int)


# ============================================================
# BIT ERROR RATE
# ============================================================

bit_errors = np.sum(
    bits != recovered_bits
)

ber = (
    bit_errors
    / NUM_BITS
)


# ============================================================
# PRINT RESULTS
# ============================================================

print()
print("=" * 65)
print("BPSK BASIC DIGITAL COMMUNICATION LINK")
print("=" * 65)

print()

print(
    f"Number of bits:          {NUM_BITS}"
)

print(
    f"Samples per symbol:      "
    f"{SAMPLES_PER_SYMBOL}"
)

print(
    f"Carrier frequency:       "
    f"{CARRIER_FREQUENCY_HZ / 1000:.1f} kHz"
)

print(
    f"Sampling frequency:      "
    f"{SAMPLE_RATE_HZ / 1e6:.2f} MHz"
)

print()

print("-" * 65)
print("TRANSMITTED DATA")
print("-" * 65)

print()

print(
    "Bits:     ",
    " ".join(map(str, bits))
)

print(
    "Symbols:  ",
    " ".join(map(str, symbols))
)

print()

print("-" * 65)
print("RECEIVED DATA")
print("-" * 65)

print()

print(
    "Bits:     ",
    " ".join(map(str, recovered_bits))
)

print()

print(
    f"Bit errors:              {bit_errors}"
)

print(
    f"BER:                     {ber:.6f}"
)

print()

print("=" * 65)

if bit_errors == 0:

    print(
        "STATUS: PERFECT RECOVERY"
    )

else:

    print(
        "STATUS: ERRORS DETECTED"
    )

print("=" * 65)


# ============================================================
# PLOT 1 — ORIGINAL BITS / BASEBAND
# ============================================================

plt.figure()

plt.step(
    time,
    baseband,
    where="post"
)

plt.xlabel(
    "Time (s)"
)

plt.ylabel(
    "BPSK Symbol"
)

plt.title(
    "BPSK Baseband Symbols"
)

plt.grid(True)

plt.tight_layout()

plt.show()


# ============================================================
# PLOT 2 — BPSK WAVEFORM
# ============================================================

plt.figure()

plt.plot(
    time,
    bpsk_signal
)

plt.xlabel(
    "Time (s)"
)

plt.ylabel(
    "Amplitude"
)

plt.title(
    "BPSK Passband Waveform"
)

plt.grid(True)

plt.tight_layout()

plt.show()


# ============================================================
# PLOT 3 — DEMODULATOR OUTPUT
# ============================================================

plt.figure()

symbol_numbers = np.arange(
    1,
    NUM_BITS + 1
)

plt.stem(
    symbol_numbers,
    demodulated_symbols
)

plt.axhline(
    0,
    linestyle="--"
)

plt.xlabel(
    "Symbol Number"
)

plt.ylabel(
    "Decision Variable"
)

plt.title(
    "BPSK Demodulator Output"
)

plt.grid(True)

plt.tight_layout()

plt.show()