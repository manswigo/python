import math
s = input('Talen: ')
list = [int(x) for x in s.split()]
medel = sum(list)/len(list)
sum = 0
for x in list:
    sum += (x-medel)**2
avvikelse = math.sqrt((1/len(list))*sum)
print(avvikelse)