mest = 0
current = ''
namnen = ''
minuterna = 0
with (open('tid.txt', 'r') as f1):
    for rad in f1:
        ord = rad.split()
        
        namnen = ''
        minuterna = 0
        for i in range(0, len(ord)):
            if ord[i].isdecimal():
                minuterna += int(ord[i])
            else:
                namnen += (ord[i]+' ')
        if minuterna > mest:
            mest = minuterna
            current = namnen
   
        
f1.close()
print(f'{current}{mest}')
        