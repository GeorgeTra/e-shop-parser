import csv
import requests
from bs4 import BeautifulSoup
from os import getcwd, makedirs
from os.path import basename, exists, join
from src.parse2 import products_list
from tqdm import tqdm


def parse_product_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    cats = [cat.text for cat in soup.find('ul', class_='breadcrumb').findChildren('a')]

    sep_cats = [cat.replace('\n                                    ', '').
                replace('\n                                ', '') for cat in cats]

    last_cat = [cat.text for cat in soup.find('ul', class_='breadcrumb').
                findChildren('li')][-1].replace('  ', '').replace('\n', '')

    sep_cats.append(last_cat)

    if len(sep_cats) == 3:
        sep_cats.append('0')
    elif len(sep_cats) == 2:
        sep_cats.extend(['0', '0'])

    main_title = soup.find('span', class_='title-main')
    if main_title:
        main_title = main_title.text.split(' | ')
        product_code = main_title[0]
        brand = main_title[1]
    else:
        product_code = '0'
        brand = '0'

    product_name = soup.find('span', class_='title-name')
    if product_name:
        product_name = product_name.text
    else:
        product_name = '0'

    product_desc = soup.find('p', class_='desc')
    if product_desc:
        product_desc = product_desc.text.replace('\n                        ', '') \
            .replace('\n                    ', '')
    else:
        product_desc = '0'
    if product_desc == '\n':
        product_desc = '0'

    condition = soup.find('p', class_='state')
    if condition:
        condition = condition.text.replace('\n', '').replace(' ', '').replace('en', 'e n')
    else:
        condition = '0'

    price = soup.find('p', class_='price')
    if price:
        price = price.text.replace('€\xa0Tax Excl.\n', '').replace('\n', '').replace(' ', '')
    else:
        price = '0'

    photo = soup.find('img', class_='main-image')
    if photo:
        photo = photo['src']
        upload_dir = join(getcwd(), "photos")
        if not exists(upload_dir):
            makedirs(upload_dir)
        photo_path = join("photos", basename(photo))

        with open(photo_path, "wb") as f:
            f.write(requests.get(photo).content)
    else:
        photo_path = '0'

    product_features_list_part2 = [product_code, brand, product_name, product_desc, condition, price, photo_path]

    end_product_features_list = sep_cats[1:] + product_features_list_part2 \
        if sep_cats != ['Home'] else ['0', '0', '0'] + product_features_list_part2

    return end_product_features_list


# products_list = ['https://market.kheoos.com/en/p/network-switches/3com-3c16792a-officeconnect-dual-speed-switch-16/kh015D819_BBE', 'https://market.kheoos.com/en/p/price-on-request/3m-92-a-25-f/kh010B318_BFR', 'https://market.kheoos.com/en/p/price-on-request/3m-10120-3000ve/kh010R656_BCZ', 'https://market.kheoos.com/en/p/price-on-request/3m-8822/kh011B490_DES', 'https://market.kheoos.com/en/p/price-on-request/3m-n7e50-7516pk-20/kh012O221_BFR', 'https://market.kheoos.com/en/p/price-on-request/3m-92-nba4/kh012W715_BFR', 'https://market.kheoos.com/en/p/price-on-request/3m-78-8054-8813-3/kh013Y897_BLT', 'https://market.kheoos.com/en/p/price-on-request/3m-volpccg/kh015T185_BFR', 'https://market.kheoos.com/en/p/price-on-request/3m-volppcbf16k/kh018N292_BFR', 'https://market.kheoos.com/en/p/price-on-request/3m-69-3-4-x66/kh019Q909_BFR', 'https://market.kheoos.com/en/p/price-on-request/3m-volpccr/kh019Q947_BFR', 'https://market.kheoos.com/en/p/safety-io-modules/a-puissance-3-naev30-di2n-c024-0-logical-processing-modules/kh016M822_BCZ', 'https://market.kheoos.com/en/p/hydraulic-filters/aaf-international-dripak-sf-pocket-filter/kh010I046_BFR', 'https://market.kheoos.com/en/p/hydraulic-filters/aaf-international-amerglas-box-disposable-panel-filters/kh011D236_BFR', 'https://market.kheoos.com/en/p/hydraulic-filters/aaf-international-amair-300-prefilters-high-quality/kh011H676_BFR', 'https://market.kheoos.com/en/p/hydraulic-filters/aaf-international-astrocel-i-hepa-astrocel-i/kh012G160_BFR', 'https://market.kheoos.com/en/p/hydraulic-filters/aaf-international-chevronet-4-m1-287x594x50-lightweight-pleated-filter/kh014J175_BFR', 'https://market.kheoos.com/en/p/hydraulic-filters/aaf-international-netply-r35-1-light-pleated-filters/kh015C994_BFR', 'https://market.kheoos.com/en/p/hydraulic-filters/aaf-international-metanet-71-1111-1237-filter-light-metal/kh017P694_BFR', 'https://market.kheoos.com/en/p/price-on-request/abb-2tla020051r0000/kh010A084_BCZ', 'https://market.kheoos.com/en/p/price-on-request/abb-tp40d70451/kh010C428_BFR', 'https://market.kheoos.com/en/p/price-on-request/abb-16836616/kh010D564_BFR', 'https://market.kheoos.com/en/p/price-on-request/abb-1svr430800r9100/kh010F519_BFR', 'https://market.kheoos.com/en/p/contactors/abb-b12-40-00-contactor/kh010F813_BFR', 'https://market.kheoos.com/en/p/auxiliary-contacts/abb-gh-s270-1916-r1-auxiliary-contact/kh010G696_BFR', 'https://market.kheoos.com/en/p/machine-guarding-accessories/abb-2tla020039r0800-dalton-tongue-a/kh010G775_DES', 'https://market.kheoos.com/en/p/price-on-request/abb-2tla020046r0000/kh010H856_BCZ']
# products_list = ['https://market.kheoos.com/en/p/network-switches/3com-3c16792a-officeconnect-dual-speed-switch-16/kh015D819_BBE', 'https://market.kheoos.com/en/p/price-on-request/3m-92-a-25-f/kh010B318_BFR']
# products_list = ['https://market.kheoos.com/en/p/network-switches/3com-3c16792a-officeconnect-dual-speed-switch-16/kh015D819_BBE']
# products_list = ['https://market.kheoos.com/en/p/price-on-request/abb-2tla020051r0000/kh010A084_BCZ']

product_features_list = []

for i in tqdm(products_list):
    # print(parse_product_page(i))
    p = (parse_product_page(i))
    product_features_list.append(p)


# print(product_features_list)


def csv_maker(lst):
    col_names = ['Category 1', 'Category 2', 'Category 3', 'Item number', 'Brand', 'Product name', 'Description',
                 'Condition', 'Price', 'Photo path']

    with open('src/products.csv', 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(col_names)
        for item in lst:
            writer.writerow(item)


csv_maker(product_features_list)

# print(products_list)
