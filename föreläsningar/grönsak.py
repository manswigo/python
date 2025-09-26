databas = [['gurka', 31.50],
           ['tomat', 43.99],
           ['sallad', 26.00],
           ['paprika', 58.45]]
print('Ange vad du vil ha')
print('grönsak antal kg')
print('avsluta med tom rad')
print('skriv finns om du vill veta vad som finns')

inköp = []
vill_ha = True
while (vill_ha != []):
    vill_ha = input('>').split()
    if vill_ha == ['finns']:
        for i in databas:
            print(f'{i[0]}: {i[1]} kr/kg')
    elif(vill_ha != []):
        grönsak = vill_ha[0]
        kg = float(vill_ha[1])
        inköp.append([grönsak, kg])

for i in range(0, len(inköp)):
    grönsak = inköp[i][0]
    kg = inköp[i][1]
    pris = 0
    for sort in databas:
        if (sort[0] == grönsak):
            pris = kg*sort[1]
    inköp[i].append(pris)

    bara_priser = [info[1] for info in inköp]
    tot_pris = sum( bara_priser)
    print(f'du har handlat för {tot_pris: .2f} kr')
    for köp in inköp:
        print(f'{köp[0]:8s} {köp[1]:8f} {köp[2]:8f}')