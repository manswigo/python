import numpy as np

a = np.arange(16).reshape(4,4)
b = np.arange(4).reshape(4,1)
print(a)
print(b)
print(a*b)
print(a@b)