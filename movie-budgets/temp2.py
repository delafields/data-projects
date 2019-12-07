import pandas as pd
from urls_to_scrape import urls_n_filenames
import json
import gzip

with gzip.GzipFile(f'./data/Movie_Budget_1to100.json', 'r') as fin:
    
    data = json.loads(fin.read().decode('utf-8'))
    print(data)