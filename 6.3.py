list = []
import random
for n in range(1, 101):
    list.append(random.randint(1, 1000))
list.sort()
print(list[0], list[-1])