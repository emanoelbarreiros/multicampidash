"""
This app creates a simple sidebar layout using inline style arguments and the
dbc.Nav component.

dcc.Location is used to track the current location. There are two callbacks,
one uses the current location to render the appropriate page content, the other
uses the current location to toggle the 'active' properties of the navigation
links.

For more details on building multi-page Dash applications, check out the Dash
documentation: https://dash.plot.ly/urls
"""

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import unidecode as und
import pandas as pd
import csv
import plotly.express as px

import course
import multicampi
import campus
import monitor
import maps
from server import app
import json



# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '16rem',
    'padding': '2rem 1rem',
    'background-color': '#f8f9fa',
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    'margin-left': '18rem',
    'margin-right': '2rem',
    'padding': '2rem 1rem',
}

px.set_mapbox_access_token('pk.eyJ1IjoiZW1hbm9lbGJhcnJlaXJvcyIsImEiOiJja2Izb3QxM3cwbWE5MnJtdnp2eG16azB0In0.nUa34PVgI5csOJTbI-uosg')

def remove_accents(s):
    return und.unidecode(s)


def load_data(file, nrows):
    if nrows >= 0:
        data = pd.read_csv(file, sep=';', encoding='utf-8')
    else:
        data = pd.read_csv(file, sep=';', nrows=nrows, encoding='utf-8')

    data['cidade'] = data['cidade'].str.lower()
    data['cidade'] = data['cidade'].str.strip()
    data['cidade'] = data['cidade'].apply(remove_accents)
    return data


def load_dict_from_csv_transp(file):
    data = {}
    with open(file, newline='', encoding='utf-8') as transportation:
        reader = csv.reader(transportation, delimiter=';')
        next(reader, None)  # skip the headers
        for row in reader:
            data[str.lower(row[0])] = row[1]
    return data


def load_dict_from_csv_student(file):
    data = {}
    campi_courses = {'Geral': []}
    with open(file, newline='', encoding='utf-8') as std_count:
        reader = csv.reader(std_count, delimiter=';')
        next(reader, None)  # skip the headers
        for row in reader:
            data[row[0] + '-' + row[1]] = row[2]
            if row[0] in campi_courses:
                campi_courses[row[0]].append(row[1])
            else:
                campi_courses[row[0]] = ['Geral', row[1]]
    return data, campi_courses


# this callback uses the current pathname to set the active state of the
# corresponding nav link to true, allowing users to tell see page they are on
@app.callback(
    [Output(f'{p}-link', 'active') for p in ['multicampi', 'campus', 'monitoramento']],
    [Input('url', 'pathname')],
)
def toggle_active_links(pathname):
    if pathname == '/':
        # Treat page 1 as the homepage / index
        return True, False, False
    return [pathname == f'/{i}' for i in ['multicampi', 'campus', 'monitoramento']]


@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def render_page_content(pathname):
    if pathname in ['/', '/multicampi']:
        return multicampi_layout
    elif pathname == '/campus':
        return campus_layout
    elif pathname == '/monitoramento':
        return monitor_layout
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1('404: Não encontrado', className='text-danger'),
            html.Hr(),
            html.P(f'O caminho {pathname} não foi reconhecido...'),
        ]
    )


sidebar = html.Div(
    [
        html.H2('Multicampi Dashboard'),
        html.P(
            'Visualização de dados relacionados a COVID-19 para a UPE Multicampi', className='lead'
        ),
        dbc.Nav(
            [
                dbc.NavLink('Multicampi', href='/multicampi', id='multicampi-link'),
                dbc.NavLink('Dados por Campus', href='/campus', id='campus-link'),
                dbc.NavLink('Monitoramento Epidemiológico', href='/monitoramento', id='monitoramento-link'),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id='page-content', style=CONTENT_STYLE, className='container')

app.layout = html.Div([dcc.Location(id='url'), sidebar, content])

data = load_data('cidades_normalizadas.csv', 0)
localities = maps.load_cities_coordinates('localidades.csv')
df_localities = maps.load_cities_dataframe('localidades.csv')
student_count, campi_courses = load_dict_from_csv_student('qtd_estudantes.csv')

with open('pernambuco2.json', encoding='utf8') as file:
    geojson = json.load(file)

multicampi_layout = multicampi.get_layout(data, student_count)

#course_view = course.Course(app, data, localities)
course_layout = course.get_layout()

campus_layout = campus.get_layout(data, df_localities, geojson)

#monitor.set_data(...)
monitor_layout = monitor.get_layout()


if __name__ == '__main__':
    app.run_server(debug=True)
