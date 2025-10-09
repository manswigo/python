n = 'temps.txt'
with open(n, 'r') as f1:
    file_arr = f1.readlines()
    for rad in file_arr:
        rad = rad.replace('\t', '   ')
with open(n, 'w') as f1:
    count = 0
    for rad in file_arr:
        f1.write(rad)
        count += 1