s = input('Siffror: ')
list = [int(x) for x in s.split()]

newlist = []
i = 0
while i <= (len(list)-1):
   
    if list[i] in newlist:
        del list[i]
    else:
        newlist.append(list[i]) 
        i += 1
print(list)
            
