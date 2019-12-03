from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

#launch url
url = 'https://247sports.com/Season/2019-Basketball/CompositeTeamRankings/#'

# create a new Chrome session
print('Opening the url')
driver = webdriver.Chrome(executable_path=r'C:\Users\jfields\Desktop\Code\data-projects\cbb-recruiting\chromedriver.exe')
driver.implicitly_wait(5)
driver.get(url)

# click load more button
while True:
    try:
        loadMoreButton = driver.find_element_by_link_text('Load More')
        time.sleep(2)
        # execute click action via javascript, not selenium's built-in click()
        print('clicking load more...')
        driver.execute_script('arguments[0].click();', loadMoreButton)
        time.sleep(5)
    except Exception as e:
        print(e)
        break

# parse the html using beautiful soup and store in variable `soup`
print('pulling the html')
soup = BeautifulSoup(driver.page_source, 'html.parser')

# close page
print('closing the driver')
driver.quit()

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

print('going through the rows..')
for row in rows:
    #Team = row.find('a', attrs={'class': 'rankings-page__name-link'}).getText().strip()
    Team = row.find('div', attrs={'class': 'team'})
    if Team.find('a') == None:
        Team = Team.getText().strip()
    else:
        Team = Team.find('a').getText().strip()

    Ranking = row.find('div', attrs={'class': 'primary'}).getText().strip()

    Num_Commits = row.find('div', attrs={'class': 'total'}).getText().strip()
    Num_Commits = Num_Commits.split(' ')[0]

    Star_List = row.find('ul', attrs={'class': 'star-commits-list'})
    Num_5_Stars = Star_List.find_all('li')[0]
    Num_5_Stars = Num_5_Stars.find('div').getText().strip()
    Num_4_Stars = Star_List.find_all('li')[1]
    Num_4_Stars = Num_4_Stars.find('div').getText().strip()
    Num_3_Stars = Star_List.find_all('li')[2]
    Num_3_Stars = Num_3_Stars.find('div').getText().strip()

    Avg = row.find('div', attrs={'class': 'avg'}).getText().strip()

    #Points = row.find('a', attrs={'class': 'number'}).getText().strip()
    Points = row.find('div', attrs={'class': 'points'})
    if Points.find('a', attrs={'class': 'number'}) == None:
        Points = Points.getText().strip()
    else:
        Points = Points.find('a', attrs={'class': 'number'}).getText().strip()

    print('Team: ', Team)
    print('Num_5_Stars: ', Num_4_Stars)

    if Ranking == 'N/A':
        pass
    else:
        rowdict['Team'].append(Team)
        rowdict['Ranking'].append(Ranking)
        rowdict['Num_Commits'].append(Num_Commits)
        rowdict['Avg'].append(Avg)
        rowdict['Num_5_Stars'].append(Num_5_Stars)
        rowdict['Num_4_Stars'].append(Num_4_Stars)
        rowdict['Num_3_Stars'].append(Num_3_Stars)
        rowdict['Points'].append(Points)

#print(rowdict)

df = pd.DataFrame(rowdict)
df.to_csv('2019.csv')