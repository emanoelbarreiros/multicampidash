import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from server import app
import maps

global_student_count = None
global_data:pd.DataFrame = None
def get_layout(data, student_count):
    global global_student_count, global_data

    global_student_count = student_count
    global_data = data

    layout = html.Div([
        html.Div([
            html.Div([
                html.H1('Dados por Curso'),
                html.P(
                    'Análise do quantitativo de estudantes que responderam ao formulário disponível em: https://docs.google.com/forms/d/e/1FAIpQLSfJ6cf9I_cxoOf0DH5eHDYUPD8HgERFFRxiAQIIlck-yOvSkQ/viewform'),
                html.Hr(),
                html.P('Selecione o Curso'),
                dcc.Dropdown(
                    id="course-select",
                    options=[
                        {"label": "Arcoverde - Bacharelado em Odontologia",
                         "value": "Arcoverde-Bacharelado em Odontologia"},
                        {"label": "Arcoverde - Bacharelado em Direito", "value": "Arcoverde-Bacharelado em Direito"},
                        {"label": "Garanhuns - Bacharelado em Engenharia de Software",
                         "value": "Garanhuns-Bacharelado em Engenharia de Software"},
                        {"label": "Garanhuns - Bacharelado em Medicina", "value": "Garanhuns-Bacharelado em Medicina"},
                        {"label": "Garanhuns - Bacharelado em Psicologia",
                         "value": "Garanhuns-Bacharelado em Psicologia"},
                        {"label": "Garanhuns - Licenciatura em Ciências Biológicas",
                         "value": "Garanhuns-Licenciatura em Ciências Biológicas"},
                        {"label": "Garanhuns - Licenciatura em Computação",
                         "value": "Garanhuns-Licenciatura em Computação"},
                        {"label": "Garanhuns - Licenciatura em Geografia",
                         "value": "Garanhuns-Licenciatura em Geografia"},
                        {"label": "Garanhuns - Licenciatura em História",
                         "value": "Garanhuns-Licenciatura em História"},
                        {"label": "Garanhuns - Licenciatura em Letras", "value": "Garanhuns-Licenciatura em Letras"},
                        {"label": "Garanhuns - Licenciatura em Matemática",
                         "value": "Garanhuns-Licenciatura em Matemática"},
                        {"label": "Garanhuns - Licenciatura em Pedagogia",
                         "value": "Garanhuns-Licenciatura em Pedagogia"},
                        {"label": "Serra Talhada - Bacharelado em Medicina",
                         "value": "Serra Talhada-Bacharelado em Medicina"},
                    ],
                    value='Arcoverde-Bacharelado em Odontologia',
                    clearable=False
                ),
            ], className='col-12')
        ], className='row'),
        html.Br(),
        html.Div([
            html.Div(id='course-info', className='col-12'),
        ], className='row'),
        html.Div([
            html.Div([
                html.H4('Proporção de estudantes por período'),
                html.Hr(),
            ], className='col-12')
        ], className='row'),
        html.Div([
            html.Div([
                html.P('Carregando gráfico...')
            ], id='course-set1', className='col-12'),
        ], className='row'),
        html.Br(),
        html.Div([
            html.Div([
                html.H4('Localidades onde declararam residir estudantes do curso'),
                html.Hr(),
            ], className='col-12')
        ], className='row'),
        html.Div([
            html.Div([
                html.P('Carregando mapa...')
            ], id='course-map2', className='col-6'),
            html.Div([
                html.P('Carregando tabela...')
            ], id='course-table2', className='col-6'),
        ], className='row'),
        html.Br(),
        html.Div([
            html.Div([
                html.H4('Meios de transporte que estudantes do curso utilizam para se deslocar para a Universidade'),
                html.Hr(),
            ], className='col-12')
        ], className='row'),
        html.Div([
            html.Div([
                html.P('Carregando tabela...')
            ], id='course-table3', className='col-12'),
        ], className='row'),
        html.Br(),
        html.Div([
            html.Div([
                html.H4('Ambiente propício para estudo'),
                html.Hr(),
            ], className='col-12')
        ], className='row'),
        html.Div([
            html.Div([
                html.P('Carregando tabela...')
            ], id='course-table4', className='col-12'),
        ], className='row'),
        html.Br(),
        html.Div([
            html.Div([
                html.H4('Estudantes pertencentes a grupos de risco'),
                html.Hr(),
            ], className='col-12')
        ], className='row'),
        html.Div([
            html.Div([
                html.P('Carregando tabela...')
            ], id='course-table5', className='col-12'),
        ], className='row'),
        html.Br(),
        html.Div([
            html.Div([
                html.H4('Localidades onde estudantes declararam não possuir acesso a internet'),
                html.Hr(),
            ], className='col-12')
        ], className='row'),
        html.Div([
            html.Div([
                html.P('Carregando mapa...')
            ], id='course-map6', className='col-6'),
            html.Div([
                html.P('Carregando tabela...')
            ], id='course-table6', className='col-6'),
        ], className='row'),
        html.Br(),
        html.Div([
            html.Div([
                html.H4('Localidades onde residem estudantes com acesso limitado a internet'),
                html.Hr(),
                html.P('Nesta análise exibimos onde estudantes que declararam acessar a internet apenas com dados móveis LIMITADOS declararam residir.')
            ], className='col-12')
        ], className='row'),
        html.Div([
            html.Div([
                html.P('Carregando mapa...')
            ], id='course-map7', className='col-6'),
            html.Div([
                html.P('Carregando tabela...')
            ], id='course-table7', className='col-6'),
        ], className='row'),
        html.Br(),
        html.Div([
            html.Div([
                html.H4('Localidades onde residem estudantes que declararam não possuir PC nem tablet'),
                html.Hr(),
                html.P(
                    'Nesta análise é exibida a quantidade de estudantes que possuem acesso de banda larga mas não possuem computador (notebook ou desktop) nem tablet.')
            ], className='col-12')
        ], className='row'),
        html.Div([
            html.Div([
                html.P('Carregando mapa...')
            ], id='course-map8', className='col-6'),
            html.Div([
                html.P('Carregando tabela...')
            ], id='course-table8', className='col-6'),
        ], className='row'),
        html.Br(),
        html.Div([
            html.Div([
                html.H4('Tipos de dispositivos para acesso a internet'),
                html.Hr(),
                html.P(
                    'Nesta análise exibimos os dispositivos utilizados para acesso dos estudantes à internet.')
            ], className='col-12')
        ], className='row'),
        html.Div([
            html.Div([
                html.P('Carregando tabela...')
            ], id='course-table9', className='col-12'),
        ], className='row'),
        html.Br(),
        html.Div([
            html.Div([
                html.H4('Análise de estudantes que declararam acesso limitado a tecnologia e como se deslocam para a Universidade'),
                html.Hr(),
                html.P(
                    'Nesta análise estamos considerando estudantes que, alternativamente, não possuem acesso à internet, ou acessam a internet apenas por smartphone (mesmo que tenham franquia de dados ILIMITADA).')
            ], className='col-12')
        ], className='row'),
        html.Div([
            html.Div([
                html.P('Carregando tabela...')
            ], id='course-table10', className='col-12'),
        ], className='row'),
    ])
    return layout


