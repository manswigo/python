# Lösningsförslag Uppgift 3 240827 TME136

import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return x**7 - 3*x**2 + 4

def f_derivative(x):
    return 7*x**6 - 6*x

def newton_raphson(f, f_derivative, x0, tol):
    x = x0
    j = 0
    while abs(f(x)) > tol:
        x = x - f(x)/f_derivative(x)
        j += 1
        print(f'Iteration {j:2d}: x = {x:+f}')
    return (x, j)

newton_raphson(f, f_derivative, 3, 1e-3)