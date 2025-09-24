d = input('Svenskt datum åååå-mm-dd: ')
å = d[2:4]
m = d[5:7]
dag = d[8:]
d2 = f'{m}/{dag}/{å}'
print(d2)