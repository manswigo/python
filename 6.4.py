list = [342, 562346, 7, 6, -2, -2, 1]
for n in range(0, len(list)):
    
    if list[n] == 0:
        list.pop(n)

print(list)