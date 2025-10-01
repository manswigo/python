from scipy import optimize
import numpy as np
def f(x):
    return(x**2 - 5*x - 1)
sol = optimize.root(f, 4)
print(sol.x)

def g(x_in):
    x = x_in[0]
    y = x_in[1]
    return([x*y - 2*y -1, 5*y + 1 - x])
sol = optimize.root(g, [1, 1])
print(sol.x[0], sol.x[1])

p = [1, -5, -1]
print(np.roots(p))