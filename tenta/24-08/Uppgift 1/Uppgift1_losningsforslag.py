# Lösningsförslag Uppgift 1 240827 TME136

import matplotlib.pyplot as plt
import numpy as np
from scipy import optimize
from scipy import integrate

# definiera funktionerna
def g(x):
    return (7 + np.cos(x))*x**2

def f(x):
    return 500.0 - x

# intervallet är x = [5/2*np.pi, n.psqrt(97)]
x_vector = np.linspace(5/2*np.pi, np.sqrt(97))

# fontstorleken ska vara 14
plt.rc('axes', labelsize=14)
plt.rc('legend', fontsize=14)
plt.rc('xtick', labelsize=14)
plt.rc('ytick', labelsize=14)

# skapa figur enligt specifikationerna
fig, ax1 = plt.subplots()
ax1.plot(x_vector, f(x_vector), '-k', linewidth=2, label='f(x)')
ax1.plot(x_vector, g(x_vector), ':b', linewidth=2, label='g(x)')

# namnge axlar
ax1.set_xlabel('x')
ax1.set_ylabel('f(x), g(x)')

# hitta och plotta skärningspunkten
def h(x):
    return f(x) - g(x)
sol = optimize.root(h, 9)
x_intersect = sol.x[0]
ax1.plot(x_intersect, f(x_intersect), '^r', markeredgewidth=2, markersize=10, markerfacecolor='k')

# lägg till legend i nedre högra hörnet
ax1.legend(loc='lower right')

# lägg till grid
plt.grid()

# beräkna integralen B och skriv ut titel med värde
Q = integrate.quad(h, 5*np.pi/2, x_intersect)
ax1.text(8, 470, f'B = {Q[0]:.1f}', fontsize=14) # OK att hårdkoda position här (men ej värde på B)

# visa upp figuren i ett figurfönster
plt.tight_layout()
# plt.savefig('fig1.pdf') # behövs ej i tentauppgiften men skapar exempelfiguren som visas
plt.show()