def get_campus_course(campus_course):
    campus = campus_course.split('-')[0]
    course = campus_course.split('-')[1]
    return campus, course


def get_course_data(campus_course):
    campus, course = get_campus_course(campus_course)
    data_course = global_data[global_data.campus.eq(campus) & global_data.curso.eq(course)]
    return data_course


@app.callback(Output(component_id='course-info', component_property='children'),
              [Input(component_id='course-select', component_property='value')])
def update_course_info(campus_course:str):
    campus, course = get_campus_course(campus_course)

    data_course = global_data[global_data.campus.eq(campus) & global_data.curso.eq(course)]
    respondents_count = data_course.index.to_numpy().size
    enrolled_count = int(global_student_count[campus_course])

    layout = dcc.Markdown('Neste relatório, **{} (~{:.1f}%)** estudantes responderam à pesquisa, do total de **{}** matriculados.'.format(respondents_count, round(respondents_count/enrolled_count*100,1), enrolled_count))

    return layout

@app.callback(Output(component_id='course-set1', component_property='children'),
              [Input(component_id='course-select', component_property='value')])
def update_set1(campus_course:str):
    campus, course = get_campus_course(campus_course)

    data_course = global_data[global_data.campus.eq(campus) & global_data.curso.eq(course)]
    semesters = pd.DataFrame(data_course['periodo'].value_counts()).reset_index()
    semesters.columns = ['periodo', 'quantidade']
    fig = px.pie(semesters, values='quantidade', names='periodo',
                 title='Proporção por período do curso {}'.format(course))
    layout_graph = html.Div([
        dcc.Graph(figure=fig)
    ])
    return layout_graph

