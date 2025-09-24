min = float(input('Minuter: '))

if min <= 33:
    abb = 'Kontant'
elif min >=66:
    abb = 'Plus'
else:
    abb = 'Normal'

print(f'Du borde skaffa {abb}')