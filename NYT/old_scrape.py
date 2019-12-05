import requests
import re
import json
from bs4 import BeautifulSoup

#launch url
url = 'https://www.nytimes.com/books/best-sellers/'

# get the page
print('Opening the url')

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }

try:
    page = requests.get(url, headers=headers, timeout=5)
except requests.ConnectionError as e:
    print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
    print(str(e))
except requests.Timeout as e:
    print("OOPS!! Timeout Error")
    print(str(e))
except requests.RequestException as e:
    print("OOPS!! General Error")
    print(str(e))
except KeyboardInterrupt:
    print("Someone closed the program")

# parse the html using beautiful soup and store in variable `soup`
print('pulling the html')
soup = BeautifulSoup(page.text, 'html.parser')

section = soup.find_all('section')

book_dict = {}

def parse_weeks(text):
    new_book = re.compile('New')
    num_weeks = re.compile('\d+')

    if new_book.search(text):
        return 'New'

    elif re.findall(num_weeks, text):
        num_weeks = re.findall(num_weeks, weeks)
        return ''.join(num_weeks) + ' weeks'

    else:
        return 'N/A'

for category in section:
    if category.find('h2'):
        # get book category
        category_name = category.find('h2').getText()
        #print('category_name: ', category_name)
        # get book title & author

        book_dict[category_name] = {}

        book_list = category.find_all('li')

        titles = []
        authors = []
        week = []

        for book in book_list:
            if book.find('p'):
                weeks = book.find('p').getText()
                #print(parse_weeks(weeks))
                week.append(parse_weeks(weeks))

            if book.find('h3', attrs={'itemprop': 'name'}):
                title = book.find('h3', attrs={'itemprop': 'name'}).getText()
                author = book.find('p', attrs={'itemprop': 'author'}).getText()
                #print('title: ', title)
                #print('author: ', author)

                titles.append(title)
                authors.append(author[3:])

        #print('all titles: ', titles)
        #print('all authors: ', authors)

        book_dict[category_name]['titles']  = titles
        book_dict[category_name]['authors'] = authors
        book_dict[category_name]['weeks'] = week

                #book_dict[category]['titles'].append(title)

print('book_dict')
#print(book_dict)
temp = json.dumps(book_dict)
print(temp)