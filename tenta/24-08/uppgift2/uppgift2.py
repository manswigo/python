import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv('sommar_os.csv', sep=';')

highest = 0
year = ''

for i in range(len(df)):
   
    if df.loc[i]['Totalt']/df.loc[i]['Deltagare'] > highest:
        highest = float(df.loc[i]['Totalt'])/float(df.loc[i]['Deltagare'])
        year = df.loc[i]['Spel'].split()[0]

print(year)

x = list(df['Deltagare'])
y = list(df['Totalt'])
print(x)
fig, ax = plt.subplots()
ax.scatter(x, y)
plt.xlabel('Antal deltagare')
plt.ylabel('Antal medaljer')
plt.title('Sommar-Os')
plt.show()
