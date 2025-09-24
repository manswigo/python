n = int(input('Antal: '))
l = [2]
for x in range(1, n):
    l += [3*l[-1]]
print(l)
