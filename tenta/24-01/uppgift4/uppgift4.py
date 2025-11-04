from scipy import optimize
def f(x_in):
    x = x_in[0]
    y = x_in[1]
    z = x_in[2]
    return[y + z - 7, x + z - 5, x + y - 8]
sol = optimize.root(f, [0, 0, 0])
print('x=',sol.x[0],' y=',sol.x[1],' z=',sol.x[2])

name = input('Skriv ett namn: ')
name = name.lower()
nameSorted = sorted(name)
nameSorted[0] = (nameSorted[0]).upper()
print(str(nameSorted))