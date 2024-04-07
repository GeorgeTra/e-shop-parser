import requests
from bs4 import BeautifulSoup
from src.parse1 import parse_first_page


page_url = 'https://market.kheoos.com/en/b/allbrands?slug=all%20brands'

brands_list1 = parse_first_page(page_url)


def parse_brand(brands_list):
    products_list = []

    for i in brands_list:
        response = requests.get(i)

        soup = BeautifulSoup(response.content, 'html.parser')

        goods_links = soup.find(class_='results-products-container').findChildren('a')

        products = [link.get('href') for link in goods_links]

        for item in products:
            if item is not None:
                products_list.append('https://market.kheoos.com' + item)

    return products_list


products_list = parse_brand(brands_list1)

print(products_list)