import maps
import unidecode as und
import csv
import multicampi
import pandas as pd
import app

def obter_nome_correto(nome_errado, localidades):
    for localidade in localidades.keys():
        if localidade in und.unidecode(str.lower(nome_errado)):
            return localidade
    print(nome_errado)
    return nome_errado


localidades = maps.load_cities_coordinates('data/localidades.csv')
df = app.load_data('data/dados_pesquisa.csv', 0)
df['cidade'] = df['cidade'].apply(lambda c: obter_nome_correto(c, localidades))

df.to_csv('cidades_normalizadas3.csv', sep=';')
