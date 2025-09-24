l = [1, 5, 34, 64,334, 63, 2]
ojämn = lambda x: x%2 != 0
l2 = list(filter(ojämn, l))
print(l2)