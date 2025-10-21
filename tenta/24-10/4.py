from scipy import optimize
def f(x_in):
    x = x_in[0]
    y = x_in[1]
    z = x_in[2]
    return([x-2*y+3*z-9, 
            -1*x+3*y-z+6, 
            2*x-5*y+5*z-17])
sol = optimize.root(f, [0, 0, 0])
print(f'x = {sol.x[0]}, y = {sol.x[1]}, z = {sol.x[2]}')