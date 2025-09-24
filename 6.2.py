s = input('Talen: ')
l = s.split()
tal = [float(n) for n in l]
counter = 0
for n in tal:
    if n < 0:
        counter += 1
print(counter)
