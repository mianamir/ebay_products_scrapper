import csv
from re import sub
from decimal import Decimal


def convert_a_currency_string_to_a_floating_point_number():
    pass


def get_bgs_products_average():
    with open('bgs_products_output.csv', newline='') as f:
        rows_object = csv.reader(f)
        products_prices_list = list()
        total = 0.0
        for index, value in enumerate(rows_object):
            if index == 0:
                pass
            else:
                total += float(str(value[3]).split()[1])
        print(total)
