import pandas as pd
cards = pd.read_csv('magic.csv', sep=',', decimal='.')
land = 0
common = 0
uncommon = 0
rare = 0
tot_value = 0
for i in range(0, len(cards)):
    tot_value += cards.loc[i]['Market Price']
    if cards.loc[i]['Rarity'] == 'Land':
        land += 1
    elif cards.loc[i]['Rarity'] == 'Common':
        common += 1
    elif cards.loc[i]['Rarity'] == 'Uncommon':
        uncommon += 1
    elif cards.loc[i]['Rarity'] == 'Rare':
        rare += 1
print(f'''Common: {common}
Uncommon: {uncommon}
Rare: {rare}
Total value: {tot_value}
''')