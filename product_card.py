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

    if len(sep_cats) == 4:
        sep_cats.append('0')
    elif len(sep_cats) == 3:
        sep_cats.extend(['0', '0'])
    elif len(sep_cats) == 2:
        sep_cats.extend(['0', '0', '0'])

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
    else:
        photo_path = '0'
    if photo:
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
        if sep_cats != ['Home'] else ['0', '0', '0', '0'] + product_features_list_part2

    return end_product_features_list


# products_list = ['https://market.kheoos.com/en/p/network-switches/3com-3c16792a-officeconnect-dual-speed-switch-16/kh015D819_BBE', 'https://market.kheoos.com/en/p/price-on-request/3m-92-a-25-f/kh010B318_BFR', 'https://market.kheoos.com/en/p/price-on-request/3m-10120-3000ve/kh010R656_BCZ', 'https://market.kheoos.com/en/p/price-on-request/3m-8822/kh011B490_DES', 'https://market.kheoos.com/en/p/price-on-request/3m-n7e50-7516pk-20/kh012O221_BFR', 'https://market.kheoos.com/en/p/price-on-request/3m-92-nba4/kh012W715_BFR', 'https://market.kheoos.com/en/p/price-on-request/3m-78-8054-8813-3/kh013Y897_BLT', 'https://market.kheoos.com/en/p/price-on-request/3m-volpccg/kh015T185_BFR', 'https://market.kheoos.com/en/p/price-on-request/3m-volppcbf16k/kh018N292_BFR', 'https://market.kheoos.com/en/p/price-on-request/3m-69-3-4-x66/kh019Q909_BFR', 'https://market.kheoos.com/en/p/price-on-request/3m-volpccr/kh019Q947_BFR', 'https://market.kheoos.com/en/p/safety-io-modules/a-puissance-3-naev30-di2n-c024-0-logical-processing-modules/kh016M822_BCZ', 'https://market.kheoos.com/en/p/hydraulic-filters/aaf-international-dripak-sf-pocket-filter/kh010I046_BFR', 'https://market.kheoos.com/en/p/hydraulic-filters/aaf-international-amerglas-box-disposable-panel-filters/kh011D236_BFR', 'https://market.kheoos.com/en/p/hydraulic-filters/aaf-international-amair-300-prefilters-high-quality/kh011H676_BFR', 'https://market.kheoos.com/en/p/hydraulic-filters/aaf-international-astrocel-i-hepa-astrocel-i/kh012G160_BFR', 'https://market.kheoos.com/en/p/hydraulic-filters/aaf-international-chevronet-4-m1-287x594x50-lightweight-pleated-filter/kh014J175_BFR', 'https://market.kheoos.com/en/p/hydraulic-filters/aaf-international-netply-r35-1-light-pleated-filters/kh015C994_BFR', 'https://market.kheoos.com/en/p/hydraulic-filters/aaf-international-metanet-71-1111-1237-filter-light-metal/kh017P694_BFR', 'https://market.kheoos.com/en/p/price-on-request/abb-2tla020051r0000/kh010A084_BCZ', 'https://market.kheoos.com/en/p/price-on-request/abb-tp40d70451/kh010C428_BFR', 'https://market.kheoos.com/en/p/price-on-request/abb-16836616/kh010D564_BFR', 'https://market.kheoos.com/en/p/price-on-request/abb-1svr430800r9100/kh010F519_BFR', 'https://market.kheoos.com/en/p/contactors/abb-b12-40-00-contactor/kh010F813_BFR', 'https://market.kheoos.com/en/p/auxiliary-contacts/abb-gh-s270-1916-r1-auxiliary-contact/kh010G696_BFR', 'https://market.kheoos.com/en/p/machine-guarding-accessories/abb-2tla020039r0800-dalton-tongue-a/kh010G775_DES', 'https://market.kheoos.com/en/p/price-on-request/abb-2tla020046r0000/kh010H856_BCZ']
# products_list = ['https://market.kheoos.com/en/p/network-switches/3com-3c16792a-officeconnect-dual-speed-switch-16/kh015D819_BBE', 'https://market.kheoos.com/en/p/price-on-request/3m-92-a-25-f/kh010B318_BFR']
# products_list = ['https://market.kheoos.com/en/p/network-switches/3com-3c16792a-officeconnect-dual-speed-switch-16/kh015D819_BBE']
# products_list = ['https://market.kheoos.com/en/p/price-on-request/abb-2tla020051r0000/kh010A084_BCZ']
# products_list = ['https://market.kheoos.com/en/p/network-switches/3com-3c16792a-officeconnect-dual-speed-switch-16/kh015D819_BBE', 'https://market.kheoos.com/en/p/price-on-request/3m-92-a-25-f/kh010B318_BFR', 'https://market.kheoos.com/en/p/price-on-request/3m-10120-3000ve/kh010R656_BCZ', 'https://market.kheoos.com/en/p/price-on-request/3m-8822/kh011B490_DES', 'https://market.kheoos.com/en/p/price-on-request/3m-n7e50-7516pk-20/kh012O221_BFR', 'https://market.kheoos.com/en/p/price-on-request/3m-92-nba4/kh012W715_BFR', 'https://market.kheoos.com/en/p/price-on-request/3m-78-8054-8813-3/kh013Y897_BLT', 'https://market.kheoos.com/en/p/price-on-request/3m-volpccg/kh015T185_BFR', 'https://market.kheoos.com/en/p/price-on-request/3m-volppcbf16k/kh018N292_BFR', 'https://market.kheoos.com/en/p/price-on-request/3m-69-3-4-x66/kh019Q909_BFR', 'https://market.kheoos.com/en/p/price-on-request/3m-volpccr/kh019Q947_BFR', 'https://market.kheoos.com/en/p/drills/xebec-a21-cb25m-brush/kh010W553_BCZ', 'https://market.kheoos.com/en/p/tool--machine-components/xebec-s25m-sleeve/kh018Q355_BCZ', 'https://market.kheoos.com/en/p/price-on-request/xilinx-xc3090a-7pg175i/kh015V355_BFR', 'https://market.kheoos.com/en/p/price-on-request/yamatake-hpj-a21/kh017S540_DES', 'https://market.kheoos.com/en/p/price-on-request/yamawa-tcnr6-0j3/kh017Q756_BCZ', 'https://market.kheoos.com/en/p/servo-motors/yaskawa-usafed-13fa2-ac-servo-motor/kh010R075_DFR', 'https://market.kheoos.com/en/p/price-on-request/yaskawa-hw9380915-a/kh011A096_BCZ', 'https://market.kheoos.com/en/p/inverter-drives/yaskawa-cimr-j7aa20p2-drive/kh011C795_ECZ', 'https://market.kheoos.com/en/p/servo-motors/yaskawa-sgmgv-13dda6h-servo-motor/kh011N368_ACZ', 'https://market.kheoos.com/en/p/inverter-drives/yaskawa-cimr-ac4a0675aaa-high-performance-vector-controlled-frequency-variator/kh011X603_ECZ', 'https://market.kheoos.com/en/p/inverter-drives/yaskawa-cacr-sr10bb1bf-servo-drive/kh011Z269_DFR', 'https://market.kheoos.com/en/p/inverter-drives/yaskawa-cpcr-mr05c-servo-drive/kh012B752_BSK', 'https://market.kheoos.com/en/p/inverter-drives/yaskawa-cacr-sr10sb1bf-servo-drive/kh012C874_DFR', 'https://market.kheoos.com/en/p/servo-motors/yaskawa-jusp-acpcb05jaa-servo-drive/kh012F517_BCZ', 'https://market.kheoos.com/en/p/price-on-request/yaskawa-jancd-cg31-24/kh012G184_DFR', 'https://market.kheoos.com/en/p/inverter-drives/yaskawa-cimr-e7c4220-inverters/kh012R009_ECZ', 'https://market.kheoos.com/en/p/servo-motors/yaskawa-sgmdh-12a2a-yr12-ac-servo-motor/kh013H301_BCZ', 'https://market.kheoos.com/en/p/price-on-request/yaskawa-hw9380947-a/kh013H318_BCZ', 'https://market.kheoos.com/en/p/price-on-request/yaskawa-hw9280631-a/kh013Q092_BCZ', 'https://market.kheoos.com/en/p/inverter-drives/yaskawa-sgmas-01a2a-yr11-drives/kh013U408_BCZ', 'https://market.kheoos.com/en/p/price-on-request/yaskawa-sgdh-01ae-oy/kh013U664_BCZ', 'https://market.kheoos.com/en/p/price-on-request/yaskawa-jancd-22-3/kh014A485_DFR', 'https://market.kheoos.com/en/p/plc-cpus/yaskawa-jancd-pc20-pc-board/kh014E128_DFR', 'https://market.kheoos.com/en/p/inverter-drives/yaskawa-cimr-e7z4220-drive/kh014G440_ECZ', 'https://market.kheoos.com/en/p/gearboxes/yaskawa-hw9380623-a-reducer-harmonic/kh014R058_BCZ', 'https://market.kheoos.com/en/p/printers-scanners--printing-supplies/yokogawa-b9565as-pin-retaining-clip/kh012Q311_BFR', 'https://market.kheoos.com/en/p/printers-scanners--printing-supplies/yokogawa-b9906ja-chart-recorder-ribbon/kh014Y365_BFR', 'https://market.kheoos.com/en/p/printers-scanners--printing-supplies/yokogawa-b9901ax-ribbon-cassette/kh015R342_BFR', 'https://market.kheoos.com/en/p/price-on-request/yokohama-rubber-1022-16/kh015S219_BFR', 'https://market.kheoos.com/en/p/price-on-request/yudo-sas-32-vc-232/kh010K937_DES', 'https://market.kheoos.com/en/p/price-on-request/yudo-nztpic161850/kh011C130_DES', 'https://market.kheoos.com/en/p/price-on-request/yudo-nztpic160850/kh012W442_DES', 'https://market.kheoos.com/en/p/price-on-request/yudo-nztpic163450/kh014G380_DES', 'https://market.kheoos.com/en/p/butterfly-valves/yudo-sas-42-vc-310-single-valve/kh014U633_DES', 'https://market.kheoos.com/en/p/price-on-request/yudo-nztpic161350/kh015U684_DES', 'https://market.kheoos.com/en/p/price-on-request/yudo-nztpic162150/kh017E336_DES', 'https://market.kheoos.com/en/p/price-on-request/yudo-sas-32-vc-182/kh017I782_DES', 'https://market.kheoos.com/en/p/price-on-request/yudo-nztpic162650/kh017L392_DES', 'https://market.kheoos.com/en/p/price-on-request/yudo-sas-32-vc-252/kh018A930_DES', 'https://market.kheoos.com/en/p/price-on-request/yudo-nztpic160650/kh018E648_DES', 'https://market.kheoos.com/en/p/price-on-request/yudo-nztpic162353/kh018Y023_DES', 'https://market.kheoos.com/en/p/cartridge-heaters/zd-motor-5292472-motor/kh011H927_BFR', 'https://market.kheoos.com/en/p/price-on-request/zebra-zd41022-d0ee00ez/kh015Y848_BCZ', 'https://market.kheoos.com/en/p/price-on-request/zebra-ls3408-fz/kh018R216_EFR', 'https://market.kheoos.com/en/p/printers-scanners--printing-supplies/zebra-g32433m-printhead/kh019X000_AFR', 'https://market.kheoos.com/en/p/price-on-request/zf-friedrichshafen-db2c-a1ld/kh012G502_BFR', 'https://market.kheoos.com/en/p/price-on-request/ziehl-abegg-qk10a-2dm-38-fe/kh011J139_BFR', 'https://market.kheoos.com/en/p/price-on-request/zimmer-group-mks1501a/kh010L619_BDE', 'https://market.kheoos.com/en/p/price-on-request/zimmer-group-mks2001a/kh017I676_BDE', 'https://market.kheoos.com/en/p/price-on-request/zimmer-group-mkr-4000-a/kh017T557_BDE', 'https://market.kheoos.com/en/p/price-on-request/zkl-51101-a/kh014Y740_BCZ', 'https://market.kheoos.com/en/p/price-on-request/zkl-32012ax/kh015B740_BCZ']
# products_list = ['https://market.kheoos.com/en/p/drills/xebec-a21-cb25m-brush/kh010W553_BCZ', 'https://market.kheoos.com/en/p/network-switches/3com-3c16792a-officeconnect-dual-speed-switch-16/kh015D819_BBE']
# products_list = ['https://market.kheoos.com/en/p/din-rail-terminal-accessories/wago-769-110-x-com-1-conductor-female-connector/kh010G210_BFR', 'https://market.kheoos.com/en/p/flat-connectors/wago-209-602-wsb-marking-card/kh010G216_BFR', 'https://market.kheoos.com/en/p/connection-terminals/wago-769-102-x-com-1-conductor-female-connector/kh010I957_BFR', 'https://market.kheoos.com/en/p/din-rail-terminal-accessories/wago-780-453-staggered-jumper/kh010M883_BFR', 'https://market.kheoos.com/en/p/d-sub-connectors/wago-890-213-plug/kh010P059_BFR', 'https://market.kheoos.com/en/p/connection-terminals/wago-870-101-x-com-1-conductor-1-pin-double-deck-receptacle-terminal-block/kh010S186_BFR', 'https://market.kheoos.com/en/p/din-rail-terminal-accessories/wago-2010-1307-terminal-block/kh010T773_BFR', 'https://market.kheoos.com/en/p/connection-terminals/wago-280-641-terminal-block/kh010U201_BFR', 'https://market.kheoos.com/en/p/price-on-request/wago-870-402/kh011C032_BFR', 'https://market.kheoos.com/en/p/d-sub-connectors/wago-890-203-socket/kh011H015_BFR', 'https://market.kheoos.com/en/p/price-on-request/wago-248-505/kh011N157_BFR', 'https://market.kheoos.com/en/p/price-on-request/wago-769-105/kh011S023_BFR', 'https://market.kheoos.com/en/p/din-rail-terminal-accessories/wago-2002-800-empty-component-plug-housing/kh011V305_BFR', 'https://market.kheoos.com/en/p/din-rail-terminal-accessories/wago-2009-174-test-plug-adapter/kh011W907_BFR', 'https://market.kheoos.com/en/p/din-rail-terminal-accessories/wago-870-681-terminal-block/kh011Y400_BFR', 'https://market.kheoos.com/en/p/din-rail-terminal-accessories/wago-769-108-x-com-1-conductor-female-connector/kh012D055_BFR', 'https://market.kheoos.com/en/p/din-rail-terminal-accessories/wago-780-452-staggered-jumper/kh012D348_BFR', 'https://market.kheoos.com/en/p/connection-terminals/wago-279-673-281-410-terminal-block/kh012T922_BFR', 'https://market.kheoos.com/en/p/cable-marker-accessories/wago-248-570-mini-wsb-marking-card/kh012Y703_BFR', 'https://market.kheoos.com/en/p/plc-i-o-modules/wago-750-513-plc-i-o-module-system-750/kh012Z171_BCZ', 'https://market.kheoos.com/en/p/price-on-request/walterscheid-gev12lr1-4/kh014A105_BBE', 'https://market.kheoos.com/en/p/brake-modules/warner-electric-5375-631-012-magnet-assembly/kh011M917_DFR', 'https://market.kheoos.com/en/p/price-on-request/weidmuller-sail-vsa-3-0u/kh010D652_BHU', 'https://market.kheoos.com/en/p/retaining-clips/weidmuller-trs-120vuc-1co-au-relay-module/kh010T979_BFR', 'https://market.kheoos.com/en/p/connection-terminals/weidmuller-wdu-2-5-gn-feed-through-terminal/kh010V624_BHU', 'https://market.kheoos.com/en/p/price-on-request/weidmuller-pac-s1500-sd25-v1-3m/kh010Z305_BFR', 'https://market.kheoos.com/en/p/price-on-request/weidmuller-ztw-ztl6/kh011C831_BHU', 'https://market.kheoos.com/en/p/pcb-terminal-blocks/weidmuller-slt-5-08-10-180b-sn-or-bx-connector-for-printed-circuit-board/kh011N180_BFR', 'https://market.kheoos.com/en/p/electrical-equipment/weidmuller-zdu-2-5-feed-through-terminal/kh011O422_ACZ', 'https://market.kheoos.com/en/p/plc-accessories/weidmuller-rs-16io-1w-i-r-s-interface/kh011R078_BFR', 'https://market.kheoos.com/en/p/terminal-block-accessories/weidmuller-pac-univ-he10-f-3m-pre-assembled-cable/kh011T174_BFR', 'https://market.kheoos.com/en/p/safety-input---output-terminals/weidmuller-ur20-4ai-ui-16-remote-i-o-module/kh012A727_BHU', 'https://market.kheoos.com/en/p/price-on-request/weidmuller-zad-1-4/kh012E357_BHU', 'https://market.kheoos.com/en/p/price-on-request/weidmuller-ew-35/kh012E559_BHU', 'https://market.kheoos.com/en/p/cartridge-fuses/weidmuller-wgz-24vdc-315a-electronic-fuse/kh012N786_DFR', 'https://market.kheoos.com/en/p/electrical-equipment/weidmuller-wtl-4-2-stb-test-disconnect-terminal/kh012N884_BFR', 'https://market.kheoos.com/en/p/price-on-request/weidmuller-a2t-2-5-ft-pe/kh012O059_ACZ', 'https://market.kheoos.com/en/p/communing-blocks/weidmuller-a2t-2-5-feed-through-terminal/kh012P273_ACZ', 'https://market.kheoos.com/en/p/price-on-request/weidmuller-lm-mt300-15-6-ws/kh012R787_BHU', 'https://market.kheoos.com/en/p/cable-connector--crimping-tools/weidmuller-hdc-c-hd-sm0-75-1-00ag-crimp-contacts/kh012S273_BHU', 'https://market.kheoos.com/en/p/price-on-request/weidmuller-vpu-ii-4-280v-40ka/kh012W551_BCZ', 'https://market.kheoos.com/en/p/connection-terminals/weidmuller-wdu-2-5-bl-terminal-blocks/kh012Z363_BHU', 'https://market.kheoos.com/en/p/touch-screen-hmi-displays/weinview-mt6050ip-human-machine-interface/kh011B615_DES', 'https://market.kheoos.com/en/p/price-on-request/welwyn-wh5-120rji/kh017N095_BFR', 'https://market.kheoos.com/en/p/sensor-reflectors/wenglor-xr96pct2-retro-reflex-sensor-universal/kh011I401_BCZ', 'https://market.kheoos.com/en/p/price-on-request/werma-280-120-55/kh014T684_BFR', 'https://market.kheoos.com/en/p/price-on-request/werma-88430068/kh017T115_BFR', 'https://market.kheoos.com/en/p/price-on-request/werma-482-052-68/kh018F246_BFR', 'https://market.kheoos.com/en/p/price-on-request/werma-95589068/kh018J778_BFR', 'https://market.kheoos.com/en/p/price-on-request/wiedenbach-10-001031-00/kh015J765_BFR', 'https://market.kheoos.com/en/p/price-on-request/wiedenbach-10-001009-05/kh017F176_BFR', 'https://market.kheoos.com/en/p/price-on-request/wieland-71-350-1035-0/kh010X461_BCZ', 'https://market.kheoos.com/en/p/price-on-request/wieland-70-310-1040-0/kh011C809_BCZ', 'https://market.kheoos.com/en/p/price-on-request/wieland-bas-stf-10-25-50/kh012B420_BHU', 'https://market.kheoos.com/en/p/price-on-request/wieland-bas-stf-6-25-50/kh012H301_BHU', 'https://market.kheoos.com/en/p/price-on-request/wieland-bas-bas-gut-gp-6-a/kh013A024_BHU', 'https://market.kheoos.com/en/p/price-on-request/wieland-bas-sts-24-25-50/kh014E525_BHU', 'https://market.kheoos.com/en/p/price-on-request/wieland-bas-buf-10-25-50/kh015O801_BHU', 'https://market.kheoos.com/en/p/cable-connector--crimping-tools/wieland-bas-bas-gut-ga-16-a-enclosure-base/kh016F040_BHU', 'https://market.kheoos.com/en/p/price-on-request/wieland-bas-buf-16-25-50/kh016I392_BHU', 'https://market.kheoos.com/en/p/price-on-request/wieland-bas-bas-gut-gk-6-a/kh018C616_BHU', 'https://market.kheoos.com/en/p/price-on-request/wieland-bas-bas-gut-ga-10-a/kh018Q735_BHU', 'https://market.kheoos.com/en/p/price-on-request/wieland-bas-buf-6-25-50/kh018V123_BHU', 'https://market.kheoos.com/en/p/industrial-interlocks/wieland-bas-bus-24-25-50-female-contact-insert/kh019O109_BHU', 'https://market.kheoos.com/en/p/price-on-request/wieland-bas-stf-16-25-50/kh019T762_BHU', 'https://market.kheoos.com/en/p/price-on-request/wika-mfre-463/kh010H071_BBE', 'https://market.kheoos.com/en/p/price-on-request/wika-mw-463/kh010H847_BBE', 'https://market.kheoos.com/en/p/price-on-request/wika-mfre-1063/kh010W220_BBE', 'https://market.kheoos.com/en/p/pressure-sensors/wika-13072021-pressure-transducer/kh013R244_BFR', 'https://market.kheoos.com/en/p/price-on-request/wika-ms-16063/kh016C333_BBE', 'https://market.kheoos.com/en/p/price-on-request/wika-mw-458/kh016V992_BBE', 'https://market.kheoos.com/en/p/price-on-request/wika-mw-10063/kh017X503_BBE', 'https://market.kheoos.com/en/p/price-on-request/wika-wg63-14b-100g/kh018L266_BBE', 'https://market.kheoos.com/en/p/price-on-request/wika-ms-4063/kh018V183_BBE', 'https://market.kheoos.com/en/p/pressure-sensors/wika-9021302-pressure-sensor/kh019I160_DFR', 'https://market.kheoos.com/en/p/pneumatic--hydraulic-pressure-gauges/wika-mw-2563-pressure-gauge-horizontal/kh019P818_BBE', 'https://market.kheoos.com/en/p/price-on-request/wilo-bl40-160-5-5-2/kh013H562_BFR', 'https://market.kheoos.com/en/p/touch-screen-hmi-displays/winmate-r15l600-obc3-pat-u-15--front-ip65-display/kh011Q776_BFR', 'https://market.kheoos.com/en/p/gearboxes/wittenstein-sp180s-mf2-16-1k1-2s-planetary-reducer/kh010Y725_BCZ', 'https://market.kheoos.com/en/p/price-on-request/wittenstein-tk050s-mf1-4-5k1-1k00/kh019N203_EFR', 'https://market.kheoos.com/en/p/sensor--switch-cables--connectors/woodhead-8a4000-32-single-keyway-field-attachable-connector/kh013I679_AFR', 'https://market.kheoos.com/en/p/price-on-request/workswell-l-wic640-13/kh011A425_BCZ', 'https://market.kheoos.com/en/p/price-on-request/workswell-wti-tpc-001/kh014W524_BCZ', 'https://market.kheoos.com/en/p/price-on-request/workswell-wic-640-fgw/kh017S959_BCZ', 'https://market.kheoos.com/en/p/inductors--coils/wurth-elektronik-744028100-fixed-inductance/kh011G123_BFR', 'https://market.kheoos.com/en/p/price-on-request/wurth-elektronik-615004141121/kh014I033_BFR', 'https://market.kheoos.com/en/p/ferrite-cores/wurth-elektronik-7427009-ferrite/kh016W018_BFR', 'https://market.kheoos.com/en/p/inductors--coils/wurth-elektronik-742792114-inductance-cms-multicouche/kh017X715_BFR']
# wrong_product = ['https://market.kheoos.com/en/p/din-rail-terminal-accessories/wago-2009-174-test-plug-adapter/kh011W907_BFR']


product_features_list = []
print(len(products_list))

for i in tqdm(products_list):
    # print(parse_product_page(i))
    p = (parse_product_page(i))
    product_features_list.append(p)


# print(product_features_list)


def csv_maker(lst):
    col_names = ['Category 1', 'Category 2', 'Category 3', 'Category 4', 'Item number', 'Brand', 'Product name', 'Description',
                 'Condition', 'Price', 'Photo path']

    with open('src/products.csv', 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(col_names)
        for item in tqdm(lst):
            writer.writerow(item)


csv_maker(product_features_list)

# print(products_list)
