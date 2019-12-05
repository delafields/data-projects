import requests
import re
import json
import datetime
import hashlib
import gzip
from bs4 import BeautifulSoup

# get the page
print('Opening the url')

def get_soup(url='https://www.nytimes.com/books/best-sellers/'):
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

print('get refresh date')

def get_refresh_date(soup):
    # get the last refreshed date
    if soup.find('time'):
        time = soup.find('time').getText()
        time = datetime.datetime.strptime(time, '%B %d, %Y').date()
    else:
        time = datetime.date.today()
        # the below gets the date of the next sunday
        time = time + datetime.timedelta( (6-today.weekday()) % 7 )

    return time
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

def main_scraper(soup, time):
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

    print(f'Data retrieved.')
    return book_dict


def scrape_and_gzip():

    soup = get_soup()
    time = get_refresh_date(soup)
    book_dict = main_scraper(soup, time)

    file_name = f'{time}.json'

    print(f'Gzipping to a json file @ {file_name}')

    with gzip.open(f'{file_name}', 'wt', encoding='utf-8') as zipfile:
        json.dump(book_dict, zipfile, indent=4)

    return file_name