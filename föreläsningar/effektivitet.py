import time
N = 1_000_000_000
start = time.time()

for i in range(0, N):
    x = [1, 2, 3]

stopp = time.time()

list_time = stopp - start

start = time.time()

for i in range(0, N):
    x = (1, 2, 3)

stopp = time.time()

tup_time = stopp - start

print(tup_time, list_time)   