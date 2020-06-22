import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from server import app
import pandas as pd
import maps

local_data: pd.DataFrame = None
local_localities: pd.DataFrame = None


def get_layout(data):
    global local_data
    local_data = data

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
        html.Div([
            html.Div([
                html.H4('Localidades onde estudantes declararam não possuir acesso a internet em sua residencia'),
                html.Hr(),
            ], className='col-12')
        ], className='row'),
        html.Div([
            html.Div([
                html.P('Carregando mapa...')
            ], id='campus-map2', className='col-6'),
            html.Div([
                html.P('Carregando tabela...')
            ], id='campus-table2', className='col-6'),
        ], className='row'),
        html.Div([
            html.Div([
                html.H4('Total de estudantes que declararam não possuir PC nem tablet'),
                html.Hr(),
            ], className='col-12')
        ], className='row'),
        html.Div([
            html.Div([
                html.P('Carregando mapa...')
            ], id='campus-map3', className='col-6'),
            html.Div([
                html.P('Carregando tabela...')
            ], id='campus-table3', className='col-6'),
        ], className='row')
    ])
    return layout


def get_table_and_map(data, color_range = 50):
    data_table = pd.DataFrame(data.cidade.value_counts()).reset_index()

    data_table.columns = ['cidade', 'estudantes']

    data_table = maps.get_city_table(data_table)

    layout_table = html.Div([
        data_table,
    ])

    data_map = pd.DataFrame(data.cidade.value_counts()).reset_index()
    data_map.columns = ['cidade', 'qtd']

    fig = maps.get_map(data_map, color_range)

    layout_map = html.Div([
        dcc.Graph(figure=fig)
    ])

    return layout_table, layout_map


@app.callback([Output(component_id='campus-table', component_property='children'),
               Output(component_id='campus-map', component_property='children')],
              [Input(component_id='campus-select', component_property='value')])
def update_set_1(campus):
    data_campus = local_data[local_data['campus'] == campus]

    return get_table_and_map(data_campus)


@app.callback([Output(component_id='campus-table2', component_property='children'),
               Output(component_id='campus-map2', component_property='children')],
              [Input(component_id='campus-select', component_property='value')])
def update_set_2(campus):
    data_campus = local_data[local_data['campus'] == campus]
    data_internet = data_campus[data_campus['internet'] == 'Não']

    return get_table_and_map(data_internet, color_range=15)


@app.callback([Output(component_id='campus-table3', component_property='children'),
               Output(component_id='campus-map3', component_property='children')],
              [Input(component_id='campus-select', component_property='value')])
def update_set_3(campus):
    data_campus = local_data[local_data['campus'] == campus]
    data_device = data_campus[data_campus.notebookpc.eq('Não') & data_campus.tablet.eq('Não')]

    return get_table_and_map(data_device, color_range=15)