import matplotlib.pyplot as plt
from scipy import optimize
import numpy as np
from scipy import integrate

def f(x):
    return(5 - np.exp(x))
def g(x):
    return((5*(x-0.5)**2) + 3)
x = np.linspace(0, 1, 1000)

def h(x):
    return(f(x) - g(x))
sol = optimize.root(h, 0.1)
x1 = sol.x[0]
y1 = f(x1) 

sol = optimize.root(h, 0.6)
x2 = sol.x[0]
y2 = f(x2)

Q = integrate.quad(f, x1, x2)
print(Q)

p1 = (f(x1)+f(x2))/2
p2 = f(x1)/2

fig, ax = plt.subplots()
ax.plot(x, f(x), 'b', linewidth=2, label='f(x)')
ax.plot(x1, y1, 'x', markerfacecolor='red', markersize=10, markeredgewidth=2, markeredgecolor='red', label='skärningspunter med g(x)')
ax.plot(x2, y2, 'x', markerfacecolor='red', markersize=10, markeredgewidth=2, markeredgecolor='red')
ax.vlines(x1, 0, f(x1), 'k', linestyles='dotted')
ax.vlines(x2, 0, f(x2), 'k', linestyles='dotted')
ax.text(0.4, 2, f'A = {Q[0]: .1f}', fontsize=15)
ax.legend(loc='upper right')
ax.set_ylim(0, 5)
ax.set_xlabel('x', fontsize=14)
ax.set_ylabel('f(x)', fontsize=14)
plt.show()