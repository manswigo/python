import matplotlib.pyplot as plt
import numpy as np

fig, axs = plt.subplots(2,2)
fig.tight_layout(pad= 2.5)

ax = axs[0, 0]
x = np.linspace(-4, 4, 500)
y = np.sin(np.exp(x))
ax.plot(x, y)
ax.set_title('a')
ax.set_xlabel('x')
ax.set_ylabel('y')

ax = axs[0, 1]
x = np.linspace(0.1, 10, 500)
y = np.sin(np.log(x))
ax.plot(x, y)
ax.set_title('b')
ax.set_xlabel('x')
ax.set_ylabel('y')

ax = axs[1, 0]
x = np.linspace(-10, 10, 500)
y = np.exp(np.sin(x))
ax.plot(x, y)
ax.set_title('a')
ax.set_xlabel('x')
ax.set_ylabel('y')

ax = axs[1, 1]
x = np.linspace(-10, 10, 500)
y = np.log(np.sin(x))
ax.plot(x, y)
ax.set_title('a')
ax.set_xlabel('x')
ax.set_ylabel('y')



plt.show()
