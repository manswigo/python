import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-1*np.pi, np.pi)
y = np.sin(x)

fig, ax = plt.subplots()
ax.plot(x, y)
plt.show()