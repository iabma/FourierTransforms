import matplotlib.pyplot as plt
import numpy as np
from scipy import integrate
import wave
import sys
import math

# SETUP
spf = wave.open("the_pipes_mono.wav", "r")
signal = spf.readframes(-1)
signal = np.fromstring(signal, "Int16")
fs = spf.getframerate() # sample rate
#np.savetxt('test.txt', signal, delimiter=',')

def com_at_frequency(start_time, frequency, real):
    rng = 0.5 # number of seconds forward to look at

    # real and imaginary components of fourier transform
    def real_fourier_component(t):
        return signal[int(t * fs)] * math.cos(-2 * math.pi * frequency * t)
    def imaginary_fourier_component(t):
        return signal[int(t * fs)] * math.sin(-2 * math.pi * frequency * t)
    
    real_component, real_error = integrate.quad(real_fourier_component, start_time, start_time + rng)
    imaginary_component, imaginary_error = integrate.quad(imaginary_fourier_component, start_time, start_time + rng)
    return real_component if real else imaginary_component

real_frequency_data = []
imaginary_frequency_data = []
for hz in range(800):
    print(str(hz) + " Hz")
    real_frequency_data.append(com_at_frequency(8, hz, True)) # real component of fourier transform at frequency
    imaginary_frequency_data.append(com_at_frequency(8, hz, False)) # real component of fourier transform at frequency
np.savetxt('test.txt', real_frequency_data, delimiter=',')

# PLOT DATA
frequency_chart_spacing = np.linspace(0, 800, num=800)
Time = np.linspace(0, len(signal) / fs, num=len(signal))
plt.figure(1)
plt.title("Sound Waves")
plt.plot(Time, signal)
plt.xlim(8,8.5)
plt.figure(2)
plt.title("Frequency")
plt.plot(frequency_chart_spacing, real_frequency_data)
plt.plot(frequency_chart_spacing, imaginary_frequency_data)
plt.show()