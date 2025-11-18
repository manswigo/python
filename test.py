from scipy import integrate
import numpy as np

def f(x):
    return np.sqrt(1 + x)

Q = integrate.quad(f, 1, 2)

print(Q)

print(2*np.sqrt(3) - ((4*np.sqrt(2))/3))