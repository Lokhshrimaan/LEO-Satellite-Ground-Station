# 14. Doppler Estimation and Compensation

## Objective

The objective of this step is to estimate an unknown Doppler frequency shift from a received BPSK signal and use the estimate to compensate the signal before demodulation.

This represents a more realistic receiver because the Doppler shift is not assumed to be known beforehand.

---

## 1. System Configuration

| Parameter | Value |
|---|---:|
| Carrier frequency | 145.8 MHz |
| Number of bits | 1000 |
| Symbol rate | 10 ksym/s |
| Sampling frequency | 1 MHz |
| Samples per symbol | 100 |
| SNR | 15 dB |
| True Doppler | +2500 Hz |

### Sampling Frequency

The sampling frequency was selected as:

\[
F_s = 1\,MHz
\]

This is a simulation parameter for the complex baseband signal and is not the 145.8 MHz RF carrier sampling rate.

The relationship used was:

\[
F_s = R_s \times N_s
\]

where:

- \(R_s\) = symbol rate = 10 ksym/s
- \(N_s\) = samples per symbol = 100

Therefore:

\[
F_s = 10,000 \times 100 = 1,000,000\;samples/s
\]

---

## 2. Samples per Symbol

Samples per symbol indicates how many digital samples are used to represent one transmitted symbol.

In this simulation:

\[
N_s=100
\]

Therefore, every BPSK symbol is represented by 100 samples.

This oversampling provides sufficient time resolution for simulating frequency offset and signal processing.

---

## 3. BPSK Signal with Unknown Doppler

The transmitted BPSK signal was represented as:

\[
s(t)\in\{-1,+1\}
\]

An unknown Doppler shift of:

\[
f_D=2500\;Hz
\]

was introduced.

The received signal can be represented as:

\[
r(t)=s(t)e^{j2\pi f_Dt}
\]

The Doppler shift therefore appears as a continuously changing phase rotation.

---

## 4. Doppler Estimation

The BPSK signal was squared:

\[
r^2(t)=s^2(t)e^{j4\pi f_Dt}
\]

Since:

\[
(+1)^2=(-1)^2=1
\]

the BPSK data modulation is removed.

Thus:

\[
r^2(t)=e^{j4\pi f_Dt}
\]

The phase of the squared signal is:

\[
\phi(t)=4\pi f_Dt
\]

Therefore:

\[
f_D=
\frac{1}{4\pi}
\frac{d\phi}{dt}
\]

The phase was unwrapped and a linear fit was applied to determine the phase slope.

---

## 5. Doppler Compensation

After estimating the Doppler frequency, an opposite frequency rotation was applied:

\[
e^{-j2\pi\hat f_Dt}
\]

The compensated signal becomes approximately:

\[
r(t)e^{-j2\pi\hat f_Dt}
\approx s(t)
\]

when the Doppler estimate is accurate.

---

## 6. Results

| Parameter | Result |
|---|---:|
| True Doppler | +2500.00 Hz |
| Estimated Doppler | +2500.00 Hz |
| Estimation error | 0.00 Hz |
| Bit errors | 0 |
| BER | 0.000000 |

The Doppler estimation was exact for the simulated conditions.

Before compensation, the BPSK constellation was distributed around the origin because the frequency offset continuously rotated the signal phase.

After compensation, the constellation returned to two clusters corresponding to the BPSK symbols.

---

## 7. Interpretation

This step demonstrates an important receiver function:

\[
\boxed{
\text{Received signal}
\rightarrow
\text{Doppler estimation}
\rightarrow
\text{Doppler compensation}
\rightarrow
\text{BPSK demodulation}
}
\]

The receiver does not need to know the Doppler shift in advance. It estimates the frequency offset from the received signal itself.

---

## 8. Key Learning

- Sampling frequency determines the temporal resolution of the digital simulation.
- Samples per symbol determine how finely each symbol is represented.
- Doppler appears as a frequency-dependent phase rotation.
- Squaring BPSK removes the ±1 data modulation.
- The slope of the resulting phase provides the Doppler estimate.
- Accurate Doppler compensation is essential for reliable coherent demodulation.
- The simulation achieved zero BER after compensation.

## Conclusion

Step 16 successfully demonstrated automatic Doppler estimation and compensation for a BPSK communication link. The estimated Doppler matched the true 2500 Hz offset and resulted in zero bit errors.