import gspread

TABLE_ID = "15_8MQbxLrCjn4YU7gZHlO76zoi6dR9SR-IuZNwF2qGY"

DIVISION = "A"
NUMBER = "B"
TABEL_RANK = "C"
REAL_RANK = "D"
NAME_COL = "E"
POSITION_NAME = "G"

JUNE_BEFORE_BALANCE_COL = "AV"


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


def get_left_for_name_to_june():
    gc = gspread.service_account(filename='.config/gspread/service_account.json')
    sh = gc.open_by_key(TABLE_ID)
    worksheet = sh.worksheet("червень")
    names = worksheet.get_values(range_name=f"{NAME_COL}3:{NAME_COL}")
    letf = worksheet.get_values(range_name=f"{JUNE_BEFORE_BALANCE_COL}3:{JUNE_BEFORE_BALANCE_COL}")

    result = []

    for idx, name in enumerate(names):
        if name[0] and len(name[0]) > 0 and name[0] != "вакант" and letf[idx][0] != "0":
            result.append({"name": name[0], "left": letf[idx][0]})

    return result
