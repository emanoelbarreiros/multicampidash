import unidecode as und
import pandas as pd


def get_epidemic_data():
    data = pd.read_excel('data/dados_epidemicos.xlsx', sheet_name=None, skiprows=1)
    worksheet_list = data.keys()
    result = pd.DataFrame()

    for sheet in worksheet_list:
        # ignore the first two rows and only get the rows
        city = str.lower(und.unidecode(sheet))
        city_data = data[sheet]
        city_data.columns = ['data', 'infectados', 'recuperados', 'obitos', 'novos']
        city_data.insert(0,'cidade', city)
        result = result.append(city_data)

    return result
