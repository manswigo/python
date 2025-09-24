
while True:
    h = float(input('Höjd i cm: '))
    if h < 0:
        break
    studs = 0
    while h > 1:
        h *= 0.7
        studs += 1
    print (studs)