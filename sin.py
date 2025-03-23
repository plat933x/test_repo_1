import numpy as np
import matplotlib.pyplot as plt

time = np.linspace(0, 100, 1000)
x = np.sin(time)

plt.figure(1)
plt.plot(time, np.sin(time))
plt.show()