# Development Log

# Day 1 — Fundamental Satellite Link Modeling

## Objective

Establish the mathematical foundation for the LEO satellite ground
station prototype before introducing hardware.

The first day focused on understanding the relationship between
electromagnetic frequency, wavelength, propagation distance, free-space
path loss, antenna gain, and received signal power.

All calculations were initially performed using a provisional carrier
frequency of 145.8 MHz. This frequency is being used only as a
development parameter; the final target satellite and operating
frequency will be selected later.

---

## Step 1 — Wavelength and Antenna Scale

### Objective

Determine the wavelength corresponding to the provisional carrier
frequency and estimate the physical scale of a simple half-wave dipole.

### Theory

The fundamental relationship between wave velocity, frequency, and
wavelength is:

v = fλ

where:

- v = wave velocity in metres per second (m/s)
- f = frequency in hertz (Hz)
- λ = wavelength in metres (m)

For an electromagnetic wave propagating through free space:

v = c

where c is the speed of light:

c = 299,792,458 m/s

Therefore:

λ = c/f

### Parameters

Carrier frequency:

f = 145.8 MHz

Since:

1 MHz = 10^6 Hz

therefore:

f = 145.8 × 10^6 Hz

### Calculation

λ = 299,792,458 / (145.8 × 10^6)

λ ≈ 2.0562 m

### Result

The wavelength at 145.8 MHz is approximately:

λ ≈ 2.0562 m

For an idealized half-wave dipole:

L ≈ λ/2

Therefore:

L ≈ 1.0281 m

### Physical Interpretation

The wavelength determines the approximate physical scale of an antenna.

At 145.8 MHz, one complete electromagnetic wavelength is
approximately 2.0562 metres long in free space.

A simple half-wave dipole therefore has an initial theoretical length
of approximately 1.0281 metres.

This is only a starting estimate. The final physical antenna dimension
will depend on conductor geometry, end effects, feed arrangement,
surrounding materials, and other practical factors.

The antenna will later be modeled in Ansys HFSS before fabrication.

### Implementation

Python implementation:

python/wavelength.py

Documentation:

theory/01_wavelength.md

---

## Step 2 — Free-Space Path Loss

### Objective

Determine how much signal power is lost as an electromagnetic wave
propagates through ideal free space between a satellite and a ground
station.

### Physical Concept

As an electromagnetic wave travels away from a transmitter, its energy
spreads over an increasingly larger area.

Therefore, the power density decreases with increasing propagation
distance.

For ideal free-space propagation, received power follows an
inverse-square relationship with distance.

### Equation

The free-space path loss is:

FSPL(dB) = 20 log10(4πd/λ)

where:

- FSPL = free-space path loss in decibels (dB)
- d = transmitter-to-receiver distance in metres (m)
- λ = wavelength in metres (m)
- π ≈ 3.14159

### Results

At 145.8 MHz:

| Distance | FSPL |
|---:|---:|
| 300 km | 125.26 dB |
| 500 km | 129.69 dB |
| 700 km | 132.62 dB |
| 1000 km | 135.72 dB |
| 1500 km | 139.24 dB |
| 2000 km | 141.74 dB |

### Validation

The distance was increased from 500 km to 1000 km.

At 500 km:

FSPL ≈ 129.69 dB

At 1000 km:

FSPL ≈ 135.72 dB

Therefore:

135.72 - 129.69 ≈ 6.03 dB

Doubling the propagation distance produced approximately 6 dB
additional free-space path loss.

This agrees with the theoretical inverse-square relationship:

Pr ∝ 1/d²

where:

- Pr = received power
- d = propagation distance

### Physical Interpretation

The approximately 6 dB increase is not an arbitrary property of
satellite communication.

It follows directly from the inverse-square spreading of electromagnetic
power in free space.

Therefore, as a LEO satellite moves farther from the ground station,
the propagation loss increases and the received signal becomes weaker.

### Implementation

Python implementation:

python/fspl.py

Documentation:

theory/02_free_space_path_loss.md

---

## Step 3 — Basic Satellite Link Budget

### Objective

Extend the free-space propagation model to estimate the power actually
available at the ground-station receiver.

### Link Budget Concept

A link budget accounts for the gains and losses experienced by a signal
between a transmitter and receiver.

The simplified link is:

Satellite transmitter
        ↓
Transmitter power
        ↓
Transmit antenna gain
        ↓
Free-space path loss
        ↓
Receive antenna gain
        ↓
Ground-station receiver

### Link Budget Equation

Pr = Pt + Gt + Gr - FSPL - Lother

where:

- Pr = received power in dBm
- Pt = transmitted power in dBm
- Gt = transmitter antenna gain in dBi
- Gr = receiver antenna gain in dBi
- FSPL = free-space path loss in dB
- Lother = additional losses in dB

### dBm

dBm is a logarithmic unit of absolute power referenced to 1 milliwatt.

P(dBm) = 10 log10(P(mW) / 1 mW)

For the initial model:

Pt = 1 W

Since:

1 W = 1000 mW

then:

Pt = 10 log10(1000)

Pt = 30 dBm

Therefore:

1 W = 30 dBm

### dBi

dBi represents antenna gain relative to an ideal isotropic radiator.

An isotropic radiator is a theoretical antenna that radiates equally
in all directions.

For the initial simplified model:

Transmit antenna gain:

Gt = 3 dBi

Receive antenna gain:

Gr = 3 dBi

These are provisional assumptions and do not yet represent the final
satellite or ground-station antenna.

### Initial Parameters

