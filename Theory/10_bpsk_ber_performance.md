# 10 — BPSK BER Performance in AWGN

## Objective

To evaluate the performance of the BPSK digital communication system as a function of Eb/N0 and verify the simulation against the theoretical BPSK BER expression.

## Key Parameters

- Number of simulated bits = 1,000,000
- Modulation = BPSK (Binary Phase Shift Keying)
- Channel = AWGN (Additive White Gaussian Noise)
- Eb/N0 range = -2 dB to 10 dB

## Theory

For coherent BPSK transmission over an AWGN channel:

BER = 1/2 × erfc(sqrt(Eb/N0))

where:

- BER = Bit Error Rate
- Eb = energy per information bit
- N0 = noise power spectral density
- Eb/N0 = energy-per-bit to noise-density ratio
- erfc = complementary error function

The ratio was converted from decibels to linear form using:

Eb/N0(linear) = 10^(Eb/N0(dB) / 10)

## Simulation Method

For each Eb/N0 value:

1. Generate random binary data.
2. Map 0 → -1 and 1 → +1.
3. Calculate the corresponding AWGN standard deviation.
4. Add Gaussian noise to the BPSK symbols.
5. Perform threshold detection at zero.
6. Compare transmitted and recovered bits.
7. Calculate BER.
8. Compare simulated BER with theoretical BER.

## Results

The simulated BER curve closely follows the theoretical BPSK curve throughout the tested Eb/N0 range.

The BER decreases rapidly as Eb/N0 increases.

Representative behavior:

- At low Eb/N0, noise is comparable to the signal energy and many decisions are incorrect.
- At higher Eb/N0, the received symbols are increasingly separated from the decision threshold.
- Consequently, the probability of an incorrect bit decision decreases.

## Interpretation

The simulation confirms:

Eb/N0 ↑  →  BER ↓

This demonstrates the fundamental trade-off between signal energy and communication reliability.

The close agreement between simulation and theory also validates the BPSK/AWGN implementation.

## Engineering Significance

BER versus Eb/N0 is a fundamental digital communication performance metric.

This result provides a validated baseline against which the later satellite-channel model can be evaluated.

The satellite link will introduce additional effects such as:

- Time-varying propagation loss
- Doppler shift
- Changing received SNR
- Doppler compensation

These effects will eventually be connected to the validated BPSK BER model.

## Implementation

Python implementation:

`Python/bpsk_ber_curve.py`

## Limitations

The present model assumes:

- AWGN only
- Perfect carrier synchronization
- Perfect symbol timing
- No fading
- No Doppler
- No coding
- No hardware impairments

Therefore, this is a controlled digital communication benchmark rather than a complete satellite communication model.