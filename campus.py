import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from server import app
import pandas as pd
import maps

local_data: pd.DataFrame = None
local_localities: pd.DataFrame = None
local_schools: pd.DataFrame = None


def get_layout(data, schools):
    global local_data, local_schools
    local_data = data
    local_schools = schools

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
        html.Br(),
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
        html.Br(),
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
        ], className='row'),
        html.Br(),
        html.Div([
            html.Div([
                html.H4('Localidades onde estudantes declararam não possuir acesso limitado internet'),
                html.Hr(),
                html.P('Nesta análise exibimos onde estudantes que declararam acessar a internet apenas com dados móveis LIMITADOS declararam residir.')
            ], className='col-12')
        ], className='row'),
        html.Div([
            html.Div([
                html.P('Carregando mapa...')
            ], id='campus-map4', className='col-6'),
            html.Div([
                html.P('Carregando tabela...')
            ], id='campus-table4', className='col-6'),
        ], className='row'),
        html.Br(),
        html.Div([
            html.Div([
                html.H4('Análise de estudantes que declararam acesso limitado a tecnologia e como se deslocam para a Universidade'),
                html.Hr(),
                html.P(
                    'Nesta análise estamos considerando estudantes que, alternativamente, não possuem acesso à internet, ou acessam a internet apenas por smartphone (mesmo que tenham franquia de dados ILIMITADA).'),
                #html.P('Também estão sendo plotadas as localidades onde existem escolas que podem receber os estudantes (possuem laboratório com internet).'),
            ], className='col-12')
        ], className='row'),
        html.Div([
            html.Div([
                html.P('Carregando mapa...')
            ], id='campus-map5', className='col-12'),
        ], className='row'),
        html.Br(),
        html.Div([
            html.Div([
                html.P('Carregando tabela...')
            ], id='campus-table5', className='col-12'),
        ])
        # html.Div([
        #     html.Div([
        #         html.P('Carregando tabela...')
        #     ], id='school-table5', className='col-12')
        # ], className='row')
    ])
    return layout


def get_table_and_map(data, schools=None, color_range=50):
    data_table = pd.DataFrame(data.cidade.value_counts()).reset_index()
    data_table.columns = ['cidade', 'estudantes']

    data_table = maps.get_city_table(data_table)

    layout_table = html.Div([
        data_table,
    ])

    data_map = pd.DataFrame(data.cidade.value_counts()).reset_index()
    data_map.columns = ['cidade', 'qtd']

    if schools is None:
        fig = maps.get_map(data_map, color_range)
    else:
        # MUDAR PARA A CHAMADA A maps.get_map_scatter(data_map, schools, color_range) ASSIM QUE CONSEGUIR PLOTAR AS
        # ESCOLAS EM CIMA DO MAPA
        fig = maps.get_map(data_map, color_range)

    layout_map = html.Div([
        dcc.Graph(figure=fig)
    ])

    return layout_table, layout_map


def get_transport_table_and_map(data, schools=None, color_range=50, columns=None):
    data_table = pd.DataFrame(data.groupby('cidade')['transporte'].value_counts())
    data_table.index = data_table.index.set_names(['cidade_i', 'transporte_i'])
    data_table = data_table.reset_index()
    data_table.columns = ['cidade', 'meio de transporte', 'estudantes']

    data_table = maps.get_city_table(data_table)

    layout_table = html.Div([
        data_table,
    ])

    data_map = pd.DataFrame(data.cidade.value_counts()).reset_index()
    data_map.columns = ['cidade', 'qtd']

    if schools is None:
        fig = maps.get_map(data_map, color_range)
    else:
        # MUDAR PARA A CHAMADA A maps.get_map_scatter(data_map, schools, color_range) ASSIM QUE CONSEGUIR PLOTAR AS
        # ESCOLAS EM CIMA DO MAPA
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

@app.callback([Output(component_id='campus-table4', component_property='children'),
               Output(component_id='campus-map4', component_property='children')],
              [Input(component_id='campus-select', component_property='value')])
def update_set_4(campus):
    data_campus = local_data[local_data['campus'] == campus]
    data_internet = data_campus[data_campus['acesso'] == 'Dados móveis LIMITADOS']

    return get_table_and_map(data_internet, color_range=15)

@app.callback([Output(component_id='campus-table5', component_property='children'),
               Output(component_id='campus-map5', component_property='children')],
              [Input(component_id='campus-select', component_property='value')])
def update_set_5(campus):
    data_campus = local_data[local_data['campus'] == campus]
    data_restricted = data_campus[(data_campus.notebookpc.eq('Não') & data_campus.tablet.eq(
        'Não') & data_campus.tablet.eq('Sim')) | data_campus.internet.eq('Não')]
    data_schools = local_schools[local_schools.lab.eq('Sim') & local_schools.internet.eq('Sim')]

    if data_restricted.index.to_numpy().size > 0:
        return get_transport_table_and_map(data_restricted, schools=data_schools, color_range=15)
    else:
        result = html.Div([
            html.P('Nenhum estudante satifaz as condições estabelecidas nesta análise.')
        ])
        return result, result, result
