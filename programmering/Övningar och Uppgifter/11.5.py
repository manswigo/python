from sys import argv
print(argv)
for arg in argv:
    tot = 0
    with open(arg, 'r') as f1:
        for rad in f1:
            tot += 1
        print(tot)