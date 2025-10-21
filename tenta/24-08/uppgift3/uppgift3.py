def newton_raphson(f, fprim, x, tol):
    i = 0
    while abs(f(x)) > tol:
        print(i)
        x = x - f(x)/fprim(x)
        print(x)
        i += 1
    return(x, i)

def f(x):
    return(x**7 - 3*x**2     + 4)
def fprim(x):
    return(7*x**6 - 6*x)
print(newton_raphson(f, fprim, 3, 10**-3))