# 13 — Doppler Compensation of BPSK

## Objective

To demonstrate the effect of real ISS Doppler on a BPSK signal and implement receiver-side Doppler compensation.

## Signal Chain

BPSK
→ Real ISS Doppler
→ Doppler-induced phase rotation
→ Doppler compensation
→ Recovered BPSK

## Doppler Model

The Doppler shift is:

f_D(t) = -(v_r(t) / c) f_c

where:

- f_D = Doppler shift
- v_r = range rate
- c = speed of light
- f_c = carrier frequency

For the simulated ISS pass at 145.8 MHz:

- Maximum Doppler = +3285.95 Hz
- Minimum Doppler = -3284.44 Hz

## Complex Baseband Model

The Doppler-affected signal is represented as:

s_rx(t) = s_tx(t) exp(jφ_D(t))

where φ_D(t) is the accumulated Doppler phase.

## Doppler Compensation

The receiver applies the opposite phase rotation:

s_comp(t) = s_rx(t) exp(-jφ_D(t))

Therefore:

s_comp(t) = s_tx(t)

when the Doppler phase is known accurately.

## Constellation

Ideal BPSK contains two constellation points:

- Bit 0 → -1
- Bit 1 → +1

Before compensation, Doppler causes the constellation to rotate continuously around the origin.

After compensation, the constellation returns to the two ideal BPSK points.

## BER Results

| Condition | Bit Errors | BER |
|---|---:|---:|
| Without Doppler compensation | 504 | 0.504 |
| With Doppler compensation | 0 | 0.000 |

## Interpretation

The simulation demonstrates that satellite motion can cause severe carrier-frequency and phase variation.

Without compensation, the changing phase causes incorrect BPSK symbol decisions.

After applying the opposite Doppler phase, the constellation is restored and all simulated bits are recovered correctly.

## Engineering Significance

This demonstrates a fundamental receiver requirement for LEO satellite communication.

A practical receiver must estimate and track Doppler rather than assuming that the carrier frequency remains constant.

## Limitation

The current compensation uses the known simulated Doppler trajectory.

A real receiver does not know the exact received phase beforehand. It must estimate the frequency/phase offset from the received signal.

The next stages will move toward a more realistic receiver implementation.