namn = []
pris = []
while True:
    s = input('Namn o pris: ')
    if s == '':
        break
    a = s.partition(' ')
    namn.append(a[0])
    pris.append(int(a[-1]))
   
m = min(pris)
k = pris.index(m)
min_namn = namn[k]
print(min_namn, m)