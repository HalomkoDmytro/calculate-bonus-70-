import re

MONTH_FROM = 'B1'
DATE_FROM = 'D1'
MONTH_TO = 'F1'
DATE_TO = 'H1'
IS_ALL_SOLDIER = 'J1'
NAME = "K1"

TITLE_RANGE = "A1:AN1"
RANK_NAME_RANGE = "D3:E1200"

MONTH = [
    'січень', 'лютий', 'березень', 'квітень', 'травень', 'червень',
    'липень', 'серпень', 'вересень', 'жовтень', 'листопад', 'грудень'
]

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


# date format "чт, 01 08"
def get_day(date_str):
    return date_str[date_str.index(",") + 1:second_index(date_str, " ") + 1]


def second_index(lst, element):
    count = 0
    for index, value in enumerate(lst):
        if value == element:
            count += 1
            if count == 2:
                return index
    return None


def get_mont_zero_num(month):
    index = MONTH.index(month)
    return "0" + str(index + 1) if index + 1 < 10 else str(index + 1)
