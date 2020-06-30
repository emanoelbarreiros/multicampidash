import gspread
import unidecode as und


def get_epidemic_data():
    gc = gspread.service_account(filename='assets/multicampidash-ce36f447e2f0.json')
    sh = gc.open("Banco V GERES 2")
    worksheet_list = sh.worksheets()
    result = []
    for sheet in worksheet_list:
        # ignore the first two rows and only get the rows where the infected number is greater than 0
        # result[sheet.title] =

        city = str.lower(und.unidecode(sheet.title))
        rows = sheet.get_all_values()[2:]
        for row in rows:
            new_row = [city] + row
            result.append(new_row)

    return result
