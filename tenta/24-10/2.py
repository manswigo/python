import pandas as pd
df = pd.read_csv('riksdag2022.csv', sep=',', decimal='.')
partier = set()
for i in range(len(df)):
    partietSet = set()
    partietSet.add(df.loc[i]['parti'])
    partier = partier | partietSet
partiList = list(partier)
for i in range(len(partiList)):
    partiList[i] = [partiList[i]]


for i in range(len(partiList)):
    count = 0
    for k in range(len(df)):
        if df.loc[k]['parti'] == partiList[i][0]:
            count += 1
    partiList[i].append(count)
print(partiList)