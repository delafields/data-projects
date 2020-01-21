import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

color_urls = {
    "nfl_colors_url": ["https://teamcolorcodes.com/nfl-team-color-codes/", "NFL"],
    "nba_colors_url": ["https://teamcolorcodes.com/nba-team-color-codes/", "NBA"],
    "mlb_colors_url": ["https://teamcolorcodes.com/mlb-color-codes/", "MLB"],
    "nhl_colors_url": ["https://teamcolorcodes.com/nhl-team-color-codes/", "NHL"],
    "epl_colors_url": ["https://teamcolorcodes.com/premier-league-color-codes/", "EPL"],
    "laliga_colors_url": ["https://teamcolorcodes.com/soccer/laliga-color-codes/", "La Liga"],
    "seriea_colors_url": ["https://teamcolorcodes.com/soccer/serie-a-color-codes/", "Serie A"],
    'aac_colors_url': ['https://teamcolorcodes.com/ncaa-color-codes/aac/', 'NCAA'],
    'acc_colors_url': ['https://teamcolorcodes.com/ncaa-color-codes/acc-color-codes/', 'NCAA'],
    'atlantic10_colors_url': ['https://teamcolorcodes.com/ncaa-color-codes/atlantic-10/', 'NCAA'],
    'bigsky_colors_url': ['https://teamcolorcodes.com/ncaa-color-codes/big-sky-conference/', 'NCAA'],
    'big10_colors_url': ['https://teamcolorcodes.com/ncaa-color-codes/big-ten-team-colors/', 'NCAA'],
    'conferenceusa_colors_url': ['https://teamcolorcodes.com/ncaa-color-codes/conference-usa/', 'NCAA'],
    'ivyleague_colors_url': ['https://teamcolorcodes.com/ncaa-color-codes/ivy-league/', 'NCAA'],
    'mac_colors_url': ['https://teamcolorcodes.com/ncaa-color-codes/mac/', 'NCAA'],
    'mountainwest_colors_url': ['https://teamcolorcodes.com/ncaa-color-codes/mountain-west/', 'NCAA'],
    'patriotleague_colors_url': ['https://teamcolorcodes.com/ncaa-color-codes/patriot-league-colors/', 'NCAA'],
    'southernconf_colors_url': ['https://teamcolorcodes.com/ncaa-color-codes/southern-conference-colors/', 'NCAA'],
    'sunbeltconf_colors_url': ['https://teamcolorcodes.com/ncaa-color-codes/sun-belt/', 'NCAA'],
    'wcc_colors_url': ['https://teamcolorcodes.com/ncaa-color-codes/west-coast-conference/', 'NCAA'],
    'americaeast_colors_url': ['https://teamcolorcodes.com/ncaa-color-codes/america-east/', 'NCAA'],
    'atlanticsun_colors_url': ['https://teamcolorcodes.com/ncaa-color-codes/atlantic-sun/', 'NCAA'],
    'bigeast_colors_url': ['https://teamcolorcodes.com/ncaa-color-codes/big-east/', 'NCAA'],
    'bigwest_colors_url': ['https://teamcolorcodes.com/ncaa-color-codes/big-west/', 'NCAA'],
    'big12_colors_url': ['https://teamcolorcodes.com/ncaa-color-codes/big-12-colors/', 'NCAA'],
    'horizonleague_colors_url': ['https://teamcolorcodes.com/ncaa-color-codes/horizon-league/', 'NCAA'],
    'maac_colors_url': ['https://teamcolorcodes.com/ncaa-color-codes/maac/', 'NCAA'],
    'missourivalley_colors_url': ['https://teamcolorcodes.com/ncaa-color-codes/missouri-valley/', 'NCAA'],
    'pac12_colors_url': ['https://teamcolorcodes.com/ncaa-color-codes/pac-12-colors/', 'NCAA'],
    'sec_colors_url': ['https://teamcolorcodes.com/ncaa-color-codes/sec-team-color-codes/', 'NCAA'],
    'summitleague_colors_url': ['https://teamcolorcodes.com/ncaa-color-codes/summit-league/', 'NCAA'],
    'wac_colors_url': ['https://teamcolorcodes.com/ncaa-color-codes/western-athletic-conference/', 'NCAA']
}

nfl_champs_url = "https://en.wikipedia.org/wiki/List_of_Super_Bowl_champions"
nba_champs_url = "https://en.wikipedia.org/wiki/List_of_NBA_champions"
mlb_champs_url = "https://en.wikipedia.org/wiki/List_of_World_Series_champions"
nhl_champs_url = "https://en.wikipedia.org/wiki/List_of_Stanley_Cup_champions"
epl_champs_url = "https://en.wikipedia.org/wiki/List_of_English_football_champions"
laliga_champs_url = "https://en.wikipedia.org/wiki/List_of_Spanish_football_champions"
seriea_champs_url = "https://en.wikipedia.org/wiki/List_of_Italian_football_champions"
ncaaf_champs_url = "https://www.ncaa.com/history/football/fbs"
ncaab_champs_url = "https://www.ncaa.com/history/basketball-men/d1"

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

def extract_colors(url, league):

    # grab the html, find the team buttons
    soup = get_soup(url)
    teams = soup.find_all("a", {"class", "team-button"})

    for t in teams:
        Team = t.text

        style = str(t["style"])

        # get the primary color (stored in the background-color of the style attr)
        primary_reg = re.compile("#(?:[0-9a-fA-F]{3}){1,2}")
        primary = primary_reg.findall(style)[0]

        # get the secondary color (stored in the border-bottom of the style attr)
        secondary_reg = re.compile("border-bottom: 4px solid .{7}")
        secondary_temp = secondary_reg.findall(style)
        # black isn't given a hex, it's given 'black'
        if not secondary_temp:
            secondary = "#000000"
        else:
            secondary = secondary_temp[0][-7:]

        team_colors.loc[len(team_colors)] = [Team, primary, secondary, league]

team_colors = pd.DataFrame(columns = ["Team", "Primary Color", "Secondary Color", "League"])

# loop through each league, grab the html and extract the colors
for league in color_urls:

    url = color_urls[league][0]
    league_name = color_urls[league][1]

    print(f"Workin on the {league_name}")

    extract_colors(url, league_name)


team_colors.to_csv("data/team_colors.csv", index = False)

print("Done!")