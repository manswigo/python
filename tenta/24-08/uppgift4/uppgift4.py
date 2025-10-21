from scipy import optimize

s = input('Skriv ett ord: ').lower()
l = list(s)
vokal = 'aouåeiyäö'
for i in range(len(l)):
    if l[i] in vokal:
        l[i] = str(i)[-1]

s = ''.join(str(i) for i in l)

for i in range(len(s)):
    print(f'{i} - {s[i]}')




def f(x_in):
    x = x_in[0]
    y = x_in[1]
    z = x_in[2]
    return([x+y-z-1, 3*x+4*y-2*z-2, -2*x+y+3*z])
sol = optimize.root(f, [-10, -10, -10])
print('x =', sol.x[0], 'y=', sol.x[1], 'z=', sol.x[2])