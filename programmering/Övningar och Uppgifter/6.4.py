s = input('Siffror: ')

list = [int(x) for x in s.split()]
print(list)
list.sort()

if len(list) % 2 != 0:
    median = list[(len(list)//2)]
else:
    median = (list[(len(list)//2)]+list[(len(list)//2)-1])/2
print(median)