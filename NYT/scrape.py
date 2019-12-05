import requests
import re
import json
import datetime
import hashlib
import gzip
from bs4 import BeautifulSoup

# NYT bestsellers url
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
print('get refresh date')
if soup.find('time'):
    time = soup.find('time').getText()
    time = datetime.datetime.strptime(time, '%B %d, %Y').date()
else:
    time = datetime.date.today()
    # the below gets the date of the next sunday
    time = time + datetime.timedelta( (6-today.weekday()) % 7 )
print('This week is', time)

def parse_weeks(text):
    '''Parses the number of weeks a book has been on the NYT list'''
    '''input (text): comes in as either X WEEKS ON THE LIST or New to list'''
    new_book = re.compile('New')
    num_weeks = re.compile('\d+')

    if new_book.search(text):
        return 'New'

    elif re.findall(num_weeks, text):
        num_weeks = re.findall(num_weeks, text)
        return ''.join(num_weeks) + ' weeks'

    else:
        return 'N/A'

def get_title(book):
    if book.find('h3', attrs={'itemprop': 'name'}):
        title = book.find('h3', attrs={'itemprop': 'name'}).getText()
        title = title.title()
    else:
        title = ''
    return title

def get_author(book):
    if book.find('p', attrs={'itemprop': 'author'}):
        author = book.find('p', attrs={'itemprop': 'author'}).getText()
        author = re.sub('by ', '', author)
    else:
        author = ''
    return author

def get_weeks_on_list(book):
    if book.find('p'):
        weeks = book.find('p').getText()
        num_weeks = parse_weeks(weeks)
    else:
        num_weeks = ''
    return num_weeks

# each section is a category on the NYT site
categories = soup.find_all('section')

book_dict = {}

for cat in categories:
    if cat.find('h2'):
        # get book category
        category_name = cat.find('h2').getText()
        print('Getting books in the', category_name, 'category')

        books_in_category = cat.find_all('li')

        for book in books_in_category: 
            # get the book titles in this category
            title = get_title(book)

            # hash the title+category and store in dictionary
            title_category = title + category_name
            hashed_book = hashlib.sha1(title_category.encode('utf8')).hexdigest()

            book_dict[hashed_book] = {}
            book_dict[hashed_book]['title'] = title

            # get author
            author = get_author(book)
            book_dict[hashed_book]['author'] = author

            book_dict[hashed_book]['category_name'] = category_name

            # get number of weeks on list
            num_weeks = get_weeks_on_list(book)
            book_dict[hashed_book]['weeks_on_list'] = num_weeks

            # add pull date
            book_dict[hashed_book]['date'] = str(time)

print(f'Data retrieved. Gzipping to a json file @ {time}.json')

#temp = json.dumps(book_dict, indent=4)
#print(temp)

with gzip.open(f'{time}.json', 'wt', encoding='utf-8') as zipfile:
    json.dump(book_dict, zipfile, indent=4)

num_books = 0
for key in book_dict:
    num_books += 1

print('numbooks (non_unique): ', num_books)