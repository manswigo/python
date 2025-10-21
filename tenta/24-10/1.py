import matplotlib.pyplot as plt
import numpy as np
from scipy import optimize
from scipy import integrate


def f(x):
   return(2.1 + x**2 - np.cos(x))
def g(x):
   return(np.exp(x))
def h(x):
   return((125/17) - x**3)
x = np.linspace(0, 2, 2000)

def point(x):
   return(f(x)-(g(x)))
def point1(x):
   return(g(x)-h(x))
sol = optimize.root(point, 0)
x1= sol.x[0]
y1 = f(x1)
sol = optimize.root(point1, 0)
x2 = sol.x[0]
y2 = g(x2) 

q = integrate.quad(g, x1, x2)     

fig, ax = plt.subplots()
ax.plot(x, f(x), 'g', linewidth= 2, label= 'f(x)')
ax.plot(x, g(x), 'b', linewidth= 2, label= 'g(x)')
ax.plot(x, h(x), 'r', linewidth= 2, label= 'h(x)')
ax.legend(loc='lower center')
ax.set_xlabel('X', fontsize=18)
ax.set_ylabel('f(x), g(x), h(x)', fontsize=18)
plt.plot(x1, y1, 'k', marker='s')
plt.plot(x2, y2, 'k', marker='s')
ax.set_title(f'Integralen A = {q[0]: .2f}')
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)

plt.show()
