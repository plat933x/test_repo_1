import numpy as np
import matplotlib.pyplot as plt

time = np.linspace(0, 10000, 1)
x = np.sin(time)

plt.figure(1)
plt.plot(np.sin(time),time)
plt.show()
