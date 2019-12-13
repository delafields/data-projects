from bs4 import BeautifulSoup
import pandas as pd
import requests
import re

base_url = 'https://boldwebdesign.com.au/colour-palettes/?_button='

def get_page_html(url):
  print(f'Opening {url}')
  try:
      headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
      main_page = requests.get(url, headers=headers, timeout=5)
      print('Successfully opened url')
  except requests.ConnectionError as e:
      print("Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
      print(str(e))
  except requests.Timeout as e:
      print("Timeout Error")
      print(str(e))
  return (main_page)

company_categories = ['retail', 'financial-services', 'technology',
                      'manufacturer', 'energy', 'food', 'insurance',
                      'natural-resource','health-beauty', 'auto', 
                      'pharmaceuticals', 'transport-company', 'computer-electronics'
                      'animation-industry', 'aerospace-and-defense', 'chemicals', 'construction', 'travel', 'casino-hotel', 'supplier', 'real-estate']


main_page = get_page_html(f'{base_url}real-estate')

soup = BeautifulSoup(main_page.text, 'html.parser')

companies = soup.find_all('a', attrs={'class': 'wpgb-card-layer-link'})

first_company = companies[0]['href']

def find_second_last(text, pattern):
  return text.rfind(pattern, 0, text.rfind(pattern))

start = find_second_last(first_company, '/') + 1

# 15 is where the company name ends
print('company name: ', first_company[start:-15])

company_page = get_page_html(f'{first_company}')

company_soup = BeautifulSoup(company_page.text, 'html.parser')

hex_colors = company_soup.find_all('span', text=re.compile('^#(?:[0-9a-fA-F]{3}){1,2}$'))

for color in hex_colors:
  print(color.text)

# 1 because [0] is the main pages logo
company_image = company_soup.find_all('img', attrs={'class': 'fl-photo-img'})[1]['src']

print(company_image)