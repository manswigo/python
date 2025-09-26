import math
import matplotlib.pyplot as plt
x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
y= [0]

for xbar in range(1, 11):
    ybar = 0 
    for k in range(1, 101):
        ybar += (math.sin(k**2*math.pi*xbar)/(k**2*math.pi))
    y.append(ybar)

print('x är lika med ',x)
print('y är lika med ',y)
fig, ax = plt.subplots()            #skapa figur som innehåller en axes
ax.plot(x, y) 
plt.show()