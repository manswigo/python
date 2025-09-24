import math

def tabell(x, z):
    #Skapar variabler
    år = []
    vikt = []
    te_sum = 0

    for i in range(0, len(x)):
        te_sum += z[i]  #Summan av alla års värden
        if x[i] % 5 == 0 or i == 0 or i == len(x)-1:  #Sparar dom åren som ska skrivas ut
            år.append(x[i])
            vikt.append(te_sum)
    längsta = str(math.floor(max(vikt))) + '.xx'    #Beräknar antalet tecken i det längsta talet efter avrundning

    print(f'Ackumulerad tekonsumtion\n[kg/person sedan {x[0]}\n===========================') #Skriver titel baserat på första året med data
    for i in range(0, len(år)): #Går igenom dom åren som ska visas
        print(f'{år[i]}    {str(round(vikt[i], 2)).rjust(len(längsta))}')#Skriver ut år samt summan för det året justerat så att dom längsta talen 
                                                                         #hamnar 3 blanksteg från året och allt annat i linje till höger
    print('===========================')

