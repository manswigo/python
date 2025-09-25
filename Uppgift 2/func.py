#Måns Persson 05-12-24 Lucas Ödmar 05-07-03
#Hjälpfunktioner till programmet. För att skriva ut tabellen samt skapa x-labels



import math

def tabell(x, z):
    #Skapar variabler
    år = []
    vikt = []
    te_sum = 0

    for i in range(0, len(x)):
        te_sum += z[i]    #Summan av alla års värden
        if x[i] % 5 == 0 or i == 0 or i == len(x)-1:    #Sparar dom åren som ska skrivas ut
            år.append(x[i])
            vikt.append(te_sum)
    längsta = str(math.floor(max(vikt))) + '.xx'    #Beräknar antalet tecken i det längsta talet efter avrundning

    print(f'Ackumulerad tekonsumtion\n[kg/person sedan {x[0]}]\n===========================') #Skriver titel baserat på första året med data
    for i in range(0, len(år)):    #Går igenom dom åren som ska visas
        formaterad = str(f'{vikt[i]: .2f}').strip()    #Avrundar talet till två decimaler även om sista är 0
        print(f'{år[i]}    {formaterad.rjust(len(längsta))}')    #Skriver ut år samt summan för det året justerat så att dom längsta talen 
                                                                         #hamnar 3 blanksteg från året och allt annat i linje till höger
    print('===========================')


#Funktion för att bestämma vilka år som visas under x-axeln
def xlabels(x):

    xlabels = []    #Skapar listan för åren
    div = 5     #Börjar med att skriva vart femte år
    while len(x) // div > 8:    #Ökar hoppet mellan åren tills det är max 8 år som visas
        div += 5

    first = x[0]    #Bestämmer det första året
    while first % div != 0:    #Sätter första året till ett tiotal
        first -= 1
    xlabels.append(first)

    for i in range(1, len(x)):    #Går igenom listan med år
        if x[i] % div == 0:    #Väljer åren enligt det tidigare bestämda hoppet
            xlabels.append(x[i])
  
    return(xlabels)    #Returnerar listan