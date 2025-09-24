def g(n):
    counter = 0
    while n > 0:
        counter += 1
        n //=10
    return(counter)
n = 56678   
print(g(n)) 