import requests
from bs4 import BeautifulSoup


def parse_first_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    letter_list = [chr(letter) for letter in range(65, 91)]
    letter_list.insert(0, '0-9')

    print(letter_list)

    final_brands_list = []

    for i in letter_list:

        brand_links = soup.find('section', letterfilter=f'{i}').findChildren('a')
        brands_list = ['https://market.kheoos.com'+link.get('href') for link in brand_links]
        final_brands_list += brands_list

    return final_brands_list


page_url = 'https://market.kheoos.com/en/b/allbrands?slug=all%20brands'
# print(parse_first_page(page_url))




