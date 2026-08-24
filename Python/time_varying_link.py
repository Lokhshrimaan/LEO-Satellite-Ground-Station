import math

# ============================================================
# CONSTANTS
# ============================================================

c = 299_792_458
k = 1.380649e-23
mu = 3.986004418e14

earth_radius_km = 6371.0

# ============================================================
# SATELLITE
# ============================================================

altitude_km = 500.0

orbital_radius_m = (
    earth_radius_km + altitude_km
) * 1000

velocity_mps = math.sqrt(
    mu / orbital_radius_m
)

velocity_kmps = velocity_mps / 1000

# ============================================================
# COMMUNICATION PARAMETERS
# ============================================================

frequency_hz = 145.8e6

transmit_power_w = 1.0
transmit_gain_dbi = 3.0
receive_gain_dbi = 3.0

temperature_k = 290
bandwidth_hz = 10e3
noise_figure_db = 5.0

wavelength_m = c / frequency_hz

transmit_power_dbm = (
    10 * math.log10(transmit_power_w * 1000)
)

thermal_noise_w = (
    k * temperature_k * bandwidth_hz
)

thermal_noise_dbm = (
    10 * math.log10(thermal_noise_w / 1e-3)
)

receiver_noise_dbm = (
    thermal_noise_dbm + noise_figure_db
)

# ============================================================
# TIME-VARYING LINK
# ============================================================

time_values = range(-300, 301, 30)

print("========== TIME-VARYING LEO LINK ==========")
print()
print(
    "Time(s) | Range(km) | FSPL(dB) | "
    "Rx Power(dBm) | SNR(dB)"
)

for t in time_values:

    # Horizontal displacement
    x_km = velocity_kmps * t

    # Slant range
    distance_km = math.sqrt(
        altitude_km**2 + x_km**2
    )

    distance_m = distance_km * 1000

    # FSPL
    fspl_db = 20 * math.log10(
        (4 * math.pi * distance_m) / wavelength_m
    )

    # Received power
    received_power_dbm = (
        transmit_power_dbm
        + transmit_gain_dbi
        + receive_gain_dbi
        - fspl_db
    )

    # SNR
    snr_db = (
        received_power_dbm
        - receiver_noise_dbm
    )

    print(
        f"{t:>+6d} | "
        f"{distance_km:>9.1f} | "
        f"{fspl_db:>8.2f} | "
        f"{received_power_dbm:>13.2f} | "
        f"{snr_db:>7.2f}"
    )