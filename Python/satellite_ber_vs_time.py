from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

from scipy.special import erfc
from skyfield.api import load, EarthSatellite, wgs84


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

TLE_FILE = PROJECT_ROOT / "Data" / "ISS_25544.tle"


# ============================================================
# SATELLITE / GROUND STATION
# ============================================================

GROUND_LATITUDE_DEG = 9.45
GROUND_LONGITUDE_DEG = 77.566667

MIN_ELEVATION_DEG = 10.0


# ============================================================
# COMMUNICATION PARAMETERS
# ============================================================

FREQUENCY_HZ = 145.8e6

TX_POWER_DBM = 30.0

TX_GAIN_DBI = 2.0
RX_GAIN_DBI = 10.0

SYSTEM_LOSS_DB = 2.0

BANDWIDTH_HZ = 12_500.0
NOISE_FIGURE_DB = 3.0

BIT_RATE_BPS = 9_600.0


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


satellite = EarthSatellite(
    lines[1],
    lines[2],
    lines[0]
)


# ============================================================
# SKYFIELD TIME SCALE
# ============================================================

ts = load.timescale()


# ============================================================
# FIND NEXT PASS
# ============================================================

ground_station = wgs84.latlon(
    GROUND_LATITUDE_DEG,
    GROUND_LONGITUDE_DEG
)


# Use the TLE epoch as the starting point.
start_time = satellite.epoch


t0 = start_time
t1 = ts.utc(
    start_time.utc_datetime().year,
    start_time.utc_datetime().month,
    start_time.utc_datetime().day + 2
)


times, events = satellite.find_events(
    ground_station,
    t0,
    t1,
    altitude_degrees=MIN_ELEVATION_DEG
)


event_names = {
    0: "RISE",
    1: "MAXIMUM ELEVATION",
    2: "SET"
}


# ============================================================
# SELECT FIRST COMPLETE PASS
# ============================================================

rise_time = None
peak_time = None
set_time = None

for time, event in zip(times, events):

    if event == 0 and rise_time is None:
        rise_time = time

    elif event == 1 and rise_time is not None and peak_time is None:
        peak_time = time

    elif event == 2 and peak_time is not None:
        set_time = time
        break


if rise_time is None or peak_time is None or set_time is None:
    raise RuntimeError(
        "Could not find a complete satellite pass."
    )


# ============================================================
# SAMPLE PASS
# ============================================================

duration_seconds = (
    set_time.utc_datetime()
    - rise_time.utc_datetime()
).total_seconds()


NUM_SAMPLES = 500

sample_seconds = np.linspace(
    0,
    duration_seconds,
    NUM_SAMPLES
)


sample_datetimes = [
    rise_time.utc_datetime()
    + __import__("datetime").timedelta(
        seconds=float(seconds)
    )
    for seconds in sample_seconds
]


sample_times = ts.from_datetimes(
    sample_datetimes
)


# ============================================================
# SATELLITE GEOMETRY
# ============================================================

difference = (
    satellite - ground_station
)

topocentric = difference.at(sample_times)

altitude, azimuth, distance = (
    topocentric.altaz()
)


elevation_deg = altitude.degrees
azimuth_deg = azimuth.degrees
range_km = distance.km


# ============================================================
# FREE-SPACE PATH LOSS
# ============================================================

# FSPL(dB) =
# 20 log10(4πd / λ)

c = 299_792_458.0

wavelength_m = c / FREQUENCY_HZ

range_m = range_km * 1000.0

fspl_db = (
    20
    * np.log10(
        4
        * np.pi
        * range_m
        / wavelength_m
    )
)


# ============================================================
# RECEIVED POWER
# ============================================================

received_power_dbm = (
    TX_POWER_DBM
    + TX_GAIN_DBI
    + RX_GAIN_DBI
    - fspl_db
    - SYSTEM_LOSS_DB
)


# ============================================================
# THERMAL NOISE
# ============================================================

# k = Boltzmann constant
# T = reference temperature
# B = bandwidth

k = 1.380649e-23

T = 290.0

noise_power_watts = (
    k
    * T
    * BANDWIDTH_HZ
    * 10 ** (NOISE_FIGURE_DB / 10)
)


noise_power_dbm = (
    10
    * np.log10(
        noise_power_watts
        / 1e-3
    )
)


# ============================================================
# SNR
# ============================================================

