import pandas as pd
import re
from helpers import get_soup, championship_urls

for league in championship_urls:
        print(f"Workin on {league}")

        url = championship_urls[league][0]
        selector = championship_urls[league][1]

        soup = get_soup(url)

        if league == "La Liga":
                champ_table = soup.find_all("table", {"class": selector})[-1]
        else:
                champ_table = soup.select_one(selector)
                
                
        champ_df = pd.read_html(str(champ_table))[0]
        champ_df["League"] = league

        league = league.replace(" ", "")
        champ_df.to_csv(f"data/{league}_Champions.csv", index = False)