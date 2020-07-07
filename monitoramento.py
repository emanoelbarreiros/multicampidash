import dash_core_components as dcc
import dash_html_components as html
import spreadsheets as sp
import pandas as pd
import plotly.graph_objects as go
import maps
from dash.dependencies import Input, Output
from server import app
import plotly.express as px

client_id = '856477862793-451r4biqr9543d3oc2injf6iif2e34ac.apps.googleusercontent.com'
client_secret = 'wlhHsBYLGXztszG38-VaVqlS'
dates_to_show = None
n_dates = 15
g_localities = None
g_campus = None
g_epidemic_data = None


def get_layout(localities, campus):
    global g_epidemic_data, dates_to_show, g_localities, g_campus
    g_campus = campus
    g_localities = localities

    epidemic_data = sp.get_epidemic_data(campus)
    g_epidemic_data = epidemic_data

    infected_graph = get_cumulative_infected_graph(epidemic_data)
    recovered_graph = get_cumulative_recovered_graph(epidemic_data)
    deceased_graph = get_cumulative_deceased_graph(epidemic_data)
    epg_graphs = get_epg_rhot_graphs(epidemic_data, campus, localities)
    dates_to_show = get_dates_to_show(epidemic_data, campus)

    infected_slider_marks = {}
    for i, date in enumerate(dates_to_show):
        infected_slider_marks[i] = date.strftime('%d %b')

    layout = html.Div([
        html.Div([
            html.H1('Monitoramento Epidemiológico - {}'.format(campus.capitalize())),
            html.Hr(),
            dcc.Tabs([
                dcc.Tab(label='Infectados', children=[
                    html.Div([
                        dcc.Graph(figure=infected_graph)
                    ]),
                ]),
                dcc.Tab(label='Recuperados', children=[
                    html.Div([
                        dcc.Graph(figure=recovered_graph)
                    ]),
                ]),
                dcc.Tab(label='Óbitos', children=[
                    html.Div([
                        dcc.Graph(figure=deceased_graph)
                    ]),
                ])
            ]),
            html.Br(),
            html.Div([
                html.H5('Novos casos de COVID-19 por município'),
                html.Hr(),
                html.P('Selecione a visualização desejada:'),
                dcc.RadioItems(
                    options=[
                        {'label': 'Média móvel (7 dias)', 'value': 'M'},
                        {'label': 'Novos casos por dia', 'value': 'O'}
                    ],
                    value='M',
                    labelStyle={'display': 'block'},
                    id='radio-rolling-average'
                ),
                html.Br(),
                html.Div(id='div-new-cases'),
            ]),
            html.Br(),
            html.H5('Evolução geoespacial da quantidade de infectados'),
            html.Hr(),
            html.Div(id='div-infected-map'),
            html.Br(),
            html.P('Selecione a data abaixo para atualizar o mapa'),
            dcc.Slider(
                id='slider-infected-graph',
                marks=infected_slider_marks,
                min=0,
                max=len(dates_to_show) - 1,
                value=0,
                updatemode='drag'
            ),
            html.Br(),
            html.Hr(),
            html.H5('Gráficos de risco'),
            html.Div([
                html.P('Os gráficos exibidos nesta seção foram adaptados do método desenvolvido pelo IRRD do Estado de Pernambuco.'),
                html.A('IRRD', href='https://www.irrd.org/'),
                html.A('Link para o método', href='https://drive.google.com/file/d/1Orwg6iwcClSNU4a8SXoqwKNpvdbW-dgj/view')
            ]),
            html.Div(children=epg_graphs),
        ], className='col-12')
    ], className='row')
    return layout


def get_cumulative_log_graph(epidemic_data, variable):
    fig = go.Figure()
    for city in epidemic_data.cidade.unique():
        city_data = epidemic_data[epidemic_data.cidade == city]
        x = city_data.data
        y = city_data[variable]
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers', name=city))

    if variable == 'obitos':
        variable = 'óbitos'

    if variable == 'novos':
        variable = 'novos casos'

    fig.update_layout(yaxis_type="log", title="Curva cumulativa de {} COVID-19".format(variable), xaxis_title="dia",
                      yaxis_title="{} (log)".format(variable))
    fig.update_yaxes(tick0=1)
    return fig


