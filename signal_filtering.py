import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
from scipy.fftpack import fft

fs, data = wavfile.read("chill_guitar.wav")
t = np.linspace(0, 25, 893664)
xn = data
k = np.arange(len(xn))
T = len(xn)/fs  # where fs is the sampling frequency
frqLabel = 1/T

b = [(elements/2**8.)*2-1 for elements in xn] # this is 8-bit track, b is now normalized on [-1,1)
c = fft(xn) # calculate fourier transform (complex numbers list)
d = len(c)/2  # you only need half of the fft list (real signal symmetry)

plt.figure(1)
plt.plot(abs(c),'r')
plt.show()

plt.figure(2)
plt.plot(b, 'b')
plt.show()