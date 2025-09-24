def fyll(a, b, c, d):
    for i in range(c, d+1):
        a.pop(i)
        a.insert(i, b)
    return(a)

arr = [1, 2, 3, 4, 5]

print(fyll(arr, 6, 2, 4))
