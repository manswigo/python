import numpy as np
import random
x = np.linspace(1, 1000000, 1000000)
xr = random.shuffle(x)
print(xr[0])