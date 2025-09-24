def cirkel(r):
    import math
    return(r*math.pi*r), (r*2*math.pi)
r = float(input('r: '))
a, o = cirkel(r)
print(a, o)
