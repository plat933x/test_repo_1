import matplotlib.pyplot as plt
import numpy as np


window = np.blackman(500)
plt.figure(1)
plt.plot(window)
plt.show()

A = np.fft.fft(window, 2048)/25.5
magnitude = np.abs(np.fft.fftshift(A))
freq = np.linspace(-0.5, 0.5, len(A))

with np.errstate(divide='ignore', invalid='ignore'):
    response = 20*np.log10(magnitude)

response = np.clip(response, -200, 200)
plt.figure(2)
plt.plot(freq, response)
plt.axis('tight')
plt.show()
print(len(A))