@app.callback([Output(component_id='course-table2', component_property='children'),
               Output(component_id='course-map2', component_property='children')],
              [Input(component_id='course-select', component_property='value')])
def update_set2(campus_course:str):
    campus, course = get_campus_course(campus_course)

    data_course = global_data[global_data.campus.eq(campus) & global_data.curso.eq(course)]

    return maps.get_table_and_map(data_course, color_range=15, center=str.lower(campus))


@app.callback(Output(component_id='course-table3', component_property='children'),
              [Input(component_id='course-select', component_property='value')])
def update_set3(campus_course:str):
    campus, course = get_campus_course(campus_course)

    data_course = global_data[global_data.campus.eq(campus) & global_data.curso.eq(course)]
    data_course = data_course['transporte'].value_counts()
    data_course = data_course.reset_index()
    data_course.columns = ['meio de transporte', 'estudantes']

    table = maps.get_city_table(data_course)
    layout_table = html.Div([
        table,
    ])

    return layout_table


@app.callback(Output(component_id='course-table4', component_property='children'),
              [Input(component_id='course-select', component_property='value')])
def update_set4(campus_course:str):
    campus, course = get_campus_course(campus_course)

    data_course = global_data[global_data.campus.eq(campus) & global_data.curso.eq(course)]
    frame = pd.DataFrame(data_course['ambiente'].value_counts())
    perc = data_course['ambiente'].value_counts(normalize=True) * 100
    frame['perc'] = perc
    frame = frame.reset_index()
    frame.columns = ['resposta', 'quantidade', 'proporção (%)']

    table = maps.get_city_table(frame)
    layout_table = html.Div([
        table,
    ])

    return layout_table


@app.callback(Output(component_id='course-table5', component_property='children'),
              [Input(component_id='course-select', component_property='value')])
def update_set5(campus_course:str):
    data_course = get_course_data(campus_course)

    frame = pd.DataFrame(data_course['risco'].value_counts())
    frame = frame.reset_index()
    frame.columns = ['resposta', 'quantidade']

    table = maps.get_city_table(frame)
    layout_table = html.Div([
        table,
    ])

    return layout_table


@app.callback([Output(component_id='course-table6', component_property='children'),
               Output(component_id='course-map6', component_property='children')],
              [Input(component_id='course-select', component_property='value')])
def update_set6(campus_course:str):
    campus, _ = get_campus_course(campus_course)
    data_course = get_course_data(campus_course)
    data_internet = data_course[data_course['internet'].eq('Não')]
    if data_internet.index.to_numpy().size > 0:
        return maps.get_table_and_map(data_internet, color_range=15, center=str.lower(campus))
    else:
        no_results = html.Div([
            html.P('Nenhum estudante satisfez a condição estabelecida nesta análise.')
        ])
        return (no_results, no_results)


