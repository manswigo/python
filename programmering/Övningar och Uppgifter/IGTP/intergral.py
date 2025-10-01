from scipy import integrate
import numpy as np
def f(x):
    return 1/(1+x**2)
inte = integrate.quad(f, 0, 1)
print(4*inte[0])