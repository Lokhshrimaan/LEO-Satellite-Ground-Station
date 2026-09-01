# 12 — Real ISS Doppler Applied to BPSK

## Objective

To apply the Doppler shift produced by the actual ISS motion to a BPSK communication signal.

This connects the satellite-orbit model with the digital communication model.

## System

The signal chain is:

Satellite motion
→ Range rate
→ Doppler shift
→ Doppler-induced phase rotation
→ Received BPSK signal

## Doppler Equation

The Doppler shift is calculated as:

f_D(t) = -(v_r(t) / c) f_c

where:

- f_D = Doppler shift in Hz
- v_r = satellite-ground-station range rate in m/s
- c = speed of light
- f_c = carrier frequency

A negative Doppler value does not mean that the carrier frequency is negative.

The actual received frequency is:

f_r(t) = f_c + f_D(t)

Therefore, negative Doppler means that the received frequency is below the nominal carrier frequency.

## Simulation Parameters

- Satellite: ISS (ZARYA)
- NORAD ID: 25544
- Carrier frequency: 145.8 MHz
- Bit rate: 9.6 kbps
- Ground station latitude: 9.45° N
- Ground station longitude: 77.566667° E

## Results

The simulated ISS pass produced approximately:

- Maximum positive Doppler: +3285.95 Hz
- Maximum negative Doppler: -3284.44 Hz
- Doppler near closest approach: approximately 0 Hz

The Doppler changed continuously from positive to negative during the pass.

## Physical Interpretation

During the approaching portion of the pass, the satellite-ground distance decreases.

Therefore:

Range rate < 0
→ Doppler > 0
→ received frequency increases.

Near closest approach:

Range rate ≈ 0
→ Doppler ≈ 0.

During the receding portion:

Range rate > 0
→ Doppler < 0
→ received frequency decreases.

## Baseband Model

Instead of directly simulating a 145.8 MHz sampled waveform, the Doppler effect was represented using a complex baseband model.

The received signal is represented as:

s_rx(t) = s_tx(t) exp(jφ_D(t))

where:

- s_tx(t) = transmitted BPSK baseband signal
- φ_D(t) = accumulated Doppler phase
- j = imaginary unit

The Doppler phase is obtained by integrating the instantaneous Doppler frequency:

φ_D(t) = 2π ∫ f_D(t) dt

## Constellation Observation

Without Doppler, ideal BPSK occupies two constellation points:

(+1, 0) and (-1, 0).

With uncompensated Doppler, the constellation rotates around the origin.

This occurs because a frequency offset produces continuously changing carrier phase.

## Significance

This stage demonstrates that satellite motion directly affects the received digital waveform.

The project has therefore progressed from:

Orbital geometry
→ RF link budget
→ SNR
→ BPSK
→ AWGN
→ Real satellite Doppler
→ Doppler-affected BPSK

## Limitations

The current model assumes:

- Perfect knowledge of satellite trajectory
- Perfect knowledge of Doppler
- No noise in the Doppler demonstration
- No oscillator frequency error
- No multipath fading
- No synchronization errors

Doppler compensation will be implemented in the next stage.