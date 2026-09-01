from pathlib import Path
from datetime import timedelta

import numpy as np
import matplotlib.pyplot as plt

from skyfield.api import load, EarthSatellite, wgs84


# ============================================================
# PROJECT PATH
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

NUM_BITS = 20_000

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
# SKYFIELD
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
# FIND A COMPLETE PASS
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
# SATELLITE TRAJECTORY
# ============================================================

duration_seconds = (
    set_time.utc_datetime()
    - rise_time.utc_datetime()
).total_seconds()


# We use a moderate trajectory grid.
NUM_TRAJECTORY_POINTS = 2000

trajectory_seconds = np.linspace(
    0,
    duration_seconds,
    NUM_TRAJECTORY_POINTS
)


trajectory_datetimes = [
    rise_time.utc_datetime()
    + timedelta(seconds=float(x))
    for x in trajectory_seconds
]

trajectory_times = ts.from_datetimes(
    trajectory_datetimes
)


# ============================================================
# RANGE RATE
# ============================================================

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


range_km = range_distance.km

range_rate_km_s = range_rate.km_per_s

elevation_deg = (
    topocentric.altaz()[0].degrees
)


# ============================================================
# DOPPLER SHIFT
# ============================================================

range_rate_m_s = (
    range_rate_km_s * 1000.0
)

doppler_hz = (
    -range_rate_m_s
    / C
    * CARRIER_FREQUENCY_HZ
)


# ============================================================
# DIGITAL DATA
# ============================================================

rng = np.random.default_rng(
    RNG_SEED
)

bits = rng.integers(
    0,
    2,
    NUM_BITS
)


# BPSK:
# 0 → -1
# 1 → +1

symbols = (
    2 * bits - 1
).astype(float)


# ============================================================
# MAP SYMBOLS ACROSS THE COMPLETE PASS
# ============================================================

symbol_times = np.linspace(
    0,
    duration_seconds,
    NUM_BITS
)


# Interpolate real satellite Doppler
# onto the digital-symbol timeline.

symbol_doppler_hz = np.interp(
    symbol_times,
    trajectory_seconds,
    doppler_hz
)


# ============================================================
# DOPPLER PHASE
# ============================================================

# Instantaneous Doppler changes the phase
# continuously.

dt = (
    duration_seconds
    / (NUM_BITS - 1)
)

doppler_phase = (
    2
    * np.pi
    * np.cumsum(symbol_doppler_hz)
    * dt
)


# ============================================================
# RECEIVED COMPLEX BASEBAND SIGNAL
# ============================================================

tx_signal = (
    symbols
    .astype(complex)
)

rx_signal = (
    tx_signal
    * np.exp(1j * doppler_phase)
)


# ============================================================
# RESULTS
# ============================================================

max_doppler_index = np.argmax(
    np.abs(doppler_hz)
)

max_positive_index = np.argmax(
    doppler_hz
)

max_negative_index = np.argmin(
    doppler_hz
)

zero_crossing_index = np.argmin(
    np.abs(doppler_hz)
)


print()
print("=" * 72)
print("REAL ISS DOPPLER APPLIED TO BPSK")
print("=" * 72)

print()

print(
    f"Satellite:              {lines[0]}"
)

print(
    "NORAD ID:               25544"
)

print(
    f"Carrier frequency:      "
    f"{CARRIER_FREQUENCY_HZ / 1e6:.3f} MHz"
)

print(
    f"Bit rate:               "
    f"{BIT_RATE_BPS / 1000:.1f} kbps"
)

print()

print("-" * 72)
print("PASS")
print("-" * 72)

print()

print(
    f"Start:                  "
    f"{rise_time.utc_strftime('%Y-%m-%d %H:%M:%S')} UTC"
)

print(
    f"End:                    "
    f"{set_time.utc_strftime('%Y-%m-%d %H:%M:%S')} UTC"
)

print(
    f"Duration:               "
    f"{duration_seconds:.1f} seconds"
)

print()

print("-" * 72)
print("DOPPLER")
print("-" * 72)

print()

print(
    f"Maximum positive Doppler:"
    f" {doppler_hz[max_positive_index]:+.2f} Hz"
)

print(
    f"Maximum negative Doppler:"
    f" {doppler_hz[max_negative_index]:+.2f} Hz"
)

print(
    f"Maximum Doppler magnitude:"
    f" {doppler_hz[max_doppler_index]:+.2f} Hz"
)

print(
    f"Doppler near closest approach:"
    f" {doppler_hz[zero_crossing_index]:+.2f} Hz"
)

print()

print("-" * 72)
print("PHYSICAL INTERPRETATION")
print("-" * 72)

print()

print(
    "Negative range rate  → satellite approaching"
)

print(
    "Positive range rate  → satellite receding"
)

print(
    "Approaching satellite → positive frequency shift"
)

print(
    "Receding satellite    → negative frequency shift"
)

print()

print("=" * 72)
print("MODEL COMPLETE")
print("=" * 72)


# ============================================================
# PLOT 1 — RANGE RATE
# ============================================================

plt.figure()

plt.plot(
    trajectory_seconds / 60.0,
    range_rate_km_s
)

plt.axhline(
    0,
    linestyle="--"
)

plt.xlabel(
    "Time from pass start (minutes)"
)

plt.ylabel(
    "Range Rate (km/s)"
)

plt.title(
    "ISS Ground-Station Range Rate"
)

plt.grid(True)

plt.tight_layout()

plt.show()


# ============================================================
# PLOT 2 — DOPPLER
# ============================================================

plt.figure()

plt.plot(
    trajectory_seconds / 60.0,
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
    "ISS Doppler Shift at 145.8 MHz"
)

plt.grid(True)

plt.tight_layout()

plt.show()


# ============================================================
# PLOT 3 — DOPPLER-AFFECTED BPSK CONSTELLATION
# ============================================================

plt.figure()

plt.scatter(
    rx_signal.real,
    rx_signal.imag,
    s=4,
    alpha=0.35
)

plt.xlabel(
    "In-phase (I)"
)

plt.ylabel(
    "Quadrature (Q)"
)

plt.title(
    "BPSK Constellation with Real ISS Doppler"
)

plt.axis("equal")

plt.grid(True)

plt.tight_layout()

plt.show()


# ============================================================
# PLOT 4 — PHASE ROTATION
# ============================================================

plt.figure()

plt.plot(
    symbol_times / 60.0,
    np.unwrap(
        np.angle(rx_signal)
    )
)

plt.xlabel(
    "Time from pass start (minutes)"
)

plt.ylabel(
    "Unwrapped Phase (rad)"
)

plt.title(
    "Doppler-Induced BPSK Phase Rotation"
)

plt.grid(True)

plt.tight_layout()

plt.show()