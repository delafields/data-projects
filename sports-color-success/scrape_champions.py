import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

championship_urls {
    "NFL": ["https://en.wikipedia.org/wiki/List_of_Super_Bowl_champions",
            "#mw-content-text > div > table:nth-child(35)"]
    "NBA": ["https://en.wikipedia.org/wiki/List_of_NBA_champions",
            "#mw-content-text > div > table:nth-child(13)"]
    "MLB": ["https://en.wikipedia.org/wiki/List_of_World_Series_champions",
            "#mw-content-text > div > table:nth-child(21)"]
    "NHL": ["https://en.wikipedia.org/wiki/List_of_Stanley_Cup_champions",
            "#mw-content-text > div > table:nth-child(44)"]
    "EPL": ["https://en.wikipedia.org/wiki/List_of_English_football_champions",
            "#mw-content-text > div > table:nth-child(17)"]
    "La Liga": ["https://en.wikipedia.org/wiki/List_of_Spanish_football_champions",
            "#mw-content-text > div > table.sortable.plainrowheaders.wikitable.jquery-tablesorter"]
    "Serie A": ["https://en.wikipedia.org/wiki/List_of_Italian_football_champions",
            "#mw-content-text > div > table.wikitable.plainrowheaders"]
    "NCAAF": ["https://www.ncaa.com/history/football/fbs",
            "#ncaa-root > div > article > div > div > div > table"]
    "NCAAB":  ["https://www.ncaa.com/history/basketball-men/d1",
            "#ncaa-root > div > article > div > div > div > table"]
}



#table = soup.find_all('table')[0] 
#df = pd.read_html(str(table))

def get_soup(url = ''):
    '''Open a webpage and return a BeautifulSoup object'''
    try:
        headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
        page = requests.get(url, headers = headers, timeout = 5)
    except requests.ConnectionError as e:
        print("Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
        print(str(e))
    except requests.Timeout as e:
        print("Timeout Error")
        print(str(e))

    # parse the html using beautiful soup and store in variable `soup`
    print('pulling the html')
    soup = BeautifulSoup(page.text, 'html.parser')

    return soup

team_colors = pd.DataFrame(columns = ['Team', 'Championships'])

temp = get_soup(nfl_champs_url)

#temp = temp.find_all("table")

#print(temp[3].prettify())

ok = temp.select_one('#mw-content-text > div > table:nth-child(35)')

print(ok.prettify())