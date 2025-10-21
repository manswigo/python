import matplotlib.pyplot as plt
from scipy import optimize
import numpy as np
from scipy import integrate

def f(x):
    return(500-x)
def g(x):
    return(x**2*(7+np.cos(x)))

def h(x):
    return(f(x)-g(x))
sol = optimize.root(h, 8)
x1 = sol.x[0]
y1 = f(x1)

b = integrate.quad(h, 5*np.pi/2, x1)



x = np.linspace(5*np.pi/2, np.sqrt(97), 2000)
fig, ax = plt.subplots()
ax.plot(x, f(x), 'k', linewidth=2, label='f(x)')
ax.plot(x, g(x), 'b', linewidth=2, ls='dotted', label='g(x)')
ax.set_xlabel('x', fontsize=14)
ax.plot(x1, y1, '^', markerfacecolor='black', markersize=10, markeredgewidth=2, markeredgecolor='red')
ax.set_ylabel('f(x), g(x)', fontsize=14)
ax.legend(loc='lower right')
ax.text(x1, 470, f'b = {b[0]: .1f}', fontsize=14)
ax.grid()
plt.yticks(fontsize=14)
plt.xticks(fontsize=14)
plt.show()
