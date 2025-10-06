fil = input('Fil: ')
with (open(fil, 'r') as f1):
    komm = 0
    rader = 0
    for rad in f1:
        if rad.find('#') != -1:
            komm += 1
            rader += 1
        else:
            rader += 1
f1.close()
print(100*(komm/rader))