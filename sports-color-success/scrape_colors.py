import pandas as pd
import re
from helpers import get_soup, color_urls

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