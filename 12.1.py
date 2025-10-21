list = [{'blå', 'gul'}, {'blå', 'röd', 'grön'}, {'vit', 'blå'}]
union = set()
for i in range(len(list)):
    union = union | list[i]

for i in range(len(list) - 1):
    snitt = list[i] & list[i+1]
print(union, snitt)



