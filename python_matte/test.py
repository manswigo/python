import math
import matplotlib.pyplot as plt
import numpy as np
def sin_taylor(x):
    tecken = 1
    while x >= 2*math.pi:
       x -= 2*math.pi
    
    if x > math.pi:
        tecken = -1
        x = math.pi*2 - x
    
    if x > math.pi/2:
        x = math.pi-x
    sin_sum = 0
    for n in range(201):
        sin_sum += ((((-1)**n)/(math.factorial(2*n+1)))*(x**(2*n+1)))  
    return(sin_sum*tecken)

def cos_taylor(x):
    tecken = 1
    while x >= 2*math.pi:
       x -= 2*math.pi
    if x > math.pi:
        x = 2*math.pi - x
    if x > math.pi/2:
        tecken = -1
        x = math.pi-x
    

    cos_sum = 0
    for n in range(201):
        cos_sum += (((-1)**n)/(math.factorial(2*n)))*(x**(2*n))
    return(tecken*cos_sum)


x = np.linspace(-10, 10, 1000)
y = []
y1 = []
y2 = 0
for i in x:
    y.append(abs(cos_taylor(i)-np.cos(i)))
    y1.append(abs(sin_taylor(i)-np.sin(i)))
fig, ax = plt.subplots()
ax.set_xticks([-3*math.pi, -2*math.pi, -1*math.pi, 0,  math.pi, 2*math.pi, 3*math.pi])
ax.plot(x, y)
ax.plot(x, y1)
plt.hlines(10**-15, -10, 10)


plt.show()






