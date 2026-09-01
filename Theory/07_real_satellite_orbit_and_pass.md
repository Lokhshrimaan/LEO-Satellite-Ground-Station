# Step 8 — Real LEO Satellite Orbit and Ground-Station Pass

## Objective

Replace the simplified artificial satellite trajectory used in earlier
steps with a realistic orbital model based on an actual Two-Line Element
(TLE) set.

The International Space Station (ISS), NORAD catalog number 25544, was
used as the test satellite.

The ground station was modeled at approximately:

- Latitude: 9.45° N
- Longitude: 77.566667° E
- Location reference: Rajapalayam, Tamil Nadu, India

A minimum elevation mask of 10° was used to define the usable portion
of the satellite pass.

---

## Theory

### TLE — Two-Line Element Set

A TLE is a standardized representation of orbital parameters used to
propagate an artificial satellite's position and velocity.

The project uses the following locally stored TLE:

ISS (ZARYA)
1 25544U 98067A   26235.53239059  .00008992  00000+0  16763-3 0  9997
2 25544  51.6331 326.7717 0007703  75.9661 284.2184 15.49588782582196

The TLE is stored locally in:

Data/ISS_25544.tle

---

## SGP4 Orbital Propagation

SGP4 means Simplified General Perturbations 4.

It is an orbital propagation model used to calculate a satellite's
position and velocity from TLE orbital elements.

The simulation uses the Skyfield Python library and its EarthSatellite
interface to propagate the ISS orbit.

The processing chain is:

TLE
→ SGP4 propagation
→ Satellite position and velocity
→ Ground-station relative geometry
→ Elevation / azimuth / range
→ Range rate
→ Doppler shift

---

## Ground-Station Geometry

The ground station is represented using its latitude and longitude.

For every time sample, the satellite position is transformed into a
topocentric coordinate system relative to the ground station.

The resulting quantities are:

- Elevation angle
- Azimuth angle
- Slant range
- Range rate

### Elevation

Elevation is the angle of the satellite above the local horizon.

0° represents the horizon.

90° represents the zenith, directly overhead.

Only elevations above 10° were considered for this experiment.

### Azimuth

Azimuth represents the horizontal direction of the satellite measured
clockwise from North.

0° = North
90° = East
180° = South
270° = West

### Slant Range

Slant range is the direct three-dimensional distance between the ground
station and the satellite.

It changes continuously during the pass.

---

## Range Rate

Range rate is the time derivative of the satellite-ground-station
distance:

v_r = dr/dt

where:

v_r = radial velocity / range rate
r = slant range
t = time

A negative range rate indicates that the satellite is approaching the
ground station.

A positive range rate indicates that the satellite is moving away.

Therefore:

v_r < 0 → approaching
v_r = 0 → closest approach
v_r > 0 → receding

---

## Doppler Shift

The carrier frequency used in this simulation was:

f_c = 145.8 MHz

The Doppler shift was calculated using:

f_D = -(v_r / c) f_c

where:

f_D = Doppler frequency shift in Hz
v_r = range rate in m/s
c = speed of light ≈ 299,792,458 m/s
f_c = transmitted carrier frequency in Hz

The received frequency was calculated as:

f_received = f_c + f_D

Therefore, when the satellite approaches:

v_r < 0
→ f_D > 0
→ received frequency increases

When the satellite recedes:

v_r > 0
→ f_D < 0
→ received frequency decreases

---

## Experimental Results

For the selected pass:

Pass start:
2026-08-24 18:10:21 UTC

Pass end:
2026-08-24 18:16:46 UTC

Pass duration:
385.5 seconds ≈ 6.43 minutes

Maximum elevation:
46.36°

Azimuth at maximum elevation:
125.23°

Minimum slant range:
559.91 km

Maximum Doppler:
+3193.98 Hz

Minimum Doppler:
−3196.67 Hz

Received frequency range:

145.796803 MHz to 145.803194 MHz

---

## Physical Interpretation

The elevation plot shows the satellite rising above the 10° elevation
mask, reaching a maximum elevation of approximately 46.36°, and then
falling back below the 10° mask.

The slant-range plot shows the distance decreasing as the satellite
approaches the ground station and increasing after closest approach.

The range-rate plot changes from negative to positive:

negative → zero → positive

This represents:

approaching → closest approach → receding

The Doppler plot exhibits the corresponding opposite-signed
frequency shift:

positive Doppler → zero Doppler → negative Doppler

The maximum magnitude of Doppler was approximately 3.2 kHz at
145.8 MHz.

---

## Important Numerical Observation

The reported range rate at the sampled minimum range was approximately
+0.006 km/s rather than exactly zero.

This is not considered a physical-model error.

The trajectory was evaluated at discrete time samples, so the exact
continuous-time minimum-range point can occur between two samples.

The range-rate plot itself shows the expected zero crossing close to
the minimum-range region.

---

## Engineering Significance

This step converts the project from a simplified fixed-distance
satellite model into a realistic time-varying satellite communication
geometry.

The output of this model will be used by later stages to determine:

1. Time-varying free-space path loss
2. Time-varying received power
3. Time-varying Doppler
4. Carrier-frequency offset
5. Link margin during a satellite pass
6. Doppler compensation requirements
7. GNU Radio receiver requirements

This therefore forms the orbital/geometry foundation of the
software-defined satellite communication system.