import pandas as pd
import numpy as np

data = [
    ["Anna", 23, "Stockholm"],
    ["Björn", 35, "Göteborg"],
    ["Cecilia", 29, "Malmö"],
    ["David", 42, "Uppsala"]
]

df = pd.DataFrame(data, columns=['Namn', 'Ålder', 'Stad'])
print(df)
print(df[df['Ålder'] > 30]['Namn'])
