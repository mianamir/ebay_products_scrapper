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


def get_detail_data(soup):
    try:
        title = soup.find('h1', id='itemTitle').text.strip('Details about    ')
    except:
        title = ''
    try:
        try:
            try:
                p = soup.find('span', id='prcIsum').text.strip()
            except:
                p = soup.find('span', id='mm-saleDscPrc').text.strip()
        except:
            p = soup.find('span', id='prcIsum_bidPrice').text.strip()
        currency, price = p.split(" ")
    except:
        currency = ''
        price = ''
    try:
        sold_items = soup.find('span', class_='vi-qtyS-hot').find('a').text
    except:
        sold_items = ''
    data = {
        'title': title,
        'price': price,
        'currency': currency,
        'total_sold': sold_items
    }

    return data


def get_index_data(soup):
    try:
        a_tags = soup.find_all('a', class_='s-item__link')
    except:
        a_tags = list()
    urls = [item.get('href') for item in a_tags]
    return urls


def write_csv(data, url):
    with open('output.csv', 'a') as csv_file:
        writer = csv.writer(csv_file)

        row = [data['title'], data['price'], data['currency'], data['total_sold'], url]

        writer.writerow(row)


def get_simple_products_url():
    # For customized URL mapping
    keyword = "bgs 9.5 zion williamson silver prizm -draft -emergent -select -mosaic -fireworks -duke -crusade -instant -american"
    number = 1
    # old_url = 'https://www.ebay.com/sch/i.html?_nkw=mens+watches&_pgn=1'
    base_url = 'https://www.ebay.com/sch/i.html?'
    request_keyword = f"_nkw={keyword}"
    page_number = f"&_pgn={str(number)}"
    url = f"{base_url}{request_keyword}{page_number}"

    return url


def get_sold_products_url():
    # For customized URL mapping
    keyword = "psa 10 zion williamson silver prizm -draft -emergent -select -mosaic -fireworks -duke -crusade -instant -american"
    number = 1
    # old_url = 'https://www.ebay.com/sch/i.html?_nkw=mens+watches&_pgn=1'
    base_url = 'https://www.ebay.com/sch/i.html?'
    request_keyword = f"_nkw={keyword}"
    page_number = f"&_pgn={str(number)}"
    sold_item_filter = f"&_sacat=0&rt=nc&LH_Sold=1&LH_Complete=1&_pgn=2"
    url = f"{base_url}{request_keyword}{sold_item_filter}{page_number}"

    return url


def main():

    products = get_index_data(get_page(get_simple_products_url()))

    for link in products:
        data = get_detail_data(get_page(link))
        write_csv(data, link)


if __name__ == '__main__':
    main()
