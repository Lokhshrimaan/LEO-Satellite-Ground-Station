# 07 — BPSK Digital Communication

## Objective

To implement a basic digital communication link using BPSK (Binary Phase Shift Keying) and verify that transmitted binary data can be recovered correctly under an ideal channel.

## Concept

BPSK represents binary information using two carrier phases separated by 180°.

The binary-to-symbol mapping used is:

s = 2b - 1

where:

- b = transmitted binary bit (0 or 1)
- s = BPSK symbol (-1 or +1)

Therefore:

| Bit | Symbol | Carrier phase |
|---|---:|---:|
| 0 | -1 | 180° |
| 1 | +1 | 0° |

The passband BPSK signal is:

s(t) = a_k cos(2πf_c t)

where:

- a_k = BPSK symbol
- f_c = carrier frequency
- t = time

A change from +1 to -1 reverses the carrier polarity:

-cos(θ) = cos(θ + π)

Therefore, the information is represented through a 180° phase change.

## Transmitter

The implemented transmitter performs:

1. Generate random binary data.
2. Map 0 → -1 and 1 → +1.
3. Repeat each symbol for multiple samples.
4. Generate a carrier.
5. Multiply the symbol sequence by the carrier.

Flow:

Bits → BPSK symbols → Carrier multiplication → BPSK waveform

## Receiver

The receiver performs coherent demodulation.

The received signal is multiplied by a locally generated carrier:

r(t) cos(2πf_c t)

The result is integrated over each symbol interval.

The resulting decision variable is approximately:

+50 → bit 1
-50 → bit 0

The sign is used for the final bit decision:

x ≥ 0 → 1
x < 0 → 0

## Implementation

Python implementation:

`Python/bpsk_basic.py`

Parameters used:

- Number of bits = 20
- Samples per symbol = 100
- Carrier frequency = 10 kHz
- Sampling frequency = 1 MHz

## Results

The transmitted and recovered bit sequences were identical.

Bit errors = 0

BER = 0.000000

where BER (Bit Error Rate) is:

BER = Number of bit errors / Total transmitted bits

## Interpretation

The zero BER result is expected because the channel contained no noise, Doppler, fading, or other impairments.

This experiment validates the basic digital communication chain:

Bits → BPSK modulation → Ideal channel → Demodulation → Recovered bits

## Engineering significance

BPSK provides the digital modulation foundation for the later satellite communication model. The same transmitter/receiver structure will subsequently be subjected to AWGN, Doppler, and time-varying satellite link conditions.

## Limitations

This experiment is an ideal simulation and does not represent an actual RF transmission. The 10 kHz carrier is used only for demonstrating the modulation process.

The later stages will replace the ideal channel with increasingly realistic satellite-channel impairments.