def get_cumulative_infected_graph(epidemic_data):
    return get_cumulative_log_graph(epidemic_data, 'infectados')


def get_cumulative_recovered_graph(epidemic_data):
    return get_cumulative_log_graph(epidemic_data, 'recuperados')


def get_cumulative_deceased_graph(epidemic_data):
    return get_cumulative_log_graph(epidemic_data, 'obitos')


def get_new_per_day(epidemic_data):
    fig = go.Figure()
    for city in epidemic_data.cidade.unique():
        city_data = epidemic_data[epidemic_data.cidade == city]
        x = city_data.data
        y = city_data['novos']
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers', name=city))

    fig.update_layout(title="Novos casos de COVID-19 por dia", xaxis_title="dia", yaxis_title="novos casos")
    return fig


def get_rolling_per_day(epidemic_data:pd.DataFrame):
    #epidemic_data.append TODO melhorar isso aqui ver se dá pra deixar de usar o copy
    fig = go.Figure()
    for city in epidemic_data.cidade.unique():
        city_data = epidemic_data[epidemic_data.cidade == city]
        x = city_data.data
        y = city_data['mm_novos']
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers', name=city))

    fig.update_layout(title="Novos casos de COVID-19 por dia (média móvel com janela de 7 dias)", xaxis_title="dia", yaxis_title="novos casos (média móvel com janela de 7 dias)")
    return fig


@app.callback(Output('div-infected-map', 'children'), [Input('slider-infected-graph', 'value')])
def update_infected_map(date):
    infected_map = maps.get_infected_graph(g_epidemic_data, 200, dates_to_show[date], g_campus)
    return dcc.Graph(figure=infected_map)


def get_dates_to_show(epidemic_data, campus):
    df_epidemic = epidemic_data.loc[::, ['cidade', 'data']]

    # choose some dates to show
    all_dates = list(df_epidemic[df_epidemic.cidade.eq(campus)]['data'])
    # selected_dates = all_dates[:: len(all_dates) // n_dates_to_show]
    selected_dates = all_dates[::7]
    if all_dates[-1] not in selected_dates:
        # always add the last date if it is not included
        selected_dates.append(all_dates[-1])

    return selected_dates


@app.callback(Output('div-new-cases', 'children'), [Input('radio-rolling-average', 'value')])
def update_new_per_day_graph(option):
    figure = None
    if option == 'M':
        figure = get_rolling_per_day(g_epidemic_data)
    elif option == 'O':
        figure = get_new_per_day(g_epidemic_data)

    return dcc.Graph(figure=figure)


def calculate_risk(epg):
    if epg > 100:
        return 'alto'
    elif 70 < epg <= 100:
        return 'moderadoalto'
    elif 30 < epg <= 70:
        return 'moderado'
    else:
        return 'baixo'


def calculate_color(risk):
    if risk == 'alto':
        return 'red'
    elif risk == 'moderadoalto':
        return 'orange'
    elif risk == 'moderado':
        return 'yellow'
    else:
        return 'green'


def get_epg_data(epidemic_data:pd.DataFrame, campus, localities):
    result = pd.read_excel('data/dados_' + campus + '.xlsx')
    return result


def get_epg_rhot_graphs(epidemic_data:pd.DataFrame, campus, localities):
    epg_data = get_epg_data(epidemic_data, campus, localities)
    result = []
    for city in epg_data.cidade.unique():
        fig_bar = px.bar(epg_data[epg_data.cidade.eq(city)], y="epg", x="data", hover_name='risk', color='risk',
                     color_discrete_map={
                         "alto": "red",
                         "moderadoalto": "orange",
                         "moderado": "yellow",
                         "baixo": "green"},
                     title="Índice de crescimento potencial: {}".format(city))

        fig_rhot = go.Figure()
        x = epg_data[epg_data.cidade == city].data
        y = epg_data[epg_data.cidade == city]['rho_t']
        fig_rhot.add_trace(go.Scatter(x=x, y=y, mode='lines+markers', name=city, connectgaps=True))
        fig_rhot.update_layout(title='Velocidade de propagação (média de 7 dias): {}'.format(city), xaxis_title="data",
                               yaxis_title='rho (média de 7 dias)')

        result.append(dcc.Graph(figure=fig_bar))
        result.append(dcc.Graph(figure=fig_rhot))
    return result

