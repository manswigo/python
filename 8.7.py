def med(x):
    summ = 0
    for i in range(0, len(x)):
        summ += x[i]
    return(summ/len(x))


list = [3, 4, 3, 4]
tup = (4, 3, 4, 3)

print(med(list))
print(med(tup))