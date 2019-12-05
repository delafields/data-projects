import json
import pandas as pd
from pandas.io.json import json_normalize #package for flattening json in pandas df

import json
with open('./data.json') as data_file:    
    data = json.load(data_file)

#df = pd.DataFrame(data)
#df = json_normalize(data, ['author', 'title'], max_level=3)

#print(df.head())

df = pd.DataFrame()

for key in data:
    df = df.append(data[key], ignore_index=True)

print(df.head())
print(df.shape)