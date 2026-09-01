from pathlib import Path
from datetime import datetime, timedelta, timezone

import numpy as np
import matplotlib.pyplot as plt

from skyfield.api import load, wgs84, EarthSatellite


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

TLE_FILE = PROJECT_ROOT / "Data" / "ISS_25544.tle"


# ============================================================
# GROUND STATION
# ============================================================

GROUND_LATITUDE = 9.45
GROUND_LONGITUDE = 77.566667

MIN_ELEVATION_DEG = 10.0


# ============================================================
# COMMUNICATION PARAMETERS
# ============================================================

# Carrier frequency
CARRIER_FREQUENCY_HZ = 145.8e6

# Speed of light
C = 299_792_458.0

# Nominal transmitter power
TX_POWER_W = 1.0

# Convert watts to dBm
TX_POWER_DBM = 10 * np.log10(TX_POWER_W * 1000)

# Nominal antenna gains
TX_ANTENNA_GAIN_DBI = 2.0
RX_ANTENNA_GAIN_DBI = 10.0

# Cable / connector / miscellaneous losses
SYSTEM_LOSS_DB = 2.0

# Assumed receiver bandwidth
BANDWIDTH_HZ = 12_500.0

# Receiver noise figure
NOISE_FIGURE_DB = 3.0

# Thermal noise density
THERMAL_NOISE_DBM_HZ = -174.0


# ============================================================
# CHECK TLE
# ============================================================

if not TLE_FILE.is_file():
    raise FileNotFoundError(
        f"\nTLE file not found:\n{TLE_FILE}"
    )


# ============================================================
# LOAD TIMESCALE
# ============================================================

ts = load.timescale()


# ============================================================
# READ TLE
# ============================================================

with open(TLE_FILE, "r", encoding="utf-8") as file:

    satellite_name = file.readline().strip()
    line1 = file.readline().strip()
    line2 = file.readline().strip()


# ============================================================
# CREATE SATELLITE
# ============================================================

satellite = EarthSatellite(
    line1,
    line2,
    satellite_name,
    ts
)


# ============================================================
# GROUND STATION
# ============================================================

ground_station = wgs84.latlon(
    GROUND_LATITUDE,
    GROUND_LONGITUDE
)


# ============================================================
# SEARCH NEXT 24 HOURS
# ============================================================

now = datetime.now(timezone.utc)

end = now + timedelta(days=1)

t0 = ts.from_datetime(now)
t1 = ts.from_datetime(end)


# ============================================================
# FIND PASSES
# ============================================================

event_times, events = satellite.find_events(
    ground_station,
    t0,
    t1,
    altitude_degrees=MIN_ELEVATION_DEG
)


# ============================================================
# FIND FIRST COMPLETE PASS
# ============================================================

pass_start = None
pass_end = None

for t, event in zip(event_times, events):

    if event == 0 and pass_start is None:
        pass_start = t

    elif event == 2 and pass_start is not None:
        pass_end = t
        break


if pass_start is None or pass_end is None:

    raise RuntimeError(
        "No complete satellite pass above "
        f"{MIN_ELEVATION_DEG} degrees was found."
    )


# ============================================================
# SAMPLE PASS
# ============================================================

duration_seconds = (
    pass_end.tt - pass_start.tt
) * 86400.0

sample_count = max(
    100,
    int(duration_seconds) + 1
)

sample_jd = np.linspace(
    pass_start.tt,
    pass_end.tt,
    sample_count
)

times = ts.tt_jd(sample_jd)


# ============================================================
# TOPOCENTRIC GEOMETRY
# ============================================================

difference = satellite - ground_station

topocentric = difference.at(times)

altitude, azimuth, distance = topocentric.altaz()


# ============================================================
# RANGE RATE
# ============================================================

(
    _latitude,
    _longitude,
    _range_distance,
    _latitude_rate,
    _longitude_rate,
    range_rate
) = topocentric.frame_latlon_and_rates(
    ground_station
)


# ============================================================
# CONVERT UNITS
# ============================================================

time_minutes = (
    (times.tt - pass_start.tt)
    * 24
    * 60
)

elevation_deg = altitude.degrees

azimuth_deg = azimuth.degrees

range_m = distance.m

range_km = distance.km

range_rate_m_s = range_rate.km_per_s * 1000.0


# ============================================================
# FREE-SPACE PATH LOSS
# ============================================================

fspl_db = (
    20
    * np.log10(
        4
        * np.pi
        * range_m
        * CARRIER_FREQUENCY_HZ
        / C
    )
)


# ============================================================
# RECEIVED POWER
# ============================================================

received_power_dbm = (
    TX_POWER_DBM
    + TX_ANTENNA_GAIN_DBI
    + RX_ANTENNA_GAIN_DBI
    - SYSTEM_LOSS_DB
    - fspl_db
)


# ============================================================
# THERMAL NOISE
# ============================================================

noise_power_dbm = (
    THERMAL_NOISE_DBM_HZ
    + 10 * np.log10(BANDWIDTH_HZ)
    + NOISE_FIGURE_DB
)


# ============================================================
# SNR
# ============================================================

snr_db = (
    received_power_dbm
    - noise_power_dbm
)


# ============================================================
# LINK MARGIN
# ============================================================

# For now we use 10 dB as a simple engineering target.
# Later this will be replaced by the required Eb/N0 of
# our actual modulation and coding scheme.

REQUIRED_SNR_DB = 10.0

link_margin_db = (
    snr_db
    - REQUIRED_SNR_DB
)


