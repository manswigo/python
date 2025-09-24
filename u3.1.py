minuter = float(input('Minuter: '))
pris = float(input('Pris: '))
tot = minuter*pris
if minuter >= 300:
    tot *= 0.9
print (f'Total priset är {tot: .2f} kr')

