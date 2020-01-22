import pandas as pd
import re
from helpers import get_soup, color_urls
import webcolors

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

        # edge cases
        if primary == "#024":  primary = "#002244"
        elif primary == "#000": primary = "#000000"
        elif primary == "#111": primary = "#111111"
        
        if secondary == "#fff": secondary = "#ffffff"
        elif secondary == "#000; c": secondary = "#000000"
        elif secondary == " #FC4C0": secondary = "#FC4C00"
        elif secondary == "#fff; c": secondary = "#ffffff"
        elif secondary == "black; ": secondary = "#000000"

        team_colors.loc[len(team_colors)] = [Team, primary, secondary, league]

team_colors = pd.DataFrame(columns = ["Team", "Primary Color", "Secondary Color", "League"])

# loop through each league, grab the html and extract the colors
for league in color_urls:

    url = color_urls[league][0]
    league_name = color_urls[league][1]

    print(f"Workin on the {league_name}")

    extract_colors(url, league_name)

# https://stackoverflow.com/questions/9694165/convert-rgb-color-to-english-color-name-like-green-with-python
def get_color_name(hex_code):

    # convert hex to an rgb triplet
    hex_code = hex_code[1: ]
    red, green, blue = bytes.fromhex(hex_code)
    rgb_triplet = (red, green, blue)

    min_colors = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - rgb_triplet[0]) ** 2
        gd = (g_c - rgb_triplet[1]) ** 2
        bd = (b_c - rgb_triplet[2]) ** 2
        min_colors[(rd + gd + bd)] = name
    return min_colors[min(min_colors.keys())]

# get the color name for each hex code
team_colors["Primary Name"] = team_colors["Primary Color"].apply(lambda c: get_color_name(c))
team_colors["Secondary Name"] = team_colors["Secondary Color"].apply(lambda c: get_color_name(c))    

team_colors.to_csv("data/team_colors.csv", index = False)

print("Done!")