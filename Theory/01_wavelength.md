# Wavelength and Antenna Scale

## Objective

Determine the electromagnetic wavelength corresponding to the
provisional carrier frequency and estimate the physical scale
of a half-wave dipole antenna.

## Parameters

Carrier frequency:

f = 145.8 MHz

where MHz (megahertz) = 10^6 Hz.

Speed of light:

c = 299,792,458 m/s

where m/s means metres per second.

## Theory

The fundamental relationship between wave velocity, frequency,
and wavelength is:

v = fλ

where:

- v = wave velocity (m/s)
- f = frequency (Hz)
- λ = wavelength (m)

For an electromagnetic wave propagating through free space:

v = c

Therefore:

λ = c/f

## Calculation

f = 145.8 × 10^6 Hz

λ = 299,792,458 / (145.8 × 10^6)

λ ≈ 2.0562 m

Therefore, the wavelength corresponding to 145.8 MHz is
approximately 2.0562 metres.

## Half-Wave Dipole Estimate

A simple half-wave dipole has an approximate electrical length:

L ≈ λ/2

Therefore:

L ≈ 2.0562/2

L ≈ 1.0281 m

This is an initial theoretical estimate, not the final physical
antenna dimension. Practical antenna dimensions can differ due
to conductor geometry, end effects, feed arrangement, and the
surrounding environment.

## Python Verification

The calculation was independently implemented in:

python/wavelength.py

The resulting values were:

Frequency: 145.8 MHz
Wavelength: 2.0562 m
Half-wave dipole length: 1.0281 m

The Python result agrees with the analytical calculation.

## Physical Interpretation

Frequency determines the spatial scale of the electromagnetic
wave. At 145.8 MHz, one complete wavelength is approximately
2.0562 metres long in free space.

This wavelength provides the starting point for designing an
antenna. A half-wave dipole is therefore approximately one metre
long at this frequency.

The actual antenna will later be designed and evaluated in HFSS
rather than relying solely on this simplified estimate.