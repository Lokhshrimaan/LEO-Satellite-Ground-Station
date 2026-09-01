import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erfc


# ============================================================
# PARAMETERS
# ============================================================

NUM_BITS = 1_000_000

EB_N0_DB_VALUES = np.arange(
    -2,
    11,
    1
)

RNG_SEED = 42


# ============================================================
# RANDOM GENERATOR
# ============================================================

rng = np.random.default_rng(RNG_SEED)


# ============================================================
# GENERATE BITS
# ============================================================

bits = rng.integers(
    0,
    2,
    NUM_BITS
)


# ============================================================
# BPSK MAPPING
# ============================================================

# 0 → -1
# 1 → +1

symbols = (
    2 * bits - 1
)


# ============================================================
# SIMULATED BER
# ============================================================

simulated_ber = []


for eb_n0_db in EB_N0_DB_VALUES:

    # Convert dB to linear
    eb_n0_linear = (
        10 ** (eb_n0_db / 10)
    )

    # For BPSK with unit-energy symbols:
    #
    # sigma² = N0 / 2
    #
    # With Eb = 1:
    #
    # sigma = sqrt(1 / (2 * Eb/N0))

    noise_std = np.sqrt(
        1 / (2 * eb_n0_linear)
    )

    noise = rng.normal(
        0,
        noise_std,
        NUM_BITS
    )

    received = (
        symbols + noise
    )

    # Decision
    recovered_bits = (
        received >= 0
    ).astype(int)

    # Count errors
    errors = np.sum(
        bits != recovered_bits
    )

    ber = errors / NUM_BITS

    simulated_ber.append(
        ber
    )


simulated_ber = np.array(
    simulated_ber
)


# ============================================================
# THEORETICAL BER
# ============================================================

eb_n0_linear = (
    10 ** (EB_N0_DB_VALUES / 10)
)

theoretical_ber = (
    0.5
    * erfc(
        np.sqrt(eb_n0_linear)
    )
)


# ============================================================
# PRINT RESULTS
# ============================================================

print()
print("=" * 70)
print("BPSK BER vs Eb/N0")
print("=" * 70)

print()

print(
    f"{'Eb/N0 (dB)':>12}"
    f"{'Simulated BER':>20}"
    f"{'Theoretical BER':>20}"
)

print("-" * 70)

for eb_n0_db, sim, theory in zip(
    EB_N0_DB_VALUES,
    simulated_ber,
    theoretical_ber
):

    print(
        f"{eb_n0_db:>12.1f}"
        f"{sim:>20.6e}"
        f"{theory:>20.6e}"
    )


# ============================================================
# PLOT
# ============================================================

plt.figure()

plt.semilogy(
    EB_N0_DB_VALUES,
    simulated_ber,
    "o-",
    label="Simulation"
)

plt.semilogy(
    EB_N0_DB_VALUES,
    theoretical_ber,
    "--",
    label="Theory"
)

plt.xlabel(
    "Eb/N0 (dB)"
)

plt.ylabel(
    "Bit Error Rate (BER)"
)

plt.title(
    "BPSK BER Performance in AWGN"
)

plt.grid(
    True,
    which="both"
)

plt.legend()

plt.tight_layout()

plt.show()