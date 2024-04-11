import requests
from bs4 import BeautifulSoup
from src.parse1 import parse_first_page
from tqdm import tqdm

page_url = 'https://market.kheoos.com/en/b/allbrands?slug=all%20brands'

brands_list1 = parse_first_page(page_url)

brands_list_f = ['https://market.kheoos.com/en/b/facom', 'https://market.kheoos.com/en/b/fag', 'https://market.kheoos.com/en/b/fagor', 'https://market.kheoos.com/en/b/fair-rite-products', 'https://market.kheoos.com/en/b/fairchild', 'https://market.kheoos.com/en/b/fairchild-semiconductor', 'https://market.kheoos.com/en/b/fanuc', 'https://market.kheoos.com/en/b/fastenal', 'https://market.kheoos.com/en/b/fath', 'https://market.kheoos.com/en/b/faulhaber', 'https://market.kheoos.com/en/b/ferraz', 'https://market.kheoos.com/en/b/ferraz-shawmut', 'https://market.kheoos.com/en/b/ferroflex', 'https://market.kheoos.com/en/b/ferryproduits', 'https://market.kheoos.com/en/b/festo', 'https://market.kheoos.com/en/b/fibro', 'https://market.kheoos.com/en/b/filcom', 'https://market.kheoos.com/en/b/filton', 'https://market.kheoos.com/en/b/finder', 'https://market.kheoos.com/en/b/finn-power', 'https://market.kheoos.com/en/b/fischerporter', 'https://market.kheoos.com/en/b/fischer-connectors', 'https://market.kheoos.com/en/b/fisher', 'https://market.kheoos.com/en/b/fisher-controls', 'https://market.kheoos.com/en/b/fisher-rosemount', 'https://market.kheoos.com/en/b/fitok', 'https://market.kheoos.com/en/b/flaig', 'https://market.kheoos.com/en/b/flexlink', 'https://market.kheoos.com/en/b/flowserve', 'https://market.kheoos.com/en/b/flowtechnologybenelux', 'https://market.kheoos.com/en/b/flygt', 'https://market.kheoos.com/en/b/forbo', 'https://market.kheoos.com/en/b/forbosiegling', 'https://market.kheoos.com/en/b/fortron', 'https://market.kheoos.com/en/b/frank', 'https://market.kheoos.com/en/b/fronius', 'https://market.kheoos.com/en/b/fst', 'https://market.kheoos.com/en/b/fyh']

brands_list_facom_fag = ['https://market.kheoos.com/en/b/facom', 'https://market.kheoos.com/en/b/fag']
brands_list_long = ['https://market.kheoos.com/en/b/fanuc', 'https://market.kheoos.com/en/b/fastenal', 'https://market.kheoos.com/en/b/fath', 'https://market.kheoos.com/en/b/faulhaber', 'https://market.kheoos.com/en/b/ferraz', 'https://market.kheoos.com/en/b/ferraz-shawmut', 'https://market.kheoos.com/en/b/ferroflex', 'https://market.kheoos.com/en/b/ferryproduits', 'https://market.kheoos.com/en/b/festo']


def parse_brand(brands_list):
    products_list = []

    for i in tqdm(brands_list):
        response = requests.get(i)

        soup = BeautifulSoup(response.content, 'html.parser')

        product_pages_hrefs = soup.find(class_='ps-pagination').findChildren('a')

        product_pages_links = [link.get('href') for link in product_pages_hrefs]

        product_pages_full_links = []

        for item in product_pages_links:
            if item is not None:
                product_pages_full_links.append('https://market.kheoos.com' + item)

        for link in product_pages_full_links:
            response = requests.get(link)

            soup = BeautifulSoup(response.content, 'html.parser')

            goods_links = soup.find(class_='results-products-container').findChildren('a')

            products = [link.get('href') for link in goods_links]

            for item in products:
                if item is not None:
                    products_list.append('https://market.kheoos.com' + item)

    return products_list
    # return product_pages_full_links


