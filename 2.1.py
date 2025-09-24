idag = float(input('mätarställning idag: '))
då = float(input('då? '))
bensin = float(input('bensinförbrukning? '))

sträcka = idag-då
snitt = sträcka/bensin

print(f'du har kört {sträcka: .0f} snittförbrukning är {snitt: .2f} l/mil')
             