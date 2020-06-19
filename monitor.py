import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

def get_layout():
    layout = html.Div([
        html.H1('Monitoramento Epidemiológico'),
        html.Hr(),
        html.Div(id='page-1-content'),
        html.Br()
    ])
    return layout