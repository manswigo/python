for n in range(2, 1001):
  
    for k in range(2, n):
        if k == n - 1:
            print(n)
        if n % k == 0:
            break


        
