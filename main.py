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


def main():
    url = 'https://www.ebay.com/sch/i.html?_nkw=mens+watches&_pgn=1'

    products = get_index_data(get_page(url))

    for link in products:
        data = get_detail_data(get_page(link))
        write_csv(data, link)


if __name__ == '__main__':
    main()
