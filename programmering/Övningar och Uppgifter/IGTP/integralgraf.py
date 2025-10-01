from scipy import integrate
import matplotlib.pyplot as plt
import numpy as np
def f(x):
    return(1/(1+x**2))

I, error = integrate.quad(f, 0, 1)
pi_approx = 4*I

print(f"{'Beräknat \u03C0':10s} ≈ {pi_approx:.6f}")
print(f"{'Numpy \u03C0':10s} = {np.pi:.6f}")
print(f"{'Skillnad':10s} = {abs(pi_approx - np.pi):.6e}")
# Plotta funktionen och markera arean
x = np.linspace(0, 1, 400)
y = f(x)
plt.plot(x, y, label=r"$f(x) = \frac{1}{1+x^2}$")
plt.fill_between(x, y, alpha=0.3, color="orange", label="Integrerat område")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.title("\u03C0-maskinen")
plt.legend()
plt.show()