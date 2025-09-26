import matplotlib.pyplot as plt

x = [1, 2, 3, 4]
y = [1, 4, 2, 3]
z = [4, 2, 3, 1]
xlabels = ['Jan', 'Feb', 'Mar', 'Apr']


fig, ax = plt.subplots()            #skapa figur som innehåller en axes
ax.plot(x, y, 'r-', label='första', linewidth = 4)                       #plotta data på en axes
ax.plot(x, z, 'bo:', label='andra', linewidth = 2, markersize = 12)

ax.set_xlabel('x-axel', fontsize = 16)
ax.set_ylabel('y-axel', fontsize = 16)
ax.set_title('Fin Graf')
ax.set_yticks(y)
ax.set_xticks(x)
ax.set_xticklabels(xlabels, rotation = 20)
fig.tight_layout()
plt.grid()
ax.legend()
plt.show()

