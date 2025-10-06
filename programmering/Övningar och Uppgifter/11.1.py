fil = 'personer.txt'
namn = ' '
with (open(fil, 'a') as f1):
    while namn != '':
        namn = input('Namn: ')
        f1.write(f'{namn}\n')
f1.close()