# ============================================================
# DOPPLER
# ============================================================

doppler_hz = (
    -range_rate_m_s
    / C
    * CARRIER_FREQUENCY_HZ
)


received_frequency_hz = (
    CARRIER_FREQUENCY_HZ
    + doppler_hz
)


# ============================================================
# FIND IMPORTANT POINTS
# ============================================================

max_elevation_index = np.argmax(
    elevation_deg
)

minimum_range_index = np.argmin(
    range_km
)

maximum_power_index = np.argmax(
    received_power_dbm
)


# ============================================================
# DISPLAY RESULTS
# ============================================================

print()
print("=" * 75)
print("TIME-VARYING SATELLITE LINK BUDGET")
print("=" * 75)

print()

print(f"Satellite:             {satellite_name}")
print("NORAD ID:               25544")

print(
    f"Ground station:         "
    f"{GROUND_LATITUDE:.6f} N, "
    f"{GROUND_LONGITUDE:.6f} E"
)

print(
    f"Carrier frequency:      "
    f"{CARRIER_FREQUENCY_HZ / 1e6:.3f} MHz"
)

print(
    f"Transmit power:         "
    f"{TX_POWER_W:.2f} W "
    f"({TX_POWER_DBM:.2f} dBm)"
)

print(
    f"Tx antenna gain:        "
    f"{TX_ANTENNA_GAIN_DBI:.1f} dBi"
)

print(
    f"Rx antenna gain:        "
    f"{RX_ANTENNA_GAIN_DBI:.1f} dBi"
)

print(
    f"System losses:          "
    f"{SYSTEM_LOSS_DB:.1f} dB"
)

print(
    f"Bandwidth:              "
    f"{BANDWIDTH_HZ / 1000:.1f} kHz"
)

print(
    f"Noise figure:           "
    f"{NOISE_FIGURE_DB:.1f} dB"
)

print()

print("-" * 75)
print("PASS")
print("-" * 75)

print()

print(
    "Start:",
    pass_start.utc_strftime(
        "%Y-%m-%d %H:%M:%S UTC"
    )
)

print(
    "End:  ",
    pass_end.utc_strftime(
        "%Y-%m-%d %H:%M:%S UTC"
    )
)

print(
    f"Duration:               "
    f"{duration_seconds:.1f} s"
)

print()

print("-" * 75)
print("LINK BUDGET")
print("-" * 75)

print()

print(
    f"Noise power:            "
    f"{noise_power_dbm:.2f} dBm"
)

print(
    f"FSPL at closest range:  "
    f"{fspl_db[minimum_range_index]:.2f} dB"
)

print(
    f"Maximum received power: "
    f"{received_power_dbm[maximum_power_index]:.2f} dBm"
)

print(
    f"SNR at closest range:   "
    f"{snr_db[minimum_range_index]:.2f} dB"
)

print(
    f"Maximum link margin:    "
    f"{link_margin_db[maximum_power_index]:.2f} dB"
)

print()

print("-" * 75)
print("CLOSEST APPROACH")
print("-" * 75)

print()

print(
    f"Minimum range:          "
    f"{range_km[minimum_range_index]:.2f} km"
)

print(
    f"Elevation:              "
    f"{elevation_deg[minimum_range_index]:.2f} deg"
)

print(
    f"FSPL:                   "
    f"{fspl_db[minimum_range_index]:.2f} dB"
)

print(
    f"Received power:         "
    f"{received_power_dbm[minimum_range_index]:.2f} dBm"
)

print(
    f"SNR:                    "
    f"{snr_db[minimum_range_index]:.2f} dB"
)

print(
    f"Link margin:            "
    f"{link_margin_db[minimum_range_index]:.2f} dB"
)

print()

print("=" * 75)
print("MODEL COMPLETE")
print("=" * 75)


# ============================================================
# PLOT 1 — FSPL
# ============================================================

plt.figure()

plt.plot(
    time_minutes,
    fspl_db
)

plt.xlabel(
    "Time from pass start (minutes)"
)

plt.ylabel(
    "Free-Space Path Loss (dB)"
)

plt.title(
    "Time-Varying Free-Space Path Loss"
)

plt.grid(True)

plt.tight_layout()

plt.show()


# ============================================================
# PLOT 2 — RECEIVED POWER
# ============================================================

plt.figure()

plt.plot(
    time_minutes,
    received_power_dbm
)

plt.xlabel(
    "Time from pass start (minutes)"
)

plt.ylabel(
    "Received Power (dBm)"
)

plt.title(
    "Time-Varying Received Power"
)

plt.grid(True)

plt.tight_layout()

plt.show()


# ============================================================
# PLOT 3 — SNR
# ============================================================

plt.figure()

plt.plot(
    time_minutes,
    snr_db
)

plt.axhline(
    REQUIRED_SNR_DB,
    linestyle="--"
)

plt.xlabel(
    "Time from pass start (minutes)"
)

plt.ylabel(
    "SNR (dB)"
)

plt.title(
    "Time-Varying Signal-to-Noise Ratio"
)

plt.grid(True)

plt.tight_layout()

plt.show()


# ============================================================
# PLOT 4 — LINK MARGIN
# ============================================================

plt.figure()

plt.plot(
    time_minutes,
    link_margin_db
)

plt.axhline(
    0,
    linestyle="--"
)

plt.xlabel(
    "Time from pass start (minutes)"
)

plt.ylabel(
    "Link Margin (dB)"
)

plt.title(
    "Time-Varying Link Margin"
)

plt.grid(True)

plt.tight_layout()

plt.show()