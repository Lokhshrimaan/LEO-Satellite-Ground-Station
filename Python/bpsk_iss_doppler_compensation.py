from pathlib import Path
from datetime import timedelta

import numpy as np
import matplotlib.pyplot as plt

from skyfield.api import load, EarthSatellite, wgs84


# ============================================================
# PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

TLE_FILE = PROJECT_ROOT / "Data" / "ISS_25544.tle"


# ============================================================
# PARAMETERS
# ============================================================

GROUND_LATITUDE_DEG = 9.45
GROUND_LONGITUDE_DEG = 77.566667

MIN_ELEVATION_DEG = 10.0

CARRIER_FREQUENCY_HZ = 145.8e6

BIT_RATE_BPS = 9600.0

NUM_BITS = 1000

RNG_SEED = 42

C = 299_792_458.0


# ============================================================
# LOAD TLE
# ============================================================

if not TLE_FILE.exists():
    raise FileNotFoundError(
        f"TLE file not found:\n{TLE_FILE}"
    )

with open(TLE_FILE, "r") as f:
    lines = [
        line.strip()
        for line in f.readlines()
        if line.strip()
    ]

if len(lines) != 3:
    raise ValueError(
        "TLE file must contain exactly 3 non-empty lines."
    )


# ============================================================
# SKYFIELD OBJECTS
# ============================================================

ts = load.timescale()

satellite = EarthSatellite(
    lines[1],
    lines[2],
    lines[0],
    ts
)

ground_station = wgs84.latlon(
    GROUND_LATITUDE_DEG,
    GROUND_LONGITUDE_DEG
)


# ============================================================
# FIND PASS
# ============================================================

start_search = satellite.epoch

end_search = ts.utc(
    satellite.epoch.utc_datetime()
    + timedelta(days=2)
)

times, events = satellite.find_events(
    ground_station,
    start_search,
    end_search,
    altitude_degrees=MIN_ELEVATION_DEG
)

rise_time = None
set_time = None

for t, event in zip(times, events):

    if event == 0 and rise_time is None:
        rise_time = t

    elif event == 2 and rise_time is not None:
        set_time = t
        break

if rise_time is None or set_time is None:
    raise RuntimeError(
        "Could not find a complete satellite pass."
    )


# ============================================================
# TIME AXIS
# ============================================================

duration_seconds = (
    set_time.utc_datetime()
    - rise_time.utc_datetime()
).total_seconds()

time_seconds = np.linspace(
    0,
    duration_seconds,
    NUM_BITS
)


# ============================================================
# SATELLITE RANGE RATE
# ============================================================

trajectory_datetimes = [
    rise_time.utc_datetime()
    + timedelta(seconds=float(x))
    for x in time_seconds
]

trajectory_times = ts.from_datetimes(
    trajectory_datetimes
)

difference = satellite - ground_station

topocentric = difference.at(
    trajectory_times
)

(
    latitude,
    longitude,
    range_distance,
    latitude_rate,
    longitude_rate,
    range_rate
) = topocentric.frame_latlon_and_rates(
    ground_station
)

range_rate_m_s = (
    range_rate.km_per_s * 1000.0
)


# ============================================================
# DOPPLER
# ============================================================

doppler_hz = (
    -range_rate_m_s
    / C
    * CARRIER_FREQUENCY_HZ
)


# ============================================================
# GENERATE BPSK DATA
# ============================================================

rng = np.random.default_rng(RNG_SEED)

bits = rng.integers(
    0,
    2,
    NUM_BITS
)

symbols = (
    2 * bits - 1
).astype(float)


# ============================================================
# DOPPLER PHASE
# ============================================================

dt = (
    duration_seconds
    / (NUM_BITS - 1)
)

doppler_phase = (
    2
    * np.pi
    * np.cumsum(doppler_hz)
    * dt
)


# ============================================================
# APPLY DOPPLER
# ============================================================

tx_signal = symbols.astype(complex)

rx_signal = (
    tx_signal
    * np.exp(1j * doppler_phase)
)


# ============================================================
# DEMODULATE WITHOUT COMPENSATION
# ============================================================

uncorrected_decisions = (
    rx_signal.real >= 0
).astype(int)

uncorrected_errors = np.sum(
    uncorrected_decisions != bits
)

uncorrected_ber = (
    uncorrected_errors / NUM_BITS
)


# ============================================================
# DOPPLER COMPENSATION
# ============================================================

compensated_signal = (
    rx_signal
    * np.exp(-1j * doppler_phase)
)


# ============================================================
# DEMODULATE AFTER COMPENSATION
# ============================================================

corrected_decisions = (
    compensated_signal.real >= 0
).astype(int)

corrected_errors = np.sum(
    corrected_decisions != bits
)

corrected_ber = (
    corrected_errors / NUM_BITS
)


# ============================================================
# RESULTS
# ============================================================

print()
print("=" * 72)
print("ISS DOPPLER COMPENSATION OF BPSK")
print("=" * 72)

print()

print(
    f"Satellite:              {lines[0]}"
)

print(
    f"Carrier frequency:      "
    f"{CARRIER_FREQUENCY_HZ / 1e6:.3f} MHz"
)

print(
    f"Number of bits:         {NUM_BITS}"
)

print(
    f"Pass duration:          "
    f"{duration_seconds:.1f} seconds"
)

print()

print("-" * 72)
print("DOPPLER")

print("-" * 72)

print()

print(
    f"Maximum Doppler:        "
    f"{np.max(doppler_hz):+.2f} Hz"
)

print(
    f"Minimum Doppler:        "
    f"{np.min(doppler_hz):+.2f} Hz"
)

print()

print("-" * 72)
print("BER PERFORMANCE")

print("-" * 72)

print()

print(
    f"BER without correction: "
    f"{uncorrected_ber:.6f}"
)

print(
    f"BER after correction:    "
    f"{corrected_ber:.6f}"
)

print(
    f"Errors without correction:"
    f" {uncorrected_errors}"
)

print(
    f"Errors after correction:  "
    f"{corrected_errors}"
)

print()

print("=" * 72)
print("MODEL COMPLETE")
print("=" * 72)


# ============================================================
# CONSTELLATION BEFORE COMPENSATION
# ============================================================

plt.figure()

plt.scatter(
    rx_signal.real,
    rx_signal.imag,
    s=8,
    alpha=0.35
)

plt.xlabel("In-phase (I)")
plt.ylabel("Quadrature (Q)")

plt.title(
    "BPSK Before Doppler Compensation"
)

plt.axis("equal")
plt.grid(True)

plt.tight_layout()

plt.show()


# ============================================================
# CONSTELLATION AFTER COMPENSATION
# ============================================================

plt.figure()

plt.scatter(
    compensated_signal.real,
    compensated_signal.imag,
    s=8,
    alpha=0.35
)

plt.xlabel("In-phase (I)")
plt.ylabel("Quadrature (Q)")

plt.title(
    "BPSK After Doppler Compensation"
)

plt.axis("equal")
plt.grid(True)

plt.tight_layout()

plt.show()


# ============================================================
# DOPPLER
# ============================================================

plt.figure()

plt.plot(
    time_seconds / 60.0,
    doppler_hz
)

plt.axhline(
    0,
    linestyle="--"
)

plt.xlabel(
    "Time from pass start (minutes)"
)

plt.ylabel(
    "Doppler Shift (Hz)"
)

plt.title(
    "ISS Doppler During Pass"
)

plt.grid(True)

plt.tight_layout()

plt.show()