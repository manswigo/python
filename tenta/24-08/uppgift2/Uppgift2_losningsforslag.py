# Lösningsförslag Uppgift 2 240827 TME136

import numpy as np
import matplotlib.pyplot as plt

# a) läs in data
with open('sommar_os.csv') as f:
    data = f.readlines()

contents = []
for row in data:
    contents.append(row.strip('\n').split(';'))

contents.pop(0)

# b) hitta landet med flest medaljer per deltagare
new_value = []
for row in contents:
    if float(row[1]) == 0:
        new_value.append(-np.inf)
    else:
        new_value.append(float(row[5])/float(row[1]))

print(f'Året som söks är {contents[new_value.index(max(new_value))][0][0:4]}')

# c) figur
antal_deltagare = [float(contents[i][1]) for i in range(len(contents))]
antal_medaljer = [float(contents[i][5]) for i in range(len(contents))]

fig, ax = plt.subplots()
ax.plot(antal_deltagare, antal_medaljer, 'o')
ax.set_xlabel('Antal deltagare')
ax.set_ylabel('Antal medaljer')
ax.set_title('Sommar-OS')
# plt.savefig('Sommar-OS.png') # behövs ej i tentauppgiften men skapar exempelfiguren som visas
plt.show()