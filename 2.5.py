import math
x1, y1, x2, y2 = float(input('x1: ')), float(input('y1: ')), float(input('x2: ')), float(input('y2: '))
d = math.sqrt((x1-x2)**2 + (y1-y2)**2)
print(d)