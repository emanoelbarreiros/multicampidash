import pandas as pd

data = {}

def get_raw_data(campus):
    campus_data = pd.read_excel('data/dados_raw_' + campus + '.xlsx')
    data[campus] = campus_data
    return campus_data


def get_epidemic_data(campus):
    if campus in data:
        return data[campus]
    else:
        campus_data = pd.read_excel('data/dados_' + campus + '.xlsx')
        data[campus] = campus_data

    return campus_data
