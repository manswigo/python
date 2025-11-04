import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv('expdata.csv', sep=',', decimal='.')
x = list(df['x'])
y1 = list(df['teoretisk'])
y2 = list(df['riktig'])
print(y1)
print(y2)
fig, ax = plt.subplots()
ax.plot(x, y1, 'r', label='Teoretisk')
ax.scatter(x, y2, color='blue', label='Mätt')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.legend()



bra = []
xbra = []
dålig = []
xdålig = []
for i in range(len(x)):
    if abs(y2[i] - y1[i]) > 2:
        dålig.append(y2[i])
        xdålig.append(x[i])

    else:
        bra.append(y2[i])
        xbra.append(x[i])


fig1, ax1 = plt.subplots()
ax1.plot(x, y1, 'k', label='Teoretisk')
ax1.scatter(xbra, bra, color='green', marker='s', label='Mätt(Godkända)')
ax1.scatter(xdålig, dålig, color='red', marker='s', label='Mätt(Ej godkända)')
ax1.legend()
plt.show()
