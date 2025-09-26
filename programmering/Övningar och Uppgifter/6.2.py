s = input('Temps: ')
temps = [float(x) for x in s.split()]
snitt = sum(temps)/len(temps)

for i in range(0, len(temps)):
    if temps[i] > snitt:
        print(f'Station {i} mätte {temps[i]: .2f} celsius')
