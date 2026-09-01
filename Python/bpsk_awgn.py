from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# PARAMETERS
# ============================================================

NUM_BITS = 10000
SAMPLES_PER_SYMBOL = 100

CARRIER_FREQUENCY_HZ = 10_000
SAMPLE_RATE_HZ = CARRIER_FREQUENCY_HZ * SAMPLES_PER_SYMBOL

SNR_DB = 5.0

RNG_SEED = 42


# ============================================================
# RANDOM BITS
# ============================================================

rng = np.random.default_rng(RNG_SEED)

bits = rng.integers(0, 2, NUM_BITS)


# ============================================================
# BPSK MAPPING
# ============================================================

symbols = 2 * bits - 1


# ============================================================
# UPSAMPLE
# ============================================================

baseband = np.repeat(
    symbols,
    SAMPLES_PER_SYMBOL
)


# ============================================================
# TIME
# ============================================================

num_samples = len(baseband)

time = np.arange(num_samples) / SAMPLE_RATE_HZ


# ============================================================
# CARRIER
# ============================================================

carrier = np.cos(
    2 * np.pi * CARRIER_FREQUENCY_HZ * time
)


# ============================================================
# BPSK MODULATION
# ============================================================

tx_signal = baseband * carrier


# ============================================================
# ADD AWGN
# ============================================================

signal_power = np.mean(tx_signal ** 2)

snr_linear = 10 ** (SNR_DB / 10)

noise_power = signal_power / snr_linear

noise_std = np.sqrt(noise_power)

noise = rng.normal(
    0,
    noise_std,
    num_samples
)

rx_signal = tx_signal + noise


# ============================================================
# COHERENT DEMODULATION
# ============================================================

mixed_signal = rx_signal * carrier


# ============================================================
# INTEGRATE EACH SYMBOL
# ============================================================

demodulated_symbols = np.zeros(NUM_BITS)

for i in range(NUM_BITS):

    start = i * SAMPLES_PER_SYMBOL
    end = start + SAMPLES_PER_SYMBOL

    demodulated_symbols[i] = np.sum(
        mixed_signal[start:end]
    )


# ============================================================
# DECISION
# ============================================================

recovered_bits = (
    demodulated_symbols >= 0
).astype(int)


# ============================================================
# BER
# ============================================================

bit_errors = np.sum(
    bits != recovered_bits
)

ber = bit_errors / NUM_BITS


# ============================================================
# RESULTS
# ============================================================

print()
print("=" * 65)
print("BPSK + AWGN COMMUNICATION LINK")
print("=" * 65)

print()

print(f"Number of bits:       {NUM_BITS}")
print(f"SNR:                  {SNR_DB:.1f} dB")
print(f"Signal power:         {signal_power:.6f}")
print(f"Noise power:          {noise_power:.6f}")
print(f"Noise standard dev.:  {noise_std:.6f}")

print()

print(f"Bit errors:           {bit_errors}")
print(f"BER:                  {ber:.6e}")

print()

print("=" * 65)


# ============================================================
# PLOT 1 — TRANSMITTED vs RECEIVED
# ============================================================

display_samples = 2000

plt.figure()

plt.plot(
    time[:display_samples],
    tx_signal[:display_samples],
    label="Transmitted"
)

plt.plot(
    time[:display_samples],
    rx_signal[:display_samples],
    alpha=0.7,
    label="Received + AWGN"
)

plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.title(f"BPSK Signal with AWGN — SNR = {SNR_DB:.1f} dB")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


# ============================================================
# PLOT 2 — DEMODULATOR OUTPUT
# ============================================================

plt.figure()

plt.stem(
    np.arange(1, 101),
    demodulated_symbols[:100]
)

plt.axhline(
    0,
    linestyle="--"
)

plt.xlabel("Symbol Number")
plt.ylabel("Decision Variable")
plt.title("BPSK Demodulator Output with AWGN")
plt.grid(True)
plt.tight_layout()
plt.show()