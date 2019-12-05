import gzip
import json
import pandas as pd

with gzip.GzipFile('2019-12-15.json', 'r') as fin:
    data = json.loads(fin.read().decode('utf-8'))


df = pd.DataFrame()

num_books = 0

for key in data:
    num_books += 1
    df = df.append(data[key], ignore_index=True)

print('numbooks: ', num_books)
print(df.head())
print(df.shape)

df.to_csv('2019-12-15.csv')