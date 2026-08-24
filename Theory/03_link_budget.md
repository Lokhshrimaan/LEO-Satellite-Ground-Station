# Satellite Link Budget

## Objective

Estimate the received signal power at a ground station after accounting
for transmitter power, antenna gains, free-space path loss, and other
propagation losses.

This step extends the free-space path-loss calculation into a basic
satellite communication link budget.

---

## 1. Link Budget Concept

A link budget accounts for the gains and losses experienced by a signal
between the transmitter and receiver.

For the simplified satellite link:

Satellite Transmitter
        ↓
Transmit Power
        ↓
Transmit Antenna Gain
        ↓
Free-Space Path Loss
        ↓
Receive Antenna Gain
        ↓
Ground Station Receiver

The received power is:

Pr = Pt + Gt + Gr - FSPL - Lother

where:

- Pr = received power in dBm
- Pt = transmitted power in dBm
- Gt = transmitter antenna gain in dBi
- Gr = receiver antenna gain in dBi
- FSPL = free-space path loss in dB
- Lother = additional losses in dB

Because all quantities are represented logarithmically, gains can be
added and losses can be subtracted directly.

---

## 2. dBm

dBm is a logarithmic unit of absolute power referenced to 1 milliwatt.

The conversion from milliwatts to dBm is:

P(dBm) = 10 log10(P(mW) / 1 mW)

For the initial model, a transmitter power of 1 W was assumed.

1 W = 1000 mW

Therefore:

Pt = 10 log10(1000)

Pt = 30 dBm

Thus:

1 W = 30 dBm

---

## 3. Antenna Gain and dBi

dBi represents antenna gain relative to an ideal isotropic radiator.

An isotropic radiator is a theoretical antenna that radiates equally
in every direction.

For the initial simplified model:

Transmit antenna gain:

Gt = 3 dBi

Receive antenna gain:

Gr = 3 dBi

These values are provisional assumptions used to develop and verify
the link-budget model.

They do not yet represent the final satellite or ground-station
antenna.

---

## 4. Initial Parameters

The initial link-budget model uses:

| Parameter | Value |
|---|---:|
| Carrier frequency | 145.8 MHz |
| Wavelength | 2.0562 m |
| Transmit power | 1 W |
| Transmit power | 30 dBm |
| Transmit antenna gain | 3 dBi |
| Receive antenna gain | 3 dBi |
| Initial distance | 500 km |
| Other losses | 0 dB |

The 145.8 MHz carrier frequency is currently a provisional development
frequency. A real target satellite and operating frequency have not yet
been selected.

Other losses are initially set to zero so that the fundamental link
budget can be understood before introducing additional effects.

---

## 5. Link Budget at 500 km

From the previous free-space path-loss calculation:

FSPL = 129.69 dB

The received power is therefore:

Pr = Pt + Gt + Gr - FSPL - Lother

Pr = 30 + 3 + 3 - 129.69 - 0

Pr = -93.69 dBm

Therefore:

Pr ≈ -93.69 dBm

The signal reaching the receiver is much weaker than the transmitted
signal because of the large free-space propagation loss.

---

## 6. Physical Interpretation of Received Power

The transmitted power was:

Pt = 1 W = 30 dBm

The calculated received power was:

Pr ≈ -93.69 dBm

Converting the received power back to watts gives approximately:

Pr ≈ 4.27 × 10^-13 W

or approximately:

Pr ≈ 0.427 pW

where:

pW = picowatt = 10^-12 W

This demonstrates that a satellite receiver must detect extremely weak
radio-frequency signals.

However, a weak received power does not by itself determine whether
communication is possible.

The received signal must later be compared with the receiver noise
level to determine the signal-to-noise ratio (SNR).

---

## 7. Distance Experiment

The satellite-ground distance was increased from 500 km to 1000 km.

### At 500 km

FSPL ≈ 129.69 dB

Pr ≈ -93.69 dBm

### At 1000 km

FSPL ≈ 135.72 dB

Pr ≈ -99.72 dBm

The distance doubled:

500 km → 1000 km

The additional path loss was approximately:

135.72 - 129.69 = 6.03 dB

Correspondingly, the received signal power decreased by approximately
6.03 dB.

---

## 8. Explanation of the 6 dB Change

Free-space received power follows an inverse-square relationship with
distance.

Therefore:

Pr ∝ 1/d²

Doubling the propagation distance gives:

Pr,new / Pr,old = 1/2² = 1/4

A reduction to one quarter of the original power corresponds to:

10 log10(1/4) ≈ -6.02 dB

Therefore, doubling the satellite-ground distance produces
approximately 6 dB additional free-space path loss.

The Python result of approximately 6.03 dB agrees with this theoretical
prediction.

---

## 9. Current Physical Relationship

The model developed so far establishes the following relationship:

Satellite motion
        ↓
Satellite-ground distance
        ↓
Free-space path loss
        ↓
Received signal power
        ↓
Signal-to-noise ratio
        ↓
Bit error rate
        ↓
Communication quality

The later stages of the project will model noise, SNR, Doppler shift,
modulation, and bit-error performance.

---

## 10. Python Implementation

The link-budget calculation is implemented in:

python/link_budget.py

The program calculates:

- wavelength
- conversion of transmitter power from watts to dBm
- free-space path loss
- received signal power
- effect of satellite-ground distance

The 500 km and 1000 km experiments were used to verify that doubling
distance produces approximately 6 dB additional propagation loss.

---

## 11. Current Limitations

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

These effects will be incorporated progressively as the ground-station
model becomes more realistic.