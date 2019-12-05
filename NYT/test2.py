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

time = soup.find('time').getText()
time = datetime.datetime.strptime(time, '%B %d, %Y').date()

section = soup.find_all('section')

book_dict = []

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

        book_list = category.find_all('li')

        for book in book_list:            

            if book.find('h3', attrs={'itemprop': 'name'}):
                title = book.find('h3', attrs={'itemprop': 'name'}).getText()
                title = title.title()

                author = book.find('p', attrs={'itemprop': 'author'}).getText()
                author = re.sub('by ', '', author)

                hashed_book = hashlib.sha1(title.encode('utf8')).hexdigest()

                this_dict = {}

                this_dict['title'] = title
                this_dict['date'] = str(time)
                this_dict['author'] = author
                this_dict['category'] = category_name

            if book.find('p'):
                weeks = book.find('p').getText()

                num = parse_weeks(weeks)
                
                this_dict['weeks_on_list'] = num
                book_dict.append(this_dict)

print('book_dict')
temp = json.dumps(book_dict, indent=4)
print(temp)

with open('data2.json', 'w') as f:
    json.dump(book_dict, f, indent=4)