import math
lam = (math.log(2)/5730)*-1
s = float(input('Hur många år? '))


exp=lam*s


n = 100*math.exp(exp)

print(f'{n: .5f} procent')