import openpyxl

from service.utils import get_mont_zero_num


def write_to_exel(data, month_from, day_from_n, month_to, day_to_n, monthes):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = f"{month_from}-{month_to}"
    sheet.append([f"{day_from_n} {month_from}", f"{day_to_n} {month_to}"])
    sheet.append(["Звання", "ФІО", "Від", "По", "Днів на БЗ+"])

    # all data to one sheet
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

    # sheet group 30 by month
    if len(monthes) > 0:
        for month in monthes:
            s_month = f".{get_mont_zero_num(month)}"
            m_sheet = workbook.create_sheet(month)
            m_sheet.append(["Звання", "ФІО", "Від", "По", "Днів на БЗ+"])
            for name in data:
                is_first_name_write = 0
                for gr in data[name]["gr"]:
                    if gr and gr["to"] and len(gr["to"]) > 0:
                        contain_month = False

                        if s_month in gr["to"][-1]:
                            contain_month = True

                        if contain_month:
                            for index, val in enumerate(gr["f"]):
                                count_ = "" if index + 1 < len(gr["f"]) else gr["count"]
                                if is_first_name_write > 0:
                                    m_sheet.append(["", "", val, gr["to"][index], count_])
                                else:
                                    m_sheet.append(
                                        [data[name]["rank"], data[name]["full_name"], val, gr["to"][index], count_])
                                    is_first_name_write += 1


    workbook.save("destination\Премія 70.xlsx")
    print("complete writing exel")
