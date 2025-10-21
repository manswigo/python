import math
import matplotlib.pyplot as plt
import numpy as np
def sin_taylor(x, i):
    tecken = 1 
    while x >= 2*math.pi: #Flyttar argumentet till 0 <= x <= 2pi
       x -= 2*math.pi #Genom att backa ett helt varv i taget
    
    if x > math.pi: #Flyttar argumentet till 0 <= x <= pi
        tecken = -1 #Ändrar då tecknet
        x = math.pi*2 - x #Flyttar x över x-axeln
    
    if x > math.pi/2: #Flyttar argumentet till 0 <= x <= pi/2
        x = math.pi-x #Enligt sin(pi-x) = sin(x)
    sin_sum = 0 #Sätter taylorpolynomets summa till 0
    for n in range(i): #Loopar det valda antalet varv
        sin_sum += ((((-1)**n)/(math.factorial(2*n+1)))*(x**(2*n+1))) #Maclaurinpolynom för sinus
    return(sin_sum*tecken) #Returnerar polynomets summa med rätt tecken

def cos_taylor(x, i):
    tecken = 1
    while x >= 2*math.pi: #Flyttar till 0 <= x <= 2pi på samma sätt
       x -= 2*math.pi
    if x > math.pi: #Flyttar argumentet till 0 <= x <= pi men ändrar ej tecken då cossinus byter tecken över y_axeln
        x = 2*math.pi - x
    if x > math.pi/2: #Flyttar argumentet till 0 <= x <= pi/2 
        tecken = -1 #Ändrar tecken
        x = math.pi-x
    

    cos_sum = 0
    for n in range(i):
        cos_sum += (((-1)**n)/(math.factorial(2*n)))*(x**(2*n))
    return(tecken*cos_sum)


print(cos_taylor(-1*math.pi/4, 100))
print(sin_taylor(-1*math.pi/4, 100))




x = np.linspace(-10, 10, 1000)
y = []
y1 = []
n = 100
for i in x:
    y.append(cos_taylor(i, n))
    y1.append(sin_taylor(i, n))
fig, ax = plt.subplots()
ax.set_xlim(-10, 10)
ax.set_xticks([-3*math.pi, -2*math.pi, -1*math.pi, 0,  math.pi, 2*math.pi, 3*math.pi])
ax.plot(x, y, label='cos')
ax.plot(x, y1, label='sin')
ax.legend(loc='lower center')




plt.show()






