# Satellite Geometry and Time-Varying Link

## Objective

Move from a static satellite-ground distance to a time-varying
geometric model in which the satellite moves relative to the ground
station.

This provides the foundation for calculating:

- satellite-ground slant range
- changing free-space path loss
- changing received power
- changing SNR
- radial velocity
- Doppler shift

---

## 1. Why Satellite Geometry Is Required

The satellite-ground distance is not constant during a satellite pass.

Previously, the link budget used a fixed distance such as:

d = 500 km

This was useful for understanding the fundamental link budget, but a
real LEO satellite continuously changes its position relative to the
ground station.

Therefore:

d = d(t)

where:

- d(t) = satellite-ground distance as a function of time
- t = time

The changing distance causes the propagation loss and received signal
power to change during the pass.

---

## 2. Orbital Radius

The satellite's distance from Earth's center is:

rs = RE + h

where:

- rs = satellite orbital radius
- RE = Earth's mean radius
- h = satellite altitude above Earth's surface

For the simplified model:

RE = 6371 km

h = 500 km

Therefore:

rs = 6371 + 500

rs = 6871 km

Thus:

rs = 6.871 × 10^6 m

---

## 3. Circular Orbital Velocity

For a simplified circular orbit, orbital velocity is:

v = sqrt(μ/rs)

where:

- v = orbital velocity in metres per second (m/s)
- μ = Earth's standard gravitational parameter
- rs = orbital radius in metres

The Earth's standard gravitational parameter is approximately:

μ = 3.986004418 × 10^14 m^3/s^2

For a 500 km circular orbit:

v ≈ 7616 m/s

or:

v ≈ 7.616 km/s

This means a LEO satellite travels at approximately 7.6 km/s in
this simplified model.

---

## 4. Simplified Satellite Pass Model

For the first time-varying model, the satellite is assumed to move
along a straight local path relative to the ground station.

The horizontal displacement from closest approach is:

x(t) = vt

where:

- x(t) = horizontal displacement from closest approach
- v = satellite velocity
- t = time from closest approach

The simplified slant range is then:

d(t) = sqrt(h^2 + x(t)^2)

or:

d(t) = sqrt(h^2 + (vt)^2)

where:

- d(t) = satellite-ground slant range
- h = satellite altitude
- v = satellite velocity
- t = time from closest approach

---

## 5. Closest Approach

At:

t = 0

the satellite is at its closest point in this simplified model.

Therefore:

x(0) = 0

and:

d(0) = h

For the 500 km example:

d(0) = 500 km

This explains why the earlier 500 km distance can be interpreted as
approximately the closest-approach distance in this simplified model.

---

## 6. Example Time-Varying Geometry

Using the approximate orbital velocity of 7.616 km/s:

| Time from closest approach | Approximate slant range |
|---:|---:|
| -300 s | ~2334 km |
| -150 s | ~1199 km |
| 0 s | 500 km |
| +150 s | ~1199 km |
| +300 s | ~2334 km |

The satellite is closest at t = 0 and progressively farther away
before and after closest approach.

The geometry is symmetric in this simplified model.

---

## 7. Effect on Free-Space Path Loss

The free-space path loss is:

FSPL(t) = 20 log10(4πd(t)/λ)

Because d(t) changes with time:

FSPL also becomes time-dependent.

Therefore:

d(t) ↑
→ FSPL(t) ↑
→ received power ↓

Conversely:

d(t) ↓
→ FSPL(t) ↓
→ received power ↑

---

## 8. Effect on Received Power

The simplified link-budget equation becomes:

Pr(t) = Pt + Gt + Gr - FSPL(t) - Lother

where:

- Pr(t) = received power as a function of time
- Pt = transmitter power
- Gt = transmitter antenna gain
- Gr = receiver antenna gain
- FSPL(t) = time-varying free-space path loss
- Lother = other losses

Therefore, received power is no longer a single number.

It becomes a time-varying quantity:

Pr = Pr(t)

---

## 9. Effect on SNR

The received signal power changes with time while the receiver noise
is initially assumed constant.

Therefore:

SNR(t) = Pr(t) - Nreceiver

where:

- SNR(t) = signal-to-noise ratio as a function of time
- Pr(t) = time-varying received power
- Nreceiver = receiver noise power

As the satellite moves farther away:

Pr(t) ↓
→ SNR(t) ↓

At closest approach:

Pr(t) is maximum
→ SNR(t) is maximum

---

## 10. Simplified Time-Varying Link

The model developed so far creates the following relationship:

Satellite motion
        ↓
Changing position
        ↓
Changing slant range
        ↓
Changing FSPL
        ↓
Changing received power
        ↓
Changing SNR

This is the first dynamic component of the satellite ground-station
model.

---

## 11. Python Implementation

The simplified geometry was implemented in:

python/satellite_geometry.py

The time-varying link was implemented in:

python/time_varying_link.py

The programs calculate:

- orbital radius
- approximate circular orbital velocity
- satellite-ground slant range
- free-space path loss as a function of time
- received power as a function of time
- SNR as a function of time

---

## 12. Model Limitations

This is intentionally a simplified educational model.

It does not yet account for:

- Earth's curvature
- Earth's rotation
- ground-station latitude and longitude
- satellite inclination
- orbital eccentricity
- actual orbital position
- actual satellite trajectory
- azimuth
- elevation
- horizon visibility
- atmospheric effects
- real TLE/orbital-element data

These limitations will be addressed when the model is upgraded to
an actual satellite pass.

The simplified model is being used first so that the physical
relationship between satellite motion, distance, propagation loss,
and received power is understood before introducing full orbital
propagation.

---

## Current Engineering Model

The project has now progressed from:

Static distance

to:

Time-varying satellite-ground distance.

The next step is to model the second major consequence of satellite
motion:

Doppler frequency shift.