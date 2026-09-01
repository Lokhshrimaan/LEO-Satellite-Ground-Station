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

# Provisional satellite communication frequency
CARRIER_FREQUENCY_HZ = 145.8e6

# Speed of light
C = 299_792_458.0


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

    # 0 = rise
    if event == 0 and pass_start is None:

        pass_start = t

    # 2 = set
    elif event == 2 and pass_start is not None:

        pass_end = t
        break


if pass_start is None or pass_end is None:

    raise RuntimeError(
        "No complete satellite pass above "
        f"{MIN_ELEVATION_DEG} degrees was found."
    )


# ============================================================
# SAMPLE THE PASS
# ============================================================

# 1-second-ish sampling for this short pass
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
# SATELLITE RELATIVE TO GROUND STATION
# ============================================================

difference = satellite - ground_station

topocentric = difference.at(times)


# ============================================================
# ELEVATION / AZIMUTH / RANGE
# ============================================================

altitude, azimuth, distance = topocentric.altaz()


# ============================================================
# RANGE RATE
# ============================================================

(
    _latitude,
    _longitude,
    range_distance,
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

range_km = distance.km

range_rate_km_s = range_rate.km_per_s


# ============================================================
# DOPPLER
# ============================================================

# Range rate:
#
# negative = satellite approaching
# positive = satellite moving away
#
# Doppler:
#
# fD = -(vr / c) * fc

range_rate_m_s = range_rate_km_s * 1000.0

doppler_hz = (
    -range_rate_m_s
    / C
    * CARRIER_FREQUENCY_HZ
)


# ============================================================
# RECEIVED FREQUENCY
# ============================================================

received_frequency_hz = (
    CARRIER_FREQUENCY_HZ
    + doppler_hz
)


# ============================================================
# FIND KEY POINTS
# ============================================================

max_elevation_index = np.argmax(
    elevation_deg
)

minimum_range_index = np.argmin(
    range_km
)

maximum_doppler_index = np.argmax(
    doppler_hz
)

minimum_doppler_index = np.argmin(
    doppler_hz
)


# ============================================================
# DISPLAY RESULTS
# ============================================================

print()
print("=" * 75)
print("REAL ISS SATELLITE TRAJECTORY")
print("=" * 75)

print()

print(f"Satellite:          {satellite_name}")
print("NORAD ID:            25544")

print(
    f"Ground station:      "
    f"{GROUND_LATITUDE:.6f} N, "
    f"{GROUND_LONGITUDE:.6f} E"
)

print(
    f"Carrier frequency:   "
    f"{CARRIER_FREQUENCY_HZ / 1e6:.3f} MHz"
)

print()

print("-" * 75)
print("PASS INFORMATION")
print("-" * 75)

print()

print(
    "Pass start:",
    pass_start.utc_strftime(
        "%Y-%m-%d %H:%M:%S UTC"
    )
)

print(
    "Pass end:  ",
    pass_end.utc_strftime(
        "%Y-%m-%d %H:%M:%S UTC"
    )
)

print(
    f"Pass duration:       "
    f"{duration_seconds:.1f} seconds"
)

print()

print("-" * 75)
print("MAXIMUM ELEVATION")
print("-" * 75)

print()

print(
    f"Maximum elevation:   "
    f"{elevation_deg[max_elevation_index]:.2f} deg"
)

print(
    f"Azimuth there:       "
    f"{azimuth_deg[max_elevation_index]:.2f} deg"
)

print(
    f"Range there:         "
    f"{range_km[max_elevation_index]:.2f} km"
)

print()

print("-" * 75)
print("MINIMUM SLANT RANGE")
print("-" * 75)

print()

print(
    f"Minimum range:       "
    f"{range_km[minimum_range_index]:.2f} km"
)

print(
    f"Elevation there:     "
    f"{elevation_deg[minimum_range_index]:.2f} deg"
)

print(
    f"Range rate there:    "
    f"{range_rate_km_s[minimum_range_index]:+.3f} km/s"
)

print()

print("-" * 75)
print("DOPPLER")
print("-" * 75)

print()

print(
    f"Maximum Doppler:     "
    f"{doppler_hz[maximum_doppler_index]:+.2f} Hz"
)

print(
    f"Minimum Doppler:     "
    f"{doppler_hz[minimum_doppler_index]:+.2f} Hz"
)

print()

print(
    f"Received frequency "
    f"range:               "
    f"{received_frequency_hz.min() / 1e6:.6f} "
    f"to "
    f"{received_frequency_hz.max() / 1e6:.6f} MHz"
)

print()


# ============================================================
# PLOT 1 — ELEVATION
# ============================================================

plt.figure()

plt.plot(
    time_minutes,
    elevation_deg
)

plt.xlabel(
    "Time from pass start (minutes)"
)

plt.ylabel(
    "Elevation (degrees)"
)

plt.title(
    "ISS Elevation During Pass"
)

plt.grid(True)

plt.tight_layout()

plt.show()


# ============================================================
# PLOT 2 — SLANT RANGE
# ============================================================

plt.figure()

plt.plot(
    time_minutes,
    range_km
)

plt.xlabel(
    "Time from pass start (minutes)"
)

plt.ylabel(
    "Slant Range (km)"
)

plt.title(
    "ISS Ground-Station Slant Range"
)

plt.grid(True)

plt.tight_layout()

plt.show()


# ============================================================
# PLOT 3 — AZIMUTH
# ============================================================

plt.figure()

plt.plot(
    time_minutes,
    azimuth_deg
)

plt.xlabel(
    "Time from pass start (minutes)"
)

plt.ylabel(
    "Azimuth (degrees)"
)

plt.title(
    "ISS Azimuth During Pass"
)

plt.grid(True)

plt.tight_layout()

plt.show()


# ============================================================
# PLOT 4 — RANGE RATE
# ============================================================

plt.figure()

plt.plot(
    time_minutes,
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
    "ISS Radial Velocity / Range Rate"
)

plt.grid(True)

plt.tight_layout()

plt.show()


# ============================================================
# PLOT 5 — DOPPLER
# ============================================================

plt.figure()

plt.plot(
    time_minutes,
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


print("=" * 75)
print("TRAJECTORY MODEL COMPLETE")
print("=" * 75)
print()