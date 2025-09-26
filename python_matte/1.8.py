prev_x = 1
x = (1 + (2/1))/2
n = 2
while abs(x - prev_x) >= 10**(-10):
    prev_x = x
    x = (x + (2/x))/2
    n += 1
print(n)


