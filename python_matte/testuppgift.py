from scipy.differentiate import derivative
import numpy as np
x = 1
a = x**2

der = derivative(a, x)
print(der)