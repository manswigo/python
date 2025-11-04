import numpy as np
def sqrtHeron(S, xold, tol):
    x = 0.5*(xold + S/xold)
    i = 0
    while abs(x - xold)/xold > tol:
        xold = x
        x = 0.5*(xold + S/xold)
        i += 1
    return(x, i+1, abs(x - xold)/xold)

approximation_save = []
n_save = []
for i in range(1, 51):
    temp = sqrtHeron(i, i, 10**-2)
    approximation_save.append(temp[0])
    n_save.append(temp[1])
for i in range(1, 51):
    if i % 10 == 0 or i == 1:
        print(f'{str(i).rjust(2)}    {n_save[i-1]}    {np.sqrt(i): .5f}    {approximation_save[i-1]: .5f}')