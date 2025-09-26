#pickle: sparar i binär form
#json = javascript object notation

import pickle
#skriv med pickle
min_data = [1, 2, 3, 'hej', 82.1]
with open('min_datafil.pkl', 'wb') as f:
    pickle.dump(min_data, f)
#läs med pickle
with open('min_datafil', 'rb') as f:
    inläst_data = pickle.load(f)

import json
#skriv med json
min_data = [1, 2, 3, 'hej', 82.1]
with open('min_datafil.json', 'w') as f:
    json.dump(min_data, f)
#läs med json
with open('min_datafil.json', 'r') as f:
    inläst_data = json.load(f)