products_list = parse_brand(brands_list1)
# products_list = parse_brand(brands_list_f)
# products_list = parse_brand(brands_list_fag)
# products_list = parse_brand(brands_list_facom_fag)
# products_list = parse_brand(brands_list_long)

print(products_list)

# products_fag = ['https://market.kheoos.com/en/p/roller-bearings/fag-6302-deep-groove-ball-bearing/kh011F240_AFR', 'https://market.kheoos.com/en/p/roller-bearings/fag-6017-deep-groove-ball-bearings/kh011W883_AFR', 'https://market.kheoos.com/en/p/roller-bearings/fag-1203-tv-ball-bearing/kh012D629_AFR', 'https://market.kheoos.com/en/p/price-on-request/fag-20212t/kh012F777_BDE', 'https://market.kheoos.com/en/p/roller-bearings/fag-7202-b-tvp-ball-bearing/kh012R784_AFR', 'https://market.kheoos.com/en/p/roller-bearings/fag-4203bb-tvh-deep-groove-ball-bearing/kh012V918_BFR', 'https://market.kheoos.com/en/p/price-on-request/fag-6008-2rsr/kh012X356_AFR', 'https://market.kheoos.com/en/p/roller-bearings/fag-6301-2zr-deep-groove-ball-bearings-single-row/kh013A928_ADE', 'https://market.kheoos.com/en/p/roller-bearings/fag-6005-ball-bearing/kh013H032_BFR', 'https://market.kheoos.com/en/p/roller-bearings/fag-6307-ball-bearing/kh013K889_BFR', 'https://market.kheoos.com/en/p/price-on-request/fag-61804-2rsr-hlc/kh014O911_DFR', 'https://market.kheoos.com/en/p/price-on-request/fag-h2309/kh015B167_AFR', 'https://market.kheoos.com/en/p/spherical-bearings/fag-20415mb-spherical-roller-bearing/kh015B226_BBE', 'https://market.kheoos.com/en/p/roller-bearings/fag-6211-open-deep-groove-ball-bearing/kh015C032_BFR', 'https://market.kheoos.com/en/p/price-on-request/fag-6200z-c3/kh015E694_BCZ', 'https://market.kheoos.com/en/p/roller-bearings/fag-625z-ball-bearing/kh015K946_BFR', 'https://market.kheoos.com/en/p/price-on-request/fag-52207/kh015S181_AFR', 'https://market.kheoos.com/en/p/spherical-bearings/fag-22208-e1-k-spherical-roller-bearing--40x80x23mm/kh015S926_BIT', 'https://market.kheoos.com/en/p/roller-bearings/fag-51110-ball-thrust/kh015W054_BFR', 'https://market.kheoos.com/en/p/roller-bearings/fag-1201-tv-ball-bearing/kh015X007_AFR', 'https://market.kheoos.com/en/p/roller-bearings/fag-16004-ball-bearing/kh017E758_BFR', 'https://market.kheoos.com/en/p/roller-bearings/fag-3204-b-2rs-tvh-ball-bearing/kh017I981_BFR', 'https://market.kheoos.com/en/p/price-on-request/fag-nutr45100/kh017S168_BFR', 'https://market.kheoos.com/en/p/roller-bearings/fag-2206tv-self-aligning-ball-bearing-double-row/kh017Y185_AFR', 'https://market.kheoos.com/en/p/price-on-request/fag-63801-2rsr-hlc/kh018M764_BFR', 'https://market.kheoos.com/en/p/roller-bearings/fag-hss7006e-t-p4s-ul-ball-bearing/kh018S581_BIT', 'https://market.kheoos.com/en/p/roller-bearings/fag-62206-2rsr-roller-bearing/kh018X781_BFR', 'https://market.kheoos.com/en/p/roller-bearings/fag-603-hlc-deep-groove-ball-bearing/kh019I706_BFR', 'https://market.kheoos.com/en/p/price-on-request/fag-nu306-e-tvp2-c3/kh019Q270_AFR']

print(len(products_list))