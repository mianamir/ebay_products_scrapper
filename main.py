from utilities import helpers, data_analysis
import csv

import requests
from bs4 import BeautifulSoup


def get_page(url):
    response = requests.get(url)
    soup = None
    if not response.ok:
        print(f'Server responded: {response.status_code}')
    else:
        soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_cleaned_title(title):
    cleaned_title = title \
        .replace('\xa0', "") \
        .replace('\xa02019-20', "") \
        .replace("🔥", "").replace("💎", "") \
        .replace("Details about  ", "") \
        .replace("\xa0🔥 2019-20", "") \
        .replace("💙", "") \
        .replace("2019 ", "") \
        .replace("2019-20 ", "") \
        .replace("2019-2020 ", "") \
        .replace("19-20 ", "") \
        .replace("2019/20 ", "") \
        .replace("/", "") \
        .replace("PSA 10", "")\
        .replace("psa 10", "")\
        .replace("PSA10", "")\
        .replace("PSA", "")\
        .strip()
    return cleaned_title


def get_detail_data(soup):
    try:
        title = get_cleaned_title(soup.find('h1', id='itemTitle').text)
    except:
        title = None
    try:
        # try:
        #     try:
        #         p = soup.find('span', id='prcIsum').text.strip()
        #     except:
        #         p = soup.find('span', id='mm-saleDscPrc').text.strip()
        # except:
        #     p = soup.find('span', id='prcIsum_bidPrice').text.strip()
        try:
            p = soup.find('span', class_='notranslate vi-VR-cvipPrice') \
                .text \
                .strip()
        except:
            p = soup.find('span', id='prcIsum') \
                .text \
                .strip()
        currency, price = p.split(" ")
    except:
        currency = None
        price = None
    try:
        eBay_item_number = soup.find('div',
                id='descItemNumber').text.strip()
    except:
        eBay_item_number = None
    try:
        product_date = soup.find('span',
                                 id='bb_tlft')\
                                .text\
                                .strip()\
                                .replace("\n\n", " ")
    except:
        product_date = None

    data = {
        'eBay_item_number': eBay_item_number,
        'date': product_date,
        'title': title,
        'price': price,
        'currency': currency
    }
    return data


def get_index_data(soup):
    try:
        a_tags = soup.find_all('a', class_='s-item__link')
    except:
        a_tags = list()
    urls = [item.get('href') for item in a_tags]
    return urls


def set_csv_file_header():
    # setting file title
    with open('output.csv', newline='') as f:
        r = csv.reader(f)
        data = [line for line in r]
    with open('output.csv', 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(
            [
                "#EBay Item Number",
                "Date",
                "Title",
                "Price",
                "Currency",
                "URL"
            ]
        )
        w.writerows(data)


def write_csv(data, url):
    with open('output.csv', 'a') as csv_file:
        writer = csv.writer(csv_file)
        row = [
            data['eBay_item_number'],
            data['date'],
            data['title'],
            data['price'],
            data['currency'],
            url
        ]
        print(row)
        writer.writerow(row)


def get_bgs_9_5_products_url():
    # For customized URL mapping
    keyword = "bgs 9.5 zion williamson silver prizm -draft -emergent -select -mosaic -fireworks -duke -crusade -instant -american"
    # keyword = input("Enter search keyword: ")
    number = str(1)
    # number = input("Enter page no: ")
    base_url = 'https://www.ebay.com/sch/i.html?'
    request_keyword = f"_nkw={keyword}"
    page_number = f"&_pgn={number}"
    sold_item_filter = f"&_sacat=0&rt=nc&LH_Sold=1&LH_Complete=1"
    url = f"{base_url}{request_keyword}{sold_item_filter}{page_number}"

    return url


def get_psa_10_products_url():
    # For customized URL mapping
    keyword = "psa 10 zion williamson silver prizm -draft -emergent -select -mosaic -fireworks -duke -crusade -instant -american"
    # keyword = input("Enter search keyword: ")
    number = str(1)
    # number = input("Enter page no: ")
    base_url = 'https://www.ebay.com/sch/i.html?'
    request_keyword = f"_nkw={keyword}"
    page_number = f"&_pgn={number}"
    sold_item_filter = f"&_sacat=0&rt=nc&LH_Sold=1&LH_Complete=1"
    url = f"{base_url}{request_keyword}{sold_item_filter}{page_number}"

    return url


def get_bgs_9_5_products_average():
    pass


def main():

    bgs_9_5_products = get_index_data(get_page(get_bgs_9_5_products_url()))
    # psa_10_products = get_index_data(get_page(get_psa_10_products_url()))

    print("----- BGS 9.5 Products Scrapping Started ------")
    print()
    print("**********************************************")
    print("**********************************************")
    print("**********************************************")
    print()

    # for link in bgs_9_5_products:
    #     data = get_detail_data(get_page(link))
    #     write_csv(data, link)

    print()
    print("**********************************************")
    print("**********************************************")
    print("**********************************************")
    print()
    print("----- BGS 9.5 Products Scrapping Ended ------")

    # helpers.append_14_days_data_into_file()
    data_analysis.get_bgs_products_average()

if __name__ == '__main__':
    main()
