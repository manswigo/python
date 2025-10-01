import pandas as pd
# Klossdata
L = [10, 10, 10] # cm
b = [10, 10, 10] # cm
h = [20, 20, 10] # cm
densitet = [400, 400, 400] # kg/m3
form = ['rektangulär', 'prismatisk', 'kvadratisk']
klossdata = pd.DataFrame([L, b, h, densitet, form],
index=['längd','bredd','höjd','densitet','form'],
columns=['kloss 1','kloss 2','kloss 3'])

print(klossdata['kloss 2']['höjd'])