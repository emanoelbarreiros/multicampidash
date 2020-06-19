import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from server import app
import dash_table as dt
import pandas as pd
import plotly.express as px
from urllib.request import urlopen
import json

local_data = None
local_localities: pd.DataFrame = None
local_geojson = None

def get_layout(data, localities:pd.DataFrame, geojson):
    global local_data
    global local_localities
    global local_geojson
    local_data = data
    local_localities = localities
    local_geojson = geojson

    layout = html.Div([
        html.Div([
            html.Div([
                html.H1('Dados por Campus'),
                html.Hr(),
                html.P('Selecione o Campus'),
                dcc.Dropdown(
                    id="campus-select",
                    options=[
                        {"label": "Arcoverde", "value": "Arcoverde"},
                        {"label": "Garanhuns", "value": "Garanhuns"},
                        {"label": "Salgueiro", "value": "Salgueiro"},
                        {"label": "Serra Talhada", "value": "Serra Talhada"},
                    ],
                    value='Garanhuns',
                ),
                html.Br(),
                html.H4('Localidades onde declararam residir estudantes do Campus em análise'),
                html.Br(),
            ], className='col-12'),
        ], className='row'),
        html.Div([
            html.Div([
                html.P('Carregando mapa...')
            ], id='campus-map', className='col-12'),
        ], className='row'),
        html.Br(),
        html.Div([
            html.Div(id='campus-table', className='col-12'),
        ], className='row'),
    ])
    return layout


@app.callback(Output(component_id='campus-table', component_property='children'),
              [Input(component_id='campus-select', component_property='value')])
def update_table(campus):
    data_campus = local_data[local_data['campus'] == campus]

    data_cities = pd.DataFrame(data_campus.cidade.value_counts()).reset_index()
    data_cities.columns = ['cidade', 'número de estudantes']

    data_table = dt.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in data_cities.columns],
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
            'lineHeight': '15px'
        },
        data=data_cities.to_dict('records'),
    )

    layout_table = html.Div([
        data_table,
    ])

    return layout_table


@app.callback(Output(component_id='campus-map', component_property='children'),
              [Input(component_id='campus-select', component_property='value')])
def update_map(campus):
    data_campus = local_data[local_data['campus'] == campus]

    data_cities = pd.DataFrame(data_campus.cidade.value_counts()).reset_index()
    data_cities.columns = ['cidade', 'qtd']
    campus_id = local_localities.loc[local_localities['cidade'] == str.lower(campus)].iloc[0].id

    ids = []
    for city in data_cities['cidade']:
        if city != 'nenhum':
            local = local_localities.loc[local_localities['cidade'] == city]
            ids.append(local.iloc[0].id)
        else:
            ids.append('0')

    data_cities['id'] = ids

    fig = px.choropleth_mapbox(data_cities, geojson=local_geojson, locations='id', color='qtd',
                               color_continuous_scale="Viridis", featureidkey='properties.id',
                               range_color=(0, 50),
                               mapbox_style="open-street-map",
                               zoom=8, center={"lat": -8.8828, "lon": -36.4969},
                               opacity=0.5, hover_data=['cidade','qtd'],
                               )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    # with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    #     counties = json.load(response)
    #
    # df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
    #                  dtype={"fips": str})
    #
    #
    #
    # fig = px.choropleth_mapbox(df, geojson=local_geojson, locations='fips', color='unemp',
    #                            color_continuous_scale="Viridis",
    #                            range_color=(0, 12),
    #                            mapbox_style="carto-positron",
    #                            zoom=3, center={"lat": 37.0902, "lon": -95.7129},
    #                            opacity=0.5,
    #                            labels={'unemp': 'unemployment rate'}
    #                            )
    # fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    layout_map = html.Div([
        dcc.Graph(figure=fig)
    ])

    return layout_map
