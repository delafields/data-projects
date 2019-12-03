from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

#launch url
url = 'https://247sports.com/Season/2019-Basketball/CompositeTeamRankings/#'

# create a new Chrome session
driver = webdriver.Chrome(executable_path=r'C:\Users\jfields\Desktop\Code\data-projects\cbb-recruiting\chromedriver.exe')
driver.implicitly_wait(5)
driver.get(url)

# parse the html using beautiful soup and store in variable `soup`
soup = BeautifulSoup(driver.page_source, 'html.parser')

# find rankings table
table = soup.find('ul', attrs={'class': 'rankings-page__list'})

# find rows in table 
rows = table.find_all('li', attrs={'class': 'rankings-page__list-item'})

rowdict = {
    #'Year': [],
    'Team': [],
    'Ranking': [],
    'Num_Commits': [],
    'Num_5_Stars': [],
    'Num_4_Stars': [],
    'Num_3_Stars': [],
    'Avg': [],
    'Points': []
}

#for row in rows:

first_row = rows[0]

team = first_row.find('a', attrs={'class': 'rankings-page__name-link'}).getText().strip()
ranking = first_row.find('div', attrs={'class': 'primary'}).getText().strip()
Num_Commits = first_row.find('div', attrs={'class': 'total'}).getText().strip()
Num_Commits = Num_Commits.split(' ')[0]
Num_5_Stars = first_row.find('div', attrs={'class': 'gold'}).getText().strip()
Num_4_Stars = first_row.find('div', attrs={'class': 'silver'}).getText().strip()
Num_3_Stars = first_row.find('ul', attrs={'class': 'star-commits-list'})
Num_3_Stars = Num_3_Stars.find_all('li')[2]
Num_3_Stars = Num_3_Stars.find('div').getText().strip()
Avg = first_row.find('div', attrs={'class': 'avg'}).getText().strip()
Points = first_row.find('a', attrs={'class': 'number'}).getText().strip()


print(f'team : {team}')
print(f'ranking : {ranking}')
print(f'Num_Commits : {Num_Commits}')
print(f'Num_5_Stars : {Num_5_Stars}')
print(f'Num_4_Stars : {Num_4_Stars}')
print(f'Num_3_Stars : {Num_3_Stars}')
print(f'Avg : {Avg}')
print(f'Points : {Points}')

driver.quit()