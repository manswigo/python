div = 1
sum = 0
while 1/div >= 0.00001:
    if div % 2 == 0:
        sum -= 1/div
    else:
        sum += 1/div
    div += 1
print(sum)
