import requests
from bs4 import BeautifulSoup

#launch url
url = 'https://www.nytimes.com/books/best-sellers/'

# get the page
print('Opening the url')
page = requests.get(url)

# parse the html using beautiful soup and store in variable `soup`
print('pulling the html')
soup = BeautifulSoup(page.text, 'html.parser')

section = soup.find_all('section')

book_dict = {}

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

        for book in book_list:
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

                #book_dict[category]['titles'].append(title)

print('book_dict')
print(book_dict)