import csv
import pandas as pd
import json
import plotly.express as px
import dash_table as dt

geojson = None
with open('data/pernambuco2.json', encoding='utf8') as file:
    geojson = json.load(file)

garanhuns = {'lat': -8.8828, 'lon': -36.4969}


def get_city_table(data_cities):
    data_table = dt.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in data_cities.columns],
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
            'lineHeight': '15px',
        },
        data=data_cities.to_dict('records'),
        style_table={
            'height': '440px',
            'overflowY': 'scroll'
        },
    )
    return data_table


def load_cities_coordinates(file):
    localities = {}
    with open(file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            localities[row['cidade']] = {'lat': float(row['lat']), 'lon': float(row['lon'])}
    return localities


def load_cities_dataframe(file):
    return pd.read_csv(file, sep=',', dtype={"id": str})


def load_localities_coord_list(cities):
    global dict_localities
    data = []
    for city in cities:
        if city != 'nenhum':
            data.append([dict_localities[city]['lat'], dict_localities[city]['lon']])
    return data


def load_localities_coord_size_list(cities:pd.Series):
    global dict_localities
    data = []
    for (city,size) in cities.iteritems():
        if city != 'nenhum':
            data.append([dict_localities[city]['lat'], dict_localities[city]['lon'], size, city])
    return pd.DataFrame(data, columns=['lat', 'lon', 'size', 'city'])


def get_map(data_cities, color_range):
    global df_localities
    ids = []
    for city in data_cities['cidade']:
        if city != 'nenhum':
            local = df_localities.loc[df_localities['cidade'] == city]
            ids.append(local.iloc[0].id)
        else:
            ids.append('0')
    data_cities['id'] = ids
    fig = px.choropleth_mapbox(data_cities, geojson=geojson, locations='id', color='qtd',
                               color_continuous_scale="Viridis", featureidkey='properties.id',
                               range_color=(0, color_range),
                               mapbox_style="open-street-map",
                               zoom=8, center={"lat": garanhuns['lat'], "lon": garanhuns['lon']},
                               opacity=0.5, hover_data=['cidade', 'qtd'],
                               )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig


def get_infected_graph(epidemic_data, color_range, date):
    global df_localities
    df_epidemic = pd.DataFrame(epidemic_data)
    df_epidemic.columns = ['cidade', 'data', 'infectados', 'recuperados', 'obitos', 'novos']
    df_epidemic = df_epidemic.loc[::, ['cidade', 'data', 'infectados']]

    # filter based on the selected dates
    df_epidemic = df_epidemic[df_epidemic.data == date]

    ids = []
    for city in df_epidemic['cidade']:
        local = df_localities.loc[df_localities['cidade'] == city]
        ids.append(local.iloc[0].id)

    df_epidemic['id'] = ids
    df_epidemic

    fig = px.choropleth_mapbox(df_epidemic, geojson=geojson, locations='id', color='infectados',
                               color_continuous_scale="YlOrRd", featureidkey='properties.id',
                               mapbox_style="open-street-map",
                               range_color=(0, color_range),
                               zoom=8, center={"lat": garanhuns['lat'], "lon": garanhuns['lon']},
                               opacity=0.7, hover_data=['cidade', 'infectados'],
                               )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig


dict_localities = load_cities_coordinates('data/localidades.csv')
df_localities = load_cities_dataframe('data/localidades.csv')