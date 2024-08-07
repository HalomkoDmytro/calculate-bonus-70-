import gspread

TABLE_ID = "15_8MQbxLrCjn4YU7gZHlO76zoi6dR9SR-IuZNwF2qGY"

DIVISION = "A"
NUMBER = "B"
TABEL_RANK = "C"
REAL_RANK = "D"
NAME_COL = "E"
POSITION_NAME = "G"


def get_names(month):
    gc = gspread.service_account(filename='.config/gspread/service_account.json')
    sh = gc.open_by_key(TABLE_ID)
    worksheet = sh.worksheet(month)
    data = worksheet.get_values(range_name=f"{REAL_RANK}3:{NAME_COL}")

    filtered_data = [sublist for sublist in data if sublist[0] not in (None, '')]

    return filtered_data


def gel_all_from(month):
    gc = gspread.service_account(filename='.config/gspread/service_account.json')
    sh = gc.open_by_key(TABLE_ID)
    worksheet = sh.worksheet(month)
    data = worksheet.get_values(range_name=f"{REAL_RANK}1:AN")

    filtered_data = [sublist for sublist in data if sublist[1] not in (None, '', 'вакант')]

    return filtered_data
