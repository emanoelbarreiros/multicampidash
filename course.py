import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

def get_layout():
    layout = html.Div([
        html.H1('Dados por Curso'),
        html.Hr(),
        html.Div(id='page-1-content'),
        html.Br(),
        dcc.Link('Go to Page 2', href='/page-2'),
        html.Br(),
        dcc.Link('Go back to home', href='/'),
    ])
    return layout