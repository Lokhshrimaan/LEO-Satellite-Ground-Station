# Free-Space Path Loss

## Objective

Calculate the propagation loss between a LEO satellite
and a ground station under ideal free-space conditions.

## Parameters

Carrier frequency:
145.8 MHz

Wavelength:
2.0562 m

## Equation

FSPL(dB) = 20 log10(4πd/λ)

## Results

| Distance | FSPL |
|---:|---:|
| 300 km | 125.26 dB |
| 500 km | 129.69 dB |
| 700 km | 132.62 dB |
| 1000 km | 135.72 dB |
| 1500 km | 139.24 dB |
| 2000 km | 141.74 dB |

## Physical interpretation

Free-space path loss increases as the square of
distance in linear power terms. Therefore doubling
the propagation distance produces approximately
6 dB additional loss.

## Validation

At 500 km → 1000 km, distance doubles and FSPL
increases by approximately 6 dB.