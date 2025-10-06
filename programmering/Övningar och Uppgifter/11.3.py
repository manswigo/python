mest = 0
current = ''
namnen = []
minuterna = []
with (open('tid.txt', 'r') as f1):
    for rad in f1:
        ord = rad.split()
        for i in range(0, 2):
            namnen.append(ord[i])
        for i in range(2, len(ord)):
            minuterna.append(int(ord[i]))
        if sum(minuterna) > mest:
            mest = sum(minuterna)
            current = ' '.join(namnen)
            current += str(sum(minuterna))
        
f1.close()
print(current)
        