snr_db = (
    received_power_dbm
    - noise_power_dbm
)


# ============================================================
# Eb/N0
# ============================================================

# Eb/N0 =
# SNR × B/Rb

eb_n0_db = (
    snr_db
    + 10
    * np.log10(
        BANDWIDTH_HZ
        / BIT_RATE_BPS
    )
)


# ============================================================
# THEORETICAL BPSK BER
# ============================================================

eb_n0_linear = (
    10 ** (eb_n0_db / 10)
)


ber = (
    0.5
    * erfc(
        np.sqrt(eb_n0_linear)
    )
)


# Avoid zero values on logarithmic plots.
ber_plot = np.maximum(
    ber,
    1e-20
)


# ============================================================
# FIND IMPORTANT VALUES
# ============================================================

max_elevation_index = np.argmax(
    elevation_deg
)

best_range_index = np.argmin(
    range_km
)


# ============================================================
# RESULTS
# ============================================================

print()
print("=" * 72)
print("SATELLITE SNR → Eb/N0 → BER MODEL")
print("=" * 72)

print()

print(
    f"Satellite:              {lines[0]}"
)

print(
    f"NORAD ID:               25544"
)

print(
    f"Ground station:         "
    f"{GROUND_LATITUDE_DEG:.6f} N, "
    f"{GROUND_LONGITUDE_DEG:.6f} E"
)

print(
    f"Carrier frequency:      "
    f"{FREQUENCY_HZ / 1e6:.3f} MHz"
)

print(
    f"Bandwidth:              "
    f"{BANDWIDTH_HZ / 1000:.1f} kHz"
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
print("LINK PERFORMANCE")
print("-" * 72)

print()

print(
    f"Noise power:            "
    f"{noise_power_dbm:.2f} dBm"
)

print(
    f"Maximum SNR:            "
    f"{np.max(snr_db):.2f} dB"
)

print(
    f"Minimum SNR:            "
    f"{np.min(snr_db):.2f} dB"
)

print(
    f"Maximum Eb/N0:          "
    f"{np.max(eb_n0_db):.2f} dB"
)

print(
    f"Minimum Eb/N0:          "
    f"{np.min(eb_n0_db):.2f} dB"
)

print()

print("-" * 72)
print("BEST POINT OF PASS")
print("-" * 72)

print()

print(
    f"Elevation:              "
    f"{elevation_deg[max_elevation_index]:.2f} deg"
)

print(
    f"Range:                  "
    f"{range_km[max_elevation_index]:.2f} km"
)

print(
    f"Received power:         "
    f"{received_power_dbm[max_elevation_index]:.2f} dBm"
)

print(
    f"SNR:                    "
    f"{snr_db[max_elevation_index]:.2f} dB"
)

print(
    f"Eb/N0:                  "
    f"{eb_n0_db[max_elevation_index]:.2f} dB"
)

print(
    f"Theoretical BER:        "
    f"{ber[max_elevation_index]:.6e}"
)

print()

print("=" * 72)
print("MODEL COMPLETE")
print("=" * 72)


# ============================================================
# PLOT 1 — SNR
# ============================================================

time_minutes = sample_seconds / 60.0

plt.figure()

plt.plot(
    time_minutes,
    snr_db
)

plt.xlabel(
    "Time from pass start (minutes)"
)

plt.ylabel(
    "SNR (dB)"
)

plt.title(
    "ISS Time-Varying SNR"
)

plt.grid(True)

plt.tight_layout()

plt.show()


# ============================================================
# PLOT 2 — Eb/N0
# ============================================================

plt.figure()

plt.plot(
    time_minutes,
    eb_n0_db
)

plt.xlabel(
    "Time from pass start (minutes)"
)

plt.ylabel(
    "Eb/N0 (dB)"
)

plt.title(
    "ISS Time-Varying Eb/N0"
)

plt.grid(True)

plt.tight_layout()

plt.show()


# ============================================================
# PLOT 3 — BER
# ============================================================

plt.figure()

plt.semilogy(
    time_minutes,
    ber_plot
)

plt.xlabel(
    "Time from pass start (minutes)"
)

plt.ylabel(
    "Theoretical BPSK BER"
)

plt.title(
    "ISS Time-Varying BPSK BER"
)

plt.grid(
    True,
    which="both"
)

plt.tight_layout()

plt.show()