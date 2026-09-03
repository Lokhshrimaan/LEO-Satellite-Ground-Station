# SDR Fundamentals

## 1. Software Defined Radio

SDR stands for Software Defined Radio.

In a conventional radio, much of the signal processing is performed using dedicated
analog and digital hardware. In an SDR, the hardware performs the essential RF
reception, frequency conversion and analog-to-digital conversion, while much of
the remaining signal processing is performed in software.

## 2. SDR Receive Chain

The conceptual receive chain is:

Satellite
→ Antenna
→ RF Front-End
→ Frequency Conversion
→ ADC
→ IQ Samples
→ Digital Signal Processing
→ Demodulation
→ Protocol/Data Decoding

## 3. RF

RF means Radio Frequency.

A satellite carrier may be represented as:

fc = 145.8 MHz

where fc is the carrier frequency.

## 4. Local Oscillator and Frequency Conversion

A receiver can use a Local Oscillator (LO) to translate an incoming RF signal to
a lower intermediate or baseband frequency.

Conceptually:

fIF = |fRF - fLO|

where:

- fRF = incoming radio frequency
- fLO = local oscillator frequency
- fIF = intermediate frequency

The exact frequency-conversion architecture depends on the SDR design.

## 5. ADC

ADC means Analog-to-Digital Converter.

It converts a continuous-time analog signal x(t) into discrete digital samples x[n].

Before ADC:

x(t)

After ADC:

x[n]

where:

- t = continuous time
- n = discrete sample index

## 6. IQ Representation

SDRs commonly represent complex baseband signals as:

x[n] = I[n] + jQ[n]

where:

- I = In-phase component
- Q = Quadrature component
- j = sqrt(-1)

IQ representation preserves amplitude and phase information and is therefore
suitable for digital signal processing and demodulation.

## 7. Complex Baseband

The SDR does not necessarily provide the computer with samples of the original
145.8 MHz RF carrier.

Instead, the SDR can tune to the desired RF region and translate the signal to
a lower-frequency complex baseband representation.

Therefore, a simulation can model a 145.8 MHz RF communication system using a
much lower baseband sampling frequency.

For example:

Fs = 1 MHz

can be used in a complex-baseband simulation even when:

fc = 145.8 MHz

because Fs represents the baseband sampling process rather than direct sampling
of the original RF carrier.

## 8. Why SDRs Are Useful

An SDR moves a large portion of the radio signal-processing chain into software.

The same hardware can therefore support different processing systems through
software changes, depending on the SDR's frequency range, bandwidth, ADC and
other hardware limitations.

## 9. Importance to the Satellite Ground Station

The final ground station will transform a physical satellite RF signal into
digital IQ samples and then process those samples in software.

The major software stages will include:

- filtering
- frequency correction
- Doppler correction
- synchronization
- demodulation
- frame/protocol decoding
- data extraction

This establishes the connection between the theoretical communication models
developed earlier and the eventual real SDR receiver.

## 10. Fedora Environment

The SDR development environment is being established on Fedora Linux.

Verified components:

- Fedora 41
- Python 3.13.9
- GNU Radio 3.10.11.0
- GNU Radio Python module successfully imported

No SDR hardware is required for this stage.
