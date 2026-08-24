# Doppler Shift Model

## Objective

Model the frequency shift produced by the relative motion between a
LEO satellite and the ground station.

This is essential for the eventual SDR receiver because the received
carrier frequency changes continuously during a satellite pass.

---

## 1. Doppler Effect

Doppler shift is the apparent change in observed frequency caused by
relative motion between a transmitter and receiver.

For the low-velocity approximation used in this project:

fD = -(vr/c)fc

where:

- fD = Doppler frequency shift in hertz (Hz)
- vr = radial velocity between satellite and ground station in metres
  per second (m/s)
- c = speed of light = 299,792,458 m/s
- fc = transmitted carrier frequency in hertz (Hz)

The negative sign follows the convention used in this project:

- vr < 0 → satellite approaching → positive Doppler shift
- vr = 0 → no Doppler shift
- vr > 0 → satellite receding → negative Doppler shift

---

## 2. Why Radial Velocity Is Used

The satellite's total orbital velocity is approximately 7.6 km/s for
the 500 km circular-orbit example.

However, the entire velocity does not contribute directly to Doppler
shift.

Only the component of velocity along the line connecting the satellite
and ground station contributes.

This component is called radial velocity.

Therefore:

total satellite velocity ≠ radial velocity

The radial velocity changes continuously during the satellite pass.

---

## 3. Simplified Pass Geometry

The simplified model uses:

d(t) = sqrt(h² + (vt)²)

where:

- d(t) = satellite-ground slant range
- h = satellite altitude
- v = satellite velocity
- t = time from closest approach

Radial velocity is obtained from the rate of change of slant range:

vr = dd/dt

which gives:

vr(t) = v²t / sqrt(h² + (vt)²)

At closest approach:

t = 0

therefore:

vr = 0

and consequently:

fD = 0

---

## 4. Doppler Behaviour During a Pass

Before closest approach:

vr < 0

Therefore:

fD > 0

The received frequency is higher than the nominal transmitted
frequency.

At closest approach:

vr ≈ 0

Therefore:

fD ≈ 0

The received frequency is approximately equal to the nominal carrier.

After closest approach:

vr > 0

Therefore:

fD < 0

The received frequency becomes lower than the nominal carrier.

The expected progression is therefore:

Positive Doppler
      ↓
Doppler approaches zero
      ↓
Doppler ≈ 0 at closest approach
      ↓
Negative Doppler

---

## 5. Example

The provisional carrier frequency is:

fc = 145.8 MHz

For an example radial velocity of:

vr = 1000 m/s

the Doppler shift is:

fD = -(1000 / 299,792,458) × 145.8 × 10^6

fD ≈ -486.3 Hz

Therefore, a radial velocity of 1 km/s produces approximately a
486 Hz frequency shift at 145.8 MHz.

This demonstrates why Doppler compensation is relevant to LEO
satellite communications.

---

## 6. Python Implementation

The Doppler model was implemented in:

python/doppler.py

The program calculates:

- satellite slant range
- radial velocity
- Doppler shift
- received carrier frequency

as functions of time.

The model was evaluated from -300 seconds to +300 seconds around
closest approach.

---

## 7. Validation

The expected behaviour was verified:

- Doppler is positive before closest approach.
- Doppler approaches zero near closest approach.
- Doppler is approximately zero at t = 0.
- Doppler becomes negative after closest approach.
- The received frequency is above the nominal carrier before closest
  approach and below it afterwards.

This agrees with the physical Doppler relationship.

---

## 8. Significance to the SDR Receiver

The transmitter may use a nominal carrier such as:

fc = 145.8 MHz

but the SDR does not necessarily observe exactly 145.8 MHz during
the entire satellite pass.

Instead:

fr(t) = fc + fD(t)

where:

- fr(t) = received carrier frequency
- fc = nominal transmitted carrier
- fD(t) = time-varying Doppler shift

Therefore, the eventual receiver must either track or compensate for
this changing frequency.

The Python Doppler model will later provide the basis for the
Doppler-affected channel and Doppler-compensation stages in GNU Radio.

---

## 9. Current Limitations

The present Doppler model uses simplified local-pass geometry.

It does not yet include:

- actual satellite orbital elements
- TLE propagation
- Earth's rotation
- ground-station latitude/longitude
- true azimuth/elevation
- actual line-of-sight velocity
- atmospheric effects

A realistic satellite-specific Doppler model will be implemented later.

---

## Current Status

The project now has a time-varying physical model connecting:

Satellite motion
    ↓
Slant range
    ↓
Radial velocity
    ↓
Doppler shift
    ↓
Received frequency

The next stage is to replace the simplified mathematical pass with
a realistic satellite pass and then introduce the Doppler effect into
the digital communication channel.