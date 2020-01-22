import pandas as pd
import re
from helpers import get_soup, championship_urls

        if league == "Serie A"
        champ_df = get_champs_table(league = "Serie A")[["Club", "Champions", "League"]]
        champ_df = champ_df.rename(columns = {"Club": "Team", "Champions": "Wins"})
        champ_df = champ_df.replace({"Milan": "A.C. Milan", "Internazionale": "Inter Milan", "Roma": "A.S. Roma"}) # don't have many colors

        LA LIGA DONE
        champ_df = get_champs_table(league = "La Liga")[["Club", "Winners", "League"]]
        champ_df = champ_df.rename(columns = {"Club": "Team", "Winners": "Wins"})
        champ_df = champ_df.replace({"Real Madrid": "Real Madrid CF", "Barcelona": "Barcelona FC", "Atlético Madrid": "Atletico Madrid",
                                     "Valencia": "Valencia CF", "Deportivo La Coruña": "Deportivo"})

        EPL DONE
        champ_df = get_champs_table(league = "EPL")[["Club", "Winners", "League"]]
        champ_df = champ_df.rename(columns = {"Club": "Team", "Winners": "Wins"})
        champ_df = champ_df.replace({"Everton FC": "Everton", "Newcastle United": "Newcastle United FC", 
                                     "Wolverhampton Wanderers": "Wolverhampton", "Watford": "Watford FC",
                                     "Southampton": "Southampton FC"})

        NHL DONE
        champ_df = get_champs_table(league = "NHL")[["Team", "Wins", "League"]]
        champ_df["Team"] = champ_df["Team"].str.replace(r"\[.\]", "")

        MLB DONE
        champ_df = get_champs_table(league = "MLB")[["Team", "Wins", "League"]]
        champ_df = champ_df.replace({"New York/San Francisco GiantsNY until 1957, SF 1958-present": "San Francisco Giants",
                                     "Brooklyn/Los Angeles DodgersBKN until 1957, LA 1958-present": "Los Angeles Dodgers",
                                     "Philadelphia/Kansas City/Oakland AthleticsPHI until 1954, KC 1955-1967, OAK 1968-present": "Oakland Athletics",
                                     "Boston/Milwaukee/Atlanta BravesBOS until 1952, MIL 1953-1965, ATL 1966-present": "Atlanta Braves",
                                     "St. Louis Browns/Baltimore OriolesSTL until 1953, BAL 1954-present": "Baltimore Orioles",
                                     "Washington Senators/Minnesota TwinsWSH until 1960, MIN 1961-present": "Minnesota Twins",
                                     "Washington Senators/Texas Rangers WSH until 1971, TEX 1972-present": "Texas Rangers",
                                     "Montreal Expos/Washington Nationals MTL until 2004, WSH 2005-present": "Washington Nationals",
                                     "Seattle Pilots/Milwaukee Brewers SEA 1969, MIL 1970-present": "Milwaukee Brewers"})

        NBA DONE
        champ_df = get_champs_table(league = "NBA")[["Teams", "Win", "League"]]
        champ_df = champ_df.rename(columns = {"Teams": "Team", "Win": "Wins"})
        champ_df["Team"] = champ_df["Team"].str.replace(r"\[.*\]", "")
        champ_df["Wins"] = champ_df["Wins"].replace("—", 0)

        NFL DONE
        champ_df = get_champs_table(league = "NFL")[["Team", "Wins", "League"]]
        champ_df = champ_df[: -1] # remove last header row
        champ_df["Team"] = champ_df["Team"].str.replace(r"\[.*\]", "") # get rid of bracketed numbers
        champ_df["Team"] = champ_df["Team"].str.rstrip(r"(N|n|A|a)")   # get rid of text artifacts
        champ_df = champ_df.replace({"Boston/New England Patriots": "New England Patriots",
                                     "Oakland/Los Angeles Raiders": "Oakland Raiders",
                                     "Baltimore/Indianapolis Colts": "Indianapolis Colts",
                                     "St. Louis/Los Angeles Rams": "Los Angeles Rams",
                                     "San Diego/Los Angeles Chargers": "Los Angeles Chargers",
                                     "Houston/Tennessee Oilers/Titans": "Tennessee Titans",
                                     "St. Louis/Phoenix/Arizona Cardinals": "Arizona Cardinals"})

        SERIE A DONE
        champ_df = get_champs_table(league = "Serie A")[["Club", "Champions", "League"]]
        champ_df = champ_df.rename(columns = {"Club": "Team", "Champions": "Wins"})
        champ_df = champ_df.replace({"Milan": "A.C. Milan", "Internazionale": "Inter Milan", "Roma": "A.S. Roma"}) # don't have many colors

        LA LIGA DONE
        champ_df = get_champs_table(league = "La Liga")[["Club", "Winners", "League"]]
        champ_df = champ_df.rename(columns = {"Club": "Team", "Winners": "Wins"})
        champ_df = champ_df.replace({"Real Madrid": "Real Madrid CF", "Barcelona": "Barcelona FC", "Atlético Madrid": "Atletico Madrid",
                                     "Valencia": "Valencia CF", "Deportivo La Coruña": "Deportivo"})

        EPL DONE
        champ_df = get_champs_table(league = "EPL")[["Club", "Winners", "League"]]
        champ_df = champ_df.rename(columns = {"Club": "Team", "Winners": "Wins"})
        champ_df = champ_df.replace({"Everton FC": "Everton", "Newcastle United": "Newcastle United FC", 
                                     "Wolverhampton Wanderers": "Wolverhampton", "Watford": "Watford FC",
                                     "Southampton": "Southampton FC"})

        NHL DONE
        champ_df = get_champs_table(league = "NHL")[["Team", "Wins", "League"]]
        champ_df["Team"] = champ_df["Team"].str.replace(r"\[.\]", "")

        MLB DONE
        champ_df = get_champs_table(league = "MLB")[["Team", "Wins", "League"]]
        champ_df = champ_df.replace({"New York/San Francisco GiantsNY until 1957, SF 1958-present": "San Francisco Giants",
                                     "Brooklyn/Los Angeles DodgersBKN until 1957, LA 1958-present": "Los Angeles Dodgers",
                                     "Philadelphia/Kansas City/Oakland AthleticsPHI until 1954, KC 1955-1967, OAK 1968-present": "Oakland Athletics",
                                     "Boston/Milwaukee/Atlanta BravesBOS until 1952, MIL 1953-1965, ATL 1966-present": "Atlanta Braves",
                                     "St. Louis Browns/Baltimore OriolesSTL until 1953, BAL 1954-present": "Baltimore Orioles",
                                     "Washington Senators/Minnesota TwinsWSH until 1960, MIN 1961-present": "Minnesota Twins",
                                     "Washington Senators/Texas Rangers WSH until 1971, TEX 1972-present": "Texas Rangers",
                                     "Montreal Expos/Washington Nationals MTL until 2004, WSH 2005-present": "Washington Nationals",
                                     "Seattle Pilots/Milwaukee Brewers SEA 1969, MIL 1970-present": "Milwaukee Brewers"})

        NBA DONE
        champ_df = get_champs_table(league = "NBA")[["Teams", "Win", "League"]]
        champ_df = champ_df.rename(columns = {"Teams": "Team", "Win": "Wins"})
        champ_df["Team"] = champ_df["Team"].str.replace(r"\[.*\]", "")
        champ_df["Wins"] = champ_df["Wins"].replace("—", 0)

        NFL DONE
        champ_df = get_champs_table(league = "NFL")[["Team", "Wins", "League"]]
        champ_df = champ_df[: -1] # remove last header row
        champ_df["Team"] = champ_df["Team"].str.replace(r"\[.*\]", "") # get rid of bracketed numbers
        champ_df["Team"] = champ_df["Team"].str.rstrip(r"(N|n|A|a)")   # get rid of text artifacts
        champ_df = champ_df.replace({"Boston/New England Patriots": "New England Patriots",
                                     "Oakland/Los Angeles Raiders": "Oakland Raiders",
                                     "Baltimore/Indianapolis Colts": "Indianapolis Colts",
                                     "St. Louis/Los Angeles Rams": "Los Angeles Rams",
                                     "San Diego/Los Angeles Chargers": "Los Angeles Chargers",
                                     "Houston/Tennessee Oilers/Titans": "Tennessee Titans",
                                     "St. Louis/Phoenix/Arizona Cardinals": "Arizona Cardinals"})