| Parameter | Value |
|---|---:|
| Carrier frequency | 145.8 MHz |
| Wavelength | 2.0562 m |
| Transmitter power | 1 W |
| Transmitter power | 30 dBm |
| Transmit antenna gain | 3 dBi |
| Receive antenna gain | 3 dBi |
| Other losses | 0 dB |

### 500 km Link

From Step 2:

FSPL = 129.69 dB

Therefore:

Pr = 30 + 3 + 3 - 129.69 - 0

Pr ≈ -93.69 dBm

### 1000 km Link

At 1000 km:

FSPL = 135.72 dB

Therefore:

Pr = 30 + 3 + 3 - 135.72 - 0

Pr ≈ -99.72 dBm

### Distance Comparison

| Distance | FSPL | Received Power |
|---:|---:|---:|
| 500 km | 129.69 dB | -93.69 dBm |
| 1000 km | 135.72 dB | -99.72 dBm |

The received power decreases by approximately:

-99.72 - (-93.69) = -6.03 dB

when the distance doubles.

This agrees with the 6 dB change predicted from the free-space
inverse-square relationship.

### Physical Interpretation

A satellite may transmit power on the order of watts, while the power
available at the ground-station receiver can be many orders of
magnitude smaller.

However, received power alone does not determine whether communication
is possible.

The receiver must distinguish the desired signal from thermal and
receiver-generated noise.

Therefore, the next major quantity to determine is the
signal-to-noise ratio (SNR).

### Important Limitation

The current link budget is intentionally simplified.

It does not yet include:

- receiver noise
- receiver noise figure
- cable loss
- connector loss
- antenna mismatch loss
- polarization mismatch
- atmospheric loss
- actual satellite transmit power
- actual satellite antenna gain
- actual ground-station antenna gain
- time-varying satellite slant range
- Doppler shift

These effects will be added progressively.

### Implementation

Python implementation:

python/link_budget.py

Documentation:

theory/03_link_budget.md

---

# Day 1 Summary

## Completed

- [x] Established frequency-wavelength relationship
- [x] Calculated wavelength at 145.8 MHz
- [x] Estimated half-wave dipole physical scale
- [x] Implemented wavelength calculation in Python
- [x] Derived free-space path loss
- [x] Calculated FSPL for multiple satellite-ground distances
- [x] Verified approximately 6 dB additional loss when distance doubles
- [x] Introduced dBm
- [x] Introduced dBi
- [x] Developed a basic satellite link-budget equation
- [x] Calculated received power at 500 km
- [x] Calculated received power at 1000 km
- [x] Verified the received-power change against the theoretical
      inverse-square relationship

## Software Created

python/wavelength.py
python/fspl.py
python/link_budget.py

## Theory Documentation Created

theory/01_wavelength.md
theory/02_free_space_path_loss.md
theory/03_link_budget.md

## Key Results

At the provisional frequency of 145.8 MHz:

Wavelength:

λ ≈ 2.0562 m

Estimated half-wave dipole length:

L ≈ 1.0281 m

Free-space path loss at 500 km:

FSPL ≈ 129.69 dB

Received power at 500 km under the initial assumptions:

Pr ≈ -93.69 dBm

Free-space path loss at 1000 km:

FSPL ≈ 135.72 dB

Received power at 1000 km:

Pr ≈ -99.72 dBm

## Engineering Understanding Gained

The first day established the relationship:

Frequency
    ↓
Wavelength
    ↓
Antenna physical scale

and:

Distance
    ↓
Free-space path loss
    ↓
Received power

The complete communication-quality relationship will later be extended
to:

Satellite motion
    ↓
Distance + Doppler
    ↓
Path loss + frequency offset
    ↓
Received power
    ↓
Noise
    ↓
SNR
    ↓
BER
    ↓
Communication reliability

## Day 1 Status

The mathematical foundation of the ground-station prototype has been
established.

No RF hardware was required during Day 1.

The next stage will introduce receiver noise, bandwidth, noise figure,
SNR, and link margin before developing the digital communication chain
in GNU Radio.

## Step 8 — Real Satellite Orbit and Pass Modeling

### Work Completed

Implemented a realistic LEO satellite pass model using the ISS
(NORAD 25544) as the test satellite.

Instead of assuming a fixed satellite altitude or artificial trajectory,
a real TLE was loaded from:

`Data/ISS_25544.tle`

The satellite orbit was propagated using SGP4 through the Skyfield
Python library.

An approximate ground station was defined at:

- Latitude: 9.45° N
- Longitude: 77.566667° E

A 10° minimum elevation mask was applied.

### Results

The next usable ISS passes were successfully identified.

For the selected pass:

- Pass duration: 385.5 s
- Maximum elevation: 46.36°
- Minimum slant range: 559.91 km
- Maximum Doppler: +3193.98 Hz
- Minimum Doppler: −3196.67 Hz
- Received frequency range: 145.796803–145.803194 MHz

### Validation

The elevation profile followed the expected rise–maximum–fall pattern.

The slant range decreased toward closest approach and increased
afterwards.

The range rate transitioned from negative to positive, corresponding
to the satellite changing from approaching to receding.

The Doppler shift showed the expected opposite-sign relationship with
range rate.

The small non-zero range rate at the numerically sampled minimum range
was attributed to discrete time sampling rather than a physical-model
error.

### Engineering Understanding Gained

This step demonstrated how an actual satellite orbital state can be
converted into a time-varying communication geometry.

The model now provides the physical inputs required for realistic
satellite link-budget and Doppler analysis.

### Status

Step 8 COMPLETE.