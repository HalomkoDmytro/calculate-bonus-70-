import openpyxl


def write_to_exel(data, month_from, day_from_n, month_to, day_to_n):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = f"{month_from}-{month_to}"
    sheet.append([f"{day_from_n} {month_from}", f"{day_to_n} {month_to}"])
    sheet.append(["Звання", "ФІО", "Від", "По", "Днів на БЗ+"])

    for name in data:
        is_first_name_write = 0
        for gr in data[name]["gr"]:
            if gr and gr["f"] and len(gr["f"]) > 0:
                for index, val in enumerate(gr["f"]):
                    count_ = "" if index + 1 < len(gr["f"]) else gr["count"]
                    if is_first_name_write > 0:
                        sheet.append(["", "", val, gr["to"][index], count_])
                    else:
                        sheet.append([data[name]["rank"], data[name]["full_name"], val, gr["to"][index], count_])
                        is_first_name_write += 1

    workbook.save("destination\Премія 70.xlsx")
    print("complete writing exel")
