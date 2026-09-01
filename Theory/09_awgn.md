# 08 — AWGN Channel and BPSK Error Performance

## Objective

To introduce channel noise into the BPSK communication system and observe its effect on the received waveform and bit recovery.

## AWGN

AWGN stands for Additive White Gaussian Noise.

- Additive: noise is added to the transmitted signal.
- White: noise has approximately constant spectral density over the relevant bandwidth.
- Gaussian: noise amplitude follows a Gaussian probability distribution.

The received signal can be represented as:

r(t) = s(t) + n(t)

where:

- r(t) = received signal
- s(t) = transmitted BPSK signal
- n(t) = AWGN

## Implementation

Python implementation:

`Python/bpsk_awgn.py`

The simulation used:

- Number of bits = 10,000
- Samples per symbol = 100
- Carrier frequency = 10 kHz
- Sampling frequency = 1 MHz
- Channel SNR = 5 dB

The noise power was calculated from:

SNR_linear = 10^(SNR_dB / 10)

P_noise = P_signal / SNR_linear

The noise standard deviation was then:

σ = sqrt(P_noise)

Gaussian random noise with this standard deviation was added to the transmitted waveform.

## Results

At 5 dB simulated passband SNR:

- Signal power = 0.500000
- Noise power = 0.158114
- Noise standard deviation = 0.397635
- Bit errors = 0
- BER = 0

The received waveform visibly contains significant noise compared with the clean transmitted waveform.

However, the receiver still recovered all 10,000 bits correctly.

## Why BER remained zero

The absence of observed errors does not mean that AWGN has no effect.

The receiver integrates 100 samples for every symbol. This integration averages the noise contribution while accumulating the desired signal energy.

Therefore, the decision variable remains sufficiently far from zero for this particular simulation.

Also, the 10,000-bit experiment only measures errors that actually occur. If no errors occur in the finite sample, the measured BER is:

BER = 0 / 10,000 = 0

This does not imply that the theoretical BER is exactly zero.

## Important SNR distinction

The SNR used in this experiment is a sample-level/passband waveform SNR.

For communication-system performance analysis, the more useful quantity is Eb/N0.

Eb = energy per bit

N0 = noise power spectral density

The relationship between BER and Eb/N0 will be investigated in the next step.

## Engineering significance

This experiment establishes the transition from an ideal communication link to an impaired communication channel.

The next stages will quantify the relationship between noise level and communication reliability using BER versus Eb/N0.

## Limitations

The present experiment does not yet include:

- Doppler shift
- Time-varying satellite range
- Fading
- Antenna pointing losses
- Atmospheric losses
- Coding
- Synchronization errors

These effects will be introduced progressively.

## Key takeaway

Increasing noise makes the received signal less reliable, but a single finite-length simulation at one SNR is insufficient to characterize communication performance.

A BER-versus-Eb/N0 curve is therefore required.