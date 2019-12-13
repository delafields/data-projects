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

company_categories = ['retail', 'financial-services', 'technology', 'manufacturer', 'energy', 'food', 
                      'insurance', 'natural-resource','health-beauty', 'auto', 'pharmaceuticals', 
                      'transport-company', 'computer-electronics' 'animation-industry', 'aerospace-and-defense', 
                      'chemicals', 'construction', 'travel', 'casino-hotel', 'supplier', 'real-estate']

company_categories_temp = ['real-estate']

df = pd.DataFrame()

# got this by running the script through 
# checking for the max number of colors given
max_colors = 8

def url_to_company_name(text):
  # finds the second to last /
  url_end =  text.rfind('/', 0, text.rfind('/')) + 1

  text = text[url_end:]

  # if `text` contains -color-palette, remove it
  if re.match('(-color-palette)$', text):
    text = re.sub('(-color-palette/)$', '', text)
  
  # remove trailing /
  text = re.sub('/', '', text)

  return text

max_colors = 0

for category in company_categories:

    print(f'Starting category {category}')

    main_page = get_page_html(f'{base_url}{category}')

    soup = BeautifulSoup(main_page.text, 'html.parser')

    companies = soup.find_all('a', attrs={'class': 'wpgb-card-layer-link'})

    # there are duplicate `a`'s for each company above
    companies = companies[::2]

    for company in companies:

        company_data = {}

        company_url = company['href']

        company_name = url_to_company_name(company_url)
        print(f'company name: {company_name}')

        company_page = get_page_html(f'{company_url}')

        company_soup = BeautifulSoup(company_page.text, 'html.parser')

        hex_colors = company_soup.find_all('span', text=re.compile('^#(?:[0-9a-fA-F]{3}){1,2}$'))

        company_colors = [color.text for color in hex_colors]

        #max_colors = max(max_colors, len(company_colors))

        print(f'{company_name} colors are: {company_colors}')
        #for color in hex_colors: print(color.text)

        # 1 because [0] is the main pages logo
        company_image = company_soup.find_all('img', attrs={'class': 'fl-photo-img'})[1]['src']

        print(f'{company_name}\'s logo is @ {company_image}')

        # dropping data
        company_data['company'] = company_name
        company_data['category'] = category
        #company_data['logo_location'] = logo_location
        # dropping colors in
        for i in range(1, max_colors+1):
            if i <= len(hex_colors):
                company_data[f'color_{i}'] = hex_colors[i - 1]
            else:
                company_data[f'color_{i}'] = ''

        df = df.append(company_data, ignore_index = True)

#print(f'max colors = {max_colors}')
# 8