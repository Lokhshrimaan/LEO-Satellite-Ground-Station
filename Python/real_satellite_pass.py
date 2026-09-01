from pathlib import Path
from datetime import datetime, timedelta, timezone

from skyfield.api import load, wgs84, EarthSatellite


# ============================================================
# PROJECT PATH
# ============================================================

# This automatically finds:
#
# LEO Ground Station/
# ├── Data/
# │   └── ISS_25544.tle
# │
# └── Python/
#     └── real_satellite_pass.py
#
PROJECT_ROOT = Path(__file__).resolve().parent.parent

TLE_FILE = PROJECT_ROOT / "Data" / "ISS_25544.tle"


# ============================================================
# GROUND STATION
# ============================================================

# Approximate Rajapalayam coordinates

GROUND_LATITUDE = 9.45
GROUND_LONGITUDE = 77.566667

# Minimum elevation considered for a usable pass

MIN_ELEVATION_DEG = 10.0


# ============================================================
# CHECK TLE FILE
# ============================================================

if not TLE_FILE.is_file():

    raise FileNotFoundError(
        "\n"
        "ERROR: TLE file was not found.\n\n"
        f"Expected file:\n{TLE_FILE}\n\n"
        "Make sure the following file exists:\n"
        "Data/ISS_25544.tle\n"
    )


# ============================================================
# LOAD SKYFIELD TIMESCALE
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
# VALIDATE TLE
# ============================================================

if not satellite_name:
    raise ValueError("TLE name line is empty.")

if not line1.startswith("1 "):
    raise ValueError(
        "Invalid TLE line 1.\n"
        f"Received:\n{line1}"
    )

if not line2.startswith("2 "):
    raise ValueError(
        "Invalid TLE line 2.\n"
        f"Received:\n{line2}"
    )


# ============================================================
# CREATE SATELLITE OBJECT
# ============================================================

satellite = EarthSatellite(
    line1,
    line2,
    satellite_name,
    ts
)


# ============================================================
# CREATE GROUND STATION
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
# FIND SATELLITE PASSES
# ============================================================

times, events = satellite.find_events(
    ground_station,
    t0,
    t1,
    altitude_degrees=MIN_ELEVATION_DEG
)


# ============================================================
# EVENT DEFINITIONS
# ============================================================

event_names = {
    0: "RISE above 10 deg",
    1: "MAXIMUM elevation",
    2: "SET below 10 deg"
}


# ============================================================
# DISPLAY HEADER
# ============================================================

print()
print("=" * 70)
print("REAL SATELLITE PASS MODEL")
print("=" * 70)

print()

print(f"Satellite:        {satellite_name}")
print("NORAD ID:          25544")
print(f"TLE file:          {TLE_FILE}")

print()

print(
    f"Ground latitude:   "
    f"{GROUND_LATITUDE:.6f} deg"
)

print(
    f"Ground longitude:  "
    f"{GROUND_LONGITUDE:.6f} deg"
)

print(
    f"Minimum elevation: "
    f"{MIN_ELEVATION_DEG:.1f} deg"
)

print()


# ============================================================
# DISPLAY PASS EVENTS
# ============================================================

print("-" * 70)
print("PASS EVENTS")
print("-" * 70)

if len(times) == 0:

    print()
    print(
        "No pass above the selected elevation "
        "was found during the next 24 hours."
    )

else:

    for t, event in zip(times, events):

        print(
            t.utc_strftime(
                "%Y-%m-%d %H:%M:%S UTC"
            ),
            "|",
            event_names[event]
        )


# ============================================================
# FINISH
# ============================================================

print()
print("=" * 70)
print("MODEL COMPLETE")
print("=" * 70)
print()