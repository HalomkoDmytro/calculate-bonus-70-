from service.exel_writer import write_to_exel
from service.position_table_reader import get_names, gel_all_from, get_left_for_name_to_june
from service.utils import MONTH, get_day, get_mont_zero_num


def filter_with_date_range(month_from, day_from_n, month_to, day_to_n, raw_data):
    for name in raw_data[month_from]:
        temp = -1
        for index, day in enumerate(raw_data[month_from][name]):
            if day >= day_from_n:
                temp = index
                raw_data[month_from][name] = raw_data[month_from][name][temp:]
                break
        if temp == -1:
            raw_data[month_from][name] = []

    for name in raw_data[month_to]:
        temp = []
        for day in raw_data[month_to][name]:
            if day <= day_to_n:
                temp.append(day)
        raw_data[month_to][name] = temp


def process(date_from, date_to, tk):
    month_from_n = date_from.month
    month_from = MONTH[month_from_n - 1]
    day_from_n = date_from.day

    month_to_n = date_to.month
    month_to = MONTH[month_to_n - 1]
    day_to_n = date_to.day

    monthes = MONTH[MONTH.index(month_from):MONTH.index(month_to) + 1]
    person = get_names(monthes[-1])

    balance_bonus = get_left_for_name_to_june()

    result = []
    for row in person:
        result.append({
            "rank": row[0],
            "name": row[1],
            "bz": []
        })

    raw_data = {}
    for month in monthes:
        all_from_month = gel_all_from(month)
        raw_data[month] = transform_moth(all_from_month)

    filter_with_date_range(month_from, day_from_n, month_to, day_to_n, raw_data)

    result = group_30_days(monthes, raw_data, person, balance_bonus)

    write_to_exel(result, month_from, day_from_n, month_to, day_to_n, monthes)


def group_30_days(monthes, raw_data, person, balance_bonus):
    result = {}

    for pers in person:
        name = pers[1]
        for month_numb, month in enumerate(monthes):
            if name not in result:
                result[name] = {
                    "full_name": name,
                    "rank": pers[0],

                    "gr": [{"count": 0, "f": [], "to": []}]
                }
            if name in raw_data[month]:
                bz = raw_data[month][name]
                count = get_start_count(month, monthes, name, result, balance_bonus)
                result[name]["gr"][-1]["count"] = count
                f = None
                to = None
                temp = None
                for j, day in enumerate(bz):
                    count += 1
                    if j == 0:
                        f = bz[j]
                        temp = bz[j]
                        to = bz[j]
                        if count == 30:
                            last = result[name]["gr"][-1]
                            last["count"] = 30
                            last["f"].append(f"{str(f)}.{get_mont_zero_num(month)}")
                            last["to"].append(f"{str(to)}.{get_mont_zero_num(month)}")
                            result[name]["gr"].append({"count": 0, "f": [], "to": []})
                            if j + 1 < len(bz):
                                f = bz[j + 1]
                            count = 0
                    else:
                        # if j == 1:
                        #     f = bz[j - 1]
                        temp = bz[j - 1]
                        to = bz[j]
                        dif_days = to - temp

                        if dif_days == 1:
                            if count == 30:
                                last = result[name]["gr"][-1]
                                last["count"] = 30
                                last["f"].append(f"{str(f)}.{get_mont_zero_num(month)}")
                                last["to"].append(f"{str(to)}.{get_mont_zero_num(month)}")
                                result[name]["gr"].append({"count": 0, "f": [], "to": []})
                                if j + 1 < len(bz):
                                    f = bz[j + 1]
                                count = 0

                        else:
                            if count == 30:
                                last = result[name]["gr"][-1]
                                last["count"] = 30
                                last["f"].append(f"{str(f)}.{get_mont_zero_num(month)}")
                                last["to"].append(f"{str(temp)}.{get_mont_zero_num(month)}")
                                last["f"].append(f"{str(to)}.{get_mont_zero_num(month)}")
                                last["to"].append(f"{str(to)}.{get_mont_zero_num(month)}")
                                result[name]["gr"].append({"count": 0, "f": [], "to": []})
                                if j + 1 < len(bz):
                                    f = bz[j + 1]
                                count = 0
                            else:
                                last = result[name]["gr"][-1]
                                last["count"] += count
                                last["f"].append(f"{str(f)}.{get_mont_zero_num(month)}")
                                last["to"].append(f"{str(temp)}.{get_mont_zero_num(month)}")
                                f = bz[j]

                        # count += 1

                    if j + 1 == len(bz) and count > 0:
                        last = result[name]["gr"][-1]
                        # plus = 1 if monthes[-1] == month else 0
                        plus = 1 if monthes[-1] == month and len(monthes) == 1 else 0
                        last["count"] = count
                        last["f"].append(f"{str(f)}.{get_mont_zero_num(month)}")
                        last["to"].append(f"{str(to)}.{get_mont_zero_num(month)}")

    # for name in result:
    #     if len(result[name]["gr"][0]["f"]) > 0:
    #         print(name)
    #         for x in result[name]["gr"]:
    #             for idx, y in enumerate(x["f"]):
    #                 print(str(y) + " " + str(x["to"][idx]))

    return result


def get_start_count(month, monthes, name, result, balance_bonus):
    if result[name]["gr"][-1]["count"] == 30:
        return 0

    temp = 0
    if 'червень' in monthes:
        for bb in balance_bonus:
            if bb["name"] == name:
                temp = int(bb["left"])
                bb["left"] = "0"
            if temp > 0:
                break

    return result[name]["gr"][-1]["count"] + temp


def transform_moth(month_data):
    data = {}
    date_line = month_data[:1][0]

    for row in month_data[1:]:
        date = []

        for i, cell in enumerate(row):
            if cell == 'БЗ+':
                date.append(int(get_day(date_line[i])))

        data[row[1]] = date

    return data
