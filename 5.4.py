t = input('Text: ')
finns = False

for i in range(0, len(t)):
    if t[i] == ' ' or t[i] == '\t':
        finns = True
        index = i
        print('tomt tecken')
        print(i)
        print(index)
    
if finns == True:
    print(f'Det finns vita tecken, den sista ligger på {index + 1}')
else:
    print('Det finns inga vita tecken')