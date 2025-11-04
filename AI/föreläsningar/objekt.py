#listor är ett objekt i python

class Elevator:
    def __init__(self):
        self.current_floor = 2
        self.direction = 1 

    def move(self):
        self.current_floor += self.direction



e = Elevator()
print(e.direction)
print(e.current_floor)

e.move()
e.move()
print(e.current_floor)







#gambling break
'''import random
p =  1000

while p > 0:
    r = random.randrange(1, 6)
    i = float(input('money'))
    g = int(input('Guess'))
    if g == r: 
        p += i*5
        print('rätt')
        print(p)
    else: 
        p -= i
        print('fel')
        print(p)
'''