s = input('List: ')
s2 = input('Tuple: ')
s3 = s2.split
my_list = list(s.split())
my_tuple = tuple(s3)
if len(my_list) != len(my_tuple):
    print('Inte samma')
    exit()
for i in range(0, len(my_list)):
    if my_list[i] != my_tuple[i]:
        print('Inte samma')
        exit()
print('Samma')