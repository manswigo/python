import egenfunktion

# filnamn = 'test.txt'
filnamn = 'input.txt'

# läs in från fil
with open(filnamn, 'r') as f:
    data = f.readlines()

# ta ut den relevanta informationen
lyckokarta = []
for rad in data:
    delar = rad.strip('.\n').split()
    if (delar[3] == 'plus'):
        lyckokarta.append([delar[0], int(delar[4]), delar[-1]])
    else:
        lyckokarta.append([delar[0], -int(delar[4]), delar[-1]])

# ta fram alla unika namn
namn = list(set([e[0] for e in lyckokarta]))

# ta fram alla unika kombinationer
# notera att placeringen saknar riktning -- det enda viktiga är vilka grannar man har
kombinationer = egenfunktion.circular_permutations_nodir(namn)

# utvärdera alla kombinationer
kombinationspoäng = []
for kombination in kombinationer:
    summa = 0
    for i, n1 in enumerate(kombination):
        for regel in lyckokarta:
            if (n1 == regel[0]):
                if (i < (len(kombination)-1)):
                    if (kombination[i+1] == regel[2]):
                        summa += regel[1]
                else:
                    if (kombination[0] == regel[2]):
                        summa += regel[1]
                if (i == 0):
                    if (kombination[-1] == regel[2]):
                        summa += regel[1]
                else:
                    if (kombination[i-1] == regel[2]):
                        summa += regel[1]
    kombinationspoäng.append(summa)

# testutskrift av alla kombinationer och poäng, kommenteras bort när klar
# for i, kombination in enumerate(kombinationer):
#     for namn in kombination:
#         print(namn, end=' ')
#     print(f' = {kombinationspoäng[i]}')

# skriv ut optimala placeringen och dess poäng
index_optimal = kombinationspoäng.index(max(kombinationspoäng))

print('Den optimala placeringen är:')
for namn in kombinationer[index_optimal]:
    print(namn, end=' ')
print(f'({kombinationspoäng[index_optimal]} lyckoenheter)')