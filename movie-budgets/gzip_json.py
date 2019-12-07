import gzip
import json
from urls_to_scrape import urls_n_filenames

for thang in urls_n_filenames:

    file = thang[1]

    infile = f'./json_data/{file}.json'
    outfile = f'./data/{file}.json'

    with open(infile) as json_file:
        data = json.load(json_file)

    with gzip.open(outfile, 'wt', encoding='utf-8') as zipfile:
        json.dump(data, zipfile, indent=4)

import os

def get_size(start_path = ''):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size

print(get_size(start_path='./json_data'), 'bytes')
print(get_size(start_path='./data'), 'bytes')