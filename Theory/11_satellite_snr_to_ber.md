# 11 — Satellite SNR to BPSK BER

## Objective

To connect the time-varying physical satellite link model with the validated BPSK digital communication model.

The complete chain is:

Range → FSPL → Received Power → SNR → Eb/N0 → BER

## Communication Parameters

- Satellite: ISS (ZARYA)
- NORAD ID: 25544
- Carrier frequency = 145.8 MHz
- Bandwidth = 12.5 kHz
- Bit rate = 9.6 kbps
- Tx power = 30 dBm
- Tx antenna gain = 2 dBi
- Rx antenna gain = 10 dBi
- System losses = 2 dB
- Noise figure = 3 dB

## Eb/N0 Conversion

The relationship between SNR and Eb/N0 is:

Eb/N0 = SNR × B/Rb

In decibel form:

(Eb/N0)dB = SNRdB + 10 log10(B/Rb)

where:

- B = receiver bandwidth
- Rb = bit rate

## BER Calculation

For coherent BPSK in AWGN:

BER = 1/2 × erfc(sqrt(Eb/N0))

The BER was calculated at every sampled point of the ISS pass.

## Results

For the simulated pass:

- Minimum SNR = 30.85 dB
- Maximum SNR = 41.18 dB
- Minimum Eb/N0 = 32.00 dB
- Maximum Eb/N0 = 42.33 dB

The calculated theoretical BPSK BER was effectively zero across the pass.

## Interpretation

As the ISS approaches the ground station, the slant range decreases.

Therefore:

Range ↓
→ FSPL ↓
→ Received power ↑
→ SNR ↑
→ Eb/N0 ↑
→ BER ↓

After closest approach, the reverse occurs.

The results demonstrate that satellite motion directly affects the predicted digital communication performance.

## Important Observation

The calculated Eb/N0 is sufficiently high that the theoretical BPSK BER becomes extremely small and numerically approaches zero.

Therefore, the flat BER curve does not mean that BER is universally zero. It means that the assumed link parameters provide a very large communication margin for this particular pass.

## Implementation

Python implementation:

`Python/satellite_ber_vs_time.py`

## Engineering Significance

This stage connects orbital mechanics and RF link-budget analysis with digital communication performance.

The project is no longer treating satellite propagation and digital modulation as independent models.

## Limitations

The model currently assumes:

- AWGN channel
- Perfect synchronization
- No fading
- No atmospheric attenuation
- No polarization mismatch
- No implementation losses beyond the specified system loss
- Perfect Doppler-free carrier recovery

Doppler effects will be introduced in the following stage.