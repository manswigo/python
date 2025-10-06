fn = input('Namn: ')
with open(fn, 'r') as f1:
    temps = [int(rad) for rad in f1]

print(f'Varmast: {max(temps)} Medel: {sum(temps)/len(temps)}')