import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import spreadsheets as sp
import pandas as pd
import plotly.graph_objects as go
import maps
from dash.dependencies import Input, Output
from server import app

client_id = '856477862793-451r4biqr9543d3oc2injf6iif2e34ac.apps.googleusercontent.com'
client_secret = 'wlhHsBYLGXztszG38-VaVqlS'
epidemic_data = None
dates_to_show = None
n_dates = 15


def get_layout(localities):
    global epidemic_data, dates_to_show

    epidemic_data = sp.get_epidemic_data()
    df = pd.DataFrame(epidemic_data)
    df.columns = ['cidade', 'data', 'infectados', 'recuperados', 'obitos', 'novos']
    df['infectados'] = pd.to_numeric(df['infectados'])
    df['obitos'] = pd.to_numeric(df['obitos'])
    df['novos'] = pd.to_numeric(df['novos'])
    epidemic_data = df

    infected_graph = get_cumulative_infected_graph(epidemic_data)
    recovered_graph = get_cumulative_recovered_graph(epidemic_data)
    deceased_graph = get_cumulative_deceased_graph(epidemic_data)
    new_cases_graph = get_new_per_day(epidemic_data)

    dates_to_show = get_dates_to_show(epidemic_data, n_dates)

    infected_slider_marks = {}
    for i, date in enumerate(dates_to_show):
        infected_slider_marks[i] = date

    layout = html.Div([
        html.Div([
            html.H1('Monitoramento Epidemiológico'),
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
                dcc.Graph(figure=new_cases_graph)
            ]),
            html.Br(),
            html.Div(id='div-infected-map'),
            html.Br(),
            html.P('Selecione a data abaixo para atualizar o mapa'),
            dcc.Slider(
                id='slider-infected-graph',
                marks=infected_slider_marks,
                min=0,
                max=n_dates,
                value=0,
                updatemode='drag'
            ),
        ], className='col-12')
    ], className='row')
    return layout


def get_cumulative_log_graph(data, variable):
    epidemic_data

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


@app.callback(Output('div-infected-map', 'children'), [Input('slider-infected-graph', 'value')])
def update_infected_map(date):
    infected_map = maps.get_infected_graph(epidemic_data, 200, dates_to_show[date])
    return dcc.Graph(figure=infected_map)


def get_dates_to_show(epidemic_data, n_dates_to_show):
    df_epidemic = epidemic_data.loc[::, ['cidade', 'data']]

    # choose some dates to show
    all_dates = list(df_epidemic[df_epidemic.cidade.eq('garanhuns')]['data'])
    selected_dates = all_dates[:: len(all_dates) // n_dates_to_show]
    if all_dates[-1] not in selected_dates:
        # always add the last date if it is not included
        selected_dates.append(all_dates[-1])

    return selected_dates
