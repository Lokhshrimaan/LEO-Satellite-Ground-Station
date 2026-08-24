import math

# ============================================================
# CONSTANTS
# ============================================================

c = 299_792_458              # speed of light (m/s)
k = 1.380649e-23             # Boltzmann constant (J/K)

# ============================================================
# SYSTEM PARAMETERS
# ============================================================

frequency_hz = 145.8e6       # carrier frequency (Hz)
distance_km = 500            # satellite-ground distance (km)

transmit_power_w = 1.0       # transmitter power (W)
transmit_gain_dbi = 3.0      # transmitter antenna gain (dBi)
receive_gain_dbi = 3.0       # receiver antenna gain (dBi)

temperature_k = 290          # system temperature (K)
bandwidth_hz = 10e3          # receiver bandwidth (Hz)
noise_figure_db = 5.0        # receiver noise figure (dB)

other_losses_db = 0.0        # additional losses (dB)

# ============================================================
# WAVELENGTH
# ============================================================

wavelength_m = c / frequency_hz

# ============================================================
# DISTANCE
# ============================================================

distance_m = distance_km * 1000

# ============================================================
# TRANSMITTER POWER
# ============================================================

transmit_power_dbm = 10 * math.log10(
    transmit_power_w * 1000
)

# ============================================================
# FREE-SPACE PATH LOSS
# ============================================================

fspl_db = 20 * math.log10(
    (4 * math.pi * distance_m) / wavelength_m
)

# ============================================================
# RECEIVED SIGNAL POWER
# ============================================================

received_power_dbm = (
    transmit_power_dbm
    + transmit_gain_dbi
    + receive_gain_dbi
    - fspl_db
    - other_losses_db
)

# ============================================================
# THERMAL NOISE
# ============================================================

thermal_noise_w = (
    k * temperature_k * bandwidth_hz
)

thermal_noise_dbm = 10 * math.log10(
    thermal_noise_w / 1e-3
)

# ============================================================
# RECEIVER NOISE
# ============================================================

receiver_noise_dbm = (
    thermal_noise_dbm + noise_figure_db
)

# ============================================================
# SIGNAL-TO-NOISE RATIO
# ============================================================

snr_db = (
    received_power_dbm
    - receiver_noise_dbm
)

# ============================================================
# RESULTS
# ============================================================

print("========== LEO LINK ANALYSIS ==========")
print()

print(f"Carrier frequency:      {frequency_hz/1e6:.2f} MHz")
print(f"Wavelength:             {wavelength_m:.4f} m")
print(f"Distance:               {distance_km:.0f} km")
print()

print(f"Transmit power:         {transmit_power_dbm:.2f} dBm")
print(f"Transmit antenna gain:  {transmit_gain_dbi:.2f} dBi")
print(f"Receive antenna gain:   {receive_gain_dbi:.2f} dBi")
print(f"Free-space path loss:   {fspl_db:.2f} dB")
print(f"Other losses:           {other_losses_db:.2f} dB")
print()

print(f"Received signal:        {received_power_dbm:.2f} dBm")
print()

print(f"Bandwidth:              {bandwidth_hz/1e3:.1f} kHz")
print(f"Thermal noise:          {thermal_noise_dbm:.2f} dBm")
print(f"Noise figure:           {noise_figure_db:.2f} dB")
print(f"Receiver noise:         {receiver_noise_dbm:.2f} dBm")
print()

print(f"SNR:                    {snr_db:.2f} dB")