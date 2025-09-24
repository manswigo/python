l = float(input('Längd i mm: '))
b = float(input(' Bredd i mm: '))
t = float(input('Tjocklek i mm: '))

if l <= 600 and t <= 100 and \
b+t+l <= 900 and l >= 140 and b >= 90:
    print('Godkänd')
else:
    print('Ej godkänd')