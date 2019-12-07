from scrape import get_data
import os
import json

# url followed by file name
from urls_to_scrape import urls_n_filenames

def make_json(url, file):
    '''Scrape the data and put it into a json file
    
    Parameters:
    url (str): a valid url
    file (str): the file being saved to
    '''
    # check if file exists
    if os.path.exists(f'./json_data/{file}.json'):
        print(f'./json_data/{file}.json already exists')
        return

    # scrape the data into a dict
    dictionary = get_data(url)

    # put dict into json and save to file
    print(f'Data scraped. Saving to ./data/{file}.json')

    with open(f'./json_data/{file}.json', 'w') as outfile:
        json.dump(dictionary, outfile, indent=4)
        
    print('Saved!')

# where tha magic happens
for u_n_f in urls_n_filenames:
    make_json(u_n_f[0], u_n_f[1])

