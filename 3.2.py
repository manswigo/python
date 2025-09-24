bilj = float(input('Enkelbiljett: '))
års = float(input('Årskort: '))
bes = float(input('Hur många besök?'))

if års < bes * bilj:
    print('Årskort är värt')
else:
    print('Enkelviljett är värt')
