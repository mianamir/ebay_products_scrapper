
import csv

from datetime import datetime, timedelta


def get_min_max_date_no_days():
    with open('output.csv', newline='') as f:
        r = csv.reader(f)
        date_list = pack_all_dates(r)
        res_data = {
            "min_date": get_min_date(date_list[1:]),
            "max_date": get_max_date(date_list[1:]),
            "no_days": get_days_from_two_dates(get_min_date(date_list[1:]),get_max_date(date_list[1:])),
        }
        return res_data


def pack_all_dates(file):
    date_list = list()
    for line in file:
        date_list.append(line[1])
    return date_list


def check_date_exist(date, data):
    if date in data:
        return True
    return False


def append_14_days_data_into_file():
    min_max_date_no_days = get_min_max_date_no_days()
    with open('output.csv', newline='') as f:
        r = csv.reader(f)
        data = list()
        for line in r:
            row_date = get_date_from_date_string(line[1])
            min_date = get_date_from_date_string(min_max_date_no_days['min_date'])
            min_date = min_date + timedelta(days=1)
            max_date = get_date_from_date_string(min_max_date_no_days['max_date'])
            if ((row_date > min_date) and (row_date <= max_date)) and \
                    (min_max_date_no_days['no_days']-1 <= 14):
                data.append(line)

    with open('bgs_products_output.csv', 'w', newline='') as f:
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


def get_min_date(date_list):
    min_date = min(date_list)
    return min_date


def get_max_date(date_list):
    max_date = max(date_list)
    return max_date


def get_days_from_two_dates(min_date, max_date):
    d1 = get_date_from_date_string(min_date)
    d2 = get_date_from_date_string(max_date)
    return abs((d2 - d1).days)


def get_date_from_date_string(date_string):
    date_list = date_string.split()
    try:
        month, day, year, time_, time_zone = date_list
    except:
        month, day, year, time_, time_zone = None, None, None, None, None
    return convert_date_object(month, day, year)


def convert_date_object(month, day, year):
    try:
        month_int = int(month_string_to_number(str(month).lower()))
        date_res = datetime(int(year),  month_int, int(str(day).strip(',')))
    except:
        date_res = None
    return date_res


def month_string_to_number(string):
    m = {
        'jan': 1,
        'feb': 2,
        'mar': 3,
        'apr': 4,
         'may': 5,
         'jun': 6,
         'jul': 7,
         'aug': 8,
         'sep': 9,
         'oct': 10,
         'nov': 11,
         'dec': 12
        }
    s = string.strip()[:3].lower()

    try:
        out = m[s]
        return out
    except:
        raise ValueError('Not a month')


append_14_days_data_into_file()