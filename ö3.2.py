import math
radie = float(input('Radie: '))
if radie > 0:
    area = radie * radie * math.pi
    omkrets = 2 * radie * math.pi

    print(f'Arean är: {area: .2f} och omkretsen är {omkrets: .2f} ')
else:
    print('Radien måste vara större än noll')