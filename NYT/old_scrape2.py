import requests
import re
import json
import datetime
import hashlib
from bs4 import BeautifulSoup

#launch url
url = 'https://www.nytimes.com/books/best-sellers/'

# get the page
print('Opening the url')

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

# get the last refreshed date
if soup.find('time'):
    time = soup.find('time').getText()
    time = datetime.datetime.strptime(time, '%B %d, %Y').date()
else:
    time = datetime.date.today()
    # the below gets the date of the next sunday
    time = time + datetime.timedelta( (6-today.weekday()) % 7 )

def parse_weeks(text):
    '''Parses the number of weeks a book has been on the NYT list'''
    '''input (text): comes in as either X WEEKS ON THE LIST or New to list'''
    new_book = re.compile('New')
    num_weeks = re.compile('\d+')

    if new_book.search(text):
        return 'New'

    elif re.findall(num_weeks, text):
        num_weeks = re.findall(num_weeks, weeks)
        return ''.join(num_weeks) + ' weeks'

    else:
        return 'N/A'

# each section is a category on the NYT site
categories = soup.find_all('section')

book_dict = {}

for cat in categories:
    if cat.find('h2'):
        # get book category
        category_name = cat.find('h2').getText()

        books_in_category = cat.find_all('li')

        for book in books_in_category:            
            # Get book title
            if book.find('h3', attrs={'itemprop': 'name'}):
                title = book.find('h3', attrs={'itemprop': 'name'}).getText()
                title = title.title()
            else:
                title = ''
            # hash the title and store in dictionary
            hashed_book = hashlib.sha1(title.encode('utf8')).hexdigest()
            book_dict[hashed_book] = {}
            book_dict[hashed_book]['title'] = title

            # Get author
            if book.find('p', attrs={'itemprop': 'author'}):
                author = book.find('p', attrs={'itemprop': 'author'}).getText()
                author = re.sub('by ', '', author)
            else:
                author = ''

            book_dict[hashed_book]['author'] = author

            # get number of weeks on list
            if book.find('p'):
                weeks = book.find('p').getText()
                num_weeks = parse_weeks(weeks)
            else:
                num_weeks = ''
            
            book_dict[hashed_book]['weeks_on_list'] = num_weeks

            # add date & category name
            book_dict[hashed_book]['date'] = str(time)
            book_dict[hashed_book]['category_name'] = category_name


temp = json.dumps(book_dict, indent=4)
print(temp)

with open('data.json', 'w') as f:
    json.dump(book_dict, f, indent=4)