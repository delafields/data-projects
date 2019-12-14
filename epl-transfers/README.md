# EPL TRANSFERS ⚽

Data on English Premier League transfers and season-end position from the 1992-93 season through 2018-19. Season-end tables scraped from wikipedia. Transfer data from [@ewenme](https://github.com/ewenme)'s awesome pre-scraped [repo](https://github.com/ewenme/transfers) (<- that data is from [Transfermarkt](https://www.transfermarkt.co.uk/)).

See [epl_table_scraper.r]('epl_scraper.r') for the results-table scraper code.

## Data
Season-end tables can be found in the `data/epl-results/` folder. Filenames follow the format `year_EPL_results.csv`; ex: `1992-93_EPLResults.csv`.
* `year`: season (1992-93)
* `Pos`: standing end-of-year (1, 2, etc) 
* `Team`: team name
* `Pld`: num games played 
* `W`: num games won
* `D`: num games drawn
* `L`: num games lost
* `GF`: goals for (scored)
* `GA`: goals against
* `GD`: goal differential
* `Pts`: num pts from W/L/D
* `Qualification or relegation`: qualification for European cups, relegated