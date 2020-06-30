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
import monitoramento
import maps
from server import app

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


nav_multicampi = dbc.NavItem(dbc.NavLink("Multicampi", href="/multicampi"))
nav_campus = dbc.NavItem(dbc.NavLink("Campus", href="/campus"))
nav_monitor = dbc.NavItem(dbc.NavLink("Mon. Epidemiológico", href="/monitoramento"))

# this is the default navbar style created by the NavbarSimple component
navbar = dbc.NavbarSimple(
    children=[nav_multicampi, nav_campus, nav_monitor],
    brand="UPE Multicampi - Dashboard",
    brand_href="#",
    sticky="top",
    className="mb-5",
)

flask = app.server
content = html.Div(id='page-content', className='container')
app.layout = html.Div([dcc.Location(id='url'), navbar, content])

data = load_data('data/cidades_normalizadas.csv', 0)
student_count, campi_courses = load_dict_from_csv_student('data/qtd_estudantes.csv')
localities = maps.load_cities_dataframe('data/localidades.csv')

multicampi_layout = multicampi.get_layout(data, student_count)
course_layout = course.get_layout()
campus_layout = campus.get_layout(data)
monitor_layout = monitoramento.get_layout(localities)


if __name__ == '__main__':
    app.run_server(debug=True)
