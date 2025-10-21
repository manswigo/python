# Lösningsförslag Uppgift 4 240827 TME136

import numpy as np

# a)
# linjärt ekvationssystem - skriv på matrisform
A = np.matrix([[1, 1, -1], [3, 4, -2], [-2, 1, 3]], float)
b = np.matrix([[1], [2], [0]], float)
x = np.linalg.solve(A, b)
print('a) Lösningen är:')
variables = list('xyz')
for i in range(len(variables)):
    print(f'{variables[i]} = {x.item(i):.2f}')

# b)
mening = input('b) Skriv ett ord: ')
mening = mening.lower()

# c)
vokaler = 'aouåeiyäö'
index_vokaler = [i for i in range(len(mening)) if mening[i] in vokaler]
ny_mening = []
for i in range(len(mening)):
    if i in index_vokaler:
        if i >= 10:
            ny_mening.append(f'{i % 10}')
        else:
            ny_mening.append(f'{i}')
    else:
        ny_mening.append(mening[i])
ny_mening = ''.join(ny_mening)

# d)
for i, bokstav in enumerate(ny_mening):
    print(f'{i} - {bokstav}')