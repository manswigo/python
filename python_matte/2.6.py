def poly(a, x):
    p = 0
    exp = 0
    for n in range(0, len(a)):
        
        p += a[n]*(x**exp)
        exp += 1
    return(p)
a = [4, 3, 7, 2, 0, 3]
print(poly(a, 5))
    