@app.callback([Output(component_id='course-table7', component_property='children'),
               Output(component_id='course-map7', component_property='children')],
              [Input(component_id='course-select', component_property='value')])
def update_set7(campus_course:str):
    campus, _ = get_campus_course(campus_course)
    data_course = get_course_data(campus_course)
    data_internet = data_course[data_course['acesso'] == 'Dados móveis LIMITADOS']
    if data_internet.index.to_numpy().size > 0:
        return maps.get_table_and_map(data_internet, color_range=15, center=str.lower(campus))
    else:
        no_results = html.Div([
            html.P('Nenhum estudante satisfez a condição estabelecida nesta análise.')
        ])
        return (no_results, no_results)


@app.callback([Output(component_id='course-table8', component_property='children'),
               Output(component_id='course-map8', component_property='children')],
              [Input(component_id='course-select', component_property='value')])
def update_set8(campus_course:str):
    campus, _ = get_campus_course(campus_course)
    data_course = get_course_data(campus_course)
    data_internet = data_course[data_course.notebookpc.eq('Não') & data_course.tablet.eq('Não') & data_course.acesso.eq('Banda larga')]
    if data_internet.index.to_numpy().size > 0:
        return maps.get_table_and_map(data_internet, color_range=15, center=str.lower(campus))
    else:
        no_results = html.Div([
            html.P('Nenhum estudante satisfez a condição estabelecida nesta análise.')
        ])
        return (no_results, no_results)


@app.callback(Output(component_id='course-table9', component_property='children'),
              [Input(component_id='course-select', component_property='value')])
def update_set9(campus_course:str):
    campus, _ = get_campus_course(campus_course)
    data_course = get_course_data(campus_course)

    data_restricted = data_course[data_course.acesso.eq('Banda larga')]
    notebook_count = data_restricted[data_course.notebookpc.eq('Sim')].index.to_numpy().size
    smartphone_count = data_restricted[data_course.smartphone.eq('Sim')].index.to_numpy().size
    tablet_count = data_restricted[data_course.tablet.eq('Sim')].index.to_numpy().size
    respondents_count = data_course.index.to_numpy().size
    devices = pd.DataFrame({'Quantidade': [notebook_count, smartphone_count, tablet_count],
                            'Proporção (%)': [notebook_count / respondents_count * 100,
                                              smartphone_count / respondents_count * 100,
                                              tablet_count / respondents_count * 100]
                            }, index=['Possui notebook/pc', 'Possui smartphone', 'Possui tablet'])
    devices = devices.reset_index()
    devices.columns = ['resposta', 'quantidade', 'proporção']
    table = maps.get_city_table(devices)
    layout_table = html.Div([
        table,
    ])

    return layout_table


@app.callback(Output(component_id='course-table10', component_property='children'),
              [Input(component_id='course-select', component_property='value')])
def update_set10(campus_course:str):
    campus, _ = get_campus_course(campus_course)
    data_course = get_course_data(campus_course)

    data_restricted = data_course[(data_course.notebookpc.eq('Não') & data_course.tablet.eq('Não') & data_course.tablet.eq('Sim')) | data_course.internet.eq('Não')]


    if data_restricted.index.to_numpy().size > 0:
        frame = pd.DataFrame(data_restricted.groupby('cidade')['transporte'].value_counts())
        frame.index = frame.index.set_names(['cidade_i', 'transporte_i'])
        frame = frame.reset_index()
        frame.columns = ['cidade', 'meio de transporte', 'estudantes']

        table = maps.get_city_table(frame)

        layout_table = html.Div([
            table,
        ])

        return layout_table
    else:
        no_results = html.Div([
            html.P('Nenhum estudante satisfez a condição estabelecida nesta análise.')
        ])
        return no_results
