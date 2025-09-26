x = 0
for n in range(0, 10**6+1):
    term = ((-1)**n)/(2*n+1)
    x += 4*term
    print(x)
