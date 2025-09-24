import math
pop = 26000
år = int(input('År: '))
årdiff = år - 2025
for n in range(1, årdiff):
    född = 0.007*pop
    död = 0.006*pop
    pop = pop + född - död - 25
print(math.trunc(pop))