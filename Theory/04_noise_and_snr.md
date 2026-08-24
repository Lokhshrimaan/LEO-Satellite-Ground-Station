# Thermal Noise, Noise Figure and SNR

## Objective

Determine whether the received signal predicted by the link budget is
strong enough relative to receiver noise for communication to be
possible.

## 1. Thermal Noise

Every practical communication receiver is affected by noise.

A fundamental source is thermal noise, which results from the random
thermal motion of charge carriers.

The ideal thermal noise power is:

Pn = kTB

where:

- Pn = thermal noise power in watts (W)
- k = Boltzmann constant = 1.380649 × 10^-23 J/K
- T = absolute temperature in kelvin (K)
- B = receiver bandwidth in hertz (Hz)

For the initial model:

T = 290 K

### Bandwidth Results

| Bandwidth | Thermal Noise |
|---:|---:|
| 10 kHz | -133.98 dBm |
| 100 kHz | -123.98 dBm |
| 1 MHz | -113.98 dBm |

The results demonstrate that increasing bandwidth increases thermal
noise power.

Because:

Pn ∝ B

a tenfold increase in bandwidth produces a 10 dB increase in thermal
noise.

---

## 2. Receiver Noise Figure

Real receivers introduce additional noise and therefore perform worse
than an ideal thermal-noise-only receiver.

NF means Noise Figure.

For the initial model:

NF = 5 dB

The effective receiver noise level was approximated as:

Nreceiver = Nthermal + NF

For a 10 kHz bandwidth:

Nthermal = -133.98 dBm

Therefore:

Nreceiver = -133.98 + 5

Nreceiver ≈ -128.98 dBm

The 5 dB noise figure is a provisional modeling assumption and does
not represent the final SDR specification.

---

## 3. Signal-to-Noise Ratio

SNR means Signal-to-Noise Ratio.

It describes the strength of the desired signal relative to the
receiver noise.

In dB:

SNR = Pr - Nreceiver

where:

- SNR = signal-to-noise ratio in dB
- Pr = received signal power in dBm
- Nreceiver = receiver noise power in dBm

At 500 km:

Pr = -93.69 dBm

Nreceiver = -128.98 dBm

Therefore:

SNR = -93.69 - (-128.98)

SNR ≈ 35.29 dB

---

## 4. Effect of Bandwidth

At 500 km, keeping the received signal constant:

| Bandwidth | Receiver Noise | SNR |
|---:|---:|---:|
| 10 kHz | -128.98 dBm | 35.29 dB |
| 100 kHz | -118.98 dBm | 25.29 dB |
| 1 MHz | -108.98 dBm | 15.29 dB |

The signal power does not change in this experiment.

The noise increases because a larger receiver bandwidth admits more
thermal noise.

Therefore:

Bandwidth ↑
→ Noise ↑
→ SNR ↓

This demonstrates the fundamental tradeoff between communication
bandwidth and noise performance.

---

## 5. Effect of Distance

At 1000 km, the received signal decreases because of increased
free-space path loss.

At 500 km:

Pr ≈ -93.69 dBm

At 1000 km:

Pr ≈ -99.72 dBm

For the same 10 kHz bandwidth and receiver noise:

SNR at 500 km ≈ 35.29 dB

SNR at 1000 km ≈ 29.26 dB

Therefore, increasing satellite-ground distance reduces SNR.

---

## 6. Link Margin

Link margin represents the available SNR above the minimum SNR required
by a particular communication system.

Link Margin = SNRavailable - SNRrequired

For demonstration only, assuming:

SNRrequired = 10 dB

At 500 km:

Link Margin = 35.29 - 10

Link Margin = 25.29 dB

At 1000 km:

Link Margin = 29.26 - 10

Link Margin = 19.26 dB

The 10 dB requirement is only a temporary illustrative value. The final
required performance will be determined from the actual modulation and
coding scheme used later.

---

## 7. Python Implementation

The combined analysis is implemented in:

python/link_analysis.py

The program calculates:

- wavelength
- transmitter power in dBm
- free-space path loss
- received signal power
- thermal noise
- receiver noise including noise figure
- SNR

---

## 8. Limitations

The current model is intentionally simplified.

It does not yet include:

- actual satellite orbital geometry
- time-varying slant range
- Doppler shift
- atmospheric losses
- polarization mismatch
- antenna mismatch
- actual antenna gain
- actual satellite transmit power
- actual receiver noise figure
- modulation-specific SNR requirements
- coding gain

These will be introduced in later stages.