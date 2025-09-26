n = 2
counter = 0
while counter < 999:
    for k in range(2, n):
        if k == n - 1:
            print(n)
            counter += 1
        if n % k == 0:
            break
    n += 1