import math
a = float(input('a: '))
b = float(input('b: '))
v = math.radians(float(input('v: ')))

c = math.sqrt((a**2)+(b**2)-(2*a*b*math.cos(v)))



if abs(a-b)< 0.001 and abs(a-c) < 0.001 and abs(b-c) < 0.001:
    print('Liksidig')
elif abs(a-b) < 0.001 or abs(a-c) < 0.001 or abs(b-c) < 0.001:
    print('Likbent')
else: 
    print('oliksidig')
