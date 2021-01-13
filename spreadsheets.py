import pandas as pd
import unidecode as und

data = {}

def get_raw_data(campus):
    data = pd.read_excel('data/dados_raw_' + campus + '_7.xlsx', sheet_name=None, skiprows=1)
    worksheet_list = data.keys()
    result = pd.DataFrame()

    for sheet in worksheet_list:
        # ignore the first two rows and only get the rows
        city = str.lower(und.unidecode(sheet))
        print(city)
        city_data = data[sheet]
        if len(city_data.columns) == 6:
            print(sheet)
            city_data.columns = ['data', 'infectados', 'recuperados', 'obitos', 'acompanhamento', 'novos']
            city_data.drop('acompanhamento', axis=1, inplace=True)
        else:
            city_data.columns = ['data', 'infectados', 'recuperados', 'obitos', 'novos']

        city_data['data'] = city_data['data'].astype('datetime64')
        city_data.insert(0, 'cidade', city)
        result = result.append(city_data)

    return result


def get_epidemic_data(campus):
    if campus in data:
        return data[campus]
    else:
        campus_data = pd.read_excel('data/dados_' + campus + '.xlsx')
        data[campus] = campus_data

    